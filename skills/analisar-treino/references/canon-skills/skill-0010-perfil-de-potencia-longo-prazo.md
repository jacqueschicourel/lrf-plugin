---
id: skill-gerais-perfil-de-potencia-longo-prazo
numero: skill-0010
titulo: "Perfil de potência de longo prazo — MMP/PDC, Pmax, FRC, TTE, Stamina, Mapa Fenotípico, Power Profile, resistência à fadiga"
dominio: metricas-de-potencia
tipo_skill: calculadora+detector
notas_usadas:
  - {id: nota-0053, uso: "MMP Curve — dado real, melhor potência por duração; requisitos de leitura válida (≥6 meses, esforços genuinamente máximos)"}
  - {id: nota-0103, uso: "distinção MMP (dado real) vs. PDC (modelo ajustado) — expor os dois, não só o modelo"}
  - {id: nota-0037, uso: "PDC — conceito introdutório, curva de melhor ajuste sobre a MMP"}
  - {id: nota-0077, uso: "Pmax — potência máxima numa volta de pedal, aproximada pelo pico de 1s disponível"}
  - {id: nota-0078, uso: "FRC — capacidade em joules acima do FTP; fórmula potência-sustentável = FTP + FRC/duração"}
  - {id: nota-0080, uso: "TTE — tempo que o atleta sustenta o próprio mFTP; dois atletas com mFTP igual podem ter TTE muito diferente"}
  - {id: nota-0081, uso: "Stamina — % resistência à fadiga sub-FTP prolongada; maioria dos atletas 75-85%"}
  - {id: nota-0082, uso: "Mapa Fenotípico — razões Pmax/FTP e FRC/Pmax; nota com status 'revisar' no cânone, cautela extra"}
  - {id: nota-0031, uso: "Tabela 4.1 — Power Profile, faixas W/kg por categoria nas 4 durações-índice"}
  - {id: nota-0032, uso: "as 4 durações-índice (5s/1min/5min/FTP) e a capacidade fisiológica que cada uma reflete"}
  - {id: nota-0034, uso: "protocolo de teste de campo para preencher o Power Profile"}
  - {id: nota-0124, uso: "gráfico de resistência à fadiga — potência fresco vs. após acúmulo de kJ; degradação % do sprint"}
  - {id: nota-0104, uso: "interpretar breakpoints e 'vales' da MMP Curve sem confundi-los com erro de dado"}
  - {id: nota-0105, uso: "além de ~1h, usar NP em vez da potência média bruta ao comparar recordes/picos"}
  - {id: nota-0097, uso: "priorizar limitante relevante ao objetivo do atleta, não a fraqueza numérica absoluta"}
  - {id: nota-0038, uso: "revisar o Power Profile a cada 4-6 semanas"}
  - {id: nota-0035, uso: "fenótipo do ciclista pelo formato do Power Profile (all-rounder/sprinter/CRI-escalador/perseguidor)"}
confianca_herdada: 0.7
# = mínimo das confianças acima (nota-0082, nota-0124 e nota-0105 empatam em 0.7).
# Ressalva adicional: nota-0082 tem status "revisar" no cânone (não "auto-aprovado") — a própria nota
# registra que depende de software (WKO4) para o cálculo individualizado de Pmax/FRC via ajuste de
# curva, e que a base não tem exemplo numérico completo do mapa. Tratar o Mapa Fenotípico com cautela
# extra além do número de confiança.
condicao_nao_calculavel: "sem pelo menos ~6 meses de histórico de potência (idealmente 1 ano) → MMP Curve não é confiável (nota-0053) — todos os cálculos derivados dela (PDC, Pmax, FRC, TTE, Stamina, Mapa Fenotípico) ficam Estimados na melhor hipótese, nunca Medidos. Um ponto da MMP só é válido se veio de um esforço genuinamente máximo naquela duração específica — não inferir o pico de 6min a partir de um esforço de 5min. Mapa Fenotípico (nota-0082): sem acesso a um ajuste de curva PDC individualizado (tipicamente feito por software como WKO4), reportar como Ausente ou Estimado de baixa confiança — o cânone não fornece a fórmula de ajuste completa, só a lógica conceitual das razões Pmax/FTP e FRC/Pmax. Power Profile (nota-0031): a tabela não tem correção por idade — não inferir isso ao aplicá-la a atletas mais velhos."
status: proposto
skills_relacionadas:
  - {id: skill-gerais-ftp-e-zonas, tipo: pre-requisito}
  - {id: skill-gerais-tss-sessao, tipo: pre-requisito}
  - {id: skill-gerais-qualidade-de-dado, tipo: pre-requisito}
log_de_teste: []
# populado após cada rodada de validação: {data, caso, resultado, veredito}
---

## O que faz

Constrói o perfil de potência de longo prazo do atleta: a MMP Curve (dado real dos melhores esforços por duração) e a PDC (modelo ajustado sobre ela), derivando Pmax, FRC, TTE e Stamina; o Power Profile clássico (Tabela 4.1, 4 durações-índice) e o fenótipo resultante (all-rounder/sprinter/CRI-escalador/perseguidor); o Mapa Fenotípico 2D (Pmax/FTP × FRC/Pmax, com cautela extra por ser uma nota "revisar" no cânone); e a curva de resistência à fadiga (queda de potência de pico fresco vs. após acúmulo de trabalho). Sempre expõe o dado real (MMP) ao lado do modelado (PDC), nunca só o modelo.

