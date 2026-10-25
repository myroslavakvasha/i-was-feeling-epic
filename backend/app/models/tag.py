from sqlalchemy import String, ForeignKey, UniqueConstraint, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.user_movie import UserMovie

user_movie_tag = Table(
    "user_movie_tag", Base.metadata,
    Column("user_movie_id", ForeignKey("user_movie.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", ForeignKey("tag.id", ondelete="CASCADE"), primary_key=True),
)

class Tag(Base):
    __tablename__ = "tag"
    __table_args__ = (UniqueConstraint("user_id", "name", name="uq_tag_user_id_name"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("app_user.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(100))

    user: Mapped["User"] = relationship(back_populates="tags")
    user_movies: Mapped[list["UserMovie"]] = relationship(secondary=user_movie_tag, back_populates="tags")

