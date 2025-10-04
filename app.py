import asyncio
import logging
import random
import os
import threading
from typing import List, Dict
from datetime import datetime

from flask import Flask, render_template, request, jsonify, redirect, url_for
from telethon import TelegramClient
from telethon.tl.types import Channel, Message
from telethon.errors.rpcerrorlist import UserNotParticipantError, ChatWriteForbiddenError

app = Flask(__name__)

# ======================================================================
# ======== CONFIGURAÇÕES ========
# ======================================================================

# Credenciais do Telegram (agora usando variáveis de ambiente)
API_ID = int(os.getenv('API_ID', '26183526'))
API_HASH = os.getenv('API_HASH', '07e32e3de152f98a9b96365ecdde76cc')

# Nome do arquivo de sessão
SESSION_NAME = "bot_refresh_session2"

# Lista de links dos grupos (pode ser configurada via interface web)
GRUPOS_LINKS = [
    "https://t.me/+JKlz_wTPVvowNzZh",
    "https://t.me/+YVUI_g48Lac0MTQx",
    "https://t.me/+2kauWUisZbkwODg5"
]

# Mensagem padrão
MENSAGEM_PADRAO = """
🔮🔥 𝗔𝗥𝗤𝗨𝗜𝗩𝗢𝗦 𝗦𝗘𝗖𝗥𝗘𝗧𝗢𝗦 +𝟭𝟴  
🔮🔥 𝑽𝑰‌𝑫𝑬𝑶𝑺 𝑽𝑨𝒁𝑨𝑫𝑶𝑺 +𝟭𝟴  
🔮🔥 𝑪𝑶𝑵𝑻𝑬𝑼‌𝑫𝑶 𝑷𝑹𝑶𝑰𝑩𝑰𝑫𝑶 +𝟭𝟴  
                                    👇  
[🗂 🔞 ➡️ 𝐃𝐄𝐒𝐁𝐋𝐎𝐐𝐔𝐄𝐈𝐄 𝐒𝐄𝐔 𝐀𝐂𝐄𝐒𝐒𝐎](https://t.me/Sejavipbrasilgrupobot)  
[🗂 🔞 ➡️ 𝐃𝐄𝐒𝐁𝐋𝐎𝐐𝐔𝐄𝐈𝐄 𝐒𝐄𝐔 𝐀𝐂𝐄𝐒𝐒𝐎](https://t.me/Sejavipbrasilgrupobot)  
"""

# Configurações de tempo
MIN_DELAY_MINUTOS = 5
MAX_DELAY_MINUTOS = 40

# ======================================================================
# ======== VARIÁVEIS GLOBAIS ========
# ======================================================================

bot_status = {
    'running': False,
    'last_update': None,
    'cycle_count': 0,
    'next_update': None,
    'logs': []
}

bot_task = None
client = None

# ======================================================================
# ======== CONFIGURAÇÃO DO LOGGING ========
# ======================================================================

class WebLogHandler(logging.Handler):
    def emit(self, record):
        log_entry = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'level': record.levelname,
            'message': record.getMessage()
        }
        bot_status['logs'].append(log_entry)
        # Manter apenas os últimos 100 logs
        if len(bot_status['logs']) > 100:
            bot_status['logs'] = bot_status['logs'][-100:]

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        WebLogHandler()
        # Removido StreamHandler para não interferir com a entrada do usuário
    ]
)

# ======================================================================
# ======== FUNÇÕES DO BOT ========
# ======================================================================

async def resolver_entidades(client: TelegramClient, grupos_links: List[str]) -> List[Channel]:
    """Converte links de convite em entidades do Telegram."""
    grupos_entidades = []
    logging.info("ℹ️ Resolvendo links dos grupos para otimizar o bot...")
    for link in grupos_links:
        try:
            entidade = await client.get_entity(link)
            grupos_entidades.append(entidade)
            logging.info(f"  [OK] Link resolvido para o grupo: {entidade.title}")
            await asyncio.sleep(1)
        except (ValueError, TypeError) as e:
            logging.error(f"  [ERRO DE LINK] O link '{link}' parece ser inválido. Detalhe: {e}")
        except Exception as e:
            logging.error(f"  [ERRO AO ACESSAR] Não foi possível resolver o grupo {link}. Detalhe: {e}")

    return grupos_entidades

