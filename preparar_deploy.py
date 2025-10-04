#!/usr/bin/env python3
"""
Script para preparar arquivos para deploy
Este script verifica e prepara todos os arquivos necessários para o deploy.
"""

import os
import shutil
import zipfile
from datetime import datetime

def verificar_arquivos_necessarios():
    """Verifica se todos os arquivos necessários estão presentes."""
    arquivos_obrigatorios = [
        'app.py',
        'requirements.txt', 
        'Procfile',
        'runtime.txt',
        'templates/index.html',
        '.gitignore',
        'README.md'
    ]
    
    print("🔍 Verificando arquivos necessários...")
    print("=" * 50)
    
    todos_presentes = True
    for arquivo in arquivos_obrigatorios:
        if os.path.exists(arquivo):
            tamanho = os.path.getsize(arquivo)
            print(f"✅ {arquivo} ({tamanho} bytes)")
        else:
            print(f"❌ {arquivo} - FALTANDO!")
            todos_presentes = False
    
    return todos_presentes

def criar_pasta_deploy():
    """Cria uma pasta com todos os arquivos prontos para deploy."""
    pasta_deploy = "deploy_railway"
    
    # Remover pasta antiga se existir
    if os.path.exists(pasta_deploy):
        shutil.rmtree(pasta_deploy)
    
    # Criar nova pasta
    os.makedirs(pasta_deploy)
    os.makedirs(f"{pasta_deploy}/templates")
    
    # Arquivos para copiar
    arquivos_para_copiar = [
        ('app.py', 'app.py'),
        ('requirements.txt', 'requirements.txt'),
        ('Procfile', 'Procfile'),
        ('runtime.txt', 'runtime.txt'),
        ('.gitignore', '.gitignore'),
        ('README.md', 'README.md'),
        ('templates/index.html', 'templates/index.html'),
        ('login_telegram.py', 'login_telegram.py'),
        ('GUIA_DEPLOY.md', 'GUIA_DEPLOY.md')
    ]
    
    print(f"\n📁 Criando pasta de deploy: {pasta_deploy}")
    print("=" * 50)
    
    for origem, destino in arquivos_para_copiar:
        if os.path.exists(origem):
            destino_completo = os.path.join(pasta_deploy, destino)
            shutil.copy2(origem, destino_completo)
            print(f"✅ Copiado: {origem} → {destino}")
        else:
            print(f"⚠️  Arquivo não encontrado: {origem}")
    
    return pasta_deploy

def criar_zip_deploy(pasta_deploy):
    """Cria um arquivo ZIP com todos os arquivos para deploy."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_zip = f"bot_telegram_deploy_{timestamp}.zip"
    
    print(f"\n📦 Criando arquivo ZIP: {nome_zip}")
    print("=" * 50)
    
    with zipfile.ZipFile(nome_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(pasta_deploy):
            for file in files:
                arquivo_completo = os.path.join(root, file)
                arquivo_no_zip = os.path.relpath(arquivo_completo, pasta_deploy)
                zipf.write(arquivo_completo, arquivo_no_zip)
                print(f"✅ Adicionado ao ZIP: {arquivo_no_zip}")
    
    return nome_zip

def mostrar_instrucoes_github():
    """Mostra instruções para upload no GitHub."""
    print("\n🐙 PRÓXIMOS PASSOS - GitHub:")
    print("=" * 50)
    print("1. Acesse: https://github.com")
    print("2. Clique em 'New' para criar repositório")
    print("3. Nome: 'bot-telegram-online'")
    print("4. Deixe público e marque 'Add README'")
    print("5. Clique 'Create repository'")
    print("6. Clique 'uploading an existing file'")
    print("7. Arraste os arquivos da pasta 'deploy_railway'")
    print("8. Escreva: 'Upload inicial do bot'")
    print("9. Clique 'Commit changes'")

def mostrar_instrucoes_railway():
    """Mostra instruções para deploy no Railway."""
    print("\n🚂 DEPOIS - Railway Deploy:")
    print("=" * 50)
    print("1. Acesse: https://railway.app")
    print("2. Login with GitHub")
    print("3. New Project → Deploy from GitHub repo")
    print("4. Escolha 'bot-telegram-online'")
    print("5. Aguarde o deploy")
    print("6. Vá em 'Variables' e adicione:")
    print("   - API_ID: 28183526")
    print("   - API_HASH: 07e32e3de152f98a9b96365ecdde76cc")
    print("   - PORT: 5000")
    print("7. Clique 'Deploy' novamente")
    print("8. Copie a URL gerada")
    print("9. 🎉 SEU BOT ESTARÁ ONLINE!")

def main():
    """Função principal."""
    print("🚀 PREPARAÇÃO PARA DEPLOY ONLINE")
    print("=" * 50)
    print("Este script prepara todos os arquivos para colocar seu bot online!")
    print()
    
    # Verificar arquivos
    if not verificar_arquivos_necessarios():
        print("\n❌ Alguns arquivos estão faltando!")
        print("Execute o script de configuração primeiro.")
        return
    
    # Criar pasta de deploy
    pasta_deploy = criar_pasta_deploy()
    
    # Criar ZIP (opcional)
    resposta = input("\n📦 Deseja criar um arquivo ZIP? (s/N): ")
    if resposta.lower() == 's':
        nome_zip = criar_zip_deploy(pasta_deploy)
        print(f"\n✅ ZIP criado: {nome_zip}")
    
    # Mostrar instruções
    mostrar_instrucoes_github()
    mostrar_instrucoes_railway()
    
    print(f"\n🎯 RESUMO:")
    print("=" * 50)
    print(f"✅ Pasta criada: {pasta_deploy}")
    print("✅ Arquivos verificados e copiados")
    print("✅ Pronto para upload no GitHub")
    print("✅ Siga as instruções acima")
    print("\n💡 DICA: Leia o arquivo GUIA_DEPLOY.md para instruções detalhadas!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Preparação cancelada pelo usuário.")
    except Exception as e:
        print(f"\n❌ Erro durante a preparação: {e}")
        import traceback
        traceback.print_exc()