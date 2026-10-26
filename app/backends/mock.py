
import time

from app.backends.base import ModelBackend


class ModelInferenceError(Exception):
    """Raised when model inference fails."""


class MockBackend(ModelBackend):

    def __init__(
        self,
        delay: float = 0.0,
        should_fail: bool = False,
    ):
        if delay < 0:
            raise ValueError("delay must be non-negative")

        self.delay = delay
        self.should_fail = should_fail

    def predict(self, text: str) -> str:

        # Simulate inference latency
        time.sleep(self.delay)

        # Simulate model failure
        if self.should_fail:
            raise ModelInferenceError(
                "Mock model inference failed"
            )

        return f"Mock prediction: {text}"
