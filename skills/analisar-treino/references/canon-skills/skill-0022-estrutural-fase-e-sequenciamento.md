---
id: skill-estrutural-fase-e-sequenciamento
numero: skill-0022
titulo: "Fase da temporada e sequenciamento semanal — stacking de treinos perdidos, assinatura de zonas por fase, ordem de estímulos na semana"
dominio: metodologia-e-periodizacao
tipo_skill: detector
notas_usadas:
  - {id: nota-0099, uso: "evitar 'stacking' de treinos perdidos — regra de decisão sobre repor ou não um treino perdido"}
  - {id: nota-0106, uso: "assinatura de distribuição de tempo-em-zona esperada por fase da temporada (base/construção/pico)"}
  - {id: nota-0190, uso: "sequenciamento de estímulos no microciclo — complexidade quando descansado, evitar sobreposição de estímulos semelhantes"}
confianca_herdada: 0.5
# = mínimo das confianças acima (nota-0190, 0.5 — a mais baixa de toda a base de skills construída até agora).
# nota-0190 tem status "auto-aprovado", mas sua confiança numérica já é baixa por vir de uma lista de princípios
# gerais do Manual sem estudo/exemplo numérico específico — tratar seus alertas de sequenciamento como
# sugestões fracas a considerar, nunca como conclusões fortes ou automáticas.
condicao_nao_calculavel: "sem histórico de pelo menos a semana anterior de sessões consecutivas → o sequenciamento (nota-0190) não é avaliável, reportar Ausente. Sem a fase da temporada declarada pelo atleta (base/construção/pico) → a assinatura de distribuição de zonas (nota-0106) não tem referência para comparação, reportar Ausente. O detector de stacking (nota-0099) exige saber se houve um período de baixa atividade recente seguido de concentração de carga — sem esse padrão temporal claro, não aplicar o alerta."
status: proposto
skills_relacionadas:
  - {id: skill-classificacao-tipo-de-sessao, tipo: pre-requisito}
  - {id: skill-gerais-tss-sessao, tipo: pre-requisito}
  - {id: skill-gerais-fadiga-carga-avancada, tipo: complementar}
log_de_teste: []
# populado após cada rodada de validação: {data, caso, resultado, veredito}
---

## O que faz

Detecta o padrão de risco de "stacking" (empilhamento de múltiplos treinos difíceis em poucos dias após um período de baixa atividade), compara a distribuição real de tempo-em-zona de um período contra a assinatura esperada para a fase da temporada declarada pelo atleta (base, construção, pré-competição, temporada de corridas), e sinaliza sequenciamento subótimo de estímulos intensos dentro da semana.

## Quando usar

- Ao detectar múltiplas sessões de alta intensidade/TSS concentradas em poucos dias após um período de baixa atividade.
- Ao avaliar se a distribuição de treino de um atleta é consistente com a fase da temporada que ele diz estar vivendo.
- Ao revisar o calendário semanal de treino em busca de sequenciamento subótimo (ex.: intervalado intenso no dia seguinte a uma sessão muito exigente).

## Passo a passo

1. **Detectar stacking**: se múltiplos treinos de alta intensidade/TSS elevado se concentram em 1-2 dias, logo após um período de baixa atividade na semana, sinalizar padrão de risco — com mais peso se for comportamento recorrente do atleta (nota-0099).
2. **Regra sobre treino perdido**: por padrão, não penalizar a ausência de reposição de um treino perdido — seguir para o próximo treino do plano é o comportamento recomendado. Exceção: se o treino perdido era altamente específico e não se repetirá por pelo menos 2 semanas, repor o quanto antes é válido — mas nunca empilhado com outro treino difícil no mesmo dia (nota-0099).
3. **Comparar distribuição de zonas contra a fase declarada**: Base (inverno/entressafra) → predomínio de Níveis 1-3; Construção (primavera) → aumento de Nível 3, 5 e 6; Pré-competição intensa → Nível 6 e Nível 1 sobem juntos (mais intensidade exige mais recuperação); Temporada de corridas → predomínio perto da FTP (Nível 4), com queda acentuada logo acima (nota-0106).
4. **Sinalizar desvios de fase**: um atleta "em fase de base" com tempo desproporcional em Níveis 5-6, ou "em pico de temporada" ainda predominantemente em Nível 2, são desvios dignos de nota no feedback.
5. **Avaliar sequenciamento semanal** (tratar como sugestão fraca — nota-0190 tem confiança baixa, 0,5): sinalizar quando uma sessão de maior complexidade/intensidade (VO2max, força) é feita no dia seguinte a uma sessão muito longa/extenuante ou a outro intervalado intenso — princípios gerais: complexidade quando descansado, qualidade antes de quantidade, recuperação ativa após sessões exigentes, evitar empilhar estímulos semelhantes em dias consecutivos.
6. **Checar a condição de não-calculável** (ver frontmatter) antes de reportar qualquer alerta.

## Output

```
{
  "stacking_detectado": <bool, null>,
  "treino_perdido_reposicao_recomendada": <bool, null>,
  "fase_temporada_declarada": "base" | "construcao" | "pre_competicao" | "temporada_corridas" | null,
  "distribuicao_zonas_consistente_com_fase": <bool, null>,
  "sequenciamento": {"sessao_complexa_apos_sessao_exigente": <bool, null>, "confianca": "baixa"},
  "alertas": [
    "stacking_padrao_de_risco" | "distribuicao_zonas_inconsistente_com_fase_declarada" | "sequenciamento_subotimo_sugestao_fraca" | null
  ],
  "provenance": "Medido" | "Estimado" | "Ausente",
  "motivo_provenance": "<texto, obrigatório se Estimado ou Ausente>",
  "notas_citadas": ["nota-0099", "nota-0106", "nota-0190"]
}
```
