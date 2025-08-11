import os
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.azure_open_ai import AzureChatCompletion
from semantic_kernel.contents import ChatHistory
import asyncio

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    def __repr__(self):
        return f'<Student {self.name}>'

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    student = db.relationship('Student', backref=db.backref('questions', lazy=True))

# Semantic Kernel setup
kernel = None
chat_completion = None

def initialize_semantic_kernel():
    global kernel, chat_completion
    
    model = os.getenv("DEPLOYMENT_MODEL")
    endpoint = os.getenv("ENDPOINT")
    api_key = os.getenv("API_KEY")
    
    if not all([model, endpoint, api_key]):
        raise ValueError("Missing required environment variables for Semantic Kernel")
    
    kernel = Kernel()
    chat_completion = AzureChatCompletion(
        deployment_name=model,
        api_key=api_key,
        endpoint=endpoint,
        service_id="chat-gpt"
    )
    kernel.add_service(chat_completion)

async def get_ai_response(question: str, student_context: str = None) -> str:
    """Get AI response for student question using RAG approach"""
    history = ChatHistory()
    
    system_prompt = """
    You are an AI assistant helping students with their questions. 
    Provide helpful, educational responses that encourage learning.
    If you don't know the answer, suggest ways the student can find the information.
    """
    
    if student_context:
        system_prompt += f"\nStudent context: {student_context}"
    
    history.add_system_message(system_prompt)
    history.add_user_message(question)
    
    try:
        response = await chat_completion.get_chat_message_contents(
            chat_history=history,
            settings=None,
            kernel=kernel
        )
        return response[0].content if response else "I'm sorry, I couldn't generate a response."
    except Exception as e:
        return f"Error generating response: {str(e)}"

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.get_json()
    question = data.get('question', '').strip()
    student_name = data.get('student_name', 'Anonymous')
    
    if not question:
        return jsonify({'error': 'Question cannot be empty'}), 400
    
    try:
        # Get or create student
        student = Student.query.filter_by(name=student_name).first()
        if not student:
            student = Student(name=student_name, email=f"{student_name.lower().replace(' ', '.')}@students.com")
            db.session.add(student)
            db.session.commit()
        
        # Generate AI response
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        answer = loop.run_until_complete(get_ai_response(question, f"Student: {student_name}"))
        loop.close()
        
        # Save question and answer
        new_question = Question(
            student_id=student.id,
            question=question,
            answer=answer
        )
        db.session.add(new_question)
        db.session.commit()
        
        return jsonify({
            'answer': answer,
            'student': student_name,
            'question_id': new_question.id
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/history/<student_name>')
def get_history(student_name):
    student = Student.query.filter_by(name=student_name).first()
    if not student:
        return jsonify([])
    
    questions = Question.query.filter_by(student_id=student.id).order_by(Question.timestamp.desc()).limit(10).all()
    
    history = []
    for q in questions:
        history.append({
            'id': q.id,
            'question': q.question,
            'answer': q.answer,
            'timestamp': q.timestamp.isoformat()
        })
    
    return jsonify(history)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        initialize_semantic_kernel()
    
    app.run(debug=True, port=5000)