---
id: skill-classificacao-tipo-de-sessao
numero: skill-0014
titulo: "Classificação do tipo de sessão — roteador (tempo-em-zona/estrutura, não média geral) para os 7 níveis de Coggan e o catálogo de objetivos do Manual"
dominio: metodologia-e-periodizacao
tipo_skill: classificador
notas_usadas:
  - {id: nota-0022, uso: "os 7 níveis clássicos de Coggan (%FTP/%FTHR/RPE/duração) — referência de zona usada para classificar"}
  - {id: nota-0017, uso: "protocolo de marcação de lap para calcular potência-por-lap precisa por trecho"}
  - {id: nota-0029, uso: "mesma zona de potência média tem estresse diferente em prova vs. treino, por causa da variabilidade (VI)"}
  - {id: nota-0030, uso: "a média geral da sessão pode mascarar a estrutura real — classificar pelo bloco/tempo-em-zona, não pela média"}
  - {id: nota-0039, uso: "potência ao ar livre é estocástica — avaliar aderência a intervalo por faixa-alvo, não valor exato"}
  - {id: nota-0042, uso: "janela de 3-8min para estímulo eficaz de VO2máx"}
  - {id: nota-0052, uso: "tempo-em-zona de potência pode enganar em padrões intermitentes — potência não tem inércia como a FC"}
  - {id: nota-0007, uso: "cadência <70rpm em potência de limiar associada a perda de contato — estudo de caso N=1, status 'revisar', nunca virar recomendação automática"}
  - {id: nota-0125, uso: "quase-platô de potência após 1,5-2,5min de esforço máximo aproxima a potência real de VO2máx, sem teste de laboratório"}
  - {id: nota-0151, uso: "faixas de cadência típicas por contexto (moderado/sprint/subida) — heurística frouxa, não regra de alerta"}
  - {id: nota-0199, uso: "catálogo de sessões por objetivo fisiológico do Manual — Base Aeróbia, Limiar, VO2máx, Anaeróbio, Neuromuscular, Regenerativa"}
  - {id: nota-0044, uso: "protocolo micro-burst (15s a 150%FTP / 15s a 50%FTP) — reconhecer antes de aplicar outra métrica de zona"}
confianca_herdada: 0.55
# = mínimo das confianças acima (nota-0007 e nota-0151 empatam em 0.55).
# Ressalva adicional: nota-0007 tem status "revisar" no cânone (estudo de caso N=1, não achado sistemático) —
# o detector de cadência baixa em limiar NUNCA deve gerar recomendação automática de troca de marcha,
# só uma hipótese de baixa confiança sinalizada para revisão humana, mesmo que o resto da sessão seja classificável com confiança maior.
condicao_nao_calculavel: "sem série temporal de potência (só resumo/potência-média da atividade) → não é possível classificar pela estrutura real, reportar Ausente e avisar que uma classificação pela média isolada é pouco confiável (nota-0030). Sem Zonas de potência calculadas (depende do FTP, ver skill-gerais-ftp-e-zonas) → tempo-em-zona não é calculável, delegar primeiro para essa skill. O detector de cadência baixa em limiar (nota-0007) nunca gera recomendação automática, apenas hipótese de baixa confiança."
status: proposto
skills_relacionadas:
  - {id: skill-gerais-ftp-e-zonas, tipo: pre-requisito}
  - {id: skill-gerais-tss-sessao, tipo: pre-requisito}
  - {id: skill-limiar-intervalos-repetibilidade, tipo: despachada-para}
  - {id: skill-limiar-calibracao-rpe, tipo: despachada-para}
  - {id: skill-vo2max-janela-e-volume, tipo: despachada-para}
  - {id: skill-subida-pacing, tipo: despachada-para}
log_de_teste: []
# populado após cada rodada de validação: {data, caso, resultado, veredito}
---

## O que faz

Classifica o tipo provável de uma sessão de treino (Base Aeróbia, Endurance, Tempo, Limiar, VO2máx, Anaeróbio, Neuromuscular, ou padrão especial como micro-burst) a partir da estrutura real de tempo-em-zona/blocos — nunca pela potência-média geral do arquivo inteiro — cruzando os 7 níveis clássicos de Coggan com o catálogo de sessões por objetivo do Manual. É o **roteador**: decide o tipo antes de despachar para a skill específica que aplica as regras finas daquele tipo (limiar, VO2máx, subida-pacing).

## Quando usar

- Sempre que for necessário nomear/rotular o "tipo" de uma sessão antes de aplicar uma skill específica por tipo de treino.
- Ao gerar feedback pós-treino que precise contextualizar se a execução correspondeu ao padrão esperado daquele tipo de sessão.
- Ao comparar duas sessões que têm potência-média parecida mas podem ser fisiologicamente muito diferentes (ex.: prova vs. treino solo).

## Passo a passo

1. **Pré-requisito**: garantir que as Zonas de potência (7 níveis de Coggan, nota-0022) já foram calculadas via `skill-gerais-ftp-e-zonas` — sem isso, tempo-em-zona não é calculável.
2. **Calcular Tempo-em-zona** (Calc#14) a partir da potência-série-temporal e das zonas. Se houver marcações de lap, calcular também **Potência-por-lap** (Calc#15, nota-0017) para isolar cada trecho prescrito.
3. **Nunca classificar pela potência-média geral**: examinar a distribuição de tempo-em-zona/blocos para achar o estímulo predominante. Ex.: 30min aquecimento (N1) + 60min Tempo (N3) + 30min volta à calma (N1) tem média geral em N2, mas é uma sessão de **Tempo** (nota-0030).
4. **Detectar padrão micro-burst** (alternância regular de ~15s a ~150%FTP / ~15s a ~50%FTP em blocos de ~10min) antes de aplicar qualquer outra métrica de zona — reclassificar como estímulo neuromuscular ou limiar conforme o contexto do bloco, não como "intervalos tradicionais" (nota-0044).
5. **Ao avaliar aderência a um intervalo prescrito**, comparar contra a faixa-alvo (ex.: 300-320W), não um valor exato — a potência ao ar livre é estocástica por natureza do terreno/vento (nota-0039).
6. **Cautela com "tempo em zona" em padrões intermitentes**: a potência não tem a inércia fisiológica da FC, então "30min acumulados em Nível 5" pode vir de bursts curtos que nunca estressaram de fato o sistema daquele nível continuamente — checar a duração de cada incursão individual, não só o total acumulado (nota-0052).
7. **Candidatar a VO2máx** quando houver blocos de **3-8min** dentro de 106-120%FTP (Nível 5) — janela mínima necessária para estímulo eficaz (nota-0042). Em esforços máximos de 3+min, usar o "quase-platô" de potência que se forma entre 1,5-2,5min como estimativa de campo da potência real de VO2máx do atleta, sem precisar de teste de laboratório (nota-0125).
8. **Nomear o tipo** cruzando a estrutura observada contra o catálogo do Manual: Base Aeróbia (3h30-5h em Z2, baixa variabilidade), Limiar (2×20min/3×15min/4×10min perto de LT2/FTP), VO2máx (5×5min/6×4min/4×8min/30-30), Anaeróbio (8×1min/10×30s), Neuromuscular (sprints 6-12s, foco em qualidade não volume), Regenerativa (intensidade muito baixa, curta) (nota-0199).
9. **Ao interpretar sessão de prova (mass-start)**, lembrar que a mesma zona de potência média tem estresse fisiológico maior em prova do que em treino solo, por causa da maior variabilidade (VI mais alto) — não equiparar diretamente sem checar VI (nota-0029).
10. **Cadência como sinal de contexto (cautela)**: cadência <70rpm sustentada em potência de limiar é uma hipótese de baixa confiança (nota-0007, N=1, status "revisar") — nunca gerar recomendação automática de troca de marcha, só sinalizar para revisão humana. Faixas de cadência por contexto (80-95rpm moderado / >110rpm sprint / <75rpm subida, nota-0151) são heurística frouxa adicional, não regra de alerta.
11. **Despachar** para a skill específica do tipo classificado (`skill-limiar-*`, `skill-vo2max-janela-e-volume`, `skill-subida-pacing`) para aplicar as regras finas daquele tipo.
12. **Checar a condição de não-calculável** (ver frontmatter) antes de reportar qualquer classificação.

## Output

```
{
  "tipo_sessao_provavel": "base_aerobia" | "endurance" | "tempo" | "limiar" | "vo2max" | "anaerobio" | "neuromuscular" | "regenerativa" | "microburst" | "indeterminado",
  "metodo_classificacao": "estrutura_tempo_em_zona" | "media_geral_baixa_confianca",
  "blocos_identificados": [{"inicio_s": <int>, "fim_s": <int>, "nivel_coggan": <int 1-7>, "potencia_media_w": <float>}],
  "vo2max_watts_estimado_quase_plato": <float, null>,
  "alertas": [
    "classificado_so_pela_media_baixa_confianca" | "padrao_microburst_detectado" | "cadencia_baixa_limiar_hipotese_n1_revisar" | "prova_vs_treino_mesma_zona_estresse_diferente" | null
  ],
  "skill_despachada_para": "<id da skill específica por tipo, ou null se indeterminado>",
  "provenance": "Medido" | "Estimado" | "Ausente",
  "motivo_provenance": "<texto, obrigatório se Estimado ou Ausente>",
  "notas_citadas": ["nota-0022", "nota-0017", "nota-0029", "nota-0030", "nota-0039", "nota-0042", "nota-0052", "nota-0007", "nota-0125", "nota-0151", "nota-0199", "nota-0044"]
}
```
