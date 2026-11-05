from pydantic import BaseModel, ConfigDict

class SubgenreResponse(BaseModel):
    slug: str
    name: str

    model_config = ConfigDict(from_attributes=True)