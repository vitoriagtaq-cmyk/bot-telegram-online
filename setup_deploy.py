#!/usr/bin/env python3
"""
Script de configuração para deploy do Bot Telegram
Este script ajuda a configurar as variáveis de ambiente e preparar o projeto para deploy.
"""

import os
import sys

def criar_env_file():
    """Cria o arquivo .env com as configurações do usuário."""
    print("🔧 Configuração do Bot Telegram")
    print("=" * 50)
    
    # Verificar se já existe um arquivo .env
    if os.path.exists('.env'):
        resposta = input("Arquivo .env já existe. Deseja sobrescrever? (s/N): ")
        if resposta.lower() != 's':
            print("Configuração cancelada.")
            return
    
    # Coletar informações do usuário
    print("\n📱 Configurações do Telegram API:")
    print("Obtenha suas credenciais em: https://my.telegram.org/apps")
    
    api_id = input("Digite seu API_ID: ").strip()
    api_hash = input("Digite seu API_HASH: ").strip()
    
    if not api_id or not api_hash:
        print("❌ API_ID e API_HASH são obrigatórios!")
        return
    
    # Criar arquivo .env
    env_content = f"""# Configurações do Telegram API
API_ID={api_id}
API_HASH={api_hash}

# Porta da aplicação (Railway define automaticamente)
PORT=5000
"""
    
    with open('.env', 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print("\n✅ Arquivo .env criado com sucesso!")
    print("🔒 Suas credenciais estão seguras e não serão enviadas para o GitHub.")

def verificar_arquivos():
    """Verifica se todos os arquivos necessários estão presentes."""
    arquivos_necessarios = [
        'app.py',
        'requirements.txt',
        'Procfile',
        'runtime.txt',
        'templates/index.html',
        '.gitignore'
    ]
    
    print("\n🔍 Verificando arquivos necessários...")
    
    todos_presentes = True
    for arquivo in arquivos_necessarios:
        if os.path.exists(arquivo):
            print(f"✅ {arquivo}")
        else:
            print(f"❌ {arquivo} - FALTANDO!")
            todos_presentes = False
    
    return todos_presentes

def mostrar_instrucoes_deploy():
    """Mostra as instruções para fazer o deploy."""
    print("\n🚀 Instruções para Deploy no Railway:")
    print("=" * 50)
    print("1. Crie um repositório no GitHub")
    print("2. Faça upload de todos os arquivos (exceto .env)")
    print("3. Acesse https://railway.app")
    print("4. Faça login com GitHub")
    print("5. Clique em 'New Project' > 'Deploy from GitHub repo'")
    print("6. Selecione seu repositório")
    print("7. Nas configurações do Railway, adicione as variáveis:")
    print(f"   - API_ID: {os.getenv('API_ID', 'SEU_API_ID')}")
    print(f"   - API_HASH: {os.getenv('API_HASH', 'SEU_API_HASH')}")
    print("8. Railway fará o deploy automaticamente!")
    print("\n💡 Dica: O Railway oferece 500 horas gratuitas por mês.")

def main():
    """Função principal do script de configuração."""
    print("🤖 Setup do Bot Telegram para Deploy")
    print("=" * 50)
    
    # Verificar arquivos
    if not verificar_arquivos():
        print("\n❌ Alguns arquivos estão faltando. Verifique a instalação.")
        return
    
    # Criar arquivo .env
    criar_env_file()
    
    # Mostrar instruções
    mostrar_instrucoes_deploy()
    
    print("\n🎉 Configuração concluída!")
    print("Agora você pode fazer o deploy do seu bot no Railway.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Configuração cancelada pelo usuário.")
    except Exception as e:
        print(f"\n❌ Erro durante a configuração: {e}")
        sys.exit(1)