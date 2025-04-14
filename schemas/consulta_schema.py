from pydantic import BaseModel, field_validator
from typing import Optional, Union


class ConsultaInput(BaseModel):
    cep_origem: Union[str, int]
    cep_destino: Union[str, int]

    @field_validator("cep_origem", "cep_destino", mode="before")
    @classmethod
    def to_str(cls, v):
        return str(v)

class CepPathSchema(BaseModel):
    cep: str

class ConsultaPatchSchema(BaseModel):
    id: int
    cep_origem: Optional[str] = None
    cep_destino: Optional[str] = None
    distancia_km: Optional[float] = None

class ConsultaPutSchema(BaseModel):
    id: int
    cep_origem: str
    cep_destino: str
    distancia_km: Optional[float] = None

class ConsultaSearchSchema(BaseModel):
    id: int

class ConsultaPathSchema(BaseModel):
    id: int
