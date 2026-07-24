---
id: skill-estrutural-taper
numero: skill-0021
titulo: "Taper (polimento) pré-prova — verificar redução de volume de 40-60% mantendo intensidade"
dominio: metodologia-e-periodizacao
tipo_skill: detector
notas_usadas:
  - {id: nota-0247, uso: "protocolo de taper com melhor evidência — redução exponencial de volume 40-60% por 1-3 semanas mantendo intensidade, ganho de desempenho esperado 0,5-6,0%; nota com status 'revisar' no cânone"}
confianca_herdada: 0.65
# = confiança única da nota-0247 (única nota citada nesta skill).
# Ressalva adicional: nota-0247 tem status "revisar" no cânone — é evidência agregada de um único estudo
# citado por McArdle (corredores), não uma prescrição individualizada. Comunicar a faixa de ganho de
# desempenho (0,5-6,0%) sempre como expectativa de evidência, nunca como previsão garantida para o Jacques especificamente.
condicao_nao_calculavel: "sem data do evento-alvo declarada pelo atleta → a janela de taper (1-3 semanas antes) não pode ser identificada, reportar Ausente. Sem histórico de volume/TSS de pelo menos algumas semanas antes do período avaliado → não há linha de base para calcular o percentual de redução, reportar Ausente. A faixa de ganho de 0,5-6,0% nunca deve ser comunicada como previsão exata — é uma expectativa de evidência agregada de um estudo, sujeita a variação individual."
status: proposto
skills_relacionadas:
  - {id: skill-gerais-tss-sessao, tipo: pre-requisito}
  - {id: skill-gerais-pmc, tipo: pre-requisito}
  - {id: skill-classificacao-semana-recuperacao, tipo: complementar}
log_de_teste: []
# populado após cada rodada de validação: {data, caso, resultado, veredito}
---

## O que faz

Verifica se o padrão de redução de volume de treino nas semanas anteriores a uma prova-alvo corresponde ao protocolo de taper (polimento) com melhor evidência — redução de volume de 40-60%, de forma progressiva ao longo de 1-3 semanas, mantendo a intensidade das sessões remanescentes em nível moderado a alto — e reporta a faixa de ganho de desempenho esperado quando o padrão é seguido corretamente.

## Quando usar

- Ao se aproximar de uma prova-alvo declarada pelo atleta (data conhecida).
- Ao avaliar retrospectivamente se o taper de uma prova recente seguiu o padrão de melhor evidência, como parte da explicação de um resultado bom ou ruim.

## Passo a passo

1. **Identificar a janela de taper**: 1 a 3 semanas antes da data do evento-alvo informada pelo atleta. Um taper mínimo de 4-7 dias já é suficiente para reposição de glicogênio muscular/hepático e recuperação de pequenas lesões.
2. **Calcular a linha de base de volume**: usar o TSS semanal total (ou tempo-movimento total) das semanas anteriores ao início do taper como referência.
3. **Calcular a redução real de volume**: comparar o TSS/volume de cada semana da janela de taper contra a linha de base — a redução ideal fica entre 40% e 60%, de forma progressiva (exponencial), não um corte abrupto único numa única semana.
4. **Verificar que a intensidade foi mantida**: calcular o IF médio das sessões remanescentes durante o taper — deve permanecer moderado a alto, não cair junto com o volume (reduzir intensidade junto com volume tende a produzir resultado pior que reduzir só o volume).
5. **Concluir o veredito**: se o volume permanece alto até poucos dias antes da prova (taper tardio/insuficiente), ou se a intensidade cai junto com o volume, sinalizar que o padrão não corresponde ao protocolo com melhor evidência de ganho de desempenho.
6. **Reportar a expectativa de ganho** (0,5-6,0%) apenas como referência de evidência agregada quando o padrão foi seguido corretamente — nunca como previsão garantida individual (nota-0247, status "revisar").
7. **Checar a condição de não-calculável** (ver frontmatter) antes de reportar qualquer veredito.

## Output

```
{
  "evento_alvo_data": "<data ou null>",
  "janela_taper_semanas": <float, null>,
  "volume_linha_de_base_tss_semana": <float, null>,
  "volume_durante_taper_tss_semana": [<float>],
  "reducao_pct": <float, null>,
  "dentro_da_faixa_40_60pct": <bool, null>,
  "reducao_progressiva": <bool, null>,
  "if_medio_mantido_moderado_alto": <bool, null>,
  "veredito": "seguiu_protocolo_de_melhor_evidencia" | "taper_insuficiente_ou_tardio" | "intensidade_caiu_junto_com_volume" | "nao_calculavel",
  "ganho_desempenho_esperado_pct": {"min": 0.5, "max": 6.0, "aplicavel": <bool>},
  "alertas": ["taper_insuficiente" | "intensidade_nao_mantida" | null],
  "provenance": "Estimado" | "Ausente",
  "motivo_provenance": "<texto, obrigatório — esta skill nunca reporta Medido, só Estimado (evidência agregada) ou Ausente>",
  "notas_citadas": ["nota-0247"]
}
```
