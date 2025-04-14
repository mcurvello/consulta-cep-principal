from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError
from model import Session, Consulta
from schemas import *
from utils.presenter import show_consulta, show_consultas
from schemas.response_schema import CepSchema, DistanciaResponseSchema
from schemas.consulta_schema import CepPathSchema, ConsultaPathSchema
import requests

info = Info(title="Consulta CEP API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

home_tag = Tag(name="Documentação", description="Swagger, Redoc ou RapiDoc")
consulta_tag = Tag(name="Consultas", description="Operações de CRUD para consultas")
externa_tag = Tag(name="Serviços Externos", description="Consulta de CEP e cálculo de distância")

@app.get('/', tags=[home_tag])
def home():
    return redirect('/openapi')

from pydantic import BaseModel


@app.post('/consulta', tags=[consulta_tag], responses={"200": ConsultaViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_consulta(body: ConsultaInput):
    form = body
    session = None
    try:
        response = requests.post("http://api_secundaria:5002/calcular", json={
            "origem": form.cep_origem,
            "destino": form.cep_destino
        })

        if response.status_code != 200:
            return {"message": "Erro ao calcular distância.", "detalhes": response.text}, 500

        distancia_km = response.json().get("distancia_km")

        if distancia_km is None:
            return {"message": "Distância não foi calculada corretamente."}, 500

        consulta = Consulta(
            cep_origem=form.cep_origem,
            cep_destino=form.cep_destino,
            distancia_km=distancia_km
        )

        session = Session()
        session.add(consulta)
        session.commit()
        return show_consulta(consulta), 200

    except IntegrityError:
        return {"message": "Erro de integridade ao salvar consulta."}, 409
    except Exception as e:
        return {"message": f"Erro inesperado ao salvar consulta: {str(e)}"}, 400
    finally:
        if session:
            session.close()



@app.get('/consultas', tags=[consulta_tag], responses={"200": ListConsultasSchema})
def get_consultas():
    session = Session()
    consultas = session.query(Consulta).all()
    session.close()
    return show_consultas(consultas), 200

@app.get('/consulta/<int:id>', tags=[consulta_tag], responses={"200": ConsultaViewSchema, "404": ErrorSchema})
def get_consulta(path: ConsultaPathSchema):
    session = Session()
    consulta = session.query(Consulta).filter(Consulta.id == path.id).first()
    session.close()
    if not consulta:
        return {"message": "Consulta não encontrada."}, 404
    return show_consulta(consulta), 200

@app.delete('/consulta/<int:id>', tags=[consulta_tag], responses={"200": ConsultaDelSchema, "404": ErrorSchema})
def del_consulta(path: ConsultaPathSchema):
    session = Session()
    consulta = session.query(Consulta).filter(Consulta.id == path.id).first()
    count = session.query(Consulta).filter(Consulta.id == path.id).delete()
    session.commit()
    session.close()
    if count:
        return {"message": "Consulta removida", "id": path.id}
    else:
        return {"message": "Consulta não encontrada."}, 404

@app.put('/consulta', tags=[consulta_tag], responses={"200": ConsultaViewSchema, "404": ErrorSchema})
def update_consulta(form: ConsultaPutSchema):
    session = Session()
    consulta = session.query(Consulta).filter(Consulta.id == form.id).first()
    if not consulta:
        session.close()
        return {"message": "Consulta não encontrada."}, 404
    consulta.cep_origem = form.cep_origem
    consulta.cep_destino = form.cep_destino
    consulta.distancia_km = form.distancia_km
    session.commit()
    session.close()
    return show_consulta(consulta), 200

@app.patch('/consulta', tags=[consulta_tag], responses={"200": ConsultaViewSchema, "404": ErrorSchema})
def partial_update_consulta(form: ConsultaPatchSchema):
    session = Session()
    consulta = session.query(Consulta).filter(Consulta.id == form.id).first()
    if not consulta:
        session.close()
        return {"message": "Consulta não encontrada."}, 404
    if form.cep_origem:
        consulta.cep_origem = form.cep_origem
    if form.cep_destino:
        consulta.cep_destino = form.cep_destino
    if form.distancia_km is not None:
        consulta.distancia_km = form.distancia_km
    session.commit()
    session.close()
    return show_consulta(consulta), 200

@app.get('/cep/<cep>', tags=[externa_tag], responses={"200": CepSchema, "404": ErrorSchema})
def consultar_cep(path: CepPathSchema):
    response = requests.get(f"https://viacep.com.br/ws/{path.cep}/json/")
    return response.json() if response.ok else ({"message": "CEP inválido."}, 404)

@app.post('/distancia', tags=[externa_tag], responses={"200": DistanciaResponseSchema, "500": ErrorSchema})
def calcular_distancia(form: ConsultaInput):
    response = requests.post("http://api_secundaria/calcular", json={
        "origem": str(form.cep_origem),
        "destino": str(form.cep_destino)
    })
    return response.json() if response.ok else ({"message": "Erro ao calcular distância."}, 500)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
