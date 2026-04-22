# Antonio Discord Bot

Bot simples de teste para Discord.

## Arquivos
- `index.js`: responde mensagens recebidas
- `.env`: variáveis sensíveis locais, não versionadas

## Configuração
Crie um arquivo `.env` com:

```env
DISCORD_BOT_TOKEN=seu_token_aqui
OPENAI_API_KEY=sua_chave_openai_aqui
```

Observações:
- não versione o `.env`
- a chave OpenAI deve ficar apenas no formato `sk-...`, sem prefixos extras no valor

## Instalação
```bash
npm install
node index.js
```
