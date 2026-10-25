from sqlalchemy import Text, ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.models.tag import user_movie_tag
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.movie import Movie
    from app.models.tag import Tag

class UserMovie(Base):
    __tablename__ = "user_movie"
    __table_args__ = (
        UniqueConstraint("user_id", "movie_id", name="uq_user_movie_user_movie"),
        CheckConstraint("rating BETWEEN 1 AND 10", name="ck_user_movie_rating"),
        CheckConstraint("scariness BETWEEN 1 AND 10", name="ck_user_movie_scariness"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("app_user.id", ondelete="CASCADE"))
    movie_id: Mapped[int] = mapped_column(ForeignKey("movie.id"))
    rating: Mapped[int | None]
    scariness: Mapped[int | None]
    thoughts: Mapped[str | None] = mapped_column(Text)

    user: Mapped["User"] = relationship(back_populates="user_movies")
    movie: Mapped["Movie"] = relationship()
    tags: Mapped[list["Tag"]] = relationship(secondary=user_movie_tag, back_populates="user_movies")