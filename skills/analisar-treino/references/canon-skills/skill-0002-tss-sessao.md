---
id: skill-gerais-tss-sessao
numero: skill-0002
titulo: "TSS por sessão — cálculo completo (NP → VI → IF → TSS) a partir de potência bruta"
dominio: metricas-de-potencia
tipo_skill: calculadora
notas_usadas:
  - {id: nota-0059, uso: "algoritmo de NP — média móvel de 30s, ^4, média, raiz 4ª, a partir da série bruta de potência"}
  - {id: nota-0060, uso: "VI = NP ÷ potência-média — sinal secundário de variabilidade do esforço, comparado à Tabela 7.1 por tipo de prova"}
  - {id: nota-0061, uso: "IF = NP ÷ FTP; e detector de IF>1,05 em prova de ~1h como sinal de FTP desatualizado"}
  - {id: nota-0062, uso: "fórmula final: TSS = [(s × NP × IF) ÷ (FTP × 3600)] × 100"}
  - {id: nota-0012, uso: "taxa de gravação reduzida ('smart recording') distorce NP — sinalizar antes de reportar"}
  - {id: nota-0132, uso: "recortar trechos sem pedalada antes do cálculo; evitar NP como métrica principal em esforços muito curtos (pista)"}
confianca_herdada: 0.65
# = mínimo das confianças acima (nota-0132 é a mais fraca, 0.65 — é uma nota de contexto de pista,
# mas como o passo 2 do "Passo a passo" usa a lógica dela para TODA atividade, ela entra no cálculo
# do mínimo mesmo fora do caso de pista. Regra do projeto: uma skill nunca é mais confiável que sua
# citação mais fraca.)
condicao_nao_calculavel: "sem stream de potência do dispositivo (has_device_watts=false) → NP real (nota-0059) não é calculável — ver fallback_potencia_estimada abaixo antes de reportar Ausente. Menos de 30s de dados válidos de potência → NP não é interpretável (nota-0059 exige janela ≥30s); reportar Ausente, nunca um NP calculado sobre janela menor. Taxa de gravação reduzida/'smart recording' detectada → reportar NP/VI como Estimado, nunca Medido, com a ressalva da nota-0012. Atividade de pista ou com trechos longos sem pedalada → é obrigatório recortar esses trechos antes de calcular (nota-0132); se não for possível identificar/recortar os trechos parados, reportar TSS como Estimado (provavelmente inflado). Sem FTP válido do atleta na data da atividade (Calculadora FTP #8, fora do escopo desta skill) → IF e TSS ficam Ausentes; NP e VI ainda podem ser Medidos (não dependem de FTP)."
fallback_potencia_estimada: "Decisão operacional do projeto (não é regra do cânone, não citar como nota-XXXX; decidida 2026-07-19 após teste real que mostrou que o Strava não expõe stream de potência quando has_device_watts=false, só um `average_watts` resumo por atividade): quando não houver stream de potência do dispositivo mas a plataforma de origem (Strava/etc.) tiver uma potência média calculada por ela (ex.: `average_watts` do Strava mesmo com `has_device_watts: false`) — usar `NP ≈ potência_média_da_plataforma` como aproximação, SEMPRE com `provenance: Estimado` (nunca Calculado, nunca Medido) e um alerta explícito de que o VI/variabilidade real não foi capturado (essa aproximação é estruturalmente cega a picos e vales — uma sessão com surtos curtos de potência alta e uma sessão constante na mesma média ficam indistinguíveis). Se o FTP usado também for Estimado (ex. `EstimatedFtpFromPower` do Strava), IF/TSS resultantes carregam dupla incerteza — sinalizar as duas fontes de estimativa separadamente no `motivo_provenance`, não só uma. Prioridade: stream real do dispositivo (Calculado/Medido) > `average_watts` da plataforma (Estimado) > Ausente. Sempre que possível, cruzar o TSS estimado contra o perfil de zona de FC da mesma sessão (`skill-gerais-zonas-fc`) — se a intensidade por FC (ex. maioria do tempo em Z1-Z2) não bater com o IF implícito do TSS estimado, reportar essa divergência ao atleta, não escolher um dos dois sinais silenciosamente."
status: proposto
skills_relacionadas:
  - {id: skill-gerais-ftp-e-zonas, tipo: pre-requisito}
  - {id: skill-gerais-qualidade-de-dado, tipo: pre-requisito}
  - {id: skill-gerais-pmc, tipo: consumida-por}
  - {id: skill-classificacao-tipo-de-sessao, tipo: consumida-por}
