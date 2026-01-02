from google import genai
from google.genai import types
from PIL import Image
from typing import Union
import os
from pathlib import Path

class PrescriptionExtractor:
    MODEL_NAME = "gemini-2.5-flash"

    SYSTEM_PROMPT = """
    You are a medical prescription OCR assistant.
    Extract all readable text from the prescription image.
    Preserve medicine names, dosage, frequency, duration, and doctor notes.
    Do NOT hallucinate missing data.
    Return plain text only.
    """

    @staticmethod
    def extract(
        image_input: Union[str, Path, Image.Image],
        api_key: str | None = None,
    ) -> str:
        key = api_key or os.environ.get("GEMINI_API_KEY")
        if not key:
            raise RuntimeError("GEMINI_API_KEY not set")

        client = genai.Client(api_key=key)

        # Validate input if it's a path
        if isinstance(image_input, (str, Path)):
            path = Path(image_input)
            if not path.exists():
                raise FileNotFoundError(f"Image not found: {path}")
            # Convert path to string for the SDK
            image_payload = str(path)
        else:
            # Pass PIL Image directly
            image_payload = image_input

        try:
            response = client.models.generate_content(
                model=PrescriptionExtractor.MODEL_NAME,
                # SDK automatically handles mixing Images and Text in contents
                contents=[
                    image_payload,
                    "Extract the prescription text from this image:"
                ],
                config=types.GenerateContentConfig(
                    system_instruction=PrescriptionExtractor.SYSTEM_PROMPT,
                    temperature=0.0,
                    max_output_tokens=1024,
                ),
            )
            
            if not response.text:
                return "No text extracted or blocked content."
                
            return response.text.strip()

        except Exception as e:
            return f"Error processing prescription: {str(e)}"