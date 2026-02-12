# 🚀 DEPLOY NO RAILWAY - PASSO A PASSO

## 📋 O QUE VOCÊ VAI FAZER:

1. Criar conta no Railway (grátis)
2. Conectar com GitHub
3. Fazer upload do código
4. Deploy automático
5. Pegar URL pública
6. Configurar cliente

**Tempo total: ~10 minutos**

---

## 🎯 PASSO 1: CRIAR CONTA

### **1.1 - Acessar Railway:**
👉 https://railway.app/

### **1.2 - Criar conta:**
- Clique em **"Start a New Project"**
- Login com **GitHub** (recomendado) ou Email

### **1.3 - Verificar email** (se usar email)

---

## 📦 PASSO 2: CRIAR REPOSITÓRIO NO GITHUB

### **2.1 - Acessar GitHub:**
👉 https://github.com/

### **2.2 - Criar novo repositório:**
- Clique em **"New repository"**
- Nome: `zapjoe-license-server`
- Descrição: `ZAPJOE V2 License Server`
- **Private** (importante!)
- ✅ Add README
- Clique em **"Create repository"**

### **2.3 - Copiar URL do repositório:**
```
https://github.com/SEU_USUARIO/zapjoe-license-server
```

---

## 📤 PASSO 3: SUBIR CÓDIGO PARA GITHUB

### **3.1 - Abrir PowerShell na pasta do servidor:**
```powershell
cd C:\Users\Joe\Downloads\.sistema_licenca_remoto\server
```

### **3.2 - Configurar Git (primeira vez):**
```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu@email.com"
```

### **3.3 - Inicializar repositório:**
```bash
# Inicializar Git
git init

# Adicionar arquivos
git add .

# Primeiro commit
git commit -m "Initial commit - ZAPJOE License Server"

# Conectar com GitHub (COLE A URL DO SEU REPO)
git remote add origin https://github.com/SEU_USUARIO/zapjoe-license-server.git

# Enviar código
git branch -M main
git push -u origin main
```

Se pedir senha, use **Personal Access Token** do GitHub:
👉 https://github.com/settings/tokens

---

## 🚂 PASSO 4: DEPLOY NO RAILWAY

### **4.1 - Voltar ao Railway:**
👉 https://railway.app/dashboard

### **4.2 - Criar novo projeto:**
- Clique em **"New Project"**
- Selecione **"Deploy from GitHub repo"**
- Autorize Railway a acessar seu GitHub
- Selecione o repositório: **zapjoe-license-server**

### **4.3 - Configurar variáveis (opcional):**
- Clique em **"Variables"**
- Adicionar:
  - `MASTER_KEY`: `SUA_CHAVE_SECRETA_AQUI_MUDE_ISSO_2026`
  - `PORT`: `8000`

### **4.4 - Deploy automático:**
Railway vai:
1. ✅ Detectar Python
2. ✅ Instalar dependências (requirements.txt)
3. ✅ Iniciar servidor (Procfile)
4. ✅ Gerar URL pública

**Aguarde 2-3 minutos...**

---

## 🌐 PASSO 5: PEGAR URL PÚBLICA

### **5.1 - Clicar em "Settings" → "Domains"**

### **5.2 - Gerar domínio:**
- Clique em **"Generate Domain"**
- Railway vai gerar algo como:
  ```
  https://zapjoe-license-server-production.up.railway.app
  ```

### **5.3 - COPIAR ESSA URL!** 📋

---

## 🔧 PASSO 6: CONFIGURAR CLIENTE

### **6.1 - No programa do cliente:**
Editar:
```
C:\Users\Joe\Videos\shein\config\servidor_licenca.json
```

Mudar para:
```json
{
  "servidor_url": "https://zapjoe-license-server-production.up.railway.app"
}
```

### **6.2 - PRONTO!** ✅

Agora qualquer PC no mundo pode usar o sistema!

---

## ✅ TESTAR

### **No navegador:**
```
https://sua-url.railway.app/docs
```

Deve abrir a documentação da API! ✅

### **No programa:**
```bash
cd C:\Users\Joe\Videos\shein
python main.py
```

Login:
- **Usuário:** `vpsbrasil`
- **Senha:** `123456`

**Deve funcionar de qualquer lugar! 🌍**

---

## 💰 CUSTOS

### **Railway Pricing:**

| Plano | Custo | Recursos |
|-------|-------|----------|
| **Trial** | Grátis | 500h/mês (~20 dias) |
| **Hobby** | $5/mês | Ilimitado |

**Recomendação:** Use Trial para testar, depois upgrade para Hobby.

---

## 🔒 SEGURANÇA

### **1. Mudar MASTER_KEY:**
No Railway, em **"Variables"**:
```
MASTER_KEY=MUDE_PARA_ALGO_SUPER_SECRETO_E_ALEATORIO_2026
```

### **2. Mesmo no api.py:**
Editar `C:\Users\Joe\Downloads\.sistema_licenca_remoto\server\api.py`:
```python
MASTER_KEY = os.getenv("MASTER_KEY", "SUA_CHAVE_AQUI")
```

### **3. Commit e push:**
```bash
git add .
git commit -m "Update security"
git push
```

Railway faz **redeploy automático**! ✅

---

## 🔄 ATUALIZAR SERVIDOR

Quando você fizer mudanças no código:

```bash
cd C:\Users\Joe\Downloads\.sistema_licenca_remoto\server

git add .
git commit -m "Update: descrição da mudança"
git push
```

Railway **redeploy automático** em 1-2 minutos! 🚀

---

## 🐛 PROBLEMAS COMUNS

### **"Build failed"**
- Verificar `requirements.txt`
- Verificar se `api.py` não tem erros

### **"Application error"**
- Verificar logs no Railway
- Dashboard → Deployments → Ver logs

### **"502 Bad Gateway"**
- Servidor pode estar iniciando (aguarde 1-2 min)
- Verificar se porta está correta ($PORT)

---

## 📞 SUPORTE RAILWAY

- Docs: https://docs.railway.app/
- Discord: https://discord.gg/railway
- Status: https://status.railway.app/

---

## 🎉 PRÓXIMOS PASSOS

### **Opcional: Domínio próprio**

Ao invés de `*.railway.app`, use seu próprio domínio:

1. Comprar domínio (ex: `registro.br` - R$40/ano)
2. No Railway: Settings → Domains → Custom Domain
3. Configurar DNS (CNAME)

Exemplo: `https://licenses.zapjoe.com.br`

**Muito mais profissional! 🚀**
