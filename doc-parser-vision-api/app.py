from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from degree_parser import DocumentParser

app = FastAPI()

document_parser = DocumentParser()


@app.post("/document_extraction")
async def extract_info(file: UploadFile = File(None), url: str = Form(None), content_type: str = Form(...)):
    """
        Extract information from an uploaded file or a URL.

        - **file**: The file to be uploaded
        - **url**: The URL of the image to be processed
        - **content_type**: The type of content to be extracted ('residence_permit' or 'university_degree')

        Returns a JSON object with the extracted information.
    """
    try:
        is_url = None
        if file:
            doc = await file.read() # Read file content as bytes
        elif url:
            doc = url
            is_url = True
        else:
            return False
            raise HTTPException(status_code=400, detail="No file or URL provided")


        extracted_text = document_parser.extract_text(doc, is_url, content_type)
        # org_json_data, en_json_data = document_parser.get_field_info(content_description, extracted_text)

        return {
            "ext_txt": extracted_text
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="127.0.0.1", port=8080, log_level="info", reload=True)