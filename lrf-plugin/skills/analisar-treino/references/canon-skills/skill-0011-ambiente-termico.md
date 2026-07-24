---
id: skill-gerais-ambiente-termico
numero: skill-0011
titulo: "Ambiente térmico — aclimatização ao calor, imunossupressão pós-esforço, desidratação, degradação de desempenho e hipotermia"
dominio: fisiologia
tipo_skill: calculadora+detector
notas_usadas:
  - {id: nota-0254, uso: "protocolo de aclimatização ao calor — maior ganho na 1ª semana, plena em ~10 dias, dissipa em 2-3 semanas sem exposição"}
  - {id: nota-0242, uso: "janela de imunossupressão de 3-72h após esforço excepcional, risco elevado de infecção respiratória por 1-2 semanas; nota com status 'revisar' no cânone, cautela extra"}
  - {id: nota-0256, uso: "cada litro de desidratação por suor eleva FC em ~8bpm e reduz débito cardíaco em ~1L/min — mecanismo de decoupling em sessões longas/quentes"}
  - {id: nota-0258, uso: "desempenho de endurance piora progressivamente (não abrupto) conforme temperatura sobe de 10°C a 25°C, mais acentuado em atletas menos condicionados"}
  - {id: nota-0261, uso: "continuum de doença por calor — cãibras, exaustão, golpe de calor — sinais de alerta e limiares de temperatura retal"}
  - {id: nota-0270, uso: "roupa molhada perde ~90% do isolamento térmico — risco de hipotermia em frio+chuva/suor, especialmente em descidas"}
confianca_herdada: 0.55
# = mínimo das confianças acima (nota-0258 é a mais fraca, 0.55).
# Ressalva adicional: nota-0242 tem status "revisar" no cânone (não "auto-aprovado") — tratar o alerta
# de imunossupressão com cautela extra além do número de confiança já baixo (0.65).
condicao_nao_calculavel: "sem dado de temperatura na atividade (Strava nem sempre captura) → nenhum detector desta skill é aplicável, reportar Ausente. Sem histórico de atividades anteriores do atleta → aclimatização ao calor não é inferível. NENHUM destes detectores substitui avaliação clínica real — são alertas educativos baseados em proxy indireto (temperatura + duração + FC do Strava), nunca um diagnóstico; a skill nunca deve afirmar que o atleta 'está' em exaustão por calor ou golpe de calor, só sinalizar risco crescente no continuum."
status: proposto
skills_relacionadas:
  - {id: skill-gerais-fadiga-carga-avancada, tipo: complementar}
log_de_teste: []
# populado após cada rodada de validação: {data, caso, resultado, veredito}
---

## O que faz

Infere o estado de aclimatização ao calor do atleta a partir do histórico recente de exposição, e aplica cinco detectores de segurança/interpretação térmica: janela de imunossupressão após esforço excepcional, efeito da desidratação sobre FC/débito cardíaco (mecanismo de decoupling em sessões quentes), degradação progressiva de desempenho com o calor, continuum de doença por calor (cãibras→exaustão→golpe de calor), e risco de hipotermia por roupa molhada.

## Quando usar

- Ao interpretar FC elevada ou decoupling numa sessão longa em dia quente — antes de concluir "perda de fitness" ou "sessão difícil".
- Ao gerar feedback logo após uma sessão de TSS/esforço muito acima do padrão do atleta (prova longa, evento excepcional).
- Ao comparar desempenho do mesmo atleta entre sessões em temperaturas diferentes.
- Ao identificar combinação de frio + chuva/suor + queda de intensidade (ex.: início de descida) que eleve risco de hipotermia.

## Passo a passo

1. **Inferir aclimatização ao calor:** se o atleta teve exposição repetida a temperatura elevada ao longo de ~10-14 dias recentes, considerar total/parcialmente aclimatizado (maior ganho na 1ª semana, plena em ~10 dias). Se sem exposição a calor nas últimas 2-3 semanas, tratar como não aclimatizado e reforçar avisos de hidratação/ritmo conservador na próxima sessão quente (nota-0254).
2. **Sinalizar janela de imunossupressão** se uma sessão teve TSS/esforço-relativo muito acima do padrão do atleta (evento isolado excepcional, não acúmulo crônico): alertar que as próximas 3-72h são de maior vulnerabilidade a infecção respiratória, com efeito residual até 1-2 semanas — tratar com cautela extra por ser nota "revisar" (nota-0242).
3. **Ao detectar decoupling elevado** numa sessão longa (>1,5-2h) e quente: cruzar com temperatura e duração para estimar se desidratação é causa provável. Regra grosseira de ordem de grandeza: subida de FC de ~8bpm ao longo da sessão é compatível com ~1L de perda de suor, com queda associada de ~1L/min no débito cardíaco (nota-0256).
4. **Ao comparar desempenho do mesmo atleta entre sessões**, esperar degradação progressiva e gradual (não um corte abrupto) conforme a temperatura sobe de ~10°C a 25°C+ — mais acentuada em atletas menos condicionados. Não sinalizar isso como "underperformando" (nota-0258).
5. **Emitir alerta educativo de risco por calor** quando houver combinação de temperatura alta + tempo-movimento prolongado + FC elevada sustentada, especialmente em atleta não aclimatado (passo 1): recomendar reduzir intensidade e buscar hidratação/sombra diante de qualquer mal-estar — nunca afirmar diagnóstico específico (cãibra/exaustão/golpe de calor), só sinalizar risco crescente no continuum (nota-0261).
6. **Emitir alerta de risco de hipotermia** quando houver temperatura baixa-moderada (<15°C) + esforço intenso prolongado (sudorese esperada) + queda de potência/velocidade (ex.: início de descida ou parada): recomendar troca de camada ou vestimenta impermeável/corta-vento antes de descidas longas, mesmo sem temperatura extrema (nota-0270).
7. **Checar a condição de não-calculável** (ver frontmatter) antes de reportar qualquer alerta.

## Output

```
{
  "aclimatizacao_calor": "total" | "parcial" | "nao_aclimatizado" | "nao_inferivel",
  "alertas": [
    "janela_imunossupressao_3_72h" | "decoupling_por_desidratacao_provavel" | "degradacao_esperada_pelo_calor_nao_e_underperforming" | "risco_continuum_calor" | "risco_hipotermia_roupa_molhada" | null
  ],
  "detalhe_decoupling_desidratacao": "<texto, ex.: 'subida de ~9bpm ao longo de 2h a 28°C — compatível com ~1L de desidratação'>",
  "provenance": "Estimado" | "Ausente",
  "motivo_provenance": "<texto, obrigatório — estes são sempre proxies indiretos, nunca medição direta>",
  "notas_citadas": ["nota-0254", "nota-0242", "nota-0256", "nota-0258", "nota-0261", "nota-0270"]
}
```
