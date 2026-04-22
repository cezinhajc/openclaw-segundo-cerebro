# Rotina: Sync GitHub

## O que faz
Serve como rede de segurança para garantir que alterações úteis sejam sincronizadas com o repositório remoto.

## Frequência
1x por dia

## Objetivo
- evitar trabalho local esquecido
- reduzir risco de divergência entre estado local e remoto
- sinalizar conflitos ou falhas de autenticação

## Boas práticas
- não commitar arquivos sensíveis, temporários ou lixo de runtime
- só gerar commit quando houver mudança relevante
- reportar conflito, erro de autenticação ou bloqueio de push

---

_Atualizado: 2026-04-22_
