from pydantic import BaseModel


class ComparisonRequest(BaseModel):
    document_id_1: str
    document_id_2: str
    comparison_type: str