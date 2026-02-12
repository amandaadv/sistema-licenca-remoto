# -*- coding: utf-8 -*-
"""
CLIENTE DE VALIDAÇÃO REMOTA - ZAPJOE V2
Usa no seu programa Python para validar licenças
"""

import requests
import hashlib
import uuid
import platform
import sys

class LicencaClient:
    """Cliente para validar licenças remotamente"""

    def __init__(self, servidor_url="http://localhost:8000"):
        """
        Inicializa cliente

        Args:
            servidor_url: URL do servidor de licenças
                         Em produção use: https://seu-servidor.com
        """
        self.servidor_url = servidor_url.rstrip('/')
        self.hardware_id = self._gerar_hardware_id()

    def _gerar_hardware_id(self):
        """
        Gera ID único baseado no hardware
        Vincula licença ao computador específico
        """
        try:
            # Combinar informações únicas
            mac = uuid.getnode()
            sistema = platform.system()
            maquina = platform.machine()
            processador = platform.processor()

            # Gerar hash SHA-256
            dados = f"{mac}-{sistema}-{maquina}-{processador}"
            hardware_id = hashlib.sha256(dados.encode()).hexdigest()

            return hardware_id
        except:
            # Fallback
            return hashlib.sha256(str(uuid.getnode()).encode()).hexdigest()

    def validar(self, usuario, senha, versao_programa="2.0"):
        """
        Valida licença com servidor remoto

        Args:
            usuario: Nome de usuário
            senha: Senha
            versao_programa: Versão do programa

        Returns:
            tuple: (valido: bool, mensagem: str, dados: dict)
        """
        try:
            # Fazer requisição ao servidor
            response = requests.post(
                f"{self.servidor_url}/validar",
                json={
                    "usuario": usuario,
                    "senha": senha,
                    "hardware_id": self.hardware_id,
                    "versao_programa": versao_programa
                },
                timeout=10
            )

            if response.status_code == 200:
                dados = response.json()

                if dados.get('valido'):
                    return True, dados.get('mensagem', 'Licença válida'), dados
                else:
                    return False, dados.get('mensagem', 'Licença inválida'), dados
            else:
                return False, f"❌ Erro do servidor: {response.status_code}", {}

        except requests.exceptions.ConnectionError:
            return False, "❌ Não foi possível conectar ao servidor de licenças\n\n📞 Contate T.I Joe", {}
        except requests.exceptions.Timeout:
            return False, "⏱️ Timeout ao conectar ao servidor\n\n📞 Contate T.I Joe", {}
        except Exception as e:
            return False, f"❌ Erro: {str(e)}", {}

    def validar_offline(self):
        """
        Validação offline (modo de emergência)
        Retorna False sempre - força conexão online
        """
        return False, "🔒 Validação online obrigatória\n\n📞 Contate T.I Joe se não conseguir conectar", {}

    def tela_login(self, titulo="ZAPJOE V2 - AUTENTICAÇÃO"):
        """
        Exibe tela de login e valida

        Returns:
            bool: True se login válido, False caso contrário
        """
        print("\n" + "=" * 60)
        print(f"          {titulo}")
        print("=" * 60)
        print()

        # Máximo 3 tentativas
        for tentativa in range(3):
            usuario = input("👤 Usuário: ").strip()
            senha = input("🔒 Senha: ").strip()
            print()
            print("  🔄 Validando...")
            print()

            valido, mensagem, dados = self.validar(usuario, senha)

            if valido:
                print("✅ " + mensagem)
                print()
                print("🚀 Iniciando sistema...")
                print("=" * 60)
                print()
                return True
            else:
                print("❌ " + mensagem)
                print()

                if tentativa < 2:
                    print(f"Tentativa {tentativa + 1}/3")
                    print()

        print("❌ Máximo de tentativas atingido")
        print("🔒 Acesso negado")
        print()
        sys.exit(1)


def exemplo_uso():
    """Exemplo de como usar no seu programa"""

    # ATENÇÃO: Em produção, use a URL do seu servidor hospedado
    # Exemplo: https://zapjoe-licenses.railway.app
    cliente = LicencaClient(servidor_url="http://localhost:8000")

    # Opção 1: Tela de login automática
    if cliente.tela_login():
        print("Sistema iniciado com sucesso!")
        # Seu código aqui...

    # Opção 2: Validação manual
    # valido, mensagem, dados = cliente.validar("joeferson", "minhasenha")
    # if valido:
    #     print("Licença válida!")
    # else:
    #     print(f"Erro: {mensagem}")
    #     sys.exit(1)


if __name__ == "__main__":
    exemplo_uso()
