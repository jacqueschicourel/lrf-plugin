---
name: analisar-treino-lrf
description: Analisa uma sessão de ciclismo do Strava do atleta com o rigor de um treinador humano, aplicando um cânone fixo de 22 skills (fisiologia do exercício, treino com potência, VO2máx, periodização) e expondo a origem de cada número (Medido, Calculado, Estimado, Manual ou Ausente). Usar sempre que o atleta pedir para analisar, revisar, ou dar feedback sobre um treino, uma pedalada, uma prova, ou uma sessão de bike — inclusive frases como "como foi meu treino de ontem", "analisa essa prova", "o que você acha desse treino de FTP".
version: 0.1.0
---

# Analisar treino (LRF)

## O que esta skill é

Este é o motor de análise do LRF: um cânone fixo de 22 skills (`references/canon-skills/skill-0001-*.md` a `skill-0022-*.md`), cada uma derivada de um livro de referência de ciência do treinamento (fisiologia do exercício, treino com medidor de potência, VO2máx, periodização), aplicado à sessão real do atleta puxada do Strava. Cada skill descreve seu próprio "Passo a passo", sua "Condição de não-calculável" e seu formato de "Output" — leia cada arquivo antes de aplicá-lo, não resuma de memória.

A regra central do projeto, que esta skill nunca pode violar: **todo número reportado ao atleta carrega uma proveniência** — Medido (sensor do dispositivo), Calculado (fórmula do cânone sobre dado medido), Estimado (aproximação com incerteza explícita), Manual (configurado pela plataforma, não pelo cânone) ou Ausente (não calculável com o dado disponível). Nunca reportar um número sem dizer de onde ele veio. Nunca inventar um dado que a sessão não sustenta.

## Passo a passo do processo completo

### 1. Identificar a sessão

Use as ferramentas do conector Strava (`mcp__strava__*` — nomes exatos dependem de como o conector está registrado nesta sessão) para localizar a atividade pedida: por data, por `activity_id`, ou "a última atividade" se o atleta não especificar. Confirme com o atleta se houver ambiguidade (mais de uma atividade de bike na mesma data).

### 2. Puxar o dado bruto completo — nunca um resumo de terceiro

Puxe os dados brutos da atividade diretamente das ferramentas do conector: perfil do atleta (idade, peso, FTP cadastrado, zonas), a atividade em si (distância, elevação, tempo decorrido/movimento, velocidades, FC média/máx/mín, cadência média/máx, calorias, temperatura, `has_device_watts`, `average_watts`), e o stream de potência/FC quando disponível.

Regra de dado bruto multi-fonte: se no futuro houver mais de uma fonte disponível para o mesmo atleta (Strava, TrainingPeaks, arquivo `.fit` direto, etc.), todas entram como dado bruto em pé de igualdade — o cálculo é sempre feito por esta skill a partir do bruto, nunca herdado de um resumo/cálculo já pronto de outra plataforma. Se o Strava já expõe um "TSS estimado" ou "FTP estimado" prontos, trate-os como um dado de entrada possível para o fallback (ver passo 4), nunca como o resultado final sem recalcular pela fórmula do cânone.

Rode `scripts/calculo_sessao.py::checar_completude()` sobre o dado bruto coletado contra a lista de campos esperados (`CAMPOS_ESPERADOS_SESSAO_BASE`). Registre explicitamente o que faltou — um campo ausente no dispositivo (ex.: sem termômetro) não é erro, mas precisa aparecer como "ausente no dispositivo", nunca ser simplesmente omitido.

### 3. Buscar FTP e zonas vigentes na data da sessão — nunca cache

O FTP e as zonas de FC/potência usados devem ser os vigentes **na data da atividade analisada**, não o FTP atual do perfil se o atleta re-testou depois. Sempre re-consultar via `skill-gerais-ftp-e-zonas` (skill-0004) e `skill-gerais-zonas-fc` (skill-0005) para esta sessão especificamente — nunca reaproveitar um FTP/zona já calculado numa sessão anterior da mesma conversa, mesmo que pareça o mesmo valor.

### 4. Aplicar as 22 skills, uma por uma, em isolamento

