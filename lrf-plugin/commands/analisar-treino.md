---
description: Analisa uma sessão de ciclismo do Strava com o cânone de 22 skills do LRF, gerando um arquivo de análise auditável e o feedback para o atleta.
allowed-tools: ["*"]
argument-hint: "[data ou activity_id, opcional — ex.: 2025-10-23 ou 16230267501]"
---

O usuário pediu a análise de um treino de ciclismo. Argumento recebido (pode estar vazio): $ARGUMENTS

Siga exatamente o processo descrito em `skills/analisar-treino/SKILL.md` deste plugin — carregue essa skill agora e execute o processo completo nela descrito, do zero ao feedback final, incluindo a auditoria de rastreabilidade obrigatória.

Se `$ARGUMENTS` estiver vazio, pergunte ao usuário qual sessão analisar (pode ser uma data, um activity_id do Strava, ou "a última atividade"). Se `$ARGUMENTS` já identificar a sessão, prossiga direto sem perguntar de novo.
