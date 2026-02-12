# -*- coding: utf-8 -*-
"""
PAINEL ADMIN CLI - ZAPJOE V2
Gerencia licenças remotamente via linha de comando
"""

import requests
import os
import sys
from datetime import datetime

# Configurar UTF-8 no Windows
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

# CONFIGURAÇÃO
SERVIDOR_URL = "http://localhost:8000"
ADMIN_KEY = "SUA_CHAVE_SECRETA_AQUI_MUDE_ISSO_2026"  # DEVE SER A MESMA do server/api.py

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def linha():
    return "=" * 70

def fazer_requisicao(method, endpoint, json_data=None):
    """Faz requisição ao servidor"""
    headers = {"X-Admin-Key": ADMIN_KEY}

    try:
        url = f"{SERVIDOR_URL}{endpoint}"

        if method == "GET":
            response = requests.get(url, headers=headers, timeout=10)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=json_data, timeout=10)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers, timeout=10)
        else:
            return None, "Método inválido"

        if response.status_code in [200, 201]:
            return response.json(), None
        elif response.status_code == 401:
            return None, "[X] CHAVE DE ADMIN INVÁLIDA! Verifique ADMIN_KEY"
        else:
            return None, f"Erro {response.status_code}: {response.text}"

    except requests.exceptions.ConnectionError:
        return None, "[X] Não foi possível conectar ao servidor"
    except requests.exceptions.Timeout:
        return None, "[Time] Timeout ao conectar"
    except Exception as e:
        return None, f"Erro: {str(e)}"

def menu_principal():
    limpar_tela()
    print()
    print(linha())
    print("          PAINEL ADMIN REMOTO - ZAPJOE V2")
    print(linha())
    print()
    print("  1. [Lista] Listar todos os clientes")
    print("  2. [Add] Adicionar novo cliente")
    print("  3. [Renova] Renovar licenca")
    print("  4. [Bloqueia] Bloquear cliente")
    print("  5. [Desbloqueia] Desbloquear cliente")
    print("  6. [Remove] Remover cliente")
    print("  7. [Config] Configurar servidor")
    print("  0. [Sair] Sair")
    print()
    print(linha())
    print()

def listar_clientes():
    limpar_tela()
    print()
    print(linha())
    print("          CLIENTES CADASTRADOS")
    print(linha())
    print()

    dados, erro = fazer_requisicao("GET", "/admin/listar_licencas")

    if erro:
        print(f"  [X] Erro: {erro}")
    elif not dados or dados['total'] == 0:
        print("  [!] Nenhum cliente cadastrado")
    else:
        print(f"  Total: {dados['total']} clientes\n")

        for i, lic in enumerate(dados['licencas'], 1):
            status = "[ATIVO]" if lic['ativo'] else "[BLOQUEADO]"

            print(f"  [{i}] {status} - {lic['usuario']}")
            print(f"      Dias restantes: {lic['dias_restantes']}")

            try:
                validade = datetime.fromisoformat(lic['validade'])
                print(f"      Vence em: {validade.strftime('%d/%m/%Y %H:%M')}")
            except:
                pass

            ultimo_login = lic.get('ultimo_login', 'Nunca')
            if ultimo_login and ultimo_login != 'Nunca':
                try:
                    dt = datetime.fromisoformat(ultimo_login)
                    ultimo_login = dt.strftime('%d/%m/%Y %H:%M')
                except:
                    pass

            print(f"      Ultimo login: {ultimo_login}")
            print(f"      Total logins: {lic.get('total_logins', 0)}")

            # Hardware ID com verificação segura
            hardware_id = lic.get('hardware_id')
            if hardware_id and len(hardware_id) > 16:
                print(f"      Hardware ID: {hardware_id[:16]}...")
            elif hardware_id:
                print(f"      Hardware ID: {hardware_id}")
            else:
                print(f"      Hardware ID: N/A")

            print()

    print(linha())
    input("\n  Pressione ENTER para voltar...")

