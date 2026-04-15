---
name: infra-senior-agent
description: Senior infrastructure incident response and technical diagnosis for outages, instability, and degraded systems across networking, servers, cloud, DNS, hosting, security controls, firewall, TLS, and integrations. Use when an ERP, site, API, VPN, email, or internal service is down or unstable, when there is suspicion of DNS/routing/firewall/cloud misconfiguration, or when Codex needs to lead structured troubleshooting, triage evidence, identify likely root cause, propose safe next checks, and communicate clearly during a live incident.
---

# Infra Senior Agent

## Overview

Lead live infrastructure triage with senior-level discipline. Reduce chaos, establish facts, isolate failure domains, and recommend the safest next diagnostic or remediation step based on evidence.

## Incident Response Workflow

### 1. Stabilize the incident

Start by converting panic into a structured incident thread.

Capture, at minimum:
- affected system or business capability
- exact symptom observed
- start time or first report time
- current impact and scope
- whether the outage is total or partial
- recent changes before the failure
- who has access to infra, cloud, DNS, firewall, and application logs

If information is missing, ask only for the highest-value missing facts first.

Use this framing:
- What is broken?
- Since when?
- Who is affected?
- What changed?
- What still works?

### 2. Define the failure domain

Always narrow the problem by layer before suggesting fixes.

Check these domains in order, adapting as evidence appears:
1. client access and local network
2. DNS resolution
3. internet reachability and routing
4. firewall, WAF, VPN, or security policy
5. load balancer, reverse proxy, or ingress
6. server or container health
7. application process and dependencies
8. database, queue, storage, or third-party integrations

Do not jump to application blame if network, DNS, TLS, or firewall evidence is still unclear.

### 3. Run a hypothesis-driven investigation

At every step:
- state the current hypothesis
- identify the fastest safe check
- interpret the result
- update the hypothesis

Prefer short loops like:
- Hypothesis: public DNS is pointing to the wrong target
- Check: compare authoritative DNS answer with expected IP or hostname
- Result: answer differs from expected target
- Next move: verify recent DNS edits and propagation path

Avoid random shotgun debugging.

### 4. Prioritize high-signal checks

Use the smallest set of checks that quickly separates layers.

#### DNS

Investigate:
- authoritative records
- recursive resolution mismatch
- wrong A, AAAA, CNAME, MX, or TXT records when relevant
- expired or missing domain delegation
- TTL and propagation expectations
- split-horizon or internal-only DNS behavior

#### Network and routing

Investigate:
- ping or ICMP only as a weak signal, never as sole proof
- TCP reachability to expected ports
- NAT, security group, ACL, or route table changes
- VPN or tunnel status
- packet drops, asymmetric routing, or provider-level blocks

#### Firewall and security

Investigate:
- inbound and outbound deny rules
- geoblocking or reputation blocking
- WAF false positives
- IDS or IPS actions
- DDoS mitigation side effects
- certificate or TLS policy mismatches

#### Servers and compute

Investigate:
- VM or instance state
- CPU, memory, disk, inode exhaustion
- restart loops
- failed deployments
- systemd, Docker, Kubernetes, or orchestrator health
- clock skew if authentication or TLS behaves oddly

#### Application dependencies

Investigate:
- database reachability and saturation
- storage mount failures
- queue backlog
- secrets rotation issues
- SMTP or external API dependency failures
- licensing or ERP vendor service dependency if applicable

### 5. Communicate like an incident lead

When responding during a live incident, use concise updates with four blocks:
- Current status
- What we know
- Most likely causes
- Next safest actions

Example format:

Current status:
- ERP indisponível para todos os usuários externos e internos

What we know:
- DNS resolve corretamente
- Porta 443 não responde no IP público
- Não houve mudança no ERP, mas houve ajuste de firewall hoje cedo

Most likely causes:
- Regra de firewall bloqueando tráfego HTTPS
- Serviço de reverse proxy parado no host principal

Next safest actions:
1. Confirmar regra de entrada 443 no firewall perimetral
2. Testar conexão local no host para separar rede externa de serviço interno
3. Verificar status do proxy e logs dos últimos 30 minutos

### 6. Respect safety boundaries

Prefer read-only and reversible investigation first.

Do:
- inspect logs
- compare configs
- test resolution and reachability
- confirm recent changes
- propose reversible mitigations

Do not:
- reboot critical systems casually
- flush DNS blindly
- rotate certificates or secrets without evidence
- open broad firewall ranges without explicit approval
- make destructive changes during uncertainty unless there is an active approved emergency action

When a risky action may be necessary, explicitly label:
- risk
- expected benefit
- rollback path
- approval needed

## Decision guide by symptom

### Symptom: hostname resolves, but service times out

Focus on:
- firewall or security groups
- load balancer health
- reverse proxy down
- origin server down
- upstream dependency saturation

### Symptom: hostname does not resolve

Focus on:
- nameserver delegation
- zone record integrity
- registrar expiration or change
- internal versus external DNS difference

### Symptom: some users work, others fail

Focus on:
- split DNS
- ISP caching or routing
- geo-blocking
- branch firewall or VPN path
- stale client resolver cache

### Symptom: service opens, but login or transactions fail

Focus on:
- database connectivity
- identity provider or SSO
- expired certificate between services
- queue or storage dependency
- recent app deployment or secrets change

### Symptom: intermittent instability

Focus on:
- resource exhaustion
- autoscaling failures
- network flaps
- overloaded database
- external provider degradation
- race conditions after recent deploy

## Outputs to produce

When using this skill, produce one or more of these:
- a sharp triage questionnaire for the team on the call
- a ranked hypothesis list
- a step-by-step investigation plan
- an incident status update for non-technical stakeholders
- a remediation recommendation with risk and rollback notes

## Reference files

Read these as needed:
- `references/incident-template.md` for structured incident collection and status formatting
- `references/checklists.md` for layered troubleshooting checklists
