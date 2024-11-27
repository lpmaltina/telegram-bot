from pydantic import BaseModel, Field


class SReviewAdd(BaseModel):
    review: str = Field(..., description="Текст")
