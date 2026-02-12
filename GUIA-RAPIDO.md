# 🚀 GUIA RÁPIDO - 5 MINUTOS

## ✅ PASSO 1: INSTALAR (1 minuto)

```bash
cd "C:\Users\Joe\Downloads\.sistema_licenca_remoto"
pip install -r requirements.txt
```

## ✅ PASSO 2: CONFIGURAR CHAVE (30 segundos)

Abra `server/api.py` e altere a linha 28:

```python
MASTER_KEY = "MinhaChaveSecreta2026JoeFerson"  # MUDE ISSO!
```

Abra `admin/painel_admin.py` e altere as linhas 11-12:

```python
SERVIDOR_URL = "http://localhost:8000"
ADMIN_KEY = "MinhaChaveSecreta2026JoeFerson"  # MESMA do api.py!
```

## ✅ PASSO 3: INICIAR SERVIDOR (1 minuto)

```bash
cd server
python api.py
```

Deixe rodando. Abra novo terminal.

## ✅ PASSO 4: ADICIONAR CLIENTE (1 minuto)

```bash
cd admin
python painel_admin.py
```

Escolha: `2. Adicionar novo cliente`

- Usuário: `joeferson`
- Senha: `123456`
- Validade: `2` (30 dias)

## ✅ PASSO 5: TESTAR CLIENTE (1 minuto)

```bash
cd cliente
python licenca_client.py
```

- Usuário: `joeferson`
- Senha: `123456`

Se aparecer "✅ Licença válida" → **FUNCIONOU!**

---

## 🎯 USAR NO SEU PROGRAMA ZAPJOE

Abra o arquivo principal do ZAPJOE (ex: `main.py`) e adicione NO INÍCIO:

```python
# ===== VALIDAÇÃO DE LICENÇA =====
import sys
import os

# Adicionar pasta do cliente ao path
sys.path.insert(0, r"C:\Users\Joe\Downloads\.sistema_licenca_remoto\cliente")

from licenca_client import LicencaClient

# Criar cliente (em produção, use URL da nuvem)
cliente = LicencaClient(servidor_url="http://localhost:8000")

# Validar licença ANTES de iniciar o programa
if not cliente.tela_login(titulo="ZAPJOE V2 - AUTENTICAÇÃO"):
    print("❌ Licença inválida!")
    sys.exit(1)

# ===== RESTO DO SEU PROGRAMA =====
# Código do ZAPJOE continua aqui...
```

**PRONTO!** Agora o ZAPJOE só inicia se a licença estiver válida.

---

## 🌐 HOSPEDAR NA NUVEM (GRÁTIS)

### Railway (Mais fácil)

1. Vá em: https://railway.app
2. Faça login com GitHub
3. "New Project" → "Deploy from GitHub"
4. Selecione o repositório
5. Configure:
   - **Start Command:** `cd server && python api.py`
   - **PORT:** `8000`
6. Copie a URL (ex: `https://zapjoe.up.railway.app`)
7. Atualize `SERVIDOR_URL` no `painel_admin.py`
8. Atualize `servidor_url` no seu programa ZAPJOE

**PRONTO! Agora funciona de qualquer lugar do mundo.**

---

## 🔒 SOBRE SEGURANÇA

### ❓ Cliente pode burlar?

**NÃO!** Porque:

1. **Sem arquivo local** - Não tem nada para apagar
2. **Validação online** - Sempre conecta ao servidor
3. **Hardware Lock** - Vinculado ao computador
4. **Sem offline** - Não funciona sem internet

### ❓ E se ele descompilar o .py?

Use **Pyarmor** para proteger:

```bash
pip install pyarmor
pyarmor gen --pack onefile seu_programa.py
```

Isso gera um `.exe` impossível de descompilar.

### ❓ Posso ver quem está usando?

SIM! No painel admin: `1. Listar clientes`

Mostra:
- Último login
- Total de logins
- Hardware ID
- Dias restantes

---

## 📊 GERENCIAR REMOTAMENTE

No painel admin você pode:

✅ **Ver todos os clientes**
✅ **Bloquear/Desbloquear** (efeito imediato)
✅ **Renovar licença** (sem copiar arquivos)
✅ **Remover cliente**

**Tudo remoto!** Cliente não precisa fazer nada.

---

## ⚡ COMANDOS RÁPIDOS

```bash
# Iniciar servidor
cd server && python api.py

# Painel admin
cd admin && python painel_admin.py

# Testar cliente
cd cliente && python licenca_client.py
```

---

## 🆘 PROBLEMAS?

### "Erro ao conectar ao servidor"

- Servidor está rodando?
- URL está correta?
- Firewall bloqueando?

### "Chave de admin inválida"

- `ADMIN_KEY` em `painel_admin.py` == `MASTER_KEY` em `api.py`?

### "Licença vinculada a outro computador"

No admin:
1. Remova o cliente
2. Crie novamente (hardware será resetado)

---

**PRONTO! Sistema 100% funcional e remoto.**
