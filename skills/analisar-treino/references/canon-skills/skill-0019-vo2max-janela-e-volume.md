---
id: skill-vo2max-janela-e-volume
numero: skill-0019
titulo: "VO2máx — janela de duração eficaz, quase-platô de campo, HIIT vs. contínuo, protocolo 4×4 padrão-ouro, volume total > duração isolada, micro-burst"
dominio: tipos-de-treino
tipo_skill: detector
notas_usadas:
  - {id: nota-0042, uso: "janela de duração eficaz por repetição — mínimo 3min, máximo ~8min, a 106-120%FTP"}
  - {id: nota-0125, uso: "quase-platô de potência entre 1,5-2,5min de esforço máximo aproxima a potência real de VO2máx, sem teste de laboratório"}
  - {id: nota-0220, uso: "meta-análise — HIIT supera treino contínuo moderado para ganho de VO2máx (+5,5 vs +4,9 mL/kg/min)"}
  - {id: nota-0221, uso: "protocolo 4×4min (90-95%FCmáx/3min recuperação a 70%FCmáx) como padrão-ouro validado (+8,8% VO2máx em 8 semanas)"}
  - {id: nota-0222, uso: "volume total acumulado de trabalho em alta intensidade na sessão prediz o ganho melhor que a duração de uma repetição isolada"}
  - {id: nota-0044, uso: "protocolo micro-burst (15s a 150%FTP/15s a 50%FTP) como estímulo alternativo, reconhecer antes de aplicar outra métrica de zona"}
confianca_herdada: 0.65
# = mínimo das confianças acima (nota-0125, 0.65). Todas as notas citadas têm status "auto-aprovado".
condicao_nao_calculavel: "sem série temporal de potência e/ou FC → a janela de duração por repetição e a estimativa de quase-platô não são calculáveis, reportar Ausente. Esta skill assume que a sessão já foi roteada como candidata a VO2máx por skill-classificacao-tipo-de-sessao — não deve ser aplicada isoladamente sem esse roteamento prévio, sob risco de aplicar as regras finas de VO2máx a uma sessão de outro tipo."
status: proposto
skills_relacionadas:
  - {id: skill-classificacao-tipo-de-sessao, tipo: pre-requisito}
  - {id: skill-gerais-ftp-e-zonas, tipo: pre-requisito}
log_de_teste: []
# populado após cada rodada de validação: {data, caso, resultado, veredito}
---

## O que faz

Aplica as regras finas de estímulo de VO2máx a uma sessão já roteada como candidata a esse tipo por `skill-classificacao-tipo-de-sessao`: verifica se a duração de cada repetição caiu na janela eficaz (3-8min), estima a potência real de VO2máx via o "quase-platô" de campo, fundamenta por que HIIT é preferível a treino contínuo moderado para esse objetivo, reconhece o protocolo 4×4min como referência de padrão-ouro validado, prioriza o volume total acumulado de trabalho em alta intensidade sobre a duração isolada de uma repetição, e reconhece o padrão micro-burst como estímulo alternativo.

## Quando usar

- Depois que `skill-classificacao-tipo-de-sessao` já classificou a sessão (ou um bloco dela) como candidata a VO2máx.
- Ao avaliar se um bloco de intervalos foi eficaz para o objetivo declarado de elevar VO2máx/potência aeróbia máxima.
- Ao estimar a potência de VO2máx do atleta a partir de um esforço máximo de campo, sem teste de laboratório.

## Passo a passo

1. **Confirmar o roteamento**: esta skill só deve ser aplicada a sessões/blocos já classificados como candidatos a VO2máx.
2. **Verificar a janela de duração eficaz**: cada repetição deve durar entre 3 e 8 minutos a 106-120% do FTP (Nível 5 de Coggan) para gerar estímulo adequado de VO2máx — fora dessa janela (mesmo na intensidade certa), o sistema predominantemente treinado tende a ser outro (capacidade anaeróbia, se muito curto; limiar, se a intensidade cair para sustentar mais tempo) (nota-0042).
3. **Estimar a potência de VO2máx pelo quase-platô**: em esforços máximos de 3+ minutos bem executados, identificar o ponto (tipicamente entre 1,5-2,5min) onde a potência para de cair rapidamente e estabiliza — esse patamar é uma boa aproximação de campo da potência real de VO2máx do atleta (nota-0125).
4. **Justificar a priorização de HIIT**: ao recomendar intervalado de alta intensidade em vez de mais volume contínuo em Z2 para o objetivo de elevar VO2máx, citar a evidência de meta-análise (+5,5 mL/kg/min HIIT vs. +4,9 contínuo moderado, vantagem de 1,2 mL/kg/min) — efeito ampliado em atletas mais velhos, com aptidão de base mais baixa, ou com intervenções/repetições mais longas (nota-0220).
5. **Reconhecer o protocolo 4×4min como padrão-ouro**: 4 séries de 4min a 90-95%FCmáx com 3min de recuperação ativa a 70%FCmáx entre elas — evidência comparativa direta mostra +8,8% de VO2máx em 8 semanas, superando 15s-on/15s-off (+6,4%) e treino contínuo (~+2%, não significativo), com o mesmo gasto energético total (nota-0221).
6. **Priorizar volume total sobre duração isolada**: ao avaliar se uma sessão "valeu a pena" para VO2máx, somar o tempo total acumulado em alta intensidade (todas as repetições), não avaliar apenas a duração de uma repetição isolada — esse volume total é o maior preditor de ganho. Intervalos curtos/sprint só contam se forem verdadeiramente "all-out"; intervalos mais longos podem ser submáximos mas ainda muito difíceis (nota-0222).
7. **Detectar padrão micro-burst** (15s a ~150%FTP / 15s a ~50%FTP em blocos de ~10min) como estímulo alternativo — reconhecer antes de aplicar outra métrica de zona, pois pode contribuir tanto ao estímulo neuromuscular quanto, dependendo do contexto do bloco, ao de VO2máx/limiar (nota-0044).
8. **Checar a condição de não-calculável** (ver frontmatter) antes de reportar qualquer estimativa.

## Output

```
{
  "repeticoes": [{"duracao_s": <int>, "dentro_da_janela_3_8min": <bool>, "potencia_media_w": <float>}],
  "vo2max_watts_estimado_quase_plato": <float, null>,
  "volume_total_alta_intensidade_s": <float, null>,
  "protocolo_reconhecido": "4x4min_padrao_ouro" | "microburst" | "outro" | "indeterminado",
  "justificativa_hiit_vs_continuo": "<texto ou null>",
  "alertas": [
    "repeticao_fora_da_janela_3_8min" | "volume_total_baixo_apesar_de_repeticoes_longas" | "protocolo_4x4_reconhecido" | "microburst_detectado" | null
  ],
  "provenance": "Medido" | "Estimado" | "Ausente",
  "motivo_provenance": "<texto, obrigatório se Estimado ou Ausente>",
  "notas_citadas": ["nota-0042", "nota-0125", "nota-0220", "nota-0221", "nota-0222", "nota-0044"]
}
```
