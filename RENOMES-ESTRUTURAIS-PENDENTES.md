# Renomes Estruturais Pendentes

## Objetivo

Listar renomes que ainda fazem sentido, mas exigem cuidado para não quebrar referências.

## Renomes recomendados

### 1. `cerebro/empresa/skills/stack-ad-creator-pixel/`
**Ideal:** `cerebro/empresa/skills/stack-ad-creator/`

Motivo:
- remove acoplamento da marca antiga no nome da pasta
- deixa a skill mais reaproveitável para clientes

Cuidados:
- atualizar `_index.md`
- atualizar referências em skills e documentação
- revisar scripts e assets associados

### 2. assets com nome de pessoa antiga
Exemplos:
- `bruno-photo.jpeg`
- outros arquivos equivalentes

Motivo:
- evitar acoplamento visual desnecessário

Ação sugerida:
- trocar por nomes neutros, como `autor-padrao.jpeg`

### 3. arquivos de demo muito específicos
Se algum arquivo ainda fizer sentido apenas como demo, considerar:
- mover para `demo-assets/`
- ou prefixar claramente como demo/legado

## Regra de execução

Só fazer renome estrutural quando houver atualização simultânea de todas as referências.
