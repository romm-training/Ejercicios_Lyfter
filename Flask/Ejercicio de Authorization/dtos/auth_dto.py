from dtos.read_base_dto import ReadBaseDTO

class TokenDTO(ReadBaseDTO):
    access_token: str
    token_type: str = "Bearer"

