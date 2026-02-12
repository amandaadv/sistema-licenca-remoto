# 🔐 SISTEMA DE LICENÇAS REMOTO - ZAPJOE V2

Sistema completo de licenciamento remoto com validação online, gerenciamento via CLI e proteção por hardware.

## 🎯 VANTAGENS SOBRE O SISTEMA ANTIGO

| Antigo (Local) | Novo (Remoto) |
|----------------|---------------|
| ❌ Copiar arquivo `.sec` manualmente | ✅ Efeito imediato, sem copiar arquivos |
| ❌ Cliente pode apagar arquivo | ✅ Validação sempre online |
| ❌ XOR fraco, fácil de quebrar | ✅ Criptografia forte + Hardware Lock |
| ❌ Digitar nome manualmente | ✅ Lista clientes para escolher |
| ❌ Offline, sem controle | ✅ Controle total remoto |

## 📂 ESTRUTURA

```
.sistema_licenca_remoto/
├── server/
│   └── api.py              # Servidor FastAPI
├── admin/
│   └── painel_admin.py     # Painel CLI para gerenciar
├── cliente/
│   └── licenca_client.py   # Biblioteca para usar no seu programa
├── requirements.txt
└── README.md
```

## 🚀 INSTALAÇÃO

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Configurar Servidor

Edite `server/api.py` e altere:

```python
MASTER_KEY = "SUA_CHAVE_SECRETA_AQUI_MUDE_ISSO_2026"
```

### 3. Iniciar Servidor

```bash
cd server
python api.py
```

Servidor estará rodando em: `http://localhost:8000`

Documentação: `http://localhost:8000/docs`

### 4. Configurar Painel Admin

Edite `admin/painel_admin.py` e altere:

```python
SERVIDOR_URL = "http://localhost:8000"
ADMIN_KEY = "SUA_CHAVE_SECRETA_AQUI_MUDE_ISSO_2026"  # MESMA do server/api.py
```

### 5. Usar Painel Admin

```bash
cd admin
python painel_admin.py
```

## 📖 COMO USAR

### Gerenciar Licenças (Admin)

1. Execute `python painel_admin.py`
2. Escolha a opção desejada:
   - Listar clientes
   - Adicionar novo cliente
   - Renovar licença
   - Bloquear/Desbloquear
   - Remover

**IMPORTANTE:** Mudanças são **IMEDIATAS** - não precisa copiar arquivos!

### Usar no Seu Programa (Cliente)

```python
from licenca_client import LicencaClient

# Criar cliente (usar URL do servidor em produção)
cliente = LicencaClient(servidor_url="http://localhost:8000")

# Opção 1: Tela de login automática
if cliente.tela_login():
    print("Sistema iniciado!")
    # Seu código aqui...

# Opção 2: Validação manual
valido, mensagem, dados = cliente.validar("usuario", "senha")
if valido:
    print("Licença válida!")
else:
    print(f"Erro: {mensagem}")
    sys.exit(1)
```

## 🌐 HOSPEDAR EM NUVEM (GRÁTIS)

### Opção 1: Railway (Recomendado)

1. Crie conta: https://railway.app
2. New Project → Deploy from GitHub
3. Conecte seu repositório
4. Configure:
   - Start Command: `cd server && python api.py`
   - PORT: 8000
5. Copie a URL gerada (ex: `https://zapjoe-licenses.up.railway.app`)

### Opção 2: Render

1. Crie conta: https://render.com
2. New → Web Service
3. Connect repository
4. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `cd server && python api.py`
5. Copie a URL gerada

### Opção 3: Heroku

1. Crie conta: https://heroku.com
2. Install Heroku CLI
3. Execute:
```bash
heroku create zapjoe-licenses
git push heroku main
```

**Depois de hospedar:**

1. Atualize `SERVIDOR_URL` em `admin/painel_admin.py`
2. Atualize `servidor_url` em `cliente/licenca_client.py`

## 🔒 SEGURANÇA

### Hardware Lock

O sistema vincula a licença ao hardware do cliente:
- Se cliente tentar usar em outro PC, será bloqueado
- Hardware ID baseado em: MAC, Sistema Operacional, Processador

### Validação Online Obrigatória

- **NÃO FUNCIONA OFFLINE**
- Cliente precisa de conexão com servidor
- Impossível burlar removendo arquivos

### Criptografia

- Senhas: PBKDF2 com SHA-256 + 100.000 iterações
- Salt único por usuário
- Impossível reverter hash

## 📊 ENDPOINTS DA API

### Admin (Requer X-Admin-Key header)

- `POST /admin/criar_licenca` - Cria nova licença
- `GET /admin/listar_licencas` - Lista todas as licenças
- `POST /admin/bloquear` - Bloqueia/desbloqueia
- `POST /admin/renovar/{usuario}/{dias}` - Renova licença
- `DELETE /admin/remover/{usuario}` - Remove licença

### Cliente (Público)

- `POST /validar` - Valida licença

## ❓ FAQ

### Como proteger ainda mais o código do cliente?

Use **Pyarmor** para ofuscar o código Python:

```bash
pip install pyarmor
pyarmor gen --pack onefile seu_programa.py
```

### Cliente pode usar sem internet?

Não. O sistema **FORÇA** validação online. Não há modo offline.

### E se o servidor cair?

- Use serviços confiáveis (Railway, Render)
- Configure múltiplos servidores (fallback)
- Monitore uptime

### Como transferir licença para outro PC?

1. Admin: remova o hardware_id do banco
2. Cliente: faça login no novo PC
3. Sistema vinculará ao novo hardware automaticamente

## 🛠️ DESENVOLVIMENTO

### Testar localmente

Terminal 1 (Servidor):
```bash
cd server
python api.py
```

Terminal 2 (Admin):
```bash
cd admin
python painel_admin.py
```

Terminal 3 (Cliente):
```bash
cd cliente
python licenca_client.py
```

### Banco de dados

O servidor salva dados em `licencas_db.json`. Faça backup regularmente!

## 📝 NOTAS IMPORTANTES

1. **MUDE A MASTER_KEY** - Use uma chave forte e única
2. **Use HTTPS** - Em produção, SEMPRE use HTTPS
3. **Backup** - Faça backup do arquivo `licencas_db.json`
4. **Monitore** - Configure alertas para o servidor
5. **Versione** - Use controle de versão (Git)

## 📞 SUPORTE

Sistema desenvolvido para ZAPJOE V2 por T.I Joe

---

**Versão:** 2.0
**Data:** 2026-02-11
**Status:** ✅ Produção
