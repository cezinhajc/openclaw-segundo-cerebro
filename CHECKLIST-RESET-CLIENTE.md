# Checklist de Reset para Cliente

Use este checklist sempre que for preparar esta base para um novo cliente.

## Antes de começar
- [ ] Confirmar que o repositório do cliente é novo ou está limpo
- [ ] Confirmar que nenhum dado sensível do cliente anterior ficou na base
- [ ] Confirmar que os remotos Git estão apontando para o repositório correto

## Reset do cérebro
- [ ] Limpar `cerebro/empresa/contexto/`
- [ ] Limpar `cerebro/empresa/projetos/`
- [ ] Limpar contextos da primeira área a ser configurada
- [ ] Limpar aprendizados, decisões e people específicos do demo anterior
- [ ] Limpar relatórios e outputs gerados anteriormente

## Agentes
- [ ] Revisar `SOUL.md` do agente principal
- [ ] Revisar `AGENTS.md` do agente principal
- [ ] Revisar `HEARTBEAT.md` do agente principal
- [ ] Garantir que o primeiro agente está alinhado com o caso do cliente

## Skills
- [ ] Manter skills estruturais reutilizáveis
- [ ] Remover ou adaptar skills que não fazem sentido para o cliente
- [ ] Garantir que a primeira skill escolhida resolve uma tarefa repetitiva real

## Canais e runtime
- [ ] Definir canal inicial do agente
- [ ] Definir política de resposta e menção
- [ ] Definir escopo de acesso
- [ ] Validar configuração do runtime antes de produção

## Validação
- [ ] O agente responde com contexto real da empresa?
- [ ] A primeira skill executa corretamente?
- [ ] A memória do cliente está sendo persistida no lugar certo?
- [ ] O cérebro está versionado no GitHub?

## Finalização
- [ ] `git add .`
- [ ] `git commit`
- [ ] `git push`
- [ ] Registrar próximos passos do cliente
