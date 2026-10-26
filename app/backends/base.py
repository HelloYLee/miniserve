
from abc import ABC, abstractmethod


class ModelBackend(ABC):
    """All inference backends implement this interface."""

    @abstractmethod
    def predict(self, text: str) -> str:
        """Run inference and return the result."""
        pass
