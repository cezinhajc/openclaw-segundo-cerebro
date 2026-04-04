# Auditoria e Plano de Refatoração — Wizard OpenClaw → Base Idens para Clientes

## Objetivo

Transformar este repositório em uma base da Idens que possa ser usada com clientes, preservando o método e removendo o acoplamento excessivo à operação original de demonstração.

## Intenção da refatoração

Esta refatoração não serve apenas para trocar nomes. Ela serve para separar:
- o que é método reutilizável
- o que é material pedagógico da imersão
- o que é demo específica da operação original
- o que pode virar base de cliente

## Critérios de classificação

Cada item auditado entra em uma destas categorias:

### A. Substituir
Trocar explicitamente nomes e referências sem mudar a função do conteúdo.

### B. Generalizar
Reescrever trechos que hoje dependem da operação original para uma forma neutra ou replicável.

### C. Remover ou isolar
Conteúdos muito específicos, com branding, fotos, demos ou relatórios históricos, que não deveriam ir para a base principal do cliente.

### D. Manter
Pode permanecer porque é estrutural, metodológico ou já suficientemente neutro.

---

# 1. Principais referências encontradas

## Pessoas
- Bruno
- Bruno Okamoto
- Cayo
- Cayo Syllos

## Marcas e organizações
- Pixel Educação
- Pixel Educacao
- pixel-educacao
- Pixel Ventures

## Repositório original
- `github.com/pixel-educacao/imersao-openclaw-negocios`
- referências Git locais apontando para esse remoto

---

# 2. Mapa de refatoração por tipo de arquivo

## 2.1. Arquivos de guia, onboarding e facilitação

### Arquivos principais
- `README.md`
- `onboarding/README.md`
- `onboarding/SETUP.md`
- `wizard-imersao/README.md`
- `wizard-imersao/FACILITADOR-WIZARD.md`
- `wizard-imersao/RUN-OF-SHOW.md`
- `wizard-imersao/SETUP-PRE-EVENTO.md`
- `wizard-imersao/dia1/*.md`
- `wizard-imersao/dia2/*.md`

### Diagnóstico
Esses arquivos carregam o método, mas também carregam papéis, nomes e referências da operação original.

### Classificação
**A + B**

### Ação proposta
- trocar Bruno → Hugo
- trocar Cayo → Flávia
- trocar Pixel Educação → Idens
- trocar `pixel-educacao/...` por repositório da Idens ou placeholder genérico
- reescrever instruções que dependem de papéis fixos da imersão
- manter a estrutura pedagógica e a ordem dos blocos

### Observação
Esses arquivos são centrais para reaproveitar o método. Devem ser preservados, mas limpos.

---

## 2.2. Cérebro da empresa demo

### Arquivos relevantes
- `cerebro/empresa/contexto/people.md`
- `cerebro/empresa/contexto/lessons.md`
- `cerebro/areas/marketing/contexto/people.md`
- `cerebro/areas/marketing/contexto/decisions.md`
- `cerebro/areas/governanca/contexto/people.md`
- `cerebro/areas/governanca/contexto/decisions.md`
- `cerebro/areas/pessoas/rotinas/onboarding-check.md`
- `cerebro/areas/atendimento/rotinas/*.md`
- `cerebro/agentes/bot-suporte/*.md`
- `cerebro/agentes/assistente/HEARTBEAT.md`
- `cerebro/agentes/marketing/TOOLS.md`
- `cerebro/seguranca/permissoes.md`

### Diagnóstico
Boa parte desses arquivos mistura estrutura útil com contexto operacional da empresa demo.

### Classificação
**B**

### Ação proposta
- transformar nomes e responsáveis fixos em placeholders ou papéis genéricos
- substituir referências de pessoa real por função: `CEO`, `responsável da área`, `gestor do suporte`, etc.
- manter exemplos apenas quando forem úteis como template
- remover dados históricos que não agregam para clientes

### Observação
Esses arquivos não devem sumir. Devem virar template neutro de empresa.

---

## 2.3. Skills muito acopladas à operação original

### Arquivos relevantes
- `cerebro/empresa/skills/twitter-banner-creator/SKILL.md`
- `cerebro/empresa/skills/twitter-banner-creator/schema.json`
- `cerebro/empresa/skills/twitter-banner-creator/scripts/generate_banners.py`
- `cerebro/empresa/skills/stack-ad-creator-pixel/SKILL.md`
- `cerebro/empresa/skills/stack-ad-creator-pixel/scripts/generate.py`
- `cerebro/empresa/skills/stack-ad-creator-pixel/references/brand.md`
- `cerebro/empresa/skills/stack-ad-creator-pixel/assets/config-example.json`
- `cerebro/empresa/skills/criar-skill/README.md`
- `cerebro/empresa/skills/criar-skill/wizard.html`
- `cerebro/empresa/skills/criar-skill/examples.html`
- `cerebro/empresa/skills/_index.md`

### Diagnóstico
Aqui existem dois tipos de problema:
1. nome/brand/autor acoplados à operação original
2. assets visuais e scripts desenhados para um branding específico

### Classificação
**B + C**

### Ação proposta
- renomear skills quando fizer sentido
  - ex: `stack-ad-creator-pixel` → `stack-ad-creator`
- mover branding específico para uma camada opcional de demo
- substituir dados de autor fixo por configuração ou placeholders
- revisar se essas skills devem estar na base principal de cliente ou em uma biblioteca opcional

### Observação
Essas skills podem ser muito úteis, mas não devem carregar marca e rosto da operação original.

