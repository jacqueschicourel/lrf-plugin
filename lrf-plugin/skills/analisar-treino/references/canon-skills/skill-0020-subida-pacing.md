---
id: skill-subida-pacing
numero: skill-0020
titulo: "Pacing de prova — orçamento de TSS→NP-alvo, diretrizes de subida, sit-on vs. puxar, DNF por excesso de ritmo, estratégia por duração ultra, isopower em CRI plano"
dominio: tipos-de-treino
tipo_skill: calculadora+detector
notas_usadas:
  - {id: nota-0111, uso: "fórmula do orçamento de TSS → IF → NP-alvo (método Endurance Nation)"}
  - {id: nota-0112, uso: "diretrizes de execução — 95% da potência-alvo nos primeiros 30-45min; +5%/+10% em subidas por duração"}
  - {id: nota-0120, uso: "pacing em subidas de CRI — empurrar mais forte com descida de recuperação; manter na FTP em subida-platô"}
  - {id: nota-0121, uso: "regra da FTP para decidir sit-on vs. puxar numa fuga — se o vale da rotação já exige potência acima do FTP, sentar na roda"}
  - {id: nota-0117, uso: "excesso de ritmo no bike leg é a principal causa citada de DNF em triathlon; diferença de ~15W de NP entre bom e mau pacing; nota com status 'revisar', afirmação qualitativa sem estudo formal"}
  - {id: nota-0138, uso: "gap inicial em prova de 24h tende a persistir; provas de 6-8h decidem no final; nota com status 'revisar', observação qualitativa de poucos casos"}
  - {id: nota-0118, uso: "protocolo isopower para CRI plano — contenção inicial proporcional à duração da prova, potência-alvo na FTP no corpo da prova"}
confianca_herdada: 0.55
# = mínimo das confianças acima (nota-0117 e nota-0138 empatam em 0.55).
# Ressalva adicional: nota-0117 e nota-0138 têm status "revisar" no cânone (afirmações qualitativas/anedóticas
# sem estudo controlado formal por trás). O valor de "~15W de NP" da nota-0117 NUNCA deve ser usado como limiar
# numérico rígido de alerta — só como justificativa qualitativa para dar peso extra a um alerta de pacing agressivo
# já fundamentado no orçamento de TSS (nota-0111). A heurística de duração ultra da nota-0138 (24h vs. 6-8h) também
# deve ser tratada como tendência qualitativa, não regra numérica validada estatisticamente.
condicao_nao_calculavel: "sem FTP válido no perfil (pré-requisito: skill-gerais-ftp-e-zonas) → NP-alvo não é calculável. Sem duração-alvo e TSS orçado declarados pelo atleta para a prova → o orçamento de TSS→NP-alvo (nota-0111) fica Ausente. Sem perfil de elevação disponível → não é possível diferenciar subida-com-descida-de-recuperação de subida-platô (nota-0120), reportar Ausente para esse eixo. O valor '~15W' (nota-0117) nunca deve ser comunicado como limiar numérico confiável, apenas como justificativa qualitativa."
status: proposto
skills_relacionadas:
  - {id: skill-gerais-ftp-e-zonas, tipo: pre-requisito}
  - {id: skill-gerais-tss-sessao, tipo: pre-requisito}
  - {id: skill-classificacao-contexto-atividade, tipo: complementar}
log_de_teste: []
# populado após cada rodada de validação: {data, caso, resultado, veredito}
---

## O que faz

Calcula a Potência Normalizada-alvo (NP-alvo) de pacing para uma prova longa a partir de um orçamento de TSS e da duração-alvo (método Endurance Nation), aplica as diretrizes práticas de execução (contenção inicial, ajustes em subidas), diferencia o pacing de subidas com descida de recuperação das subidas que "platô", aplica a regra da FTP para decidir entre sentar na roda ou puxar numa fuga, sinaliza o risco de excesso de ritmo no bike leg de triathlon, diferencia a estratégia esperada por duração em provas de ultraresistência, e aplica o protocolo isopower para contrarrelógio plano.

## Quando usar

- Ao planejar ou avaliar retrospectivamente o pacing de uma prova longa (contrarrelógio, triathlon, ultraresistência).
- Ao analisar trechos de subida dentro de uma prova com perfil de elevação disponível.
- Ao explicar por que um atleta foi "cuspido" de um grupo/fuga, ou por que não terminou uma prova (DNF).