def adicionar_cliente():
    limpar_tela()
    print()
    print(linha())
    print("          [+] ADICIONAR NOVO CLIENTE")
    print(linha())
    print()

    usuario = input("  [User] Usuário: ").strip()
    if len(usuario) < 3:
        print("\n  [X] Usuário deve ter pelo menos 3 caracteres")
        input("\n  Pressione ENTER para voltar...")
        return

    senha = input("  [Lock] Senha: ").strip()
    if len(senha) < 4:
        print("\n  [X] Senha deve ter pelo menos 4 caracteres")
        input("\n  Pressione ENTER para voltar...")
        return

    print()
    print("  [Data] Validade da licença:")
    print("    1. 7 dias (trial)")
    print("    2. 30 dias (mensal)")
    print("    3. 90 dias (trimestral)")
    print("    4. 365 dias (anual)")
    print("    5. 36500 dias (vitalício)")
    print("    6. Personalizado")
    print()

    opcao = input("  Escolha: ").strip()

    dias_map = {"1": 7, "2": 30, "3": 90, "4": 365, "5": 36500}

    if opcao in dias_map:
        dias = dias_map[opcao]
    elif opcao == "6":
        try:
            dias = int(input("\n  Quantos dias? "))
            if dias <= 0:
                print("\n  [X] Número inválido")
                input("\n  Pressione ENTER para voltar...")
                return
        except:
            print("\n  [X] Número inválido")
            input("\n  Pressione ENTER para voltar...")
            return
    else:
        print("\n  [X] Opção inválida")
        input("\n  Pressione ENTER para voltar...")
        return

    # Criar licença
    print()
    print("  [->] Criando licença...")

    dados, erro = fazer_requisicao("POST", "/admin/criar_licenca", {
        "usuario": usuario,
        "senha": senha,
        "dias_validade": dias
    })

    print()
    if erro:
        print(f"  [X] Erro: {erro}")
    else:
        print("  [OK] Cliente adicionado com sucesso!")
        print()
        print(f"  [User] Usuário: {usuario}")
        print(f"  [Lock] Senha: {senha}")
        print(f"  [Data] Validade: {dias} dias")
        print()
        print("  [!] Cliente já pode fazer login remotamente!")
        print("  [Net] Não precisa copiar nenhum arquivo!")

    print()
    input("  Pressione ENTER para voltar...")

def renovar_cliente():
    limpar_tela()
    print()
    print(linha())
    print("          [->] RENOVAR LICENÇA")
    print(linha())
    print()

    # Primeiro, listar clientes para escolher
    dados, erro = fazer_requisicao("GET", "/admin/listar_licencas")

    if erro or not dados or dados['total'] == 0:
        print("  [i]  Nenhum cliente cadastrado")
        input("\n  Pressione ENTER para voltar...")
        return

    print("  Clientes disponíveis:\n")
    for i, lic in enumerate(dados['licencas'], 1):
        status = "[+]" if lic['ativo'] else "[-]"
        print(f"  [{i}] {status} {lic['usuario']} - {lic['dias_restantes']} dias")

    print()
    escolha = input("  Escolha o número (ou digite o nome): ").strip()

    # Tentar como número primeiro
    try:
        idx = int(escolha) - 1
        if 0 <= idx < len(dados['licencas']):
            usuario = dados['licencas'][idx]['usuario']
        else:
            print("\n  [X] Número inválido")
            input("\n  Pressione ENTER para voltar...")
            return
    except:
        # Se não for número, usar como nome
        usuario = escolha

    print()
    print("  [Data] Adicionar tempo:")
    print("    1. +7 dias")
    print("    2. +30 dias")
    print("    3. +90 dias")
    print("    4. +365 dias")
    print("    5. Personalizado")
    print()

    opcao = input("  Escolha: ").strip()

    dias_map = {"1": 7, "2": 30, "3": 90, "4": 365}

    if opcao in dias_map:
        dias = dias_map[opcao]
    elif opcao == "5":
        try:
            dias = int(input("\n  Quantos dias adicionar? "))
            if dias <= 0:
                print("\n  [X] Número inválido")
                input("\n  Pressione ENTER para voltar...")
                return
        except:
            print("\n  [X] Número inválido")
            input("\n  Pressione ENTER para voltar...")
            return
    else:
        print("\n  [X] Opção inválida")
        input("\n  Pressione ENTER para voltar...")
        return

    # Renovar
    print()
    print("  [->] Renovando...")

    dados_resp, erro = fazer_requisicao("POST", f"/admin/renovar/{usuario}/{dias}")

    print()
    if erro:
        print(f"  [X] Erro: {erro}")
    else:
        print("  [OK] Licença renovada com sucesso!")
        print()
        print(f"  [User] Cliente: {usuario}")
        print(f"  [Data] Dias restantes: {dados_resp['dias_restantes']}")
        print()
        print("  [!] Renovação imediata! Cliente já pode usar.")

    print()
    input("  Pressione ENTER para voltar...")

def bloquear_cliente():
    limpar_tela()
    print()
    print(linha())
    print("          [Lock] BLOQUEAR CLIENTE")
    print(linha())
    print()

    # Listar clientes
    dados, erro = fazer_requisicao("GET", "/admin/listar_licencas")

    if erro or not dados or dados['total'] == 0:
        print("  [i]  Nenhum cliente cadastrado")
        input("\n  Pressione ENTER para voltar...")
        return

    print("  Clientes disponíveis:\n")
    for i, lic in enumerate(dados['licencas'], 1):
        status = "[+]" if lic['ativo'] else "[-]"
        print(f"  [{i}] {status} {lic['usuario']}")

    print()
    escolha = input("  Escolha o número (ou digite o nome): ").strip()

    # Tentar como número
    try:
        idx = int(escolha) - 1
        if 0 <= idx < len(dados['licencas']):
            usuario = dados['licencas'][idx]['usuario']
        else:
            print("\n  [X] Número inválido")
            input("\n  Pressione ENTER para voltar...")
            return
    except:
        usuario = escolha

    # Bloquear
    print()
    print("  [Lock] Bloqueando...")

    dados_resp, erro = fazer_requisicao("POST", "/admin/bloquear", {
        "usuario": usuario,
        "ativo": False
    })

    print()
    if erro:
        print(f"  [X] Erro: {erro}")
    else:
        print(f"  [OK] Cliente '{usuario}' BLOQUEADO!")
        print()
        print("  [!] Efeito IMEDIATO - Cliente não consegue mais logar")

    print()
    input("  Pressione ENTER para voltar...")

