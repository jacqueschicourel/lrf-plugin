---
id: skill-gerais-pmc
numero: skill-0001
titulo: "Performance Manager Chart (CTL/ATL/TSB) — cálculo e leitura de forma"
dominio: metricas-de-potencia
tipo_skill: calculadora+detector
notas_usadas:
  - {id: nota-0062, uso: "fórmula de TSS por sessão — entrada diária do EWMA"}
  - {id: nota-0083, uso: "fórmula de CTL — EWMA de TSS, constante 42 dias"}
  - {id: nota-0084, uso: "fórmula de ATL — EWMA de TSS, constante 7 dias"}
  - {id: nota-0085, uso: "TSB = CTL − ATL; leitura 'Forma = Fitness + Frescor'"}
  - {id: nota-0087, uso: "ajuste da constante do ATL pela duração do evento-alvo (10-14d curto/explosivo; 3-5d longo/aeróbio)"}
  - {id: nota-0090, uso: "limiar de ramp rate seguro do CTL (3-7 TSS/dia/semana, ajustado por idade de treino e CTL atual)"}
  - {id: nota-0092, uso: "detecção de overreaching não funcional — ATL>CTL prolongado sem TSB voltar à neutralidade"}
  - {id: nota-0094, uso: "regra: TSB não precisa ser positivo, precisa estar subindo"}
confianca_herdada: 0.75
# = mínimo das confianças acima (nota-0087 e nota-0094 empatam em 0.75; as demais são 0.8-0.95).
# Regra do projeto: uma skill nunca é mais confiável que sua citação mais fraca.
condicao_nao_calculavel: "histórico de TSS diário com menos de 42 dias de profundidade → CTL enviesado pelo efeito de 'warm-up' do EWMA (a série ainda não convergiu); reportar CTL/TSB como Estimado com essa ressalva explícita, nunca como Medido. Sem FTP válido no perfil do atleta, TSS não pode ser calculado (pré-requisito de tudo aqui) → toda a skill fica Ausente."
status: validado_com_ressalvas
# mecânica correta e coerente com o cânone contra dado real (exemplo-02); mas os valores absolutos
# ainda carregam duas aproximações registradas em log_de_teste — NP≈potência média (não o algoritmo
# exato da nota-0059) e histórico real de só 43 dias (viés de warm-up residual do EWMA). Não promover
# a "validado" puro até fechar essas duas pendências.
skills_relacionadas:
  - {id: skill-gerais-tss-sessao, tipo: pre-requisito}
  - {id: skill-classificacao-semana-recuperacao, tipo: consumida-por}
  - {id: skill-estrutural-fase-e-sequenciamento, tipo: consumida-por}
  - {id: skill-estrutural-taper, tipo: consumida-por}
  - {id: skill-gerais-fadiga-carga-avancada, tipo: consumida-por}
log_de_teste:
  - data: "2026-07-19"
    caso: "43 dias reais (2026-05-17 a 2026-06-28) do Jacques, de Base de treinamento/activities.csv (dado bruto do export Strava), até a Letape Serra Negra"
    resultado: "CTL/ATL/TSB calculados dia a dia (ver exemplos/exemplo-02-dado-real-serra-negra.md). TSB véspera da prova (06-27) = -8,45, com tendência de subida nos 5 dias anteriores (taper) — bate com o padrão da nota-0094. Ramp rate disparou alerta numa única semana (05-31→06-07, +13,24 TSS/dia/semana), autocorrigido pela semana de descanso seguinte — overreaching (nota-0092) corretamente não disparou."
    veredito: "Mecânica do EWMA e dos detectores confirmada com dado real. Duas ressalvas pendentes: (1) NP foi aproximado pela potência média da atividade — não o algoritmo exato de 30s/^4/média/raiz-4ª da nota-0059 — porque o sandbox desta sessão não teve acesso à pasta do projeto para decodificar os .fit.gz brutos nem ao MCP do Strava sem estourar limite de tokens; isso subestima a TSS em pedaladas de esforço variável (ex.: Serra Negra tem descidas longas quase sem pedalar). (2) 43 dias é o mínimo exigido pela condicao_nao_calculavel, mas ainda insuficiente para o EWMA convergir plenamente (precisa de vários múltiplos de 42 dias) — CTL0=ATL0=0 no início da série ainda produz viés de warm-up. Reabrir esta skill para 'validado' pleno quando (a) houver acesso a .fit.gz bruto decodificado ou export com potência por segundo, e (b) houver ≥90-120 dias de histórico real."
