# ══════════════════════════════════════════════════════════════════════
# CAPA DE ATRIBUTOS DEL PRODUCTO — traduce reología de la harina a pan
# ══════════════════════════════════════════════════════════════════════
# Convierte los parámetros técnicos (W, P/L, C5, cenizas, absorción...) en
# atributos observables del PAN: volumen, miga, forma, color, vida útil y
# humedad normativa. Sistema de reglas ORDINALES (no predice valores exactos):
# comunica dirección y magnitud del efecto, que es la certeza que el modelo
# posee sin calibración experimental. Ver tesis, sección 3.3.4.
#
# Uso:
#   from atributos_producto import predecir_atributos, render_atributos
#   atr = predecir_atributos(mez, absorcion_pct, rend_horneado)
#   render_atributos(atr)   # dentro de Streamlit

# Niveles ordinales y su color/ícono
_NIVEL = {
    'optimo':   ("#16a34a", "🟢", "Óptimo"),
    'bueno':    ("#16a34a", "✅", "Adecuado"),
    'medio':    ("#d97706", "⚠️", "Aceptable con reservas"),
    'malo':     ("#ef4444", "🔴", "Deficiente"),
    'info':     ("#0369a1", "📊", "Informativo"),
}


def predecir_atributos(mez, humedad_pan_pct=None):
    """
    Traduce las propiedades de la mezcla a atributos del pan.
    mez: dict con W, PL, tenacidad, extension, absorcion, cenizas, fibra,
         lipidos, C5 (salida de calcular_mezcla).
    humedad_pan_pct: humedad estimada del pan (%); si se entrega, evalúa el
         cumplimiento del Art. 357 (≤ 36%).
    Devuelve lista de dicts: {atributo, nivel, valor_txt, causa}.
    """
    W   = mez.get('W', 0)
    PL  = mez.get('PL', 0)
    L   = mez.get('extension', 0)
    fib = mez.get('fibra', 0)
    cen = mez.get('cenizas', 0)
    C5  = mez.get('C5', 0)
    lip = mez.get('lipidos', 0)
    ab  = mez.get('absorcion', 0)
    out = []

    # 1. VOLUMEN — gobernado por W, penalizado por fibra
    if W < 180:
        niv, causa = 'malo', "W muy baja: la masa no retiene suficiente gas para desarrollar volumen."
    elif W < 200:
        niv, causa = 'medio', "W bajo el rango de referencia: volumen algo reducido."
    elif W <= 260:
        niv, causa = 'bueno', "W en rango: buena retención de gas y volumen esperable."
    else:
        niv, causa = 'medio', "W muy alta: masa demasiado fuerte, puede limitar la expansión."
    if fib > 3 and niv in ('bueno', 'optimo'):
        niv, causa = 'medio', causa + " La fibra elevada (>3%) interrumpe la red de gluten y reduce el volumen."
    out.append({'atributo': "Volumen específico", 'nivel': niv,
                'valor_txt': f"W = {W:.0f}", 'causa': causa})

    # 2. MIGA (alveolado) — gobernado por P/L
    if PL < 0.7:
        niv, causa = 'medio', "P/L bajo: masa muy extensible, alvéolos tienden a colapsar (miga irregular)."
    elif PL <= 1.6:
        niv, causa = 'bueno', "P/L equilibrado: alveolado abierto e irregular, típico de la marraqueta."
    else:
        niv, causa = 'medio', "P/L alto: masa tenaz, miga cerrada y compacta."
    out.append({'atributo': "Estructura de la miga", 'nivel': niv,
                'valor_txt': f"P/L = {PL:.2f}", 'causa': causa})

    # 3. FORMA / maquinabilidad — P/L en extremos
    if PL > 1.8:
        niv, causa = 'malo', "Masa muy tenaz: resiste el formado y tiende a desgarrarse en el corte del batido."
    elif PL < 0.6:
        niv, causa = 'malo', "Masa muy extensible: se aplana y no retiene la forma dividida de la marraqueta."
    elif 0.7 <= PL <= 1.6:
        niv, causa = 'bueno', "P/L apto para el formado y el corte característico del batido."
    else:
        niv, causa = 'medio', "P/L en el límite: formado posible pero con cuidado."
    out.append({'atributo': "Forma y maquinabilidad", 'nivel': niv,
                'valor_txt': f"P/L = {PL:.2f}", 'causa': causa})

    # 4. COLOR DE MIGA — cenizas + fibra (atributo de identidad, informativo)
    if cen <= 0.65:
        niv, causa = 'info', "Miga blanca a marfil, propia de la harina de trigo refinada."
    elif cen <= 1.5:
        niv, causa = 'info', "Miga marfil oscuro por el mayor contenido mineral de las harinas alternativas."
    else:
        niv, causa = 'info', "Miga notoriamente oscura: alto contenido mineral. Cambia la identidad visual del pan."
    out.append({'atributo': "Color de la miga", 'nivel': niv,
                'valor_txt': f"cenizas = {cen:.2f}%", 'causa': causa})

    # 5. VIDA ÚTIL — C5 (retrogradación), retardada por lípidos y absorción
    if C5 > 3.5:
        niv, causa = 'medio', "C5 alto: retrogradación acelerada, el pan se endurece más rápido."
    elif C5 >= 2.0:
        niv, causa = 'bueno', "C5 en rango: velocidad de endurecimiento normal."
    else:
        niv, causa = 'bueno', "C5 bajo: buena conservación de la frescura."
    if (lip > 3 or ab > 65) and niv == 'medio':
        niv = 'bueno'
        causa += " Los lípidos/absorción elevados retardan el endurecimiento."
    out.append({'atributo': "Vida útil", 'nivel': niv,
                'valor_txt': f"C5 = {C5:.2f}", 'causa': causa})

    # 6. HUMEDAD DEL PAN — único NORMATIVO (Art. 357: ≤ 36%)
    if humedad_pan_pct is not None:
        if humedad_pan_pct <= 36:
            niv, causa = 'bueno', "Cumple el máximo legal de humedad del pan (DS 977/96, Art. 357: ≤ 36%)."
        else:
            niv, causa = 'malo', "Supera el 36% de humedad: INCUMPLE el Art. 357 del RSA. Reducir agua o aumentar cocción."
        out.append({'atributo': "Humedad del pan (normativo)", 'nivel': niv,
                    'valor_txt': f"{humedad_pan_pct:.1f}%", 'causa': causa})

    return out


