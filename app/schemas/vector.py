from pydantic import BaseModel, Field

class VectorAddRequest(BaseModel):
    text: str = Field(..., example="This is an example text to be stored.")
    metadata: dict = Field({}, example={"source": "example_source"})

class VectorSearchRequest(BaseModel):
    query: str = Field(..., example="What is the example text?")
    k: int = Field(5, example=5)
