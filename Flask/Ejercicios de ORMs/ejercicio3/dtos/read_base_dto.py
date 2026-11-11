from pydantic import BaseModel, ConfigDict

class ReadBaseDTO(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        from_attributes=True # convierte el objeto ORM al DTO de lectura.
    )