Abra cada um dos 22 arquivos em `references/canon-skills/` e aplique seu "Passo a passo" a esta sessão. Regras de isolamento e anti-viés, obrigatórias:

- Esta sessão é classificada isoladamente — nunca ajuste o resultado de uma skill porque "essa é a interpretação mais provável dado o histórico do atleta" sem que o próprio "Passo a passo" da skill peça isso explicitamente.
- As skills em `references/canon-skills/` são a fonte de verdade fixa. Nunca ajuste um limiar, fórmula ou threshold de uma skill com base no que "parece certo" para os dados observados deste atleta específico — os thresholds vêm só do cânone (das notas citadas em cada skill), nunca da base de treino do atleta sendo analisado.
- Se uma skill não é calculável para esta sessão (ver `condicao_nao_calculavel` no frontmatter de cada `skill-XXXX-*.md`), reporte `provenance: "Ausente"` com o motivo exato — nunca pule a skill silenciosamente, nunca a substitua por uma suposição.
- Duas skills têm um fallback operacional explícito (não são regras do cânone, são decisões do projeto, documentadas no próprio frontmatter da skill): `skill-0002-tss-sessao.md` (`fallback_potencia_estimada`, quando não há stream real de potência) e `skill-0005-zonas-fc.md` (`fallback_zona_manual`, quando não há idade cadastrada mas a plataforma tem zona configurada). Use-os exatamente como descritos, sempre com a proveniência correta (Estimado / Manual — nunca promovidos a Calculado/Medido).
- Para todo cálculo que se enquadre nas categorias já cobertas por `scripts/calculo_sessao.py` (zonas de potência de Coggan, IF/TSS via fallback de potência estimada, tempo-em-zona de FC, faixa de carboidrato, checklist de completude), **use exatamente essas funções** — nunca recalcule com uma expressão inline diferente. Isso garante que a mesma fórmula produza o mesmo resultado em qualquer sessão analisada por este plugin, para qualquer atleta.

### 5. Montar a tabela-resumo de auditoria (as 22 skills, sempre todas)

Monte uma tabela com uma linha para cada uma das 22 skills — inclusive as que resultaram em Ausente ou não-aplicável — com as colunas: Nº, Skill, Proveniência, Nota(s) do cânone citada(s), Resultado em 1 linha. Esta tabela é o que permite a um treinador humano auditar o que foi feito em menos de um minuto, sem precisar ler o processo inteiro. Nunca omitir uma skill da tabela por ela não ter produzido número.

### 6. Redigir o feedback ao atleta

Estilo direto, sem jargão desnecessário, como uma mensagem de um treinador que conhece o atleta — nunca um relatório técnico despejado. Cite apenas o que foi de fato calculado/medido nesta sessão; nunca insira uma afirmação motivacional genérica que não vem de um número real desta análise.

### 7. Auditoria de rastreabilidade — obrigatória, sempre, sem exceção

Antes de considerar a análise concluída, monte uma tabela frase-por-frase do feedback redigido no passo 6, apontando cada frase para a fonte exata no arquivo de análise (qual skill, qual campo do output, qual nota do cânone). Qualquer frase do feedback que não tenha uma fonte rastreável nesta tabela **não pode ir para o atleta** — remova-a ou reformule-a até que tenha lastro. Este passo roda sempre, não só quando algo "parece" suspeito.

### 8. Entregar o arquivo

Gere o arquivo de análise completo (frontmatter com `checklist_completude`, dado bruto, aplicação das 22 skills, tabela-resumo de auditoria, feedback redigido, tabela de auditoria de rastreabilidade) e entregue como um arquivo diretamente no chat (formato `.md`), para o atleta baixar. Não é necessário nenhum conector de armazenamento externo — a entrega é sempre o arquivo nativo do chat.

## Erros a não repetir

- Não classifique uma sessão pela potência-média geral do arquivo — a estrutura real (tempo-em-zona/blocos) pode mascarar o tipo verdadeiro da sessão (ver `skill-0014`).
- Não trate um "TSS"/"FTP estimado" pronto da plataforma como resultado final — sempre recalcule pela função determinística com a proveniência correta.
- Não pule a auditoria de rastreabilidade mesmo quando o feedback parecer óbvio ou curto.
