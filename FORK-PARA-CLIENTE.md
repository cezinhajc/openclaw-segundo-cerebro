# Fork para Cliente — Base Idens

## Objetivo

Usar esta base para criar rapidamente o cérebro operacional de um cliente no OpenClaw, sem recomeçar do zero.

## Fluxo recomendado

1. Fazer fork ou clonar esta base para um novo repositório do cliente
2. Renomear o repositório conforme o cliente
3. Rodar o reset controlado do cérebro
4. Preencher contexto real da empresa
5. Configurar a primeira área
6. Criar o primeiro agente
7. Criar a primeira skill
8. Criar a primeira rotina
9. Validar contexto, skill e memória
10. Publicar e operar

## Nome sugerido do repositório

Usar um padrão previsível, por exemplo:
- `cliente-openclaw-brain`
- `cliente-second-brain`
- `cliente-openclaw-base`

## O que manter

- Estrutura de pastas
- Templates de skills
- Templates de agentes
- Onboarding
- Wizard de facilitação
- Regras de segurança

## O que adaptar primeiro

- `cerebro/empresa/contexto/geral.md`
- `cerebro/empresa/contexto/people.md`
- `cerebro/empresa/contexto/metricas.md`
- `cerebro/areas/[area]/contexto/geral.md`
- primeiro agente em `cerebro/agentes/`

## O que não fazer

- não sair criando vários agentes antes da base existir
- não plugar integrações antes do contexto estar bom
- não tentar automatizar tudo no primeiro dia
- não deixar dados demo misturados com dados reais

## Ordem ideal de implantação

### Semana 1
- contexto da empresa
- primeira área
- primeiro agente

### Semana 2
- primeiras skills
- primeira rotina
- primeiros outputs reais

### Semana 3+
- expandir área a área
- adicionar agentes especializados
- conectar integrações externas

## Comando de partida

```text
Leia onboarding/SETUP.md e configure o cérebro da minha empresa
```

## Regra de ouro

Não vender só o agente. Implantar o cérebro.
