from pydantic import BaseModel, ConfigDict

class ReadBaseDTO(BaseModel):
    model_config = ConfigDict(
        frozen = True,
        from_attributes = True # Convierte el objeto ORM en DTO de lectura.
    )