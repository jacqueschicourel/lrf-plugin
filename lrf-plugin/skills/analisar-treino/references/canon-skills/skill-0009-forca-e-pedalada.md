---
id: skill-gerais-forca-e-pedalada
numero: skill-0009
titulo: "Força e qualidade de pedalada — W/kg, AEPF/CPV, Quadrant Analysis, GPR/GPA/KI, Pedaling Smoothness/Torque Efficiency"
dominio: metricas-de-potencia
tipo_skill: calculadora+detector
notas_usadas:
  - {id: nota-0033, uso: "W/kg = potência ÷ peso corporal"}
  - {id: nota-0065, uso: "AEPF = (P×60)/(C×2π×CL) — força efetiva média no pedal"}
  - {id: nota-0066, uso: "CPV = (C×CL×2π)/60 — velocidade circunferencial do pedal"}
  - {id: nota-0067, uso: "Quadrant Analysis — 4 quadrantes força×velocidade, linhas divisórias no FTP"}
  - {id: nota-0070, uso: "power balance padrão ANT+ é enganoso — não contabiliza potência absorvida na perna oposta"}
  - {id: nota-0071, uso: "GPR/GPA/Kurtotic Index — métricas corretas de análise bilateral"}
  - {id: nota-0146, uso: "Pedaling Smoothness (Pavg/Ppeak) e Torque Efficiency (100×(P+−P−)/P+)"}
  - {id: nota-0069, uso: "treino de força-resistência não aumenta força/hipertrofia de forma relevante — calibrar expectativa"}
  - {id: nota-0073, uso: "limiares de ação para desequilíbrio bilateral (>10% GPR, GPA>35W sentado); nunca recomendar 'puxar o pedal'"}
  - {id: nota-0122, uso: "comparar Quadrant Analysis de treino vs. prova-alvo para checar especificidade neuromuscular"}
  - {id: nota-0110, uso: "quadrantes-alvo (III/IV) e VI-alvo (1,04-1,07) para conservar glicogênio no bike leg de triathlon"}
confianca_herdada: 0.6
# = mínimo das confianças acima (nota-0146 é a mais fraca, 0.6).
condicao_nao_calculavel: "sem peso corporal no perfil → W/kg não calculável (demais cálculos desta skill não dependem de peso). Sem comprimento de manivela no perfil/config → AEPF, CPV e Quadrant Analysis não calculáveis. Sem FTP vigente (skill-gerais-ftp-e-zonas) → linhas divisórias dos quadrantes não calculáveis. Sem medidor de potência bilateral → GPR/GPA/Kurtotic Index/Pedaling Smoothness/Torque Efficiency não calculáveis; se houver apenas o 'power balance' padrão ANT+, reportá-lo com a ressalva explícita da nota-0070 (pode estar enviesado, não contabiliza potência absorvida)."
status: proposto
skills_relacionadas:
  - {id: skill-gerais-ftp-e-zonas, tipo: pre-requisito}
  - {id: skill-gerais-qualidade-de-dado, tipo: pre-requisito}
  - {id: skill-gerais-checklist-pos-treino, tipo: consumida-por}
log_de_teste: []
# populado após cada rodada de validação: {data, caso, resultado, veredito}
---

## O que faz

Calcula a família de métricas de força/qualidade de pedalada: razão potência/peso (W/kg), força e velocidade do pedal (AEPF/CPV), a Quadrant Analysis (distribuição em 4 quadrantes força×velocidade), e — quando houver medidor bilateral — GPR/GPA/Kurtotic Index e Pedaling Smoothness/Torque Efficiency. Aplica os detectores de interpretação correta: não confiar no "power balance" simplista do ANT+, calibrar expectativa sobre treino de "força-resistência", limiares de ação para desequilíbrio bilateral (com cautela explícita contra a recomendação intuitiva de "puxar o pedal"), comparação treino-vs-prova, e as metas específicas de triathlon (Quadrantes III/IV + VI 1,04-1,07 no bike leg).

## Quando usar

- Ao calcular W/kg de qualquer pico/média de potência para comparação entre atletas ou posicionamento no Power Profile.
- Sempre que houver comprimento de manivela e FTP vigente disponíveis, para construir a Quadrant Analysis de uma atividade.
- Ao investigar desequilíbrio bilateral reportado pelo Strava/Garmin (medidor bilateral) — antes de recomendar qualquer ajuste de técnica.
- Ao avaliar se um plano de treino com blocos de "força-resistência" está gerando o ganho de força esperado.
- Ao comparar a especificidade neuromuscular de treinos contra provas-alvo, especialmente em triathlon (conservação de glicogênio no bike leg).