## Passo a passo

1. **Calcular a NP-alvo**: `TSS_por_hora = TSS_orçado ÷ horas_de_prova`; `IF = sqrt(TSS_por_hora ÷ 100)`; `NP_alvo = IF × FTP`. Referência de orçamento para Ironman: ~280 TSS realista, 300 TSS é o teto de risco (nota-0111).
2. **Aplicar diretrizes de execução**: primeiros 30-45min a 95% da NP-alvo (início conservador); restante da prova em plano o mais próximo possível da NP-alvo; subidas mais longas que 3min a 105% da NP-alvo; subidas de 30s-2min a 110% da NP-alvo (nota-0112).
3. **Diferenciar tipo de subida** (requer perfil de elevação): se há descida de recuperação logo em seguida, pode empurrar mais forte — usar como teto a potência máxima sustentável para aquela duração (Níveis de Coggan) menos 5-10 pontos percentuais de margem (ex.: ~105%FTP numa subida de 3min). Se a subida "platô" (sem descida imediata), manter na FTP ou levemente acima, e retomar rapidamente a velocidade ao cruzar o topo — qualquer tempo abaixo da FTP no platô/reta após o topo é tempo perdido para os concorrentes (nota-0120).
4. **Decidir sit-on vs. puxar numa fuga**: se a potência mesmo no vale de menor exigência da rotação (draft) já está acima da FTP do atleta, sinalizar que o ritmo do grupo é insustentável a médio prazo e recomendar sentar na roda em vez de continuar puxando (nota-0121).
5. **Triathlon — peso extra ao alerta de excesso de ritmo**: dar peso extra (não limiar numérico) a alertas de pacing agressivo no bike leg quando o NP/IF real excede o orçamento calculado (passo 1) — citar que mesmo pequenos excessos de ritmo são apontados qualitativamente como a principal causa de DNF em triathlon, sem tratar "~15W" como limiar validado (nota-0117).
6. **Ultraresistência — estratégia por duração**: para provas de ~24h, reconhecer que pacing agressivo nas primeiras 4-6h (estabelecer um gap) tende a se manter pelo resto da prova; para provas de 6-8h, esperar que os ataques decisivos ocorram perto do final — tratar ambas como tendências qualitativas, não regras rígidas (nota-0138).
7. **CRI plano — protocolo isopower**: primeiros 15-30s para atingir velocidade sem disparar a potência; corpo da prova o mais próximo possível da FTP, com a menor variação possível; últimos minutos aumentar a intensidade. Contenção inicial proporcional à duração: ~5min de contenção para CRI de 40km, ~2min para prova de 10 milhas, quase nenhuma para perseguição de 4km — quanto mais curta a prova, menos se deve segurar (nota-0118).
8. **Checar a condição de não-calculável** (ver frontmatter) antes de reportar qualquer NP-alvo ou veredito de pacing.

## Output

```
{
  "np_alvo_w": <float, null>,
  "if_alvo": <float, null>,
  "tss_orcado": <float, null>,
  "diretrizes_execucao": {"primeiros_30_45min_pct": 95, "subida_longa_3min_pct": 105, "subida_curta_2min_pct": 110},
  "tipo_subida_identificado": "com_descida_recuperacao" | "plato" | "indeterminado",
  "sit_on_recomendado": <bool, null>,
  "risco_dnf_excesso_ritmo": {"sinalizado": <bool>, "np_real_vs_alvo_w": <float, null>},
  "estrategia_ultra_por_duracao": "agressivo_inicio_24h" | "conservar_para_final_6_8h" | null,
  "protocolo_isopower_cri_plano": {"contencao_inicial_min": <float, null>, "aderencia_ftp": <bool, null>},
  "alertas": [
    "inicio_muito_forte" | "subida_platô_perdeu_tempo_apos_topo" | "ritmo_insustentavel_no_vale_da_rotacao" | "excesso_ritmo_bike_leg_risco_dnf" | null
  ],
  "provenance": "Medido" | "Estimado" | "Ausente",
  "motivo_provenance": "<texto, obrigatório se Estimado ou Ausente>",
  "notas_citadas": ["nota-0111", "nota-0112", "nota-0120", "nota-0121", "nota-0117", "nota-0138", "nota-0118"]
}
```
