from pydantic import BaseModel
from typing import List, Optional

class CepSchema(BaseModel):
    cep: Optional[str]
    logradouro: Optional[str]
    complemento: Optional[str]
    bairro: Optional[str]
    localidade: Optional[str]
    uf: Optional[str]
    ibge: Optional[str]
    gia: Optional[str]
    ddd: Optional[str]
    siafi: Optional[str]

class DistanciaResponseSchema(BaseModel):
    distancia_km: float

class ConsultaViewSchema(BaseModel):
    id: int
    cep_origem: str
    cep_destino: str
    distancia_km: Optional[float]

class ListConsultasSchema(BaseModel):
    consultas: List[ConsultaViewSchema]

class ConsultaDelSchema(BaseModel):
    message: str
    id: int

class ErrorSchema(BaseModel):
    message: str
