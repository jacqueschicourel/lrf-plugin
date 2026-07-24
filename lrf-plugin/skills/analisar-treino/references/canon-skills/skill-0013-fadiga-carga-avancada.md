---
id: skill-gerais-fadiga-carga-avancada
numero: skill-0013
titulo: "Fadiga e carga avançada — estagnação por platô de CTL, TSB-alvo por evento, overreached vs. OTS, potência vs. FC, concordância de sinais, dias de recuperação por TSS"
dominio: recuperacao-e-fadiga
tipo_skill: detector
notas_usadas:
  - {id: nota-0089, uso: "platô de CTL por 4-6 semanas sem mudança de foco/performance indica estagnação de treino"}
  - {id: nota-0091, uso: "TSB-alvo pré-prova varia por duração do evento — curto/anaeróbio pede TSB bem positivo, longo/aeróbio tolera TSB neutro/negativo; status 'revisar' no cânone"}
  - {id: nota-0116, uso: "em ultraresistência, TSB no dia da prova é mais preditivo que picos de MMP recentes; status 'revisar' no cânone"}
  - {id: nota-0148, uso: "overreached (agudo, recupera em poucos dias) vs. overtrained/OTS (crônico, >30 dias) — critério de distinção pela duração da recuperação"}
  - {id: nota-0001, uso: "potência mais confiável que FC para detectar fadiga acumulada — FC mais baixa que o habitual na mesma potência não é 'sessão fácil'"}
  - {id: nota-0158, uso: "FC deve ser interpretada com fatores de confusão (temperatura, hidratação, altitude, fadiga, estresse, cafeína) antes de concluir mudança de condicionamento"}
  - {id: nota-0185, uso: "potência (carga externa), FC (parte da carga interna) e RPE/esforço-relativo (resposta global) são complementares, nenhuma substitui a outra"}
  - {id: nota-0194, uso: "TSS mede carga mecânica externa, não mede fadiga/recuperação/adaptação diretamente — nunca afirmar 'fadigado' só por TSS alto"}
  - {id: nota-0198, uso: "fadiga acumulada exige concordância de ≥2 sinais disponíveis (potência, FC/decoupling, TSB, esforço-relativo) antes de disparar alerta — reduz falsos positivos"}
  - {id: nota-0063, uso: "Tabela 7.3 — TSS da sessão → dias de fadiga/recuperação esperados"}
confianca_herdada: 0.55
# = mínimo das confianças acima (nota-0198, 0.55).
# Ressalva adicional: nota-0091 e nota-0116 têm status "revisar" no cânone (pesquisas informais/estudo de caso único,
# não estudos controlados) — os alertas de TSB-alvo por tipo de evento e de priorização do TSB em ultraresistência
# devem ser tratados como heurísticas qualitativas, nunca como limiares numéricos rígidos, mesmo além da cautela
# já implícita no número de confiança de cada uma.
condicao_nao_calculavel: "sem série de CTL/ATL/TSB (pré-requisito: skill-gerais-pmc) → os passos que dependem de TSB (TSB-alvo por evento, priorização em ultraresistência, distinção overreached/OTS) ficam Ausentes. Sem FC disponível na atividade → os passos que cruzam potência×FC (decoupling, fatores de confusão, carga externa vs. interna) ficam Ausentes para esse eixo, mas o eixo baseado só em TSS/potência permanece calculável. Regra inegociável da nota-0198: se só houver 1 sinal disponível (ex.: só TSS, sem FC nem esforço-relativo), a skill NUNCA deve disparar o alerta de 'fadiga acumulada/risco de overreaching' — reportar como indeterminado, não como 'sem fadiga' nem como 'fadigado'."
status: proposto
skills_relacionadas:
  - {id: skill-gerais-pmc, tipo: pre-requisito}
  - {id: skill-gerais-tss-sessao, tipo: pre-requisito}
  - {id: skill-gerais-ambiente-termico, tipo: complementar}
  - {id: skill-classificacao-semana-recuperacao, tipo: complementar}
log_de_teste: []
# populado após cada rodada de validação: {data, caso, resultado, veredito}
---

## O que faz

Aplica um conjunto de regras avançadas de interpretação de fadiga e carga, além do cálculo básico de CTL/ATL/TSB (feito por `skill-gerais-pmc`): detecta estagnação de treino por platô prolongado de CTL, ajusta o TSB-alvo pré-prova pelo tipo/duração do evento, prioriza TSB sobre picos de potência recente em provas de ultraresistência, distingue overreaching agudo de overtraining crônico pela duração da recuperação, aplica a regra de que potência é mais confiável que FC para detectar fadiga (mas com cautela sobre confundidores da FC), trata potência/FC/RPE como sinais complementares nunca substituíveis entre si, nunca afirma "fadigado" só com TSS alto, exige concordância de pelo menos 2 sinais antes de alertar fadiga acumulada, e estima dias de recuperação esperados de uma sessão via a Tabela 7.3.

## Quando usar

- Ao avaliar se um período de treino consistente na verdade estagnou (CTL platôs).
- Ao aproximar-se de uma prova e decidir a estratégia de taper/TSB-alvo.
- Ao interpretar decoupling de FC (mais baixa ou mais alta que o habitual) numa sessão.
- Ao decidir se um estado de fadiga observado é um alerta sério (OTS) ou normal (overreaching agudo recuperável).
- Sempre que for gerar um alerta de "fadiga acumulada" ou "risco de overtraining" — esta skill define o critério de quando esse alerta pode disparar.