async def bot_main_loop(mensagem_personalizada=None):
    """Função principal que orquestra a lógica do bot."""
    global client, bot_status
    
    mensagem = mensagem_personalizada or MENSAGEM_PADRAO
    
    try:
        client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
        await client.start()
        logging.info("✅ Cliente conectado com sucesso!")

        grupos_entidades = await resolver_entidades(client, GRUPOS_LINKS)
        if not grupos_entidades:
            logging.critical("❌ Nenhum grupo válido foi carregado.")
            bot_status['running'] = False
            return

        mensagens_enviadas = {}
        ciclo = 1

        while bot_status['running']:
            logging.info(f"\n--- INICIANDO CICLO DE ATUALIZAÇÃO #{ciclo} ---")
            bot_status['cycle_count'] = ciclo
            bot_status['last_update'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            novas_mensagens_enviadas = {}

            for grupo in grupos_entidades:
                if not bot_status['running']:
                    break
                    
                # Apagar mensagem anterior
                if grupo.id in mensagens_enviadas:
                    try:
                        msg_antiga = mensagens_enviadas[grupo.id]
                        await client.delete_messages(grupo.id, msg_antiga.id)
                        logging.info(f"  [APAGADO] Mensagem antiga removida de: {grupo.title}")
                    except Exception as e:
                        logging.warning(f"  [AVISO] Não foi possível apagar a mensagem antiga em '{grupo.title}'. Detalhe: {e}")
                
                # Enviar nova mensagem
                try:
                    msg_nova = await client.send_message(grupo, message=mensagem, parse_mode='markdown')
                    novas_mensagens_enviadas[grupo.id] = msg_nova
                    logging.info(f"  [ENVIADO] Nova mensagem postada em: {grupo.title}")
                except (UserNotParticipantError, ChatWriteForbiddenError) as e:
                    logging.error(f"  [ERRO DE PERMISSÃO] Sem permissão para enviar em '{grupo.title}'. Detalhe: {e}")
                except Exception as e:
                    logging.error(f"  [ERRO AO ENVIAR] Falha ao postar em '{grupo.title}'. Detalhe: {e}")

                await asyncio.sleep(3)

            mensagens_enviadas = novas_mensagens_enviadas
            
            if bot_status['running']:
                delay_em_minutos = random.randint(MIN_DELAY_MINUTOS, MAX_DELAY_MINUTOS)
                delay_em_segundos = delay_em_minutos * 60
                
                next_update_time = datetime.now()
                next_update_time = next_update_time.replace(
                    minute=(next_update_time.minute + delay_em_minutos) % 60,
                    hour=next_update_time.hour + (next_update_time.minute + delay_em_minutos) // 60
                )
                bot_status['next_update'] = next_update_time.strftime('%Y-%m-%d %H:%M:%S')
                
                logging.info(f"\n✅ Ciclo #{ciclo} concluído. Próxima atualização em {delay_em_minutos} minutos.")
                
                # Aguardar com verificação periódica do status
                for _ in range(delay_em_segundos):
                    if not bot_status['running']:
                        break
                    await asyncio.sleep(1)
                
                ciclo += 1

    except Exception as e:
        logging.error(f"❌ Erro no bot: {e}")
    finally:
        if client:
            await client.disconnect()
        bot_status['running'] = False
        bot_status['next_update'] = None
        logging.info("🔌 Bot desconectado.")

def run_bot_in_thread(mensagem_personalizada=None):
    """Executa o bot em uma thread separada."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(bot_main_loop(mensagem_personalizada))

# ======================================================================
# ======== ROTAS FLASK ========
# ======================================================================

@app.route('/')
def index():
    return render_template('index.html', status=bot_status)

@app.route('/start', methods=['POST'])
def start_bot():
    global bot_task
    
    if bot_status['running']:
        return jsonify({'error': 'Bot já está rodando'}), 400
    
    mensagem_personalizada = request.form.get('mensagem', '').strip()
    if not mensagem_personalizada:
        mensagem_personalizada = None
    
    bot_status['running'] = True
    bot_status['logs'] = []
    bot_task = threading.Thread(target=run_bot_in_thread, args=(mensagem_personalizada,))
    bot_task.start()
    
    return jsonify({'success': 'Bot iniciado com sucesso'})

@app.route('/stop', methods=['POST'])
def stop_bot():
    if not bot_status['running']:
        return jsonify({'error': 'Bot não está rodando'}), 400
    
    bot_status['running'] = False
    logging.info("🛑 Parando o bot...")
    
    return jsonify({'success': 'Bot parado com sucesso'})

@app.route('/status')
def get_status():
    return jsonify(bot_status)

@app.route('/logs')
def get_logs():
    return jsonify({'logs': bot_status['logs'][-50:]})  # Últimos 50 logs

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))

    app.run(host='0.0.0.0', port=port, debug=False)