def desbloquear_cliente():
    limpar_tela()
    print()
    print(linha())
    print("          [Unlock] DESBLOQUEAR CLIENTE")
    print(linha())
    print()

    # Listar clientes
    dados, erro = fazer_requisicao("GET", "/admin/listar_licencas")

    if erro or not dados or dados['total'] == 0:
        print("  [i]  Nenhum cliente cadastrado")
        input("\n  Pressione ENTER para voltar...")
        return

    print("  Clientes disponíveis:\n")
    for i, lic in enumerate(dados['licencas'], 1):
        status = "[+]" if lic['ativo'] else "[-]"
        print(f"  [{i}] {status} {lic['usuario']}")

    print()
    escolha = input("  Escolha o número (ou digite o nome): ").strip()

    # Tentar como número
    try:
        idx = int(escolha) - 1
        if 0 <= idx < len(dados['licencas']):
            usuario = dados['licencas'][idx]['usuario']
        else:
            print("\n  [X] Número inválido")
            input("\n  Pressione ENTER para voltar...")
            return
    except:
        usuario = escolha

    # Desbloquear
    print()
    print("  [Unlock] Desbloqueando...")

    dados_resp, erro = fazer_requisicao("POST", "/admin/bloquear", {
        "usuario": usuario,
        "ativo": True
    })

    print()
    if erro:
        print(f"  [X] Erro: {erro}")
    else:
        print(f"  [OK] Cliente '{usuario}' DESBLOQUEADO!")
        print()
        print("  [!] Efeito IMEDIATO - Cliente já pode logar")

    print()
    input("  Pressione ENTER para voltar...")

def remover_cliente():
    limpar_tela()
    print()
    print(linha())
    print("          [Del]  REMOVER CLIENTE")
    print(linha())
    print()

    # Listar clientes
    dados, erro = fazer_requisicao("GET", "/admin/listar_licencas")

    if erro or not dados or dados['total'] == 0:
        print("  [i]  Nenhum cliente cadastrado")
        input("\n  Pressione ENTER para voltar...")
        return

    print("  Clientes disponíveis:\n")
    for i, lic in enumerate(dados['licencas'], 1):
        status = "[+]" if lic['ativo'] else "[-]"
        print(f"  [{i}] {status} {lic['usuario']}")

    print()
    escolha = input("  Escolha o número (ou digite o nome): ").strip()

    # Tentar como número
    try:
        idx = int(escolha) - 1
        if 0 <= idx < len(dados['licencas']):
            usuario = dados['licencas'][idx]['usuario']
        else:
            print("\n  [X] Número inválido")
            input("\n  Pressione ENTER para voltar...")
            return
    except:
        usuario = escolha

    print()
    confirmacao = input(f"  [!]  CONFIRMA remoção de '{usuario}'? (s/n): ").strip().lower()

    if confirmacao != 's':
        print("\n  [i]  Cancelado")
        input("\n  Pressione ENTER para voltar...")
        return

    # Remover
    print()
    print("  [Del]  Removendo...")

    dados_resp, erro = fazer_requisicao("DELETE", f"/admin/remover/{usuario}")

    print()
    if erro:
        print(f"  [X] Erro: {erro}")
    else:
        print(f"  [OK] Cliente '{usuario}' REMOVIDO!")

    print()
    input("  Pressione ENTER para voltar...")

def configurar_servidor():
    limpar_tela()
    print()
    print(linha())
    print("          [Cfg]  CONFIGURAÇÕES DO SERVIDOR")
    print(linha())
    print()
    print(f"  [Net] URL do Servidor: {SERVIDOR_URL}")
    print(f"  [Key] Admin Key: {ADMIN_KEY[:20]}...")
    print()
    print("  Para alterar, edite o arquivo painel_admin.py")
    print()
    print("  IMPORTANTE:")
    print("  - ADMIN_KEY deve ser a MESMA em server/api.py")
    print("  - Em produção, use HTTPS (https://...)")
    print()
    print(linha())
    input("\n  Pressione ENTER para voltar...")

def main():
    while True:
        menu_principal()

        opcao = input("  >> Escolha: ").strip()

        if opcao == "1":
            listar_clientes()
        elif opcao == "2":
            adicionar_cliente()
        elif opcao == "3":
            renovar_cliente()
        elif opcao == "4":
            bloquear_cliente()
        elif opcao == "5":
            desbloquear_cliente()
        elif opcao == "6":
            remover_cliente()
        elif opcao == "7":
            configurar_servidor()
        elif opcao == "0":
            print()
            print("  [Bye] Saindo...")
            print()
            break
        else:
            print()
            print("  [X] Opção inválida")
            input("\n  Pressione ENTER para continuar...")

if __name__ == "__main__":
    main()
