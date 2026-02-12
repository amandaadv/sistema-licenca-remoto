# 🔐 ZAPJOE V2 - License Server

Sistema de licenciamento remoto para ZAPJOE V2.

## 🚀 Deploy Rápido

### Railway (Recomendado)
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new)

1. Clique no botão acima
2. Conecte seu GitHub
3. Configure `MASTER_KEY` nas variáveis
4. Deploy automático!

### Render
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

## 📦 Instalação Local

```bash
# Instalar dependências
pip install -r requirements.txt

# Iniciar servidor
uvicorn api:app --host 0.0.0.0 --port 8000
```

## 🔧 Configuração

### Variáveis de Ambiente

```env
MASTER_KEY=sua_chave_secreta_aqui
DATA_FILE=licencas_db.json
PORT=8000
```

## 📖 API Endpoints

### Validar Licença
```http
POST /validar
Content-Type: application/json

{
  "usuario": "cliente",
  "senha": "senha123",
  "hardware_id": "abc123",
  "versao_programa": "2.0"
}
```

### Admin - Listar Licenças
```http
GET /admin/listar_licencas
X-Admin-Key: SUA_MASTER_KEY
```

### Admin - Criar Licença
```http
POST /admin/criar_licenca
X-Admin-Key: SUA_MASTER_KEY
Content-Type: application/json

{
  "usuario": "novo_cliente",
  "senha": "senha123",
  "dias_validade": 30
}
```

## 🔒 Segurança

- ✅ Senhas hash PBKDF2 (100.000 iterações)
- ✅ API protegida com chave mestra
- ✅ SSL/HTTPS obrigatório em produção
- ✅ Validação de hardware ID (opcional)

## 📊 Estrutura

```
server/
├── api.py              # FastAPI application
├── requirements.txt    # Python dependencies
├── Procfile           # Railway/Heroku config
├── runtime.txt        # Python version
└── railway.json       # Railway config
```

## 💰 Custos

- **Railway:** $5/mês (500h grátis)
- **Render:** Grátis (hiberna após 15min)
- **Fly.io:** Grátis (bom limite)

## 📞 Suporte

Para suporte, entre em contato com T.I Joe.

## 📝 Licença

© 2026 T.I Joe - Todos os direitos reservados
