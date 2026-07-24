---
id: skill-classificacao-semana-recuperacao
numero: skill-0015
titulo: "Semana de recuperação — verificar teto de carga real e avaliar timing de adiantar/adiar"
dominio: recuperacao-e-fadiga
tipo_skill: detector
notas_usadas:
  - {id: nota-0096, uso: "teto prático de ~62%FTP e <2h/dia como critério para saber se a semana de fato reduziu a carga"}
  - {id: nota-0098, uso: "flexibilidade de timing — adiantar se muito fatigado, adiar se não, mas nunca pular a semana de recuperação"}
confianca_herdada: 0.7
# = mínimo das confianças acima (nota-0096, 0.7; nota-0098 é 0.75). Ambas auto-aprovado, sem ressalva de status adicional.
condicao_nao_calculavel: "sem declaração explícita de qual semana era planejada como recuperação (calendário/plano do atleta) → não é possível avaliar timing (adiantada/adiada/pulada), reportar Ausente para esse eixo. O teto de ~62%FTP depende de FTP válido (pré-requisito: skill-gerais-ftp-e-zonas) — sem isso, o eixo de verificação de intensidade também fica Ausente. Mesmo com os dois calculáveis, uma semana com volume/intensidade reduzidos mas sem que o atleta a tenha declarado como 'semana de recuperação' deve ser reportada como candidata, não confirmada."
status: proposto
skills_relacionadas:
  - {id: skill-gerais-ftp-e-zonas, tipo: pre-requisito}
  - {id: skill-gerais-pmc, tipo: pre-requisito}
log_de_teste: []
# populado após cada rodada de validação: {data, caso, resultado, veredito}
---

## O que faz

Verifica se uma semana declarada (ou candidata, por queda abrupta de volume/TSS) como "semana de recuperação" de fato cumpriu os critérios de redução real de carga do cânone — teto de ~62% do FTP e menos de 2h/dia, com dias de descanso completo — e avalia se o momento em que ela ocorreu (adiantada, adiada, ou pulada) foi apropriado segundo o critério qualitativo dos autores.

## Quando usar

- Ao avaliar se uma semana que o atleta chama de "recuperação" realmente reduziu a carga o suficiente para cumprir a função pretendida.
- Ao interpretar um TSB muito negativo prolongado (via `skill-gerais-pmc`) e checar se uma semana de recuperação programada foi adiada/pulada em vez de simplesmente atrasada de forma válida.
- Ao construir o calendário/periodização e decidir se uma semana de recuperação deve ser adiantada por sinais de fadiga excessiva.

## Passo a passo

1. **Identificar a semana candidata**: usar a declaração explícita do plano do atleta, ou inferir por queda abrupta de volume/TSS semanal frente à média recente.
2. **Verificar teto de intensidade**: nenhuma pedalada da semana deveria ultrapassar ~62% do FTP com frequência — calcular o percentual do FTP de cada sessão da semana e sinalizar se isso é violado com frequência (nota-0096).
3. **Verificar teto de duração diária**: cada dia deveria ficar abaixo de 2h, com a maioria das sessões em torno de 1h15, e incluir pelo menos um dia de descanso completo (nota-0096).
4. **Concluir se a semana cumpriu a função**: se a potência ultrapassar o teto com frequência OU a duração diária exceder 2h repetidamente, sinalizar que a semana provavelmente **não** cumpriu a função de recuperação pretendida, mesmo que tenha sido rotulada como tal.
5. **Avaliar o timing**: se o atleta terminou a semana anterior claramente fatigado (cruzar com TSB muito negativo e prolongado de `skill-gerais-pmc`/`skill-gerais-fadiga-carga-avancada`), adiantar a semana de recuperação é válido. Se chegou à semana programada sem fadiga real (TSB normal), adiar por mais alguns dias também é válido — não tratar automaticamente fadiga leve normal como sinal de que a recuperação é urgente (nota-0098).
6. **Restrição inegociável**: se a semana de recuperação foi adiada, ela **deve** ocorrer na semana seguinte à originalmente programada. Sinalizar alerta explícito se uma semana de recuperação programada nunca chegou a ocorrer (foi efetivamente pulada) (nota-0098).
7. **Checar a condição de não-calculável** (ver frontmatter) antes de reportar qualquer veredito.

## Output

```
{
  "semana_avaliada": "<data de início-fim>",
  "declarada_pelo_atleta": <bool>,
  "cumpriu_teto_intensidade_62pct_ftp": <bool, null>,
  "cumpriu_teto_duracao_2h_dia": <bool, null>,
  "teve_dia_de_descanso_completo": <bool, null>,
  "veredito_funcao_recuperacao": "cumpriu" | "nao_cumpriu" | "nao_calculavel",
  "timing": {
    "foi_adiantada": <bool, null>,
    "foi_adiada": <bool, null>,
    "foi_pulada": <bool, null>,
    "justificativa_por_tsb": "<texto ou null>"
  },
  "alertas": [
    "semana_recuperacao_nao_reduziu_carga_de_fato" | "semana_recuperacao_adiada_sem_ocorrer_na_seguinte" | "semana_recuperacao_pulada" | null
  ],
  "provenance": "Medido" | "Estimado" | "Ausente",
  "motivo_provenance": "<texto, obrigatório se Estimado ou Ausente>",
  "notas_citadas": ["nota-0096", "nota-0098"]
}
```