---

## O que faz

Calcula a série de CTL (fitness crônica), ATL (fadiga aguda) e TSB (forma = fitness − fadiga) do atleta a partir do histórico diário de TSS, e interpreta essa série contra 4 regras do cânone: taxa de subida segura do CTL (ramp rate), risco de overreaching não funcional, se o TSB precisa ser positivo ou só estar subindo, e se a constante de tempo padrão do ATL (7 dias) deveria ser ajustada para o evento-alvo do atleta.

Não inventa nem estima TSS — assume que a série diária de TSS já foi calculada por `skill-gerais-tss-sessao` (nota-0062) a partir de potência bruta. Esta skill só aplica o EWMA e as regras de leitura em cima dela.

## Quando usar

- Sempre que houver TSS diário de pelo menos os 42 dias anteriores à data de referência (feedback diário/semanal/mensal).
- Antes de qualquer skill de `por-tipo-de-treino/` ou `classificacao/` que dependa de saber se o atleta está fresco, fadigado ou em risco de overreaching — esta é uma skill de `gerais/`, roda antes e alimenta as demais.
- Ao avaliar prontidão para prova/teste (cruzar tendência do TSB, não só o valor absoluto — nota-0094).
- Ao decidir se uma semana de treino pesado está dentro de uma taxa de progressão segura (nota-0090).

## Passo a passo

1. **Reunir a série de TSS diário.** Pré-requisito de `skill-gerais-tss-sessao`. Dias sem atividade = TSS 0 (não pular dias — o EWMA precisa da série contínua para não distorcer a constante de tempo).
2. **Definir a constante de tempo do ATL.** Padrão = 7 dias (nota-0084). Se o atleta tiver um evento-alvo declarado: evento curto/explosivo (pista, subidas curtas) → 10-14 dias; evento longo/aeróbio (maratona MTB) → 3-5 dias (nota-0087). Sem evento-alvo declarado, manter o padrão de 7 e sinalizar a suposição.
3. **Calcular CTL do dia:** `CTL_hoje = CTL_ontem + (TSS_hoje − CTL_ontem) × (1 − e^(−1/42))` (nota-0083). Constante de suavização: `λ_CTL = 1 − e^(−1/42) ≈ 0,023546`.
4. **Calcular ATL do dia:** `ATL_hoje = ATL_ontem + (TSS_hoje − ATL_ontem) × (1 − e^(−1/τ))`, onde τ é a constante definida no passo 2 (nota-0084). Para τ=7: `λ_ATL ≈ 0,133122`.
5. **Calcular TSB do dia:** `TSB = CTL − ATL` (nota-0085).
6. **Aplicar os detectores de leitura:**
   - Ramp rate: taxa de variação do CTL nas últimas 1-4 semanas vs. tabela de referência por idade de treino/CTL atual (nota-0090). Sinalizar se > 7 TSS/dia/semana por mais de 4 semanas seguidas.
   - Overreaching: TSB fortemente negativo e não retornando à neutralidade por período prolongado (nota-0092).
   - Tendência de TSB: reportar a direção (subindo/caindo) dos últimos 3-7 dias, não só o valor do dia (nota-0094) — TSB negativo mas subindo pode ser tão favorável quanto positivo, dependendo do evento.
7. **Checar a condição de não-calculável** (ver frontmatter) antes de reportar qualquer número como Medido/Estimado.

## Output

```
{
  "data_referencia": "AAAA-MM-DD",
  "ctl": <float>,
  "atl": <float, constante_usada: 7|10-14|3-5>,
  "tsb": <float>,
  "tendencia_tsb_7d": "subindo" | "caindo" | "estavel",
  "ramp_rate_ctl_4sem": <float, TSS/dia/semana>,
  "alertas": [
    "ramp_rate_excessivo" | "overreaching_nao_funcional" | null
  ],
  "provenance": "Medido" | "Estimado" | "Ausente",
  "motivo_provenance": "<texto, obrigatório se Estimado ou Ausente>",
  "notas_citadas": ["nota-0083", "nota-0084", "nota-0085", ...]
}
```

O output nunca deve ser reportado ao atleta sem o campo `provenance` — é o que impede a skill de apresentar um CTL calculado sobre 10 dias de histórico (viés de warm-up) como se fosse tão confiável quanto um calculado sobre 90 dias.
