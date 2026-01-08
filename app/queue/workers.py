from ..db.collections.file import files_collection
from bson import ObjectId
import os
from pdf2image import convert_from_path
import base64
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()  # loads GEMINI_API_KEY

client = genai.Client()

def encode_image(image_path: str) -> bytes:
    with open(image_path, "rb") as f:
        return f.read()


async def process_file(id: str, file_path: str):

    # Status: processing
    await files_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": {"status": "converting to images"}}
    )

    # Convert PDF to images
    pages = convert_from_path(file_path)
    images = []

    image_dir = f"/mnt/uploads/images/{id}"
    os.makedirs(image_dir, exist_ok=True)

    for i, page in enumerate(pages):
        image_path = f"{image_dir}/image-{i}.jpg"
        page.save(image_path, "JPEG")
        images.append(image_path)

    await files_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": {"status": "converting to image to success"}}
    )

    # Encode first image
    image_bytes = encode_image(images[0])

    # Gemini Vision call (NEW API)
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=[
            types.Content(
                role="user",
                parts=[
                    types.Part(text="Roast this resume brutally Be sarcastic, honest, and funny. "),
                    types.Part(
                        inline_data=types.Blob(
                            mime_type="image/jpeg",
                            data=image_bytes
                        )
                    ),
                ],
            )
        ],
    )
    await files_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": {"status": "processed",
                  "result":response.text}}
    )
    response = response.text




  
  
  