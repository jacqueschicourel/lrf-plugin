---
id: skill-classificacao-contexto-atividade
numero: skill-0016
titulo: "Contexto de atividade/modalidade — exceções que mudam a leitura padrão de potência (prova de pelotão, subida/descida, ciclocross, MTB ultra)"
dominio: tipos-de-treino
tipo_skill: classificador+detector
notas_usadas:
  - {id: nota-0046, uso: "padrão de potência da 'jogada vencedora' em 3 fases — ataque, sustentação em limiar, sprint final"}
  - {id: nota-0113, uso: "assimetria subida/descida não é erro de pacing — potência acima do FTP em subida é esperada e compensada na descida"}
  - {id: nota-0130, uso: "ciclocross: potência média 20-40W abaixo do FTP é normal, não indica esforço baixo; matches partem de base já alta"}
  - {id: nota-0137, uso: "Efeito Allen em MTB ultraresistência — inverte a lógica de pacing conservador de contrarrelógio de estrada"}
  - {id: nota-0049, uso: "% de tempo pedalando <85% em prova de pelotão é o padrão dos vencedores — acima disso pode indicar posicionamento subótimo"}
confianca_herdada: 0.7
# = mínimo das confianças acima (nota-0113, nota-0130 e nota-0137 empatam em 0.7; nota-0046 e nota-0049 são 0.75).
# Todas as notas citadas têm status "auto-aprovado" — nenhuma ressalva de status adicional além do número de confiança.
condicao_nao_calculavel: "sem classificação do tipo/modalidade da atividade (prova de pelotão, contrarrelógio, ciclocross, MTB ultraresistência, treino solo) → a maioria dos detectores aqui depende de saber o contexto correto antes de decidir se uma exceção se aplica; sem essa classificação, reportar Ausente e usar a leitura padrão (sem aplicar nenhuma das exceções desta skill). Sem perfil de elevação disponível, a assimetria subida/descida (nota-0113) não pode ser confirmada como efeito natural do terreno — não presumir a exceção sem o dado."
status: proposto
skills_relacionadas:
  - {id: skill-classificacao-tipo-de-sessao, tipo: complementar}
  - {id: skill-subida-pacing, tipo: complementar}
log_de_teste: []
# populado após cada rodada de validação: {data, caso, resultado, veredito}
---

## O que faz

Reconhece contextos e modalidades específicas de atividade que alteram a leitura padrão de um arquivo de potência: o padrão de 3 fases da "jogada vencedora" em prova de pelotão, a assimetria natural subida/descida (não é erro de pacing), a potência mais baixa esperada em ciclocross, a inversão da lógica de pacing conservador em MTB de ultraresistência (Efeito Allen), e o sinal de posicionamento subótimo pelo percentual de tempo pedalando numa prova de pelotão.

## Quando usar

- Ao analisar o arquivo de potência de uma prova (não um treino estruturado solo), antes de aplicar heurísticas de pacing genéricas.
- Ao identificar que a atividade tem perfil de elevação significativo, ou está classificada como ciclocross, ou como MTB de ultraresistência.
- Antes de sinalizar automaticamente "erro de pacing" a partir de picos de potência isolados.

## Passo a passo

1. **Prova de pelotão com destaque/fuga**: procurar o padrão de 3 fases da jogada vencedora — ataque inicial (~200% do FTP em média por ~30s, pico ~300% do FTP) → esforço elevado contínuo estabilizando perto de 100-110% do FTP → arremate final (pico curto de potência/velocidade no sprint). Usar para nomear e explicar taticamente o momento decisivo de uma prova (nota-0046).
2. **Percurso com desnível significativo**: não sinalizar automaticamente picos de potência acima do FTP em trechos de subida como erro de pacing — isso é esperado (mais resistência para empurrar contra) e naturalmente compensado pela queda de potência na descida seguinte (cai a ~55% do FTP mesmo com esforço máximo, por limitação de marcha). Focar a análise de pacing no IF/NP/VI da prova inteira, não em picos isolados correlacionados ao perfil de elevação (nota-0113).
3. **Atividade classificada como ciclocross**: não aplicar o limiar padrão "potência média baixa = esforço fraco" — médias 20-40W abaixo do FTP são normais (tempo sem pedalar em descidas técnicas/carregando a bike, perda de tração em barro/areia). Ao contar "matches" (picos acima do FTP), lembrar que a base de esforço já está perto do FTP na maior parte da prova — mesmo picos de amplitude menor podem ser esforços significativos (nota-0130).
4. **Atividade classificada como MTB de ultraresistência** (ou prova offroad longa sem pelotão/draft real após os primeiros ~15min): inverter a lógica de pacing conservador desenvolvida para contrarrelógio de estrada — não sinalizar início forte como erro. O Efeito Allen mostra que acelerar antes de um trecho rápido do percurso cria um gap de distância que os concorrentes atrás dificilmente conseguem fechar, mesmo que o gap de tempo permaneça constante (nota-0137).
5. **Prova de pelotão (mass-start)**: calcular o percentual de tempo pedalando (`tempo-movimento / tempo-decorrido`). Se ultrapassar 85%, sinalizar como hipótese de posicionamento subótimo no pelotão (gastando energia à toa em vez de aproveitar a roda de outros) a investigar no feedback pós-prova — este sinal é irrelevante para treino solo/estruturado, onde o objetivo já é outro (nota-0049).
6. **Checar a condição de não-calculável** (ver frontmatter) antes de aplicar qualquer uma das exceções acima.

## Output

```
{
  "modalidade_contexto": "prova_peloton" | "contrarrelogio" | "ciclocross" | "mtb_ultraresistencia" | "treino_solo" | "indeterminado",
  "jogada_vencedora_detectada": {"fase_ataque": <bool, null>, "fase_sustentacao": <bool, null>, "fase_sprint_final": <bool, null>},
  "assimetria_subida_descida_explicada_por_terreno": <bool, null>,
  "pct_tempo_pedalando": <float, null>,
  "alertas": [
    "picos_subida_nao_sao_erro_pacing" | "potencia_media_baixa_normal_ciclocross" | "efeito_allen_inicio_forte_valido" | "posicionamento_subotimo_pct_pedalando_acima_85" | null
  ],
  "provenance": "Medido" | "Estimado" | "Ausente",
  "motivo_provenance": "<texto, obrigatório se Estimado ou Ausente>",
  "notas_citadas": ["nota-0046", "nota-0113", "nota-0130", "nota-0137", "nota-0049"]
}
```
