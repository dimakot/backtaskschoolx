class TaskNotFound(Exception):
    def __init__(self, message: str = "Задача не найдена"):
        self.code = "TaskNotFound"
        self.message = message
        super().__init__(message)


class CommentNotFound(Exception):
    def __init__(self, message: str = "Комментарий не найден"):
        self.code = "CommentNotFound"
        self.message = message
        super().__init__(message)
