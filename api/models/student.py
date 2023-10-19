from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped
from .base import Base


class Student(Base):
    __tablename__ = "students"
    id: Mapped[int] = mapped_column(primary_key=True)
    facultet: Mapped[str] = mapped_column(String(200), nullable=False)
    direction: Mapped[str] = mapped_column(String(200), nullable=False)
    rating: Mapped[int] = mapped_column(nullable=False)
    id_abitur: Mapped[int] = mapped_column(nullable=False)
    snils: Mapped[int] = mapped_column(nullable=False)
    points: Mapped[int] = mapped_column(nullable=False)
    points_fin: Mapped[int] = mapped_column(nullable=False)
    priority: Mapped[bool] = mapped_column(nullable=False)
    agreement: Mapped[bool] = mapped_column(nullable=False)
    original: Mapped[bool] = mapped_column(nullable=False)

    def __str__(self) -> str:
        return f"snils={self.snils},points={self.points_fin},rating={self.rating}"

    def __repr__(self):
        return str(self)
