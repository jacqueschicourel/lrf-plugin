---
id: skill-gerais-testes-deliberados
numero: skill-0008
titulo: "Testes deliberados de laboratório de campo — Astrand submáximo (VO2máx) e Wingate (potência/capacidade anaeróbia)"
dominio: avaliacao-e-testes
tipo_skill: calculadora
notas_usadas:
  - {id: nota-0218, uso: "protocolo Astrand submáximo: FC-alvo por Karvonen simplificado, 6min carga constante, fórmulas de VO2máx por sexo"}
  - {id: nota-0235, uso: "protocolo Wingate: 30s all-out, fórmulas de Potência Pico, Potência Pico Relativa, Fadiga Anaeróbia, Trabalho Anaeróbio, tabela de percentis"}
confianca_herdada: 0.55
# = mínimo das confianças acima (nota-0218 é a mais fraca, 0.55; a própria nota registra que o fator
# de correção por idade não pôde ser extraído em texto do PDF-fonte, só como imagem).
condicao_nao_calculavel: "escopo restrito por definição: NUNCA aplicar a uma sessão arbitrária do Strava — só reconhecer quando o atleta CONFIRMA ter executado deliberadamente um dos dois protocolos (não inferir silenciosamente pelo padrão de potência, risco de falso positivo alto). Astrand: o fator de correção de VO2máx por idade citado na fonte não foi extraído em texto (aparece só como tabela/imagem no PDF) — reportar o VO2máx SEM correção etária como Estimado, nunca aplicar uma correção inventada, e sinalizar essa lacuna explicitamente em todo output. Wingate: Potência Pico deve vir da média dos primeiros 5s do esforço, não do pico instantâneo de 1s — se só houver pico instantâneo disponível, reportar como Estimado com essa ressalva."
status: proposto
skills_relacionadas: []
log_de_teste: []
# populado após cada rodada de validação: {data, caso, resultado, veredito}
---

## O que faz

Reconhece quando uma atividade corresponde a um dos dois protocolos de teste deliberado do cânone — Astrand submáximo (estima VO2máx sem esforço máximo) ou Wingate (mede potência e capacidade anaeróbia em esforço máximo de 30s) — e aplica as fórmulas correspondentes. Diferente de todas as outras skills `gerais/`, esta **não roda sobre sessões arbitrárias**: exige confirmação de que o atleta executou o protocolo de propósito.

## Quando usar

- Quando o atleta confirma (input próprio, não inferência automática) ter feito deliberadamente um teste de Astrand (carga constante buscando FC-alvo por 6min) ou um teste de Wingate (30s all-out com resistência fixa por kg de peso corporal).
- Nunca para classificar retroativamente uma sessão comum como se fosse um desses testes.

## Passo a passo

### Astrand (nota-0218)
1. Confirmar que o atleta executou deliberadamente o protocolo.
2. Calcular FC-alvo: `FCmáx (220−idade) − FCrepouso` (fórmula simplificada de Karvonen usada especificamente por esta nota — não confundir com a versão de zona de treino da `skill-gerais-zonas-fc`, que usa FCmáx completa, não a diferença).
3. Confirmar que a sessão tem ~6min em carga constante com FC estabilizando próxima do alvo nos últimos minutos.
4. Converter carga: `kg-m/min = watts × 6,12`.
5. Aplicar a fórmula por sexo (FC = FC estável do platô, em bpm):
   - Mulheres: `VO2máx (L/min) = (0,00193×carga + 0,326) / (0,769×FC − 56,1) × 100`
   - Homens: `VO2máx (L/min) = (0,00212×carga + 0,299) / (0,769×FC − 48,5) × 100`
6. **Não aplicar fator de correção por idade** — não está disponível em texto no cânone (lacuna registrada). Reportar o valor do passo 5 como Estimado, com a ressalva explícita de que falta a correção etária.
7. Para VO2máx relativo: `mL/kg/min = (VO2máx L/min ÷ peso corporal kg) × 1000`.

### Wingate (nota-0235)
1. Confirmar que o atleta executou deliberadamente o protocolo (resistência fixa ~0,075-0,12 kg/kg de peso corporal, 30s all-out).
2. **Potência Pico (PP)**: maior potência média num intervalo de 5s dentro dos 30s (idealmente o primeiro).
3. **Potência Pico Relativa (RPP)**: `PP ÷ massa corporal (kg)`.
4. **Fadiga Anaeróbia (AF)**: `(PP mais alta − PP mais baixa) ÷ PP mais alta × 100`, comparando os intervalos de 5s ao longo dos 30s.
5. **Trabalho Anaeróbio (AW)**: soma do trabalho (J) ao longo dos 30s completos.
6. Comparar RPP e potência média (W/kg) contra a tabela de percentis (Tabela 11.2, por sexo).

## Output

```
{
  "protocolo": "astrand" | "wingate",
  "confirmado_pelo_atleta": <bool>,
  "astrand": {
    "vo2max_l_min_sem_correcao_idade": <float, null se não aplicável>,
    "vo2max_relativo_ml_kg_min": <float, null>,
    "correcao_idade_aplicada": false
  },
  "wingate": {
    "pp_w": <float, null>,
    "rpp_w_kg": <float, null>,
    "af_percentual": <float, null>,
    "aw_kj": <float, null>,
    "percentil_estimado": "<texto, ex.: 'entre P50 e P90 para potência média'>"
  },
  "alertas": ["correcao_idade_ausente_astrand" | "pico_instantaneo_usado_em_vez_de_media_5s" | null],
  "provenance": "Estimado" | "Ausente",
  "motivo_provenance": "<texto, obrigatório>",
  "notas_citadas": ["nota-0218", "nota-0235"]
}
```
