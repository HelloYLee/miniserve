from fastapi import HTTPException

from app.backends.mock import (
    MockBackend,
    ModelInferenceError,
)
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(
    title="MiniServe",
    version="0.1.0",
    description="A minimal AI inference service",
)
backend = MockBackend()

class EchoRequest(BaseModel):
    text: str = Field(min_length=1, max_length=1000)


class EchoResponse(BaseModel):
    result: str
    length: int


class PredictRequest(BaseModel):
    text: str = Field(min_length=1, max_length=1000)


class PredictResponse(BaseModel):
    result: str
    model: str

@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "miniserve",
    }


@app.post("/echo", response_model=EchoResponse)
def echo(request: EchoRequest):
    return EchoResponse(
        result=request.text,
        length=len(request.text),
    )

@app.post(
    "/predict",
    response_model=PredictResponse,
)
def predict(request: PredictRequest):

    try:
        result = backend.predict(request.text)

    except ModelInferenceError:
        raise HTTPException(
            status_code=503,
            detail="Model inference unavailable",
        ) from None

    return PredictResponse(
        result=result,
        model="mock",
    )