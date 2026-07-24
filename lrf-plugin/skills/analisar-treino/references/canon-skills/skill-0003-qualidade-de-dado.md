---
id: skill-gerais-qualidade-de-dado
numero: skill-0003
titulo: "Qualidade e viés de dado de potência — equipamento, calibração, picos espúrios e convenção de médias"
dominio: metricas-de-potencia
tipo_skill: detector
notas_usadas:
  - {id: nota-0009, uso: "coroas não circulares inflam potência registrada em ~10-20W"}
  - {id: nota-0010, uso: "medidor de cubo lê ~5-10W a menos que manivela/pedal"}
  - {id: nota-0011, uso: "medidor unilateral pode desviar ~5% do valor real por assimetria entre pernas"}
  - {id: nota-0014, uso: "recorde destoante sem contexto de prova/teste → suspeitar de erro de calibração/zeragem (offset de toda a atividade)"}
  - {id: nota-0015, uso: "pico isolado de amostra única muito acima do padrão → interpolar pela média dos vizinhos antes de usar o pico de 5s"}
  - {id: nota-0016, uso: "convenção de cálculo: potência-média inclui zeros, cadência-média exclui zeros"}
confianca_herdada: 0.8
# = mínimo das confianças acima (nota-0011 e nota-0015 empatam em 0.8; as demais são 0.85).
condicao_nao_calculavel: "sem metadado de equipamento no perfil do atleta (tipo/posição do medidor, uso de coroas ovais) → não é possível sinalizar viés de equipamento (nota-0009/0010/0011), mas os outros três detectores (calibração/nota-0014, picos espúrios/nota-0015, convenção de médias/nota-0016) continuam aplicáveis normalmente com o que estiver disponível — reportar parcialmente, nunca bloquear a skill inteira por falta desse metadado."
status: proposto
skills_relacionadas:
  - {id: skill-gerais-tss-sessao, tipo: consumida-por}
  - {id: skill-gerais-forca-e-pedalada, tipo: consumida-por}
  - {id: skill-gerais-perfil-de-potencia-longo-prazo, tipo: consumida-por}
log_de_teste: []
# populado após cada rodada de validação: {data, caso, resultado, veredito}
---

## O que faz

Roda um conjunto de checagens de qualidade e viés sobre a série bruta de potência de uma atividade **antes** que qualquer outra skill (TSS, perfil de potência, força/pedalada) confie nela: vieses sistemáticos de equipamento (coroas ovais, medidor de cubo, medidor unilateral), suspeita de erro de calibração/zeragem, picos espúrios de amostra única, e a convenção correta de cálculo de médias (potência inclui zeros, cadência exclui).

Não corrige o FTP nem o perfil do atleta automaticamente — só sinaliza, para que a skill consumidora (ou o feedback ao atleta) leve a ressalva em conta.

## Quando usar

- Como primeiro passo de qualquer skill que consome `potência-série-temporal` — não roda isolada por iniciativa própria, precede `skill-gerais-tss-sessao`, `skill-gerais-forca-e-pedalada`, `skill-gerais-perfil-de-potencia-longo-prazo` e qualquer outra que calcule NP/médias/picos.
- Ao investigar por que um "recorde" de potência (pico, média ou NP) destoa muito do histórico do atleta sem contexto de prova/teste.
- Ao comparar dados de potência entre períodos em que o atleta pode ter trocado de equipamento (medidor, coroas).

## Passo a passo

1. **Checar metadado de equipamento** (perfil/config do atleta): tipo e posição do medidor de potência (manivela/pedal vs. cubo), se é bilateral ou unilateral, se usa coroas não circulares. Se cubo → sinalizar viés de ~-5 a -10W (nota-0010). Se coroas ovais → sinalizar viés de ~+10 a +20W (nota-0009). Se unilateral → sinalizar possível desvio de ~5% do valor registrado, em qualquer direção (nota-0011).
2. **Checar suspeita de erro de calibração/zeragem.** Comparar o pico/média/NP da atividade contra o histórico do atleta — um valor muito destoante sem contexto de prova/teste é sinal de possível offset de zeragem esquecida, afetando a atividade inteira (nota-0014).
3. **Varrer a série por picos espúrios de amostra única** — um ponto isolado muito acima do padrão do restante do arquivo (ex.: vizinhos ~250W, um ponto em ~1876W) deve ser interpolado pela média dos pontos vizinhos antes de qualquer cálculo de pico de 5s ou de NP (nota-0015). Isso é diferente do erro de calibração (passo 2): aqui é 1 amostra, não a atividade inteira.
4. **Aplicar a convenção de cálculo de médias:** potência-média inclui os períodos em 0W (parado/roda livre); cadência-média exclui os períodos de cadência zero (nota-0016). Reportar as duas médias já corrigidas pela série (pós-interpolação do passo 3).
5. **Checar a condição de não-calculável** (ver frontmatter) — metadado de equipamento ausente não bloqueia os passos 2-4.
6. **Consolidar todas as sinalizações** num único output, para a skill consumidora decidir como tratar cada uma (nenhuma correção automática de FTP/perfil).

## Output

```
{
  "activity_id": "<string>",
  "vies_equipamento": [
    {"tipo": "coroas_ovais" | "medidor_cubo" | "medidor_unilateral", "vies_estimado_w": "<faixa, ex.: '+10 a +20'>"}
  ],
  "suspeita_erro_calibracao": <bool>,
  "motivo_suspeita_calibracao": "<texto, se true>",
  "picos_espurios_interpolados": [
    {"indice_ou_timestamp": "<...>", "valor_original_w": <float>, "valor_interpolado_w": <float>}
  ],
  "potencia_media_w": <float, convenção inclui zeros>,
  "cadencia_media_rpm": <float, convenção exclui zeros>,
  "provenance": "Medido" | "Estimado" | "Ausente",
  "motivo_provenance": "<texto, obrigatório se Estimado ou Ausente>",
  "notas_citadas": ["nota-0009", "nota-0010", "nota-0011", "nota-0014", "nota-0015", "nota-0016"]
}
```
