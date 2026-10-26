
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(
    title="MiniServe",
    version="0.1.0",
    description="A minimal AI inference service",
)


class EchoRequest(BaseModel):
    text: str = Field(min_length=1, max_length=1000)


class EchoResponse(BaseModel):
    result: str
    length: int


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

