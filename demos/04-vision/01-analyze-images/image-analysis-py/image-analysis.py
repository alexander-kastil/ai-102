from dotenv import load_dotenv
import os
from PIL import Image, ImageDraw
import sys
from matplotlib import pyplot as plt
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.identity import DefaultAzureCredential

def main():
    load_dotenv()
    endpoint = os.getenv('VISION_ENDPOINT')

    image_file = 'images/street.jpg'
    if len(sys.argv) > 1:
        image_file = sys.argv[1]

    with open(image_file, "rb") as f:
        image_data = f.read()

    client = ImageAnalysisClient(
        endpoint=endpoint,
        credential=DefaultAzureCredential()
    )

    AnalyzeImage(image_file, image_data, client)

def AnalyzeImage(image_filename, image_data, client):
    print('\nAnalyzing image...')

    result = client.analyze(
        image_data=image_data,
        visual_features=[
            VisualFeatures.CAPTION,
            VisualFeatures.DENSE_CAPTIONS,
            VisualFeatures.TAGS,
            VisualFeatures.OBJECTS,
            VisualFeatures.PEOPLE,
        ],
    )

    if result.caption is not None:
        print("\nCaption:")
        print(f" Caption: '{result.caption.text}' (confidence: {result.caption.confidence * 100:.2f}%)")

    if result.dense_captions is not None:
        print("\nDense Captions:")
        for caption in result.dense_captions.list:
            print(f" Caption: '{caption.text}' (confidence: {caption.confidence * 100:.2f}%)")

    if result.tags is not None:
        print("\nTags:")
        for tag in result.tags.list:
            print(f" Tag: '{tag.name}' (confidence: {tag.confidence * 100:.2f}%)")

    if result.objects is not None:
        print("\nObjects in image:")

        image = Image.open(image_filename)
        fig = plt.figure(figsize=(image.width/100, image.height/100))
        plt.axis('off')
        draw = ImageDraw.Draw(image)
        color = 'cyan'

        for detected_object in result.objects.list:
            print(f" {detected_object.tags[0].name} (confidence: {detected_object.tags[0].confidence * 100:.2f}%)")
            r = detected_object.bounding_box
            bounding_box = ((r.x, r.y), (r.x + r.width, r.y + r.height))
            draw.rectangle(bounding_box, outline=color, width=3)
            plt.annotate(detected_object.tags[0].name, (r.x, r.y), backgroundcolor=color)

        plt.imshow(image)
        plt.tight_layout(pad=0)
        outputfile = 'objects.jpg'
        fig.savefig(outputfile)
        print('  Results saved in', outputfile)

    if result.people is not None:
        print("\nPeople in image:")

        image = Image.open(image_filename)
        fig = plt.figure(figsize=(image.width/100, image.height/100))
        plt.axis('off')
        draw = ImageDraw.Draw(image)
        color = 'cyan'

        for detected_people in result.people.list:
            r = detected_people.bounding_box
            bounding_box = ((r.x, r.y), (r.x + r.width, r.y + r.height))
            draw.rectangle(bounding_box, outline=color, width=3)

        plt.imshow(image)
        plt.tight_layout(pad=0)
        outputfile = 'people.jpg'
        fig.savefig(outputfile)
        print('  Results saved in', outputfile)

if __name__ == "__main__":
    main()
