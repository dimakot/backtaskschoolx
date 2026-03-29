from sqlalchemy.orm import Session

from database.models import Comment


class CommentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_comment(self, task_id: int, author_id: int, content: str) -> Comment:
        comment = Comment(task_id=task_id, author_id=author_id, content=content)
        self.db.add(comment)
        self.db.commit()
        self.db.refresh(comment)
        return comment

    def get_task_comments(self, task_id: int) -> list[Comment]:
        return (
            self.db.query(Comment)
            .filter(Comment.task_id == task_id)
            .order_by(Comment.id.asc())
            .all()
        )
