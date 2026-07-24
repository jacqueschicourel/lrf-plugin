---
id: skill-limiar-calibracao-rpe
numero: skill-0018
titulo: "Calibração de potência-RPE — reconhecer o protocolo de 3 fases e usar a relação aprendida para validar pacing"
dominio: tipos-de-treino
tipo_skill: detector
notas_usadas:
  - {id: nota-0109, uso: "protocolo de calibração de potência-RPE de 3 fases (10min→20min→60min) para pacing em triathlon; regra crítica de no máximo 1 sessão/dia"}
confianca_herdada: 0.75
# = confiança única da nota-0109 (única nota citada nesta skill). Status auto-aprovado, sem ressalva adicional.
condicao_nao_calculavel: "sem esforço-relativo (proxy de RPE do Strava) disponível nas sessões candidatas → não é possível associar a relação RPE-potência aprendida, reportar Ausente. Reconhecer o padrão das 3 fases exige um histórico de pelo menos ~10-20 dias de sessões estruturadas repetidas por intensidade — sem esse volume de dados, não há bloco de calibração a reconhecer, mesmo que sessões isoladas pareçam parecidas com o protocolo."
status: proposto
skills_relacionadas:
  - {id: skill-gerais-tss-sessao, tipo: pre-requisito}
  - {id: skill-subida-pacing, tipo: complementar}
log_de_teste: []
# populado após cada rodada de validação: {data, caso, resultado, veredito}
---

## O que faz

Reconhece, no histórico de treino, um bloco de sessões que segue o protocolo estruturado de calibração de potência-RPE (associar esforço percebido a uma wattagem específica, essencial para pacing em triathlon, onde FC/RPE no dia da prova tende a ficar mais baixo que no treino para o mesmo esforço real) e, quando identificado, usa a relação RPE-vs-potência aprendida para validar a estratégia de pacing do atleta numa prova subsequente.

## Quando usar

- Ao analisar um histórico de treino com sessões repetidas de duração/intensidade específicas ao longo de ~10-20 dias.
- Ao validar se o pacing de uma prova (especialmente triathlon) correspondeu à relação RPE-potência que o atleta já havia calibrado em treino.

## Passo a passo

1. **Identificar candidatos à Fase 1** (curta duração): sequência de sessões com 3-4 intervalos de 10 minutos (5 minutos de recuperação entre eles), repetidas ~5 vezes ao longo de ~10 dias, num mesmo nível de intensidade-alvo.
2. **Identificar Fase 2** (duração média): se a Fase 1 foi repetida pelo menos 2 vezes numa dada intensidade, procurar 2 esforços de 20 minutos naquela mesma intensidade.
3. **Identificar Fase 3** (duração longa): esforços de 60 minutos, repetidos pelo menos mais 2 vezes na mesma intensidade.
4. **Aplicar a regra crítica**: no máximo 1 sessão de calibração por dia. Se o histórico mostrar 2+ sessões de calibração no mesmo dia, sinalizar que a internalização do RPE para aquele bloco pode estar comprometida (respostas físicas de diferentes níveis se misturam) — reduzir a confiança da relação RPE-potência aprendida nesse trecho.
5. **Usar a relação aprendida**: quando um bloco de calibração for reconhecido com confiança razoável, usar a associação RPE↔potência resultante para cruzar/validar a estratégia de pacing do atleta numa prova subsequente — especialmente relevante em triathlon.
6. **Checar a condição de não-calculável** (ver frontmatter) antes de reportar qualquer relação RPE-potência como aprendida.

## Output

```
{
  "bloco_calibracao_reconhecido": <bool>,
  "fases_completas": {"fase_1_10min": <bool>, "fase_2_20min": <bool>, "fase_3_60min": <bool>},
  "intensidades_calibradas": [{"nivel": "<texto>", "potencia_w": <float>, "rpe_associado": <float, null>}],
  "violacao_1_sessao_por_dia": <bool>,
  "relacao_rpe_potencia_aplicavel_a_pacing": <bool>,
  "alertas": ["multiplas_sessoes_calibracao_mesmo_dia_confianca_reduzida" | null],
  "provenance": "Medido" | "Estimado" | "Ausente",
  "motivo_provenance": "<texto, obrigatório se Estimado ou Ausente>",
  "notas_citadas": ["nota-0109"]
}
```
