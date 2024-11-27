from base import BaseDAO
from app.models import Review


class ReviewDAO(BaseDAO):
    model = Review