log_de_teste: []
# populado após cada rodada de validação: {data, caso, resultado, veredito}
---

## O que faz

Calcula a cadeia completa de métricas de intensidade/carga de uma única sessão a partir da série bruta de potência: Potência Normalizada (NP) → Variability Index (VI, sinal secundário) → Intensity Factor (IF) → TSS (Training Stress Score). É a skill de base que `skill-gerais-pmc` (CTL/ATL/TSB) e qualquer skill de classificação de sessão/semana precisam consumir — nenhuma delas deve recalcular TSS por conta própria.

## Quando usar

- Sempre que houver uma atividade nova do Strava com stream de potência do dispositivo, antes de qualquer leitura de carga diária/semanal.
- Como pré-requisito obrigatório de `skill-gerais-pmc` — a série diária de TSS que alimenta o EWMA de CTL/ATL deve vir desta skill, não de um cálculo ad-hoc.
- Ao investigar se o FTP cadastrado do atleta está desatualizado (IF alto em esforço de ~1h).

## Passo a passo

1. **Confirmar dado de entrada.** Verificar `has_device_watts` da atividade. Se `false`, checar o fallback (`fallback_potencia_estimada` no frontmatter) antes de reportar Ausente — se a plataforma tiver uma potência média calculada, seguir com `NP ≈ potência_média`, provenance Estimado, e os passos 5-8 abaixo normalmente (pulando o passo 4, já que não há série pra calcular NP real).
2. **Checar qualidade da gravação.** Se a atividade foi gravada em "smart recording" ou com taxa reduzida (menos de ~1 registro/segundo), sinalizar essa limitação (nota-0012) — o resultado final não poderá ser reportado como Medido.
3. **Recortar trechos sem pedalada.** Especialmente relevante em pista/critérium/treino intermitente: remover da série os trechos em que o atleta não estava pedalando ativamente (potência ~0 prolongado) antes de qualquer cálculo (nota-0132). Guardar o tempo efetivamente pedalado (s) separado do tempo decorrido total.
4. **Calcular NP** sobre a série já recortada: (a) média móvel de 30s da potência ao longo de todo o trecho; (b) elevar cada valor da média móvel à 4ª potência; (c) calcular a média de todos esses valores; (d) extrair a raiz quarta (nota-0059). Exige ≥30s de dados válidos — abaixo disso, não calcular, reportar Ausente.
5. **Calcular VI = NP ÷ potência-média** do mesmo trecho recortado (nota-0060). Comparar à Tabela 7.1 (faixas por tipo de prova) como sinal secundário — não bloqueia o cálculo de TSS, é informativo.
6. **Calcular IF = NP ÷ FTP** (nota-0061), usando o FTP vigente do atleta **na data da atividade**, não necessariamente o FTP atual do perfil.
7. **Calcular TSS = [(s × NP × IF) ÷ (FTP × 3.600)] × 100**, onde s é o tempo efetivamente pedalado em segundos (nota-0062).
8. **Aplicar o detector de FTP desatualizado:** se IF > 1,05 numa prova de aproximadamente 1h de duração, sinalizar suspeita de FTP desatualizado (nota-0061) — não ajustar o FTP automaticamente, apenas sinalizar.
9. **Checar a condição de não-calculável** (ver frontmatter) antes de reportar qualquer número como Medido/Estimado.

## Output

```
{
  "activity_id": "<string>",
  "data": "AAAA-MM-DD",
  "duracao_pedalada_s": <int>,
  "np_w": <float>,
  "potencia_media_w": <float>,
  "vi": <float>,
  "vi_faixa_esperada": "<texto, ex.: 'prova de estrada com subidas: 1,20-1,35' | null se tipo de prova desconhecido>",
  "ftp_usado_w": <float>,
  "if": <float>,
  "tss": <float>,
  "alertas": [
    "ftp_provavelmente_desatualizado (IF>1,05 em ~1h)" | "gravacao_taxa_reduzida" | "trechos_sem_pedalada_nao_recortados" | "np_aproximado_por_media_sem_stream_real" | "divergencia_com_zona_fc" | null
  ],
  "provenance": "Calculado" | "Estimado" | "Ausente",
  "motivo_provenance": "<texto, obrigatório se Estimado ou Ausente — se Estimado por fallback de potência média, citar as duas fontes de incerteza (potência estimada + FTP estimado, se aplicável)>",
  "notas_citadas": ["nota-0059", "nota-0060", "nota-0061", "nota-0062", ...]
}
```

O `tss` deste output é a entrada diária que `skill-gerais-pmc` espera (somar todas as sessões do mesmo dia antes de rodar o EWMA).
