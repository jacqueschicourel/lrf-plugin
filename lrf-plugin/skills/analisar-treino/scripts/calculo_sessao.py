"""
calculo_sessao.py — funções determinísticas de cálculo para análise de sessão (projeto LRF).

Por quê este arquivo existe (2026-07-20, v1):
Até aqui, cada sessão analisada (pilotos #1 e #2) teve seu TSS-fallback, IF, zonas de potência
e tempo-em-zona-FC recalculados "à mão", num script Python ad-hoc criado na hora, por sessão.
Em 2 sessões isso é seguro porque cada uma é revisada com cuidado individual. Em ~183 sessões,
o risco é inconsistência silenciosa entre sessões: usar tempo-timer numa e tempo-decorrido em
outra sem perceber, arredondar diferente, ou aplicar uma variante levemente diferente da fórmula
sem querer. A auditoria de rastreabilidade (ver analises/README.md) confere se uma frase do
feedback bate com o arquivo — mas não confere se a fórmula foi aplicada de forma idêntica em
todas as sessões do lote. Só uma função única, fixa, usada em todas, garante isso.

Regra: ao processar o lote de ~183 sessões, TODO cálculo destas categorias passa por aqui.
Nenhuma sessão recalcula estes números com um script/expressão inline diferente. Se uma fórmula
aqui precisar mudar, ela muda neste arquivo (com justificativa registrada), nunca só numa sessão.

Cada função cita a nota do cânone (nota-XXXX) ou a decisão operacional (fallback_*) em que se
baseia — ver os skill.md correspondentes em skills/gerais/.
"""

from __future__ import annotations


# ---------------------------------------------------------------------------
# skill-gerais-ftp-e-zonas (skill-0004) — nota-0022, Tabela 3.1 (7 níveis Coggan)
# ---------------------------------------------------------------------------
# Percentuais de FTP (tetos superiores de cada nível) confirmados empiricamente no piloto #2
# (2026-07-20): com FTP=200W, os tetos abaixo reproduzem exatamente as `power_zones` que o
# próprio conector do Strava devolveu para a mesma atividade (110/150/180/210/240/300) — cada
# zona começa em teto_anterior+1, não num percentual próprio independente (é assim que o Strava
# monta: min=111 pra zona 2, não round(0,56×200)=112). Cross-check registrado em
# analise-2025-10-23-16230267501.md, seção "Cadeia de decisão", passo 5.
_TETOS_PCT_COGGAN = [
    ("nivel_1_recuperacao_ativa", 0.55),
    ("nivel_2_endurance", 0.75),
    ("nivel_3_tempo", 0.90),
    ("nivel_4_limiar", 1.05),
    ("nivel_5_vo2max", 1.20),
    ("nivel_6_capacidade_anaerobia", 1.50),
    ("nivel_7_potencia_neuromuscular", None),  # sem teto (nota-0022)
]


def zonas_potencia_coggan(ftp_w: float) -> dict:
    """Zonas de potência em watts pelos 7 níveis clássicos de Coggan (nota-0022).

    Retorna dict {nivel: (limite_inferior_w, limite_superior_w_ou_None)}. Cada zona começa em
    (teto da zona anterior + 1) — não num percentual próprio recalculado do zero — para bater
    com a convenção observada no Strava (ver comentário acima). Teto de cada zona = round(FTP × pct).
    """
    if not ftp_w or ftp_w <= 0:
        raise ValueError("FTP inválido — zonas de potência não calculáveis sem FTP > 0")
    zonas = {}
    lo = 0
    for nivel, pct in _TETOS_PCT_COGGAN:
        if pct is None:
            zonas[nivel] = (lo, None)
            break
        hi = round(ftp_w * pct)
        zonas[nivel] = (lo, hi)
        lo = hi + 1
    return zonas


# ---------------------------------------------------------------------------
# skill-gerais-tss-sessao (skill-0002) — nota-0061 (IF), nota-0062 (TSS)
# fallback_potencia_estimada (decisão operacional, não é nota do cânone) quando
# has_device_watts=false: NP ≈ potência média da plataforma.
# ---------------------------------------------------------------------------
def if_tss_fallback_estimado(avg_watts_plataforma: float, ftp_w: float, duracao_s: float) -> dict:
    """IF e TSS aproximados quando não há stream real de potência (nota-0059 não aplicável).

    NP é aproximado pela potência média que a plataforma de origem calcula (ex.: `average_watts`
    do Strava mesmo com has_device_watts=false) — fallback_potencia_estimada, skill-gerais-tss-sessao.
    `duracao_s` é o tempo efetivamente pedalado; convenção do projeto (fixada aqui, ver docstring
    do módulo): usar `tempo timer/movimento`, não `tempo decorrido`, salvo nota em contrário
    registrada explicitamente na sessão (ex.: pista/trechos parados não recortáveis).

    SEMPRE reportar como provenance "Estimado" (nunca Calculado/Medido) e sinalizar o alerta
    `np_aproximado_por_media_sem_stream_real` — perde o sinal de VI (variabilidade do esforço).
    Se o FTP usado também for Estimado, sinalizar a dupla incerteza separadamente.
    """
    if not ftp_w or ftp_w <= 0:
        raise ValueError("FTP inválido — IF/TSS não calculáveis sem FTP > 0")
    if avg_watts_plataforma is None or avg_watts_plataforma <= 0:
        raise ValueError("potência média da plataforma inválida — fallback não aplicável")
    if not duracao_s or duracao_s <= 0:
        raise ValueError("duração inválida — TSS não calculável")

    IF = avg_watts_plataforma / ftp_w
    TSS = (duracao_s * avg_watts_plataforma * IF) / (ftp_w * 3600) * 100
    return {
        "np_aproximado_w": round(avg_watts_plataforma, 3),
        "if": round(IF, 4),
        "tss": round(TSS, 2),
        "duracao_usada_s": duracao_s,
        "alertas": ["np_aproximado_por_media_sem_stream_real"],
    }


