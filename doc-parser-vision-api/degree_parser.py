import json
import os
import re
import cv2
# import time
import numpy as np
import requests
from dotenv import load_dotenv
from google.cloud import vision_v1
from openai import OpenAI
from pdf2image import convert_from_bytes
# from utils.prompt import translator_prompt
import base64
from google.oauth2 import service_account


class DocumentParser:
    def __init__(self):
        load_dotenv()
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.openai_api_key}"
        }

        credentials_base64 = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_BASE64')
        if credentials_base64:
            credentials_json = json.loads(base64.b64decode(credentials_base64).decode('utf-8'))
            credentials = service_account.Credentials.from_service_account_info(credentials_json)
            self.client = vision_v1.ImageAnnotatorClient(credentials=credentials)
        else:
            self.client = vision_v1.ImageAnnotatorClient()

    def is_pdf(self, doc):
        return doc.startswith(b'%PDF')

    def create_composite_image(self, images):
        arrays = [np.array(image) for image in images]
        base_width = arrays[0].shape[1]
        resized_arrays = []

        for array in arrays:
            if array.shape[1] != base_width:
                height = int(array.shape[0] * (base_width / array.shape[1]))
                array = cv2.resize(array, (base_width, height))
            resized_arrays.append(array)

        composite_image = np.vstack(resized_arrays)

        return composite_image

    def get_highest_confidence_language(self, response):
        try:
            full_text_annotation = response.full_text_annotation
            if full_text_annotation.pages:
                languages = full_text_annotation.pages[0].property.detected_languages
                if languages:
                    highest_conf_lang = max(languages, key=lambda x: x.confidence)
                    return highest_conf_lang.language_code, highest_conf_lang.confidence
        except AttributeError:
            pass
        return None, None

    def download_document(self, url):
        response = requests.get(url)
        response.raise_for_status()
        return response.content

    def extract_text_from_image(self, images, client):
        composite_image = self.create_composite_image(images)
        image_bytes = vision_v1.Image(content=cv2.imencode('.png', composite_image)[1].tobytes())
        response = client.document_text_detection(image=image_bytes)
        language_code, confidence = self.get_highest_confidence_language(response)
        texts = response.text_annotations
        extracted_text = ''.join([text.description for text in texts]) + "\n"

        return {
            'text': extracted_text,
            'language_code': language_code,
            'confidence': confidence
        }

    def extract_text_from_image_upload(self, image_bytes):
        image = vision_v1.Image(content=image_bytes)
        response = self.client.document_text_detection(image=image)
        language_code, confidence = self.get_highest_confidence_language(response)
        texts = response.text_annotations
        extracted_text = ''.join([text.description for text in texts]) + "\n"
        
        return [{
            'text': extracted_text,
            'language_code': language_code,
            'confidence': confidence
        }]

    def extract_text_from_pdf(self, pdf_bytes):
        images = convert_from_bytes(pdf_bytes, first_page=1, last_page=2)
        extracted_results = []
        result = self.extract_text_from_image(images, self.client)
        extracted_results.append(result)

        return extracted_results

    def process_document(self, doc, is_url):
        if is_url:
            doc_content = self.download_document(doc)
        else:
            doc_content = doc

        if self.is_pdf(doc_content):
            return self.extract_text_from_pdf(doc_content)
        else:
            return self.extract_text_from_image_upload(doc_content)

    def extract_text(self, doc, is_url):
        try:
            return self.process_document(doc, is_url)
        except Exception as e:
            print(f"Error extracting text: {e}")
            return ""

    @staticmethod
    def get_json_response(extracted_text, en_text=None):
        org_json_string = extracted_text.choices[0].message.content
        pattern = r'{.*?}'
        org_text_match = re.search(pattern, org_json_string, re.DOTALL)
        org_json_data = json.loads(org_text_match.group(0)) if org_text_match else {}
        en_json_data = json.loads(re.search(pattern, en_text.choices[0].message.content, re.DOTALL).group(0)) if en_text else None
        return org_json_data, en_json_data

    # def get_field_info(self, prompt, extracted_results):
    #     client = OpenAI()
    #     en_text = None
    #     document_content_text = '\n'.join(result['text'] for result in extracted_results)

    #     extracted_text = client.chat.completions.create(
    #         model="gpt-4o-mini",
    #         messages=[
    #             {"role": "system", "content": f"{prompt}"},
    #             {"role": "user", "content": f"{document_content_text}"}
    #         ]
    #     )

    #     doc_lang = extracted_results[0]['language_code']
    #     if doc_lang != 'en':
    #         en_text = client.chat.completions.create(
    #             model="gpt-4o-mini",
    #             messages=[
    #                 {"role": "system", "content": f"{translator_prompt}"},
    #                 {"role": "user", "content": f"{extracted_text.choices[0].message.content}"}
    #             ]
    #         )

    #     extracted_response = self.get_json_response(extracted_text, en_text)
    #     return extracted_response


# Example usage
# if __name__ == "__main__":
#     parser = DocumentParser()
#     document_path = ''
#     extracted_text = parser.extract_text(document_path, is_url=True, content_type='university_degree')
#     extracted_fields = parser.get_field_info(university_degree_prompt, extracted_text)
#     print(extracted_fields)