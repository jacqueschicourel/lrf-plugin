---
id: skill-gerais-zonas-fc
numero: skill-0005
titulo: "Zonas de treino por frequência cardíaca — FCmáx prevista e Percentage Method vs. Karvonen (HRR)"
dominio: avaliacao-e-testes
tipo_skill: calculadora
notas_usadas:
  - {id: nota-0245, uso: "três fórmulas de FCmáx prevista (clássica, Gellish, Tanaka) e dois métodos de zona de FC (Percentage Method, Karvonen/HRR)"}
confianca_herdada: 0.7
# única nota usada; confiança igual à da nota-0245 (McArdle documenta desvio-padrão significativo
# nas fórmulas de FCmáx prevista — ±5 a ±8 bpm mesmo na melhor delas).
condicao_nao_calculavel: "sem idade do atleta no perfil → nenhuma fórmula de FCmáx prevista é aplicável, zona de FC calculada (Calculado) fica indisponível — ver fallback de zona Manual abaixo antes de reportar Ausente. Sem FC de repouso no perfil → método de Karvonen (HRR) não é aplicável; usar Percentage Method, sinalizando que produz zonas mais conservadoras (limites mais baixos) que o Karvonen para a mesma pessoa. Nunca reportar zonas calculadas por métodos diferentes para o mesmo atleta em momentos diferentes sem sinalizar a mudança de método — isso invalida a comparação ao longo do tempo."
fallback_zona_manual: "Decisão operacional do projeto (não é regra do cânone, não citar como nota-XXXX): quando não houver idade do atleta (logo, sem Calculado possível) mas a plataforma de origem (Strava/Garmin/TrainingPeaks/etc.) tiver zonas de FC configuradas com fonte 'Manual' (ex.: campo `heart_rate_zone_source: Manual` do Strava) — usar essa zona como fallback, nunca como substituto do cálculo do cânone. Prioridade: (1) idade disponível → Calculado via Gellish/Karvonen, sempre prevalece; (2) sem idade, zona Manual disponível na plataforma → usar com provenance 'Manual', alertando que a origem dos limites (teste real vs. configuração arbitrária do atleta) é desconhecida; (3) nem um nem outro → Ausente. Uma zona Manual nunca deve ser silenciosamente tratada como Calculado nem como Medido — a tag Manual precisa aparecer em qualquer output/feedback que a use."
status: proposto
skills_relacionadas:
  - {id: skill-gerais-ftp-e-zonas, tipo: complementar}
log_de_teste: []
# populado após cada rodada de validação: {data, caso, resultado, veredito}
---

## O que faz

Calcula a FCmáx prevista do atleta por idade (priorizando a fórmula de menor viés) e a zona de treino sensível por FC (limite inferior/superior), por um dos dois métodos do cânone: Percentage Method (percentual direto da FCmáx) ou Karvonen/HRR (baseado na reserva de FC). Serve como sinal complementar às zonas de potência (`skill-gerais-ftp-e-zonas`) — útil quando não há medidor de potência confiável, ou como sinal cruzado.

## Quando usar

- Quando houver FC média/máx do Strava e idade do atleta (perfil), e for útil reportar a zona de FC de uma sessão.
- Quando não houver medidor de potência (ou ele for suspeito de viés — ver `skill-gerais-qualidade-de-dado`) e a FC for o sinal de intensidade disponível.
- Ao comparar zonas de FC do atleta ao longo do tempo — sempre conferir que o mesmo método está sendo usado de ponta a ponta.

## Passo a passo

1. **Obter idade do atleta** (perfil). Sem isso, nenhuma fórmula de FCmáx é aplicável.
2. **Calcular FCmáx prevista**, priorizando **Gellish (206,9 − 0,67×idade)** por ter o menor viés documentado (desvio-padrão ±5-8 bpm, independente de sexo/IMC/FC de repouso) — evitar a fórmula clássica (220−idade), que superestima em <40 anos e subestima em >40 anos. **Tanaka (208−0,7×idade)** é a fórmula-base usada pelo método de Karvonen no cânone (passo 4).
3. **Verificar se há FC de repouso no perfil.** Se sim → usar o método de Karvonen (passo 4). Se não → usar o Percentage Method (passo 5).
4. **Método de Karvonen (HRR), se FC de repouso disponível:** `LLTHR = (FCmáx − FCrepouso) × 0,50 + FCrepouso`; `ULTHR = (FCmáx − FCrepouso) × 0,85 + FCrepouso`.
5. **Percentage Method, se sem FC de repouso:** `LLTHR = FCmáx × 70%` (60% se idade >60 anos); `ULTHR = FCmáx × 90%` (80% se idade >60 anos). Sinalizar que este método produz zonas mais baixas/conservadoras que o Karvonen para a mesma pessoa.
6. **Registrar qual fórmula de FCmáx e qual método de zona foram usados** — nunca misturar métodos diferentes para o mesmo atleta ao comparar zonas ao longo do tempo (checar o método usado na última vez antes de recalcular).
7. **Antes de reportar Ausente**, checar se a plataforma de origem tem zona de FC configurada com fonte "Manual" (ver `fallback_zona_manual` no frontmatter). Se tiver, usar como fallback com `provenance: "Manual"` — nunca promovê-la a "Calculado" nem "Medido".
8. **Checar a condição de não-calculável** (ver frontmatter) antes de reportar qualquer número como Medido/Calculado/Manual.

## Output

```
{
  "fcmax_prevista_bpm": <float>,
  "formula_fcmax_usada": "gellish" | "tanaka" | "classica",
  "fc_repouso_bpm": <float, null se ausente>,
  "metodo_zona": "karvonen_hrr" | "percentage_method",
  "zona_treino": {
    "limite_inferior_bpm": <float>,
    "limite_superior_bpm": <float>
  },
  "alertas": [
    "metodo_mudou_desde_ultima_medicao" | "sem_fc_repouso_zona_conservadora" | "zona_manual_origem_desconhecida" | null
  ],
  "provenance": "Medido" | "Calculado" | "Manual" | "Ausente",
  "motivo_provenance": "<texto, obrigatório se Calculado, Manual ou Ausente — ex.: 'FCmáx é prevista por fórmula, não medida diretamente' (Calculado), ou 'zona configurada manualmente na plataforma, origem dos limites não verificada' (Manual)>",
  "notas_citadas": ["nota-0245"]
}
```

Nota de honestidade obrigatória: mesmo com todos os dados de entrada disponíveis, `provenance` aqui **nunca deve ser "Medido"** — FCmáx por fórmula de idade é sempre uma estimativa (desvio-padrão documentado de ±5-8 bpm mesmo na fórmula de menor viés), não uma medição direta do atleta. Quando vier do fallback de plataforma, `provenance` é **"Manual"**, uma categoria à parte — não é cálculo do cânone (não é "Calculado") e não é medição de sensor (não é "Medido"); é a decisão operacional do projeto de 2026-07-19, documentada em `fallback_zona_manual` acima, não uma nota do cânone.
