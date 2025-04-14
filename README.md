# API Principal - Consulta CEP

## ✨ Descrição
Esta é a API principal do projeto de consulta de endereços e distância entre CEPs. Ela se comunica com:
- O serviço externo **ViaCEP** para obter dados de endereço
- Uma **API secundária** para calcular a distância entre dois CEPs

Todas as consultas são salvas em banco de dados SQLite e possuem interface interativa via Swagger (`/openapi`).

## ⚙️ Instalação

### ✅ Requisitos
- Python 3.9 ou superior
- Docker e Docker Compose (opcional)

### 💻 Rodar localmente (sem Docker)

```bash
git clone https://github.com/SEU_USUARIO/mvp1-backend.git
cd mvp1-backend/api-principal
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows
pip install -r requirements.txt
flask run --host 0.0.0.0 --port 5001
```

> ⚠️ A API secundária precisa estar rodando na porta 5002.

### 🐳 Rodar com Docker

```bash
docker compose up --build
```

## 💡 Uso
- Swagger: [http://localhost:5001/openapi](http://localhost:5001/openapi)

### Exemplo via `curl`
```bash
curl -X POST http://localhost:5001/consulta \
  -H "Content-Type: application/json" \
  -d '{"cep_origem": "01153000", "cep_destino": "05407002"}'
```

## 📊 Funcionalidades principais
- CRUD de consultas com CEPs
- Chamada automática à API secundária para cálculo de distância
- Consulta de dados via API ViaCEP
- Documentação via Swagger

## 🚀 Contribuição
Faça um fork, crie uma branch e envie um Pull Request.

---

> Desenvolvido por Marcio Curvello
