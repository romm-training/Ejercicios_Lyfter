from dtos.read_base_dto import ReadBaseDTO
from dtos.input_base_dto import InputBaseDTO

class TokenDTO(ReadBaseDTO):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"

class RefreshTokenDTO(InputBaseDTO):
    refresh_token: str