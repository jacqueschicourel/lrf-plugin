---
id: skill-gerais-multiesporte-corrida
numero: skill-0007
titulo: "Equivalência de carga bike-corrida (rTSS/FTp) e separação em 3 PMCs para multiesporte"
dominio: metricas-de-potencia
tipo_skill: detector
notas_usadas:
  - {id: nota-0114, uso: "rTSS/FTp — equivalência de escala: ~45min de corrida no FTp = 100 pontos, vs. 60min de bike no FTP = 100 pontos"}
  - {id: nota-0115, uso: "construir 3 PMCs separados (bike, corrida, combinado) para atletas multiesportivos"}
confianca_herdada: 0.7
# = mínimo das confianças acima (nota-0115 é a mais fraca, 0.7).
condicao_nao_calculavel: "a nota-0114 define a EQUIVALÊNCIA DE ESCALA do rTSS (45min corrida FTp ≈ 100 pontos, mesmo que 60min bike FTP ≈ 100 pontos), mas NÃO fornece a fórmula matemática completa de rTSS por segundo (que exigiria NGP — Normalized Graded Pace — cuja fórmula não foi extraída no cânone destas 4 fontes). Por isso: esta skill NÃO calcula rTSS numérico de uma corrida — reporta apenas a equivalência de escala como contexto, e sinaliza a lacuna explicitamente. Sem essa fórmula, o PMC 'combinado' (bike+corrida) fica Ausente/incompleto — só o PMC de bike (via skill-gerais-tss-sessao) é calculável com o cânone atual. Isso é uma lacuna real do cânone, não um erro desta skill."
status: proposto
skills_relacionadas:
  - {id: skill-gerais-tss-sessao, tipo: pre-requisito}
  - {id: skill-gerais-pmc, tipo: pre-requisito}
log_de_teste: []
# populado após cada rodada de validação: {data, caso, resultado, veredito}
---

## O que faz

Para atletas multiesportivos (ex.: triatletas) com dados de bike e corrida no Strava: (a) sinaliza a equivalência de escala de carga entre os dois esportes (corrida gera mais estresse por hora que bike, por isso 100 pontos de rTSS correspondem a só ~45min de corrida no FTp, não 60min); (b) orienta a construção de PMC separado por esporte (bike, corrida, combinado) em vez de um único PMC que mistura os dois sem essa correção de escala.

**Não calcula rTSS numérico** — essa é uma lacuna explícita do cânone (ver `condicao_nao_calculavel`), registrada aqui em vez de inventar uma fórmula que as 4 fontes não fornecem.

## Quando usar

- Quando o atleta tiver atividades de corrida além de bike no histórico, e for necessário decidir como tratar a carga de treino combinada.
- Para evitar o erro de aplicar a fórmula de TSS de bike (nota-0062) diretamente ao tempo de corrida, que subestimaria a carga real da corrida (por não contar o estresse musculoesquelético adicional do impacto).

## Passo a passo

1. **Identificar atividades de corrida** no histórico do atleta, separadas das de bike.
2. **Para as atividades de bike:** usar `skill-gerais-tss-sessao` normalmente (TSS via NP/IF/FTP).
3. **Para as atividades de corrida:** sinalizar que a carga não pode ser somada diretamente ao TSS de bike sem conversão — reportar a equivalência de escala (nota-0114) como contexto qualitativo (corrida no FTp gera mais estresse por hora que bike no FTP), mas não produzir um número de rTSS (lacuna do cânone).
4. **Orientar a separação em 3 PMCs** (nota-0115): bike isolado (calculável via `skill-gerais-pmc` sobre o TSS de bike), corrida isolada (não calculável numericamente com o cânone atual — ver passo 3), e combinado (não calculável enquanto rTSS não tiver fórmula).
5. **Checar a condição de não-calculável** antes de reportar qualquer PMC como completo.

## Output

```
{
  "tem_atividades_corrida": <bool>,
  "pmc_bike": "calculável via skill-gerais-pmc" | null,
  "pmc_corrida": "não calculável — fórmula de rTSS ausente do cânone",
  "pmc_combinado": "não calculável — depende de rTSS",
  "equivalencia_escala_contexto": "~45min de corrida no FTp ≈ 60min de bike no FTP, em termos de carga de treino (nota-0114) — corrida gera mais estresse por hora devido ao impacto",
  "provenance": "Ausente",
  "motivo_provenance": "fórmula de rTSS não extraída do cânone (depende de Normalized Graded Pace, não documentado nas 4 fontes) — lacuna explícita, não erro de cálculo",
  "notas_citadas": ["nota-0114", "nota-0115"]
}
```
