from src.database.base import BaseDAO
from src.database.models import Review


class ReviewDAO(BaseDAO):
    model = Review