def indice_panificabilidad(mez):
    """
    Índice sintético [0-1] de aptitud para marraqueta, sobre los determinantes
    tecnológicos (W, P/L, absorción). Devuelve (valor, etiqueta_ordinal).
    """
    def score(val, lo, hi, k=1.0):
        # k>1 endurece la caída fuera de rango
        if val < lo:  return max(0.0, 1 - k * (lo - val) / lo)
        if val > hi:  return max(0.0, 1 - k * (val - hi) / hi)
        return 1.0
    sW  = score(mez.get('W', 0),   200, 260, k=2.0)  # W penaliza fuerte
    sPL = score(mez.get('PL', 0),  0.7, 1.6)
    sAb = score(mez.get('absorcion', 0), 58, 63)
    # Pesos: W domina la aptitud panadera
    ip = 0.5 * sW + 0.3 * sPL + 0.2 * sAb
    # Candado: sin W mínima no hay marraqueta posible, con independencia del resto
    W = mez.get('W', 0)
    if W < 190:
        ip = min(ip, 0.55)
    elif W < 200:
        ip = min(ip, 0.68)
    if   ip >= 0.90: etq = "Óptima"
    elif ip >= 0.70: etq = "Apta"
    elif ip >= 0.45: etq = "Marginal"
    else:            etq = "No apta"
    return ip, etq


def render_atributos(mez, humedad_pan_pct=None):
    """Renderiza el panel de atributos del producto en Streamlit."""
    import streamlit as st
    atr = predecir_atributos(mez, humedad_pan_pct)
    ip, etq = indice_panificabilidad(mez)

    # Índice de panificabilidad como encabezado
    col_ip = {"Óptima": "#16a34a", "Apta": "#16a34a",
              "Marginal": "#d97706", "No apta": "#ef4444"}.get(etq, "#64748b")
    st.markdown(
        f'<div style="background:linear-gradient(135deg,#1e3a5f,#2c5282);'
        f'border-radius:10px;padding:10px 14px;margin-bottom:8px;color:#fff;">'
        f'<span style="font-size:.72rem;opacity:.85;">ÍNDICE DE PANIFICABILIDAD</span><br>'
        f'<span style="font-size:1.15rem;font-weight:700;">{etq}</span> '
        f'<span style="font-size:.8rem;opacity:.8;">({ip*100:.0f}/100)</span></div>',
        unsafe_allow_html=True)

    for a in atr:
        color, icono, _ = _NIVEL[a['nivel']]
        st.markdown(
            f'<div style="border-left:3px solid {color};background:#f8fafc;'
            f'border-radius:7px;padding:7px 11px;margin-bottom:5px;">'
            f'<div style="font-size:.82rem;font-weight:600;color:#1e293b;">'
            f'{icono} {a["atributo"]} '
            f'<span style="font-weight:400;color:#64748b;font-size:.75rem;">· {a["valor_txt"]}</span></div>'
            f'<div style="font-size:.73rem;color:#475569;margin-top:2px;line-height:1.4;">{a["causa"]}</div>'
            f'</div>', unsafe_allow_html=True)
