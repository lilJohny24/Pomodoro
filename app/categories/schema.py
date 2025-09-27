from pydantic import BaseModel, ConfigDict

class CategorySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # ← И здесь тоже

    id: int
    type: str
    name: str


class CategoryCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # ← И здесь тоже

    id: int
    type: str
    name: str