#!/usr/bin/env python3
"""
Script para fazer login no Telegram
Este script permite fazer login no Telegram sem interferência de logs.
"""

import asyncio
import os
from telethon import TelegramClient

# Configurações
API_ID = int(os.getenv('API_ID', '28183526'))
API_HASH = os.getenv('API_HASH', '07e32e3de152f98a9b96365ecdde76cc')
SESSION_NAME = "bot_refresh_session2"

async def fazer_login():
    """Faz login no Telegram de forma interativa."""
    print("🔐 Login no Telegram")
    print("=" * 40)
    print("Este script vai te ajudar a fazer login no Telegram.")
    print("Você precisará do seu número de telefone e código de verificação.")
    print()
    
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    
    try:
        print("📱 Conectando ao Telegram...")
        await client.start()
        
        # Verificar se já está logado
        me = await client.get_me()
        print(f"✅ Login realizado com sucesso!")
        print(f"👤 Usuário: {me.first_name} {me.last_name or ''}")
        print(f"📞 Telefone: {me.phone}")
        print()
        print("🎉 Agora você pode usar o painel web do bot!")
        
    except Exception as e:
        print(f"❌ Erro durante o login: {e}")
        print("Verifique suas credenciais API_ID e API_HASH.")
    
    finally:
        await client.disconnect()

def main():
    """Função principal."""
    print("🤖 Bot Telegram - Login")
    print("=" * 40)
    
    # Verificar se as credenciais estão configuradas
    if not API_ID or not API_HASH or API_HASH == "COLOQUE SEU API_HASH AQUI":
        print("❌ ERRO: Credenciais não configuradas!")
        print("Configure as variáveis de ambiente API_ID e API_HASH")
        print("ou edite o arquivo app.py com suas credenciais.")
        return
    
    try:
        asyncio.run(fazer_login())
    except KeyboardInterrupt:
        print("\n👋 Login cancelado pelo usuário.")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")

if __name__ == "__main__":
    main()