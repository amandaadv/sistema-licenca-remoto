# 🚀 DEPLOY NO HOSTINGER VPS

## ⚠️ ATENÇÃO
Isso é para **VPS**, não hospedagem compartilhada!

---

## 📋 PASSO 1: COMPRAR VPS

1. **Acessar:** https://www.hostinger.com.br/vps-hospedagem
2. **Plano:** KVM 1 (R$19/mês) - Suficiente
3. **Sistema:** Ubuntu 22.04
4. **Comprar e aguardar setup** (5-10 min)

---

## 🔐 PASSO 2: ACESSAR VIA SSH

### **2.1 - Pegar credenciais:**
- Email da Hostinger terá:
  - IP: `123.456.789.10`
  - Usuário: `root`
  - Senha: `abc123xyz`

### **2.2 - Conectar:**
```bash
ssh root@123.456.789.10
```

Digite a senha quando pedir.

---

## 📦 PASSO 3: INSTALAR PYTHON

```bash
# Atualizar sistema
apt update && apt upgrade -y

# Instalar Python e pip
apt install python3 python3-pip python3-venv git -y

# Verificar
python3 --version
# Deve mostrar: Python 3.10.x
```

---

## 📤 PASSO 4: SUBIR CÓDIGO

### **Opção A: Via Git (Recomendado)**

```bash
# Clonar repositório
cd /root
git clone https://github.com/SEU_USUARIO/zapjoe-license-server.git
cd zapjoe-license-server
```

### **Opção B: Via FTP**

1. Use FileZilla ou WinSCP
2. Conecte no IP do VPS
3. Upload pasta `server/` para `/root/zapjoe-license-server/`

---

## 🔧 PASSO 5: INSTALAR DEPENDÊNCIAS

```bash
cd /root/zapjoe-license-server

# Criar ambiente virtual
python3 -m venv venv

# Ativar
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

---

## 🚀 PASSO 6: INICIAR SERVIDOR

### **Teste inicial:**
```bash
uvicorn api:app --host 0.0.0.0 --port 8000
```

Abra no navegador:
```
http://SEU_IP_VPS:8000/docs
```

Se funcionar, Ctrl+C para parar.

---

## 🔄 PASSO 7: RODAR 24/7 (PM2)

### **Instalar PM2:**
```bash
# Instalar Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
apt install nodejs -y

# Instalar PM2
npm install -g pm2
```

### **Criar script de start:**
```bash
cat > start.sh << 'EOF'
#!/bin/bash
cd /root/zapjoe-license-server
source venv/bin/activate
uvicorn api:app --host 0.0.0.0 --port 8000
EOF

chmod +x start.sh
```

### **Iniciar com PM2:**
```bash
pm2 start start.sh --name zapjoe-server
pm2 save
pm2 startup
```

**Pronto! Servidor rodando 24/7!** ✅

---

## 🌐 PASSO 8: CONFIGURAR DOMÍNIO (Opcional)

### **Sem domínio:**
```
http://SEU_IP_VPS:8000
```

### **Com domínio:**

1. **No painel da Hostinger:**
   - DNS Zone Editor
   - Adicionar registro A:
     ```
     Type: A
     Name: api
     Value: SEU_IP_VPS
     ```

2. **Instalar Nginx:**
```bash
apt install nginx -y
```

3. **Configurar proxy reverso:**
```bash
cat > /etc/nginx/sites-available/zapjoe << 'EOF'
server {
    listen 80;
    server_name api.seudominio.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
EOF

ln -s /etc/nginx/sites-available/zapjoe /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

4. **SSL grátis (Certbot):**
```bash
apt install certbot python3-certbot-nginx -y
certbot --nginx -d api.seudominio.com
```

**URL final:**
```
https://api.seudominio.com
```

---

## 🔒 PASSO 9: SEGURANÇA

### **Firewall:**
```bash
# Instalar UFW
apt install ufw -y

# Liberar portas
ufw allow 22    # SSH
ufw allow 80    # HTTP
ufw allow 443   # HTTPS
ufw allow 8000  # API (se não usar Nginx)

# Ativar
ufw enable
```

### **Mudar MASTER_KEY:**
```bash
cd /root/zapjoe-license-server
nano api.py
```

Alterar linha:
```python
MASTER_KEY = os.getenv("MASTER_KEY", "SUA_CHAVE_SUPER_SECRETA_AQUI")
```

Salvar (Ctrl+X, Y, Enter)

Reiniciar:
```bash
pm2 restart zapjoe-server
```

---

## 🔄 ATUALIZAR CÓDIGO

```bash
cd /root/zapjoe-license-server
git pull
pm2 restart zapjoe-server
```

---

## 📊 MONITORAR

### **Ver logs:**
```bash
pm2 logs zapjoe-server
```

### **Status:**
```bash
pm2 status
```

### **Reiniciar:**
```bash
pm2 restart zapjoe-server
```

---

## 💰 CUSTO TOTAL

- **VPS:** R$19/mês
- **Domínio:** R$40/ano (opcional)
- **SSL:** Grátis (Certbot)

**Total:** ~R$23/mês

---

## 🆚 RAILWAY vs HOSTINGER VPS

| Aspecto | Railway | Hostinger VPS |
|---------|---------|---------------|
| **Custo** | $5 (R$25) | R$19 |
| **Setup** | 5 min | 30 min |
| **Facilidade** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **SSH** | ❌ | ✅ |
| **Controle** | Limitado | Total |
| **SSL** | Auto | Manual |
| **Deploy** | Git push | SSH/Git |

---

## 🎯 CONCLUSÃO

**Hostinger VPS funciona, mas:**
- ⚠️ Mais trabalho (30 min vs 5 min)
- ⚠️ Precisa manutenção
- ⚠️ Você gerencia segurança
- ⚠️ Você gerencia updates

**Railway:**
- ✅ Deploy automático
- ✅ SSL automático
- ✅ Zero manutenção
- ✅ Logs/monitoring incluído

**Economiza R$6/mês mas gasta 2-3 horas setup + manutenção mensal.**

**Vale mais a pena Railway para focar em VENDER! 🚀**