---

## 2.4. Slides, HTMLs e demos prontos

### Arquivos relevantes
- `wizard-imersao/slides/*.html`
- `wizard-imersao/dados-demo/*.html`
- `cerebro/empresa/gestao/reports/*.html`
- HTMLs com avatar, nome, branding e copy da operação original

### Diagnóstico
Essa é a camada mais contaminada por branding e histórico específicos.

### Classificação
**C**

### Ação proposta
Escolher uma destas abordagens:

#### Opção 1 — isolar em pasta de demo
- mover tudo para algo como `demo-assets/` ou `legado-imersao/`
- manter fora da base principal de cliente

#### Opção 2 — refatorar só o essencial
- manter apenas os HTMLs que realmente servem como template
- remover ou neutralizar os demais

### Recomendação
**Isolar**. É a opção mais segura.

---

## 2.5. Repositório e metadados Git

### Arquivos e pontos relevantes
- `.git/config`
- `.git/logs/*`
- referências no `README.md`

### Diagnóstico
O remoto original está apontando para `pixel-educacao/imersao-openclaw-negocios`.

### Classificação
**A**

### Ação proposta
- criar novo repositório da Idens
- redefinir o remote
- não transportar logs Git para a base final

---

# 3. Substituições diretas recomendadas

## Trocas nominais
- `Bruno` → `Hugo`
- `Bruno Okamoto` → `Hugo Dória`
- `Cayo` → `Flávia`
- `Cayo Syllos` → `Flávia Monteiro`
- `Pixel Educação` → `Idens`
- `Pixel Educacao` → `Idens`

## Trocas estruturais
- `pixel-educacao/imersao-openclaw-negocios` → repositório da Idens ou placeholder genérico
- `Pixel Ventures` → `Idens` ou nome neutro, dependendo do uso

## Observação importante
Nem todo caso deve ser resolvido com busca e substituição cega. Em vários pontos, o mais certo é generalizar a função, não trocar pelo nome da Idens.

Exemplo:
- `Chega no Telegram do Bruno` não deveria virar automaticamente `Chega no Telegram do Hugo`
- o certo pode ser `Chega no canal do responsável` ou `Chega no canal da diretoria`

---

# 4. Proposta de estrutura final do fork-base

## Nome sugerido do repositório
- `idens-openclaw-client-base`
- ou `idens-client-brain-base`

## Estrutura sugerida

### 1. Base principal
- `cerebro/`
- `onboarding/`
- `wizard/` ou `imersao/` neutralizado

### 2. Biblioteca opcional de demos
- `demo-assets/`
- `legado-imersao/`

### 3. Documentação de uso com cliente
- `FORK-PARA-CLIENTE.md`
- `CHECKLIST-CLIENTE.md`
- `RESET-CLIENTE.md`

---

# 5. Plano de execução recomendado

## Etapa 1 — Higienização textual
Objetivo: remover ou adaptar nomes próprios e marcas da operação original.

### Fazer
- substituir referências diretas em markdown
- revisar README, onboarding e wizard-imersao
- neutralizar papéis muito presos à imersão original

## Etapa 2 — Neutralização do cérebro demo
Objetivo: transformar a empresa demo em template base.

### Fazer
- revisar contextos, people, decisions, rotinas e agentes
- converter responsáveis fixos em papéis ou placeholders
- manter só o que é útil como template

## Etapa 3 — Separação de assets de demo
Objetivo: evitar que a base principal do cliente carregue branding e demos antigas.

### Fazer
- mover slides e HTMLs específicos para pasta separada
- avaliar skills com branding original
- isolar fotos, relatórios e exemplos históricos
- tratar renomes estruturais com cuidado quando o nome da pasta estiver acoplado à marca original
  - exemplo: `stack-ad-creator-pixel/` → idealmente `stack-ad-creator/`
  - fazer isso apenas com atualização de todas as referências internas e índices

## Etapa 4 — Preparação para cliente
Objetivo: deixar a base pronta para fork e onboarding.

### Fazer
- criar `FORK-PARA-CLIENTE.md`
- criar checklist de reset
- criar checklist de primeiros arquivos obrigatórios
- documentar primeiro agente, primeira área, primeira skill e primeira rotina

## Etapa 5 — Novo remoto da Idens
Objetivo: consolidar a base como produto interno da Idens.

### Fazer
- criar novo repositório
- conectar remote da Idens
- versionar a base limpa

---

# 6. Prioridade sugerida

## Prioridade alta
- `README.md`
- `onboarding/SETUP.md`
- `wizard-imersao/*`
- `cerebro/empresa/contexto/*`
- `cerebro/agentes/*` ligados ao fluxo principal

## Prioridade média
- `cerebro/areas/*`
- `cerebro/seguranca/*`
- skills reutilizáveis com pouca marca acoplada

## Prioridade baixa ou isolamento
- HTMLs de demo
- slides
- relatórios históricos
- assets com fotos e branding específicos

---

# 7. Recomendação final

O melhor caminho não é editar esse repositório no improviso. O melhor caminho é tratá-lo como uma refatoração em produto.

## Produto final desejado
Uma base da Idens que permita este fluxo:
1. clonar ou forkar para um novo cliente
2. rodar reset controlado
3. preencher contexto real do cliente
4. ativar primeira área
5. ativar primeiro agente
6. ativar primeira skill
7. ativar primeira rotina

Se a base fizer isso bem, vocês não terão só um repositório. Terão um método operacional replicável da Idens.