## Passo a passo

1. **W/kg** = potência (pico ou média, qualquer duração) ÷ peso corporal em kg (nota-0033).
2. **AEPF** = `(P×60) / (C×2π×CL)`, ponto a ponto ou por intervalo, com P=potência(W), C=cadência(rpm), CL=comprimento de manivela(m) (nota-0065).
3. **CPV** = `(C×CL×2π) / 60` (nota-0066).
4. **Quadrant Analysis:** calcular AEPF e CPV no FTP do atleta (na cadência autosselecionada) como linhas divisórias; classificar cada ponto/trecho da atividade em Quadrante I (alta força+alta velocidade — sprint/ataque), II (alta força+baixa velocidade — subida/largada), III (baixa força+baixa velocidade — recuperação/social) ou IV (baixa força+alta velocidade — marcha leve/criterium) (nota-0067).
5. **Se houver medidor bilateral:** calcular GPR/GPA por perna em vez de usar o "power balance" bruto do ANT+, que não contabiliza a potência absorvida pela perna oposta e pode distorcer o percentual real (nota-0070, nota-0071). Opcionalmente, calcular Pedaling Smoothness (`Pavg/Ppeak` do ciclo) e Torque Efficiency (`100×(P+−P−)/P+` do ciclo) (nota-0146).
6. **Aplicar limiares de ação bilateral:** diferença de GPR >10% entre pernas → sinalizar possível discrepância de força muscular ou problema de bike fit (investigar, não corrigir automaticamente); GPA >35W sentado em ambas as pernas (atleta com 3+ anos de treino) → sugerir foco técnico específico (joelho em direção ao guidão + ponta do pé para baixo na subida do pedal). **Nunca recomendar "puxar o pedal" deliberadamente** — a evidência citada mostra que isso reduz a eficiência metabólica (nota-0073).
7. **Se o atleta fizer/planejar treino de "força-resistência"** (cadência baixa 45-75rpm, marcha pesada): calibrar a expectativa de feedback — a evidência citada não sustenta ganho relevante de força/hipertrofia com esse tipo de treino (nota-0069).
8. **Comparar Quadrant Analysis de treino vs. prova-alvo:** se houver arquivo de prova real de duração semelhante, comparar a distribuição por quadrante contra a de treinos recentes — discrepância sistemática (ex.: treino sempre em Q3/Q4, prova com bastante Q2) é lacuna de especificidade a sinalizar (nota-0122).
9. **Para bike leg de triathlon:** verificar se a maior parte do tempo ficou em Quadrantes III/IV e se o VI da sessão ficou entre 1,04-1,07 — desvios (ex.: >41% em Quadrante II, ou VI>1,07) sinalizam risco de desperdício de glicogênio relevante para a corrida seguinte (nota-0110).
10. **Checar a condição de não-calculável** (ver frontmatter) antes de reportar qualquer número como Medido/Estimado.

## Output

```
{
  "w_kg": {"duracao": "<ex: 5min>", "valor": <float>},
  "quadrant_analysis": {
    "q1_pct": <float>, "q2_pct": <float>, "q3_pct": <float>, "q4_pct": <float>
  },
  "bilateral": {
    "gpr_esquerda_w": <float, null>, "gpr_direita_w": <float, null>,
    "gpa_esquerda_w": <float, null>, "gpa_direita_w": <float, null>,
    "diferenca_gpr_pct": <float, null>,
    "pedaling_smoothness_pct": <float, null>,
    "torque_efficiency_pct": <float, null>
  },
  "alertas": [
    "desequilibrio_bilateral_investigar" | "gpa_alta_sugerir_ajuste_tecnico" | "forca_resistencia_expectativa_calibrada" | "falta_especificidade_neuromuscular" | "risco_glicogenio_bike_leg_triathlon" | null
  ],
  "provenance": "Medido" | "Estimado" | "Ausente",
  "motivo_provenance": "<texto, obrigatório se Estimado ou Ausente>",
  "notas_citadas": ["nota-0033", "nota-0065", "nota-0066", "nota-0067", ...]
}
```
