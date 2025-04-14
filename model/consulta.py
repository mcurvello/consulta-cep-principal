from sqlalchemy import Column, String, Integer, Float
from model.base import Base

class Consulta(Base):
    __tablename__ = "consultas"

    id = Column(Integer, primary_key=True)
    cep_origem = Column(String(10), nullable=False)
    cep_destino = Column(String(10), nullable=False)
    distancia_km = Column(Float, nullable=True)

    def __init__(self, cep_origem: str, cep_destino: str, distancia_km: float = None):
        self.cep_origem = cep_origem
        self.cep_destino = cep_destino
        self.distancia_km = distancia_km