# ---------------------------------------------------------------------------
# skill-gerais-zonas-fc (skill-0005) — tempo-em-zona a partir de um stream Medido de FC
# contra limites Calculado (Gellish/Karvonen) ou Manual (fallback_zona_manual).
# ---------------------------------------------------------------------------
def tempo_em_zona_fc(hr_samples: list, zonas_bpm: list) -> dict:
    """Conta amostras de FC (assumidas ~1 amostra/segundo) em cada zona.

    `zonas_bpm`: lista ordenada de tuplas (limite_inferior, limite_superior_inclusive),
    ex.: [(0,128),(129,143),(144,149),(150,159),(160,999)]. A última zona deve ter um teto
    alto o suficiente para cobrir qualquer FC máxima real (não usar None/inf — mantém a função
    determinística e testável).

    Retorna contagem em segundos e percentual por zona, na mesma ordem de `zonas_bpm`.
    Amostras None são ignoradas (não contam nem no total).
    """
    n_zonas = len(zonas_bpm)
    contagem = [0] * n_zonas
    for h in hr_samples:
        if h is None:
            continue
        for i, (lo, hi) in enumerate(zonas_bpm):
            if lo <= h <= hi:
                contagem[i] += 1
                break
    total = sum(contagem)
    percentual = [round(100 * c / total, 1) if total else None for c in contagem]
    return {"contagem_s": contagem, "total_s": total, "percentual": percentual}


# ---------------------------------------------------------------------------
# skill-gerais-nutricao-sessao (skill-0006) — nota-0201, tabela g/h por duração
# ---------------------------------------------------------------------------
def faixa_carboidrato_g_h(duracao_min: float) -> str:
    """Faixa de carboidrato sugerida (g/h) pela duração da sessão — nunca verificação real."""
    if duracao_min is None or duracao_min <= 0:
        raise ValueError("duração inválida")
    h = duracao_min / 60
    if h <= 1:
        return "desnecessário (exceto bochecho de carboidrato em provas muito intensas perto de 60min)"
    if h <= 2:
        return "30-60"
    if h <= 3:
        return "60-90"
    return "90-120 (só para atletas com intestino treinado a tolerar essa quantidade)"


# ---------------------------------------------------------------------------
# Checklist de completude de dado bruto — não é uma skill do cânone, é controle de qualidade
# do próprio processo de extração, pedido explicitamente para a escala de 183 sessões.
# ---------------------------------------------------------------------------
CAMPOS_ESPERADOS_SESSAO_BASE = [
    "distancia_m",
    "ganho_elevacao_m",
    "perda_elevacao_m",
    "tempo_decorrido_s",
    "tempo_timer_s",
    "velocidade_media_ms",
    "velocidade_max_ms",
    "fc_media",
    "fc_max",
    "fc_min",
    "cadencia_media",
    "cadencia_max",
    "calorias",
    "temp_media",
    "temp_max",
]


def checar_completude(dados: dict, campos_esperados: list = None) -> dict:
    """Confere quais campos esperados vieram nulos/ausentes no dict de dado bruto extraído.

    Não decide sozinho se um campo ausente é "problema" — um dispositivo sem termômetro vai
    legitimamente não ter temp_media, por exemplo. Serve só para tornar visível, campo a campo,
    o que faltou, para que a análise registre explicitamente "ausente no dispositivo" em vez de
    simplesmente não mencionar o campo (o gap exato que causou 2 das 4 falhas do piloto #1).
    """
    campos = campos_esperados or CAMPOS_ESPERADOS_SESSAO_BASE
    faltando = [c for c in campos if dados.get(c) is None]
    presentes = [c for c in campos if dados.get(c) is not None]
    return {"campos_esperados": campos, "faltando": faltando, "presentes": presentes}


if __name__ == "__main__":
    # Auto-teste rápido com os números já publicados em analise-2025-10-23-16230267501.md,
    # pra confirmar que esta função reproduz exatamente o que foi calculado à mão no piloto #2.
    r = if_tss_fallback_estimado(avg_watts_plataforma=150.376, ftp_w=200, duracao_s=5063)
    assert r["if"] == 0.7519, r
    assert abs(r["tss"] - 79.51) < 0.01, r

    z = zonas_potencia_coggan(200)
    assert z["nivel_1_recuperacao_ativa"] == (0, 110), z
    assert z["nivel_2_endurance"] == (111, 150), z
    assert z["nivel_3_tempo"] == (151, 180), z
    assert z["nivel_4_limiar"] == (181, 210), z
    assert z["nivel_5_vo2max"] == (211, 240), z
    assert z["nivel_6_capacidade_anaerobia"] == (241, 300), z
    assert z["nivel_7_potencia_neuromuscular"] == (301, None), z

    zc = tempo_em_zona_fc(
        hr_samples=[110] * 360 + [135] * 3036 + [146] * 758 + [155] * 884 + [160] * 5,
        zonas_bpm=[(0, 128), (129, 143), (144, 149), (150, 159), (160, 999)],
    )
    assert zc["contagem_s"] == [360, 3036, 758, 884, 5], zc

    print("auto-teste ok:", r, z, zc["percentual"])
