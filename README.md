# 🤖 Bot Telegram - Automação de Mensagens

Este projeto transforma seu script de automação do Telegram em uma aplicação web que pode ser hospedada gratuitamente online.

## 🚀 Deploy Gratuito no Railway

### Passo 1: Preparar o Código
1. Faça upload de todos os arquivos para um repositório no GitHub
2. Certifique-se de que todos os arquivos estão na raiz do repositório

### Passo 2: Deploy no Railway
1. Acesse [Railway.app](https://railway.app)
2. Faça login com sua conta GitHub
3. Clique em "New Project"
4. Selecione "Deploy from GitHub repo"
5. Escolha o repositório com seu bot
6. Railway detectará automaticamente que é uma aplicação Python

### Passo 3: Configurar Variáveis de Ambiente
No painel do Railway, vá em "Variables" e adicione:
- `API_ID`: Seu API ID do Telegram
- `API_HASH`: Seu API Hash do Telegram
- `PORT`: 5000 (Railway define automaticamente)

### Passo 4: Deploy
- Railway fará o deploy automaticamente
- Você receberá uma URL pública para acessar seu bot

## 🔧 Configuração Local (Opcional)

Para testar localmente:

```bash
pip install -r requirements.txt
python app.py
```

Acesse: http://localhost:5000

## 📱 Como Usar

1. Acesse a URL do seu bot hospedado
2. Use a interface web para:
   - Iniciar/parar o bot
   - Personalizar mensagens
   - Monitorar logs em tempo real
   - Acompanhar status e estatísticas

## 🔒 Segurança

- Suas credenciais ficam seguras nas variáveis de ambiente
- Não compartilhe sua URL publicamente se não quiser que outros controlem seu bot
- O Railway oferece HTTPS automaticamente

## 💰 Custos

- Railway oferece 500 horas gratuitas por mês
- Suficiente para manter o bot rodando 24/7
- Sem necessidade de cartão de crédito

## 🆘 Suporte

Se tiver problemas:
1. Verifique os logs no painel do Railway
2. Certifique-se de que as variáveis de ambiente estão corretas
3. Verifique se seu bot tem permissões nos grupos do Telegram

## 📋 Arquivos do Projeto

- `app.py`: Aplicação Flask principal
- `templates/index.html`: Interface web
- `requirements.txt`: Dependências Python
- `Procfile`: Configuração de execução
- `runtime.txt`: Versão do Python
- `.env.example`: Exemplo de variáveis de ambiente