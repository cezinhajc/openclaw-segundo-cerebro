# Layered Troubleshooting Checklists

## DNS
- Confirmar domínio e subdomínio afetados
- Consultar resposta autoritativa
- Comparar com resolvedor público
- Verificar A, AAAA, CNAME, MX conforme o serviço
- Verificar nameservers delegados
- Verificar alteração recente no provedor DNS ou registrador
- Validar TTL e propagação

## Reachability
- Testar resolução a partir de múltiplos pontos
- Testar TCP nas portas críticas
- Comparar acesso interno versus externo
- Verificar NAT, rotas, VPN, ACL e security groups
- Confirmar estado de load balancer, ingress, reverse proxy

## Host and OS
- Confirmar host ou instância ligada
- Validar CPU, RAM, disco, inode
- Checar eventos recentes de reboot ou crash
- Validar serviços principais no systemd, Docker ou Kubernetes
- Verificar sincronismo de horário

## Application and Dependencies
- Verificar processo principal do ERP
- Verificar logs de erro recentes
- Testar conexão com banco
- Confirmar filas, storage e integrações externas
- Checar segredos, certificados e credenciais rotacionadas

## Security Controls
- Revisar firewall local e perimetral
- Revisar WAF, IPS, IDS, CDN e bloqueios por reputação
- Confirmar portas e origens permitidas
- Verificar expiração e cadeia TLS
- Procurar bloqueios após mudança recente
