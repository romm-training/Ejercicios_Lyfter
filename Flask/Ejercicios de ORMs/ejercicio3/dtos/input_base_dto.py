from pydantic import BaseModel, ConfigDict

class InputBaseDTO(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        str_strip_whitespace=True,
        extra="forbid" # rechaza campos inventados.
    )