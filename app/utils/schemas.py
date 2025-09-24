from pydantic import BaseModel

class IngestResponse(BaseModel):
    filename: str
    parsed_preview: dict