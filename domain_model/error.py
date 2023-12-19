from abc import ABC


class Error(ABC):
    message: str
    
    def __init__(self, message: str) -> None:
        super().__init__()
        self.message = message

    def get_error(self) -> str:
        return self.message