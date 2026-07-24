# LRF — Análise de Treino de Ciclismo

Plugin para Claude que analisa suas sessões de ciclismo do Strava com o mesmo rigor de um
treinador humano: um cânone fixo de 22 skills, derivadas de 4 livros de referência (fisiologia
do exercício, treino com medidor de potência, VO2máx, periodização), aplicado à sua sessão real
— sempre mostrando **de onde veio cada número**.

## O que faz

- Conecta com sua conta do Strava (via conector oficial da Strava).
- Aplica 22 skills de análise (FTP e zonas, TSS/CTL/ATL/TSB, qualidade de dado, força e
  pedalada, fadiga, ambiente térmico, pacing de prova, periodização, e mais) à sessão pedida.
- Classifica cada número calculado como **Medido, Calculado, Estimado, Manual ou Ausente** —
  nunca apresenta uma estimativa como se fosse medição direta.
- Gera um arquivo de análise completo, auditável por um treinador humano em menos de um minuto
  (tabela-resumo com as 22 skills) e com auditoria de rastreabilidade frase-por-frase do
  feedback dado ao atleta.
- Entrega o arquivo direto no chat — sem necessidade de configurar nenhum armazenamento externo.

## Como instalar

1. No Claude (Cowork, Claude Code, ou o chat do claude.ai/Desktop), adicione este repositório
   como fonte de plugin: `/plugin marketplace add jacqueschicourel/lrf-plugin`.
2. Instale o plugin: `/plugin install lrf@lrf-plugin`.
3. Conecte sua conta do Strava quando solicitado (OAuth, via o conector oficial da Strava).

## Como usar

- Comando: `/analisar-treino` (opcionalmente com uma data ou activity_id).
- Linguagem natural: "analisa meu treino de ontem", "o que você acha dessa prova de domingo".

## Estrutura do repositório

```
.claude-plugin/
  plugin.json         — manifesto do plugin
  marketplace.json     — catálogo (este repo funciona como seu próprio marketplace)
.mcp.json               — referência ao conector oficial da Strava
commands/
  analisar-treino.md    — comando explícito
skills/analisar-treino/
  SKILL.md              — skill orquestradora (o processo completo)
  references/canon-skills/ — as 22 skills do cânone (skill-0001 a skill-0022)
  scripts/calculo_sessao.py — funções determinísticas (zonas de potência, TSS/IF, tempo-em-zona-FC)
```

## Sobre o cânone

As 22 skills vêm de um projeto de base de conhecimento (LRF) que processou 4 livros de
referência de ciência do treinamento em ~291 notas atômicas, e delas derivou skills aplicáveis
a dados reais do Strava. Cada skill cita explicitamente as notas do cânone em que se baseia, sua
confiança herdada (nunca maior que a citação mais fraca), e sua condição de não-calculável.

## Licença

MIT.