## Passo a passo

1. **Detectar estagnação**: se o CTL ficou estável por 4-6 semanas sem mudança de foco de treino e sem evolução de performance correspondente, sinalizar possível estagnação e sugerir progressão de carga em vez de repetir o padrão atual (nota-0089).
2. **TSB-alvo pré-prova por tipo de evento** (tratar como heurística, não limiar rígido — nota-0091 é "revisar"): para eventos curtos/muito anaeróbios (pista, BMX, subidas curtas), recomendar taper para TSB bem positivo (bem descansado); para eventos longos/aeróbios, alertar contra descanso excessivo — TSB pode ficar neutro ou levemente negativo sem prejudicar a performance, e tapear demais arrisca perder a janela de pico de forma.
3. **Ultraresistência (>3-4h)** (heurística — nota-0116 é "revisar"): priorizar TSB (valor e trajetória) no dia da prova sobre picos recentes de MMP como indicador de prontidão. Não usar "melhor 20min da temporada" como proxy de prontidão para esse tipo de prova.
4. **Classificar severidade de um estado de fadiga**: se a performance se recupera em poucos dias após reduzir a carga, classificar como overreaching agudo (não é motivo de alarme excessivo); se a queda de desempenho persiste por mais de 30 dias mesmo com descanso, sinalizar indício de Overtraining Syndrome (OTS) real — recomendação de resposta muito mais séria, incluindo considerar acompanhamento médico (nota-0148).
5. **Decoupling Pw:Hr**: se a FC está mais baixa que o habitual para uma dada potência, NÃO interpretar como "sessão fácil" — é mais provável fadiga acumulada de dias anteriores; usar a potência (não a FC) para orientar a necessidade de descanso, cruzando com a carga recente (TSS/CTL/ATL) (nota-0001).
6. **Fatores de confusão da FC**: antes de sinalizar decoupling ou fadiga cardiovascular só por FC elevada/reduzida isolada, considerar temperatura, hidratação, altitude, estresse psicológico e cafeína — cruzar com `skill-gerais-ambiente-termico` quando o contexto for relevante (nota-0158).
7. **Carga externa vs. interna**: tratar potência (carga externa), FC (parte da carga interna) e esforço-relativo/RPE do Strava (resposta global) como sinais complementares — cruzar as três antes de concluir se uma sessão foi "fácil na potência mas fisiologicamente cara" (nota-0185).
8. **TSS não é fadiga real**: nunca afirmar "atleta fadigado" só porque o TSS acumulado está alto — TSS mede carga mecânica externa, não o estado fisiológico real. Cruzar sempre com pelo menos um sinal de carga interna disponível (nota-0194).
9. **Regra de concordância de ≥2 sinais**: antes de disparar qualquer alerta de "fadiga acumulada" ou "risco de overreaching", exigir que pelo menos 2 dos sinais disponíveis (potência reduzida sustentável, decoupling Pw:Hr elevado, TSB muito negativo, esforço-relativo desproporcionalmente alto) estejam concordando. Um único sinal isolado nunca é suficiente (nota-0198).
10. **Dias de recuperação esperados por sessão**: usar a Tabela 7.3 para estimar o impacto de uma sessão específica — TSS<150: baixo, recuperação completa no dia seguinte; 150-300: moderado, fadiga residual possível até o 2º dia; 300-450: alto, fadiga residual mesmo após 2 dias; >450: muito alto, fadiga residual por vários dias (nota-0063).
11. **Checar a condição de não-calculável** (ver frontmatter) antes de reportar qualquer alerta — em especial a regra inegociável dos ≥2 sinais do passo 9.

## Output

```
{
  "estagnacao_ctl": {"detectada": <bool, null>, "semanas_platô": <float, null>},
  "tsb_alvo_pre_prova": {"tipo_evento": "curto_anaerobio" | "longo_aerobio" | null, "tsb_atual": <float, null>, "dentro_da_faixa_recomendada": <bool, null>},
  "prioridade_ultraresistencia": <bool>,
  "classificacao_fadiga": "overreached_agudo" | "overtraining_syndrome_suspeito" | "indeterminado" | null,
  "decoupling": {"fc_abaixo_do_habitual": <bool, null>, "leitura": "provavel_fadiga_nao_facilidade" | null, "fatores_confusao_considerados": ["<texto>"]},
  "sinais_concordantes": {"potencia_reduzida": <bool>, "decoupling_elevado": <bool>, "tsb_muito_negativo": <bool>, "esforco_relativo_alto": <bool>, "total_concordantes": <int>},
  "alerta_fadiga_acumulada": <bool>,
  "dias_recuperacao_esperados": "menos_1_dia" | "1_2_dias" | "mais_2_dias" | "varios_dias" | null,
  "alertas": [
    "estagnacao_ctl" | "tsb_fora_da_faixa_recomendada" | "overtraining_syndrome_suspeito" | "fadiga_acumulada_concordante" | "sinal_isolado_insuficiente_nao_alertar" | null
  ],
  "provenance": "Medido" | "Estimado" | "Ausente",
  "motivo_provenance": "<texto, obrigatório se Estimado ou Ausente>",
  "notas_citadas": ["nota-0089", "nota-0091", "nota-0116", "nota-0148", "nota-0001", "nota-0158", "nota-0185", "nota-0194", "nota-0198", "nota-0063"]
}
```
