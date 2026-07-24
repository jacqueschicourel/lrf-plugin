---
id: skill-gerais-nutricao-sessao
numero: skill-0006
titulo: "Faixa de ingestão de carboidrato sugerida por duração da sessão"
dominio: nutricao-e-energia
tipo_skill: calculadora
notas_usadas:
  - {id: nota-0201, uso: "tabela de referência g/h de carboidrato por faixa de duração do exercício"}
confianca_herdada: 0.6
# única nota usada; confiança igual à da nota-0201 — a mais baixa de toda a base até agora citada
# numa skill, porque é uma recomendação geral da nutrição esportiva, não uma fórmula fisiológica
# individualizada (a própria nota diz "recomendações devem ser individualizadas").
condicao_nao_calculavel: "sem tempo-movimento nem tempo-decorrido da sessão → não é possível sugerir faixa, reportar Ausente. Esta skill NUNCA verifica ingestão real — o Strava não registra nutrição — só sugere a faixa esperada para a duração observada; nunca reportar 'provenance: Medido', mesmo com duração exata disponível, porque o que está sendo estimado é uma recomendação, não uma medição."
status: proposto
skills_relacionadas: []
log_de_teste: []
# populado após cada rodada de validação: {data, caso, resultado, veredito}
---

## O que faz

Sugere a faixa de ingestão de carboidrato (g/h) recomendada para uma sessão, a partir da duração observada (tempo-movimento ou tempo-decorrido) — não verifica ingestão real, que o Strava não registra.

## Quando usar

- Ao dar feedback educativo pós-sessão para sessões longas (>1h), como contexto nutricional complementar ao feedback de carga/potência.
- Ao planejar nutrição para uma sessão futura de duração conhecida (ex.: prova-alvo).

## Passo a passo

1. **Obter a duração da sessão** (tempo-movimento preferencialmente; tempo-decorrido como alternativa se tempo-movimento não disponível).
2. **Classificar na faixa da tabela (nota-0201):**
   - até 60min → geralmente desnecessário (exceto bochecho de carboidrato em provas muito intensas perto de 60min, que pode ajudar via efeito central/sensorial sem ingestão real).
   - 1-2h → 30-60 g/h.
   - 2-3h → 60-90 g/h.
   - acima de 3h → 90-120 g/h (só para atletas com intestino treinado a tolerar essa quantidade).
3. **Reportar a faixa como sugestão**, nunca como verificação — deixar explícito que o Strava não captura ingestão real.
4. **Checar a condição de não-calculável** antes de reportar.

## Output

```
{
  "duracao_sessao_min": <float>,
  "faixa_carboidrato_g_h": "<texto, ex.: '60-90'>",
  "observacao": "<texto, ex.: 'sessão >3h — faixa superior só recomendada com intestino treinado'>",
  "provenance": "Estimado" | "Ausente",
  "motivo_provenance": "sugestão baseada em duração, não verificação de ingestão real (Strava não registra nutrição)",
  "notas_citadas": ["nota-0201"]
}
```
