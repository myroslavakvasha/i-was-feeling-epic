from datetime import datetime, timezone
from sqlalchemy import ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.movie import Movie

class Watch(Base):
    __tablename__ = "watch"
    __table_args__ = (Index("ix_watch_user_watched_at", "user_id", "watched_at"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("app_user.id", ondelete="CASCADE"))
    movie_id: Mapped[int] = mapped_column(ForeignKey("movie.id"))
    watched_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))

    user: Mapped["User"] = relationship(back_populates="watches")
    movie: Mapped["Movie"] = relationship()