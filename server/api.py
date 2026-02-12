# -*- coding: utf-8 -*-
"""
API DE LICENÇAS REMOTO - ZAPJOE V2
Servidor FastAPI para gerenciar licenças remotamente
"""

from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import hashlib
import secrets
import json
import os
from datetime import datetime, timedelta
import uvicorn

app = FastAPI(title="ZAPJOE License Server", version="2.0")

# CORS para permitir painel web
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique domínios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# CONFIGURAÇÕES
# ==========================================

# Chave mestra do servidor (usa variável de ambiente se disponível)
MASTER_KEY = os.getenv("MASTER_KEY", "SUA_CHAVE_SECRETA_AQUI_MUDE_ISSO_2026")

# Arquivo de dados
DATA_FILE = os.getenv("DATA_FILE", "licencas_db.json")

# ==========================================
# MODELOS
# ==========================================

class Usuario(BaseModel):
    usuario: str
    senha: str

class NovaLicenca(BaseModel):
    usuario: str
    senha: str
    dias_validade: int = 30
    hardware_id: Optional[str] = None

class ValidarLicenca(BaseModel):
    usuario: str
    senha: str
    hardware_id: str
    versao_programa: str = "2.0"

class AlterarStatus(BaseModel):
    usuario: str
    ativo: bool

# ==========================================
# FUNÇÕES AUXILIARES
# ==========================================

def carregar_dados():
    """Carrega dados do arquivo JSON"""
    if not os.path.exists(DATA_FILE):
        return {}

    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

def salvar_dados(dados):
    """Salva dados no arquivo JSON"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)

def hash_senha(senha, salt=None):
    """Hash seguro de senha com salt"""
    if salt is None:
        salt = secrets.token_hex(16)

    senha_hash = hashlib.pbkdf2_hmac(
        'sha256',
        senha.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    ).hex()

    return senha_hash, salt

def verificar_senha(senha, senha_hash, salt):
    """Verifica se senha está correta"""
    hash_calculado, _ = hash_senha(senha, salt)
    return hash_calculado == senha_hash

def gerar_token_auth():
    """Gera token de autenticação"""
    return secrets.token_urlsafe(32)

def verificar_admin_key(x_admin_key: str = Header(None)):
    """Verifica se tem permissão de admin"""
    if x_admin_key != MASTER_KEY:
        raise HTTPException(status_code=401, detail="Chave de admin inválida")
    return True

# ==========================================
# ENDPOINTS - ADMIN
# ==========================================

@app.post("/admin/criar_licenca")
async def criar_licenca(licenca: NovaLicenca, _: bool = Depends(verificar_admin_key)):
    """
    Cria nova licença (apenas admin)
    """
    dados = carregar_dados()

    if licenca.usuario in dados:
        raise HTTPException(status_code=400, detail="Usuário já existe")

    # Hash da senha
    senha_hash, salt = hash_senha(licenca.senha)

    # Calcular validade
    validade = (datetime.now() + timedelta(days=licenca.dias_validade)).isoformat()

    # Criar licença
    dados[licenca.usuario] = {
        'senha_hash': senha_hash,
        'salt': salt,
        'criado_em': datetime.now().isoformat(),
        'validade': validade,
        'ativo': True,
        'hardware_id': licenca.hardware_id,
        'ultimo_login': None,
        'total_logins': 0,
        'versao_programa': '2.0'
    }

    salvar_dados(dados)

    return {
        "sucesso": True,
        "mensagem": "Licença criada com sucesso",
        "usuario": licenca.usuario,
        "validade": validade
    }

@app.get("/admin/listar_licencas")
async def listar_licencas(_: bool = Depends(verificar_admin_key)):
    """
    Lista todas as licenças (apenas admin)
    """
    dados = carregar_dados()

    licencas = []
    for usuario, info in dados.items():
        try:
            validade = datetime.fromisoformat(info['validade'])
            dias_restantes = (validade - datetime.now()).days

            licencas.append({
                'usuario': usuario,
                'ativo': info.get('ativo', False),
                'validade': info['validade'],
                'dias_restantes': dias_restantes,
                'ultimo_login': info.get('ultimo_login'),
                'total_logins': info.get('total_logins', 0),
                'hardware_id': info.get('hardware_id', 'N/A'),
                'versao_programa': info.get('versao_programa', 'N/A')
            })
        except:
            continue

    return {
        "total": len(licencas),
        "licencas": licencas
    }

@app.post("/admin/bloquear")
async def bloquear_licenca(alteracao: AlterarStatus, _: bool = Depends(verificar_admin_key)):
    """
    Bloqueia ou desbloqueia licença (apenas admin)
    """
    dados = carregar_dados()

    if alteracao.usuario not in dados:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    dados[alteracao.usuario]['ativo'] = alteracao.ativo
    salvar_dados(dados)

    acao = "desbloqueada" if alteracao.ativo else "bloqueada"

    return {
        "sucesso": True,
        "mensagem": f"Licença {acao} com sucesso",
        "usuario": alteracao.usuario,
        "ativo": alteracao.ativo
    }

@app.post("/admin/renovar/{usuario}/{dias}")
async def renovar_licenca(usuario: str, dias: int, _: bool = Depends(verificar_admin_key)):
    """
    Renova licença adicionando dias (apenas admin)
    """
    dados = carregar_dados()

    if usuario not in dados:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    licenca = dados[usuario]

    try:
        validade_atual = datetime.fromisoformat(licenca['validade'])

        # Se já expirou, renovar a partir de agora
        if validade_atual < datetime.now():
            nova_validade = datetime.now() + timedelta(days=dias)
        else:
            nova_validade = validade_atual + timedelta(days=dias)

        licenca['validade'] = nova_validade.isoformat()
        licenca['ativo'] = True

        dados[usuario] = licenca
        salvar_dados(dados)

        return {
            "sucesso": True,
            "mensagem": "Licença renovada com sucesso",
            "usuario": usuario,
            "nova_validade": nova_validade.isoformat(),
            "dias_restantes": (nova_validade - datetime.now()).days
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/admin/remover/{usuario}")
async def remover_licenca(usuario: str, _: bool = Depends(verificar_admin_key)):
    """
    Remove licença (apenas admin)
    """
    dados = carregar_dados()

    if usuario not in dados:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    del dados[usuario]
    salvar_dados(dados)

    return {
        "sucesso": True,
        "mensagem": "Licença removida com sucesso",
        "usuario": usuario
    }

# ==========================================
# ENDPOINTS - CLIENTE
# ==========================================

@app.post("/validar")
async def validar_licenca(validacao: ValidarLicenca):
    """
    Valida licença do cliente (público)
    Este é o endpoint que o programa do cliente chama
    """
    dados = carregar_dados()

    usuario = validacao.usuario

    # Verificar se usuário existe
    if usuario not in dados:
        return {
            "valido": False,
            "mensagem": "❌ Usuário não encontrado"
        }

    licenca = dados[usuario]

    # Verificar se está ativo
    if not licenca.get('ativo', False):
        return {
            "valido": False,
            "mensagem": "🔒 Licença BLOQUEADA\n\n📞 Contate T.I Joe para reativar"
        }

    # Verificar senha
    if not verificar_senha(validacao.senha, licenca['senha_hash'], licenca['salt']):
        return {
            "valido": False,
            "mensagem": "❌ Senha incorreta"
        }

    # Verificar validade
    try:
        validade = datetime.fromisoformat(licenca['validade'])
        if datetime.now() > validade:
            return {
                "valido": False,
                "mensagem": "⏰ Licença EXPIRADA\n\n📞 Contate T.I Joe para renovar"
            }

        dias_restantes = (validade - datetime.now()).days
    except:
        return {
            "valido": False,
            "mensagem": "❌ Erro ao verificar validade"
        }

    # Verificar hardware ID (vincular licença ao computador)
    # DESABILITADO - Permite usar em qualquer computador
    hardware_id_salvo = licenca.get('hardware_id')
    if hardware_id_salvo is None:
        # Primeira vez que usa - salvar hardware ID
        licenca['hardware_id'] = validacao.hardware_id
    # elif hardware_id_salvo != validacao.hardware_id:
    #     # Hardware diferente - licença vinculada a outro PC
    #     return {
    #         "valido": False,
    #         "mensagem": "🔒 Licença vinculada a outro computador\n\n📞 Contate T.I Joe para transferir"
    #     }

    # Atualizar último login
    licenca['ultimo_login'] = datetime.now().isoformat()
    licenca['total_logins'] = licenca.get('total_logins', 0) + 1
    licenca['versao_programa'] = validacao.versao_programa

    dados[usuario] = licenca
    salvar_dados(dados)

    # Login válido!
    return {
        "valido": True,
        "mensagem": f"✅ Licença válida\n\n📅 {dias_restantes} dias restantes",
        "dias_restantes": dias_restantes,
        "validade": licenca['validade'],
        "usuario": usuario
    }

@app.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "nome": "ZAPJOE License Server",
        "versao": "2.0",
        "status": "online",
        "total_licencas": len(carregar_dados())
    }

@app.get("/health")
async def health():
    """Verifica saúde do servidor"""
    return {"status": "healthy"}

# ==========================================
# START SERVIDOR (LOCAL / RAILWAY)
# ==========================================

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("api:app", host="0.0.0.0", port=port)


