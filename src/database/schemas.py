from pydantic import BaseModel, Field


class SReviewAdd(BaseModel):
    review: str = Field(..., description="Текст")

class SReviewUpdate(BaseModel):
    id: int = Field(..., description="Id текста")
    review: str = Field(..., description="Текст")