## Quando usar

- Ao construir ou atualizar o perfil de longo prazo do atleta (mensal, após acumular histórico suficiente).
- Ao identificar picos de potência de uma sessão de teste dedicada (5s/1min/5min, protocolo da nota-0034) para atualizar o Power Profile.
- Ao gerar recomendações de treino a partir de "pontos fracos" do perfil — sempre filtrando pela relevância ao objetivo do atleta, nunca pela fraqueza numérica isolada.
- Para provas longas (>3h), ao avaliar a resistência à fadiga do atleta comparando potência fresca vs. pós-acúmulo de kJ.

## Passo a passo

1. **Construir a MMP Curve**: melhor potência média real por duração, extraída do histórico (idealmente ≥6 meses). Interpretar mudanças de inclinação como candidatas a transições de sistema energético, e "vales"/inversões locais como artefato normal de dados reais esparsos — nunca como erro de medição (nota-0053, nota-0104).
2. **Ajustar a PDC** (curva de melhor ajuste sobre a MMP) — usar como modelo complementar, sempre expondo a MMP real ao lado (nota-0037, nota-0103).
3. **Derivar Pmax**: maior potência numa volta completa de pedal; aproximar pelo pico de 1s disponível se não houver PDC individualizada (nota-0077).
4. **Derivar FRC** (joules acima do FTP): `potência sustentável acima do FTP = FRC ÷ duração(s)`; potência total = FTP + esse valor (nota-0078).
5. **Derivar TTE**: duração que o atleta sustenta o próprio mFTP — reportar mesmo quando o mFTP for igual ao de outro momento/atleta, pois o TTE pode diferir bastante (nota-0080).
6. **Derivar Stamina**: % de resistência à fadiga sub-FTP prolongada, cauda da PDC além do mFTP; comparar contra a faixa típica de 75-85% (nota-0081).
7. **Mapa Fenotípico** (com cautela extra — nota-0082, status "revisar"): se houver PDC individualizada confiável, calcular Pmax/FTP (eixo X) e FRC/Pmax (eixo Y); sem isso, não calcular — reportar Ausente.
8. **Power Profile**: localizar os melhores W/kg do atleta nas 4 durações-índice (5s→potência neuromuscular, 1min→capacidade anaeróbia, 5min→VO2máx, FTP→limiar de lactato) contra a Tabela 4.1, por sexo (nota-0031, nota-0032). Usar picos de sessão de teste dedicada quando disponível (nota-0034), não picos incidentais.
9. **Classificar o fenótipo** pelo formato resultante: horizontal→all-rounder; descendente (1min>5min)→sprinter; ascendente→CRI/escalador; "V invertido"→perseguidor (checar se os valores realmente refletem esforço máximo antes de concluir "V invertido") (nota-0035).
10. **Resistência à fadiga**: se houver dado de prova longa (>3h) ou sessão com acúmulo de kJ registrado, comparar potência de pico (5min/20min) fresca vs. após o acúmulo; para sprints, calcular a degradação percentual ao longo de ~35s (nota-0124).
11. **Ao comparar recordes/picos >1h**, usar NP em vez de potência média bruta (nota-0105).
12. **Filtrar recomendações pela relevância ao objetivo**: uma "fraqueza" num sistema energético irrelevante à prova-alvo do atleta (ex.: potência neuromuscular fraca num triatleta de estrada) tem prioridade de recomendação baixa, mesmo com confiança estatística alta (nota-0097).
13. **Sinalizar revisão periódica**: se passaram mais de 4-6 semanas desde a última atualização do Power Profile, sinalizar necessidade de retestar (nota-0038).
14. **Checar a condição de não-calculável** (ver frontmatter) antes de reportar qualquer número como Medido/Estimado.

## Output

```
{
  "mmp_disponivel": <bool>,
  "profundidade_historico_meses": <float>,
  "pmax_w": <float, null>,
  "frc_j": <float, null>,
  "tte_min": <float, null>,
  "stamina_pct": <float, null>,
  "mapa_fenotipico": {"pmax_ftp": <float, null>, "frc_pmax": <float, null>, "provenance_especifica": "Ausente" },
  "power_profile": {
    "5s_w_kg": <float, null>, "1min_w_kg": <float, null>, "5min_w_kg": <float, null>, "ftp_w_kg": <float, null>,
    "categoria_por_duracao": {"5s": "<texto>", "1min": "<texto>", "5min": "<texto>", "ftp": "<texto>"}
  },
  "fenotipo": "all-rounder" | "sprinter" | "cri-escalador" | "perseguidor" | null,
  "resistencia_fadiga": {"queda_5min_pct": <float, null>, "queda_20min_pct": <float, null>, "degradacao_sprint_35s_pct": <float, null>},
  "alertas": [
    "historico_insuficiente_menos_6_meses" | "revisar_power_profile_4_6_semanas" | "fraqueza_irrelevante_ao_objetivo" | "mapa_fenotipico_baixa_confianca" | null
  ],
  "provenance": "Medido" | "Estimado" | "Ausente",
  "motivo_provenance": "<texto, obrigatório se Estimado ou Ausente>",
  "notas_citadas": ["nota-0053", "nota-0103", "nota-0037", "nota-0077", "nota-0078", "nota-0080", "nota-0081", "nota-0082", "nota-0031", "nota-0032", "nota-0034", "nota-0124", "nota-0104", "nota-0105", "nota-0097", "nota-0038", "nota-0035"]
}
```
