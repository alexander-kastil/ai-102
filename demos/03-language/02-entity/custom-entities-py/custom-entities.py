import os
from pathlib import Path

from dotenv import load_dotenv

from azure.ai.textanalytics import TextAnalysisClient
from azure.ai.textanalytics.models import (
	AnalyzeTextEntitiesResult,
	EntitiesActionContent,
	MultiLanguageInput,
	MultiLanguageTextInput,
	TextEntityRecognitionInput,
)
from azure.core.credentials import AzureKeyCredential


def print_banner(title: str) -> None:
	print("\n" + "=" * 80)
	print(title)
	print("=" * 80)


def main() -> None:
	root = Path(__file__).resolve().parent
	load_dotenv()
	AI_SERVICE_ENDPOINT = os.getenv("AI_SERVICE_ENDPOINT")
	AI_SERVICE_KEY = os.getenv("AI_SERVICE_KEY")
	MODEL_DEPLOYMENT = os.getenv("MODEL_DEPLOYMENT_NAME")

	client = TextAnalysisClient(endpoint=AI_SERVICE_ENDPOINT, credential=AzureKeyCredential(AI_SERVICE_KEY))

	ads_dir = root / "ads"
	for path in sorted(ads_dir.glob("*.txt")):
		text = path.read_text(encoding="utf-8").strip()
		print_banner(f"Processing: {path.name}")

		body = TextEntityRecognitionInput(
			text_input=MultiLanguageTextInput(
				multi_language_inputs=[MultiLanguageInput(id=path.stem, text=text, language="en")]
			),
			action_content=EntitiesActionContent(model_version=MODEL_DEPLOYMENT or "latest"),
		)

		result = client.analyze_text(body=body)
		if isinstance(result, AnalyzeTextEntitiesResult) and result.results and result.results.documents:
			doc = result.results.documents[0]
			for entity in doc.entities:
				print(f"- {entity.text} | {entity.category}", end="")
				if entity.subcategory:
					print(f"/{entity.subcategory}", end="")
				print(f" | confidence={entity.confidence_score}")


if __name__ == "__main__":
	main()
