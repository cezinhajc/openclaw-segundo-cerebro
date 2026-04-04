# Base OpenClaw para Clientes — Idens

Base de implantação para transformar OpenClaw em um cérebro operacional de empresa.

Este repositório serve para três usos:
- configurar o cérebro de um cliente
- conduzir workshops, imersões e diagnósticos ao vivo
- servir como base replicável da Idens para novos projetos

---

## Estrutura do repositório

```text
wizard-openclaw/
├── onboarding/       ← guia para configurar o cérebro de uma empresa real
│   ├── README.md
│   └── SETUP.md
│
├── cerebro/          ← template do cérebro empresarial
│   ├── empresa/
│   ├── areas/
│   ├── agentes/
│   └── seguranca/
│
└── wizard-imersao/   ← material de facilitação, operação e demo
    ├── FACILITADOR-WIZARD.md
    ├── RUN-OF-SHOW.md
    ├── SETUP-PRE-EVENTO.md
    ├── slides/
    ├── dados-demo/
    ├── dia1/
    └── dia2/
```

---

## As 3 camadas

### `onboarding/`
Guia de setup para configurar o cérebro de uma empresa real a partir desta base.

Comando sugerido:
```text
Leia onboarding/SETUP.md e configure o cérebro da minha empresa
```

### `cerebro/`
Template do cérebro empresarial.

Aqui ficam:
- contexto da empresa
- áreas operacionais
- agentes
- skills
- rotinas
- regras de segurança

A intenção é que esta estrutura seja adaptada para cada cliente, não usada como verdade fixa.

### `wizard-imersao/`
Material de facilitação para workshops, imersões, treinamentos ou implantação assistida.

Comando sugerido:
```text
Leia wizard-imersao/FACILITADOR-WIZARD.md e me guie pela imersão
```

---

## Como usar esta base

### Para configurar um cliente
1. Clone ou faça fork deste repositório
2. Aponte o OpenClaw para ele
3. Peça ao agente: **"Leia onboarding/SETUP.md e configure o cérebro da minha empresa"**
4. O agente guia o setup, limpa os dados de demonstração e estrutura o cérebro real

### Para facilitar uma imersão
1. Clone ou faça fork deste repositório
2. Aponte o OpenClaw para ele
3. Peça ao agente: **"Leia wizard-imersao/FACILITADOR-WIZARD.md e me guie pela imersão"**
4. O agente conduz a facilitação com base no roteiro

---

## Princípio central

Braços mudam. Cérebro fica.

O objetivo desta base é fazer o contexto da empresa viver em arquivos versionados, e não preso a uma conversa, ferramenta ou pessoa.

---

*Base da Idens para implantação de OpenClaw em clientes*
