from sqlalchemy import String, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from typing import TYPE_CHECKING
import enum

if TYPE_CHECKING:
    from app.models.movie import Movie
    from app.models.subgenre import Subgenre
    
class MovieSubgenre(Base):
    __tablename__ = "movie_subgenre"

    movie_id: Mapped[int] = mapped_column(ForeignKey("movie.id", ondelete="CASCADE"), primary_key=True)
    subgenre_id: Mapped[int] = mapped_column(ForeignKey("subgenre.id", ondelete="CASCADE"), primary_key=True, index=True)
    classifier_version: Mapped[str] = mapped_column(String(20))

    movie: Mapped["Movie"] = relationship(back_populates="subgenre_links")
    subgenre: Mapped["Subgenre"] = relationship(back_populates="movie_links")
