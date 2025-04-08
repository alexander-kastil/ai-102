import azure.functions as func
import logging
import json

# Array of stop words to be ignored
stopwords = ['', 'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you',
        "youre", "youve", "youll", "youd", 'your', 'yours', 'yourself',
        'yourselves', 'he', 'him', 'his', 'himself', 'she', "shes", 'her',
        'hers', 'herself', 'it', "its", 'itself', 'they', 'them',
        'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom',
        'this', 'that', "thatll", 'these', 'those', 'am', 'is', 'are', 'was',
        'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do',
        'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or',
        'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with',
        'about', 'against', 'between', 'into', 'through', 'during', 'before',
        'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out',
        'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here',
        'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each',
        'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not',
        'only', 'own', 'same', 'so', 'than', 'too', 'very', 'can', 'will',
        'just', "dont", 'should', "shouldve", 'now', "arent", "couldnt",
        "didnt", "doesnt", "hadnt", "hasnt", "havent", "isnt", "mightnt", "mustnt",
        "neednt", "shant", "shouldnt", "wasnt", "werent", "wont", "wouldnt"]

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="wordcount", methods=["POST"])
def wordcount(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        body = req.get_json()
        
        if body and 'values' in body:
            vals = body['values']
            res = {'values': []}
            
            for rec, val in enumerate(vals):
                # Get the record ID and text for this input
                res_val = {'recordId': val['recordId'], 'data': {}}
                txt = val['data']['text']
                
                # Remove punctuation and numerals and convert to lowercase
                import re
                txt = re.sub(r'[^ A-Za-z_]', '', txt).lower()
                
                # Get an array of words
                words = txt.split(' ')
                
                # Count instances of non-stopwords
                word_counts = {}
                for word in words:
                    if word not in stopwords:
                        word_counts[word] = word_counts.get(word, 0) + 1
                
                # Get unique words (not counting duplicates)
                unique_words = list(word_counts.keys())
                
                # Add the filtered words to the response
                res_val['data']['text'] = unique_words
                
                res['values'].append(res_val)
            
            return func.HttpResponse(
                json.dumps(res),
                mimetype="application/json"
            )
        else:
            return func.HttpResponse(
                json.dumps({"errors": [{"message": "Invalid input"}]}),
                status_code=400,
                mimetype="application/json"
            )
    except ValueError:
        return func.HttpResponse(
            json.dumps({"errors": [{"message": "Invalid input"}]}),
            status_code=400,
            mimetype="application/json"
        )