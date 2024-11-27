from sqlalchemy import Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapped_column, Mapped

Base = declarative_base()


class Review(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    review: Mapped[str] = mapped_column(Text, unique=True, nullable=False)

    def __repr__(self):
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"review={self.review!r},")

    def to_dict(self):
        return {
            "id": self.id,
            "review": self.review
        }

    __tablename__ = "reviews"
