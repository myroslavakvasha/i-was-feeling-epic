from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.movie_subgenre import MovieSubgenre

class Subgenre(Base):
    __tablename__ = "subgenre"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(50), unique=True)
    name: Mapped[str] = mapped_column(String(100))

    movie_links: Mapped[list["MovieSubgenre"]] = relationship(back_populates="subgenre", cascade="all, delete-orphan")