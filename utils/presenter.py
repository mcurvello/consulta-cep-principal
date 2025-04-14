def show_consulta(consulta):
    return {
        "id": consulta.id,
        "cep_origem": consulta.cep_origem,
        "cep_destino": consulta.cep_destino,
        "distancia_km": consulta.distancia_km
    }

def show_consultas(consultas):
    return {
        "consultas": [
            show_consulta(c) for c in consultas
        ]
    }
