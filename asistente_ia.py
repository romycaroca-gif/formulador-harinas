# ══════════════════════════════════════════════════════════════════════
# ASISTENTE VIRTUAL IA — Botón flotante ESQUINA INFERIOR DERECHA (Groq)
# Versión 2.0 — reescrito desde cero
# ══════════════════════════════════════════════════════════════════════
# ▸ Botón redondo 🤖 fijo abajo-derecha (funciona en CUALQUIER versión
#   de Streamlit: el anclaje se hace con JavaScript, no depende de
#   container(key=) ni de st.popover).
# ▸ Al hacer clic se abre un panel flotante con: saludo, 3 opciones
#   rápidas (Fallas · Mejoras · Comparaciones) y un buscador de
#   preguntas libres.
#
# USO — al final de FORMULADOR_FINAL.py:
#   from asistente_ia import render_asistente
#   render_asistente(mez=mez, costos=costos, ph=ph, pa=pa,
#                    receta_id=receta_id, modo_innov=modo_innov,
#                    LIMITES=LIMITES, HARINAS=HARINAS, semaforo=semaforo)
#
# API KEY — NUNCA en el código. Se lee (en este orden):
#   1. .streamlit/secrets.toml   →  GROQ_API_KEY = "gsk_..."
#   2. Variable de entorno       →  GROQ_API_KEY
# ══════════════════════════════════════════════════════════════════════

import os
import requests
import streamlit as st
import streamlit.components.v1 as components

GROQ_URL      = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL    = "llama-3.3-70b-versatile"
MAX_TOKENS    = 800
TEMPERATURA   = 0.4
MAX_HISTORIAL = 8

SALUDO = ("¡Hola! 👋 Soy el asistente del Formulador. Analizo tu "
          "formulación **actual** en tiempo real. Usa las opciones "
          "rápidas o pregúntame algo como *«¿qué ocurriría si subo "
          "el garbanzo a 20%?»*")


# ──────────────────────────────────────────────────────────────────────
# 1. API KEY — se busca en 3 lugares (en este orden):
#    a) .streamlit/secrets.toml  (estándar Streamlit)
#    b) Variable de entorno GROQ_API_KEY
#    c) Archivo "groq_api_key.txt" en la MISMA carpeta que este módulo
#       → método a prueba de errores: crea ese archivo junto a
#         asistente_ia.py y pega tu key adentro (una sola línea).
# ──────────────────────────────────────────────────────────────────────
def _obtener_api_key():
    # a) secrets.toml
    try:
        key = st.secrets.get("GROQ_API_KEY", None)
        if key:
            return str(key).strip()
    except Exception:
        pass
    # b) variable de entorno
    key = os.environ.get("GROQ_API_KEY")
    if key:
        return key.strip()
    # c) archivo de texto junto a este módulo (inmune al directorio
    #    desde donde se ejecute streamlit)
    try:
        ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "groq_api_key.txt")
        if os.path.exists(ruta):
            with open(ruta, encoding="utf-8") as f:
                key = f.read().strip().strip('"').strip("'")
            if key.startswith("gsk_"):
                return key
    except Exception:
        pass
    return None


# ──────────────────────────────────────────────────────────────────────
# 2. LLAMADA A GROQ
# ──────────────────────────────────────────────────────────────────────
def _llamar_groq(mensajes):
    api_key = _obtener_api_key()
    if not api_key:
        carpeta = os.path.dirname(os.path.abspath(__file__))
        return None, ("No se encontró la API key. Método más simple: crea un "
                      f"archivo llamado `groq_api_key.txt` en la carpeta "
                      f"`{carpeta}` y pega tu key adentro (una sola línea, "
                      "empieza con gsk_). Luego reinicia la app.")
    try:
        r = requests.post(
            GROQ_URL,
            headers={"Authorization": f"Bearer {api_key}",
                     "Content-Type": "application/json"},
            json={"model": GROQ_MODEL, "messages": mensajes,
                  "temperature": TEMPERATURA, "max_tokens": MAX_TOKENS},
            timeout=45)
        if r.status_code == 401:
            return None, "API key inválida o revocada (401). Genera una nueva en console.groq.com."
        if r.status_code == 429:
            return None, "Límite de peticiones alcanzado (429). Espera unos segundos."
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"].strip(), None
    except requests.exceptions.Timeout:
        return None, "Groq no respondió a tiempo. Reintenta."
    except requests.exceptions.ConnectionError:
        return None, "Sin conexión con api.groq.com. Revisa internet/firewall."
    except Exception as e:
        return None, f"Error inesperado: {type(e).__name__}: {e}"


# ──────────────────────────────────────────────────────────────────────
# 3. CONTEXTO — estado actual del formulador
# ──────────────────────────────────────────────────────────────────────
def _construir_contexto(mez, costos, ph, pa, receta_id, modo_innov,
                        LIMITES, HARINAS, semaforo):
    lineas = [f"RECETA BASE: {receta_id}",
              f"MODO INNOVACIÓN: {'ACTIVADO (límites relajados)' if modo_innov else 'desactivado (NCh 1237)'}",
              "", "COMPOSICIÓN ACTUAL (% sobre harina):"]
    for nm, frac in {**ph, **pa}.items():
        if frac > 0.0005:
            tipo = HARINAS.get(nm, {}).get('tipo', '?')
            lineas.append(f"  - {nm} ({tipo}): {frac*100:.1f}%")

    lineas += ["", "PROPIEDADES vs LÍMITES (✅ ok · ⚠️ marginal · ⚡ innovación · ❌ fuera de rango):"]
    for clave, lim in LIMITES.items():
        val = mez.get(clave)
        if val is None:
            continue
        if val == 0 and clave in ('W', 'PL', 'tenacidad', 'extension'):
            continue
        try:
            ico = semaforo(val, clave, modo_innov)[0]
        except Exception:
            ico = "·"
        lo = lim.get('min') if isinstance(lim, dict) else None
        hi = lim.get('max') if isinstance(lim, dict) else None
        rango = f" (rango: {lo if lo is not None else '—'} – {hi if hi is not None else '—'})" \
                if (lo is not None or hi is not None) else ""
        lineas.append(f"  {ico} {clave}: {val:.2f}{rango}")

    lineas += ["", "COSTOS:"]
    for k, et in [('c_h_sim', 'Harinas simulado ODEPA CLP/kg'),
                  ('c_h_real', 'Harinas real mercado CLP/kg'),
                  ('c_total_pan_sim', 'Costo total por pan (sim) CLP'),
                  ('c_total_pan_real', 'Costo total por pan (real) CLP')]:
        if isinstance(costos, dict) and k in costos:
            try:
                lineas.append(f"  - {et}: ${costos[k]:,.0f}")
            except Exception:
                pass

    guardadas = st.session_state.get('formulaciones', {})
    if guardadas:
        lineas.append("")
        lineas.append("FORMULACIONES GUARDADAS:")
        for nombre, d in list(guardadas.items())[:6]:
            lineas.append(f"  - {nombre}: {d}")
    return "\n".join(lineas)


def _system_prompt(contexto):
    return f"""Eres el asistente técnico del "Formulador de Mezclas de Harinas", un DSS chileno
para panificación (marraqueta y otras recetas) usado por panaderías, molinos, almacenes y hogares.
Ayudas a sustituir ingredientes (alergias, celiaquía, diabetes, costos) manteniendo viabilidad
tecnológica según NCh 1237 / DS 977/96.

REGLAS:
- Responde SIEMPRE en español chileno profesional, breve y accionable (máx ~250 palabras).
- Basa tus respuestas en el ESTADO ACTUAL del formulador (abajo). No inventes valores.
- En preguntas "¿qué ocurriría si...?", razona con los datos: leguminosas suben proteína/fibra/absorción
  y bajan W/extensibilidad; psyllium sube absorción (+4%/1%) y fibra; goma xantana sube tenacidad.
- Ante propiedades ❌, explica la causa probable y qué slider mover (dirección y magnitud aproximada).
- El modelo usa promedio ponderado lineal + efectos incrementales de aditivos: las interacciones
  reológicas reales requieren validación experimental. Menciónalo solo si es relevante.
- Sin consejos médicos; para alergias/celíacos limítate al plano tecnológico-alimentario.

ESTADO ACTUAL DEL FORMULADOR:
{contexto}"""


_PROMPTS_RAPIDOS = {
    "fallas": ("⚠️ Fallas",
               "Analiza la formulación actual: identifica TODAS las propiedades fuera de rango (❌) "
               "o marginales (⚠️), explica la causa más probable de cada una según la composición "
               "y prioriza cuál corregir primero."),
    "mejoras": ("💡 Mejoras",
                "Propón 3 mejoras concretas a la formulación actual (qué slider mover, cuánto y por qué), "
                "balanceando cumplimiento normativo, aporte nutricional y costo por kg."),
    "comparaciones": ("🔬 Comparaciones",
                      "Compara la formulación actual contra una marraqueta 100% trigo tradicional y, "
                      "si existen, contra las formulaciones guardadas: diferencias en W, P/L, absorción, "
                      "proteína, fibra, costo y viabilidad. Entrega un veredicto."),
}


def _procesar(prompt_usuario, contexto):
    hist = st.session_state.setdefault("ia_historial", [])
    mensajes = [{"role": "system", "content": _system_prompt(contexto)}]
    mensajes += hist[-MAX_HISTORIAL:]
    mensajes.append({"role": "user", "content": prompt_usuario})
    with st.spinner("Consultando al asistente..."):
        respuesta, error = _llamar_groq(mensajes)
    if error:
        st.session_state["ia_ultima"] = ("error", prompt_usuario, error)
    else:
        hist += [{"role": "user", "content": prompt_usuario},
                 {"role": "assistant", "content": respuesta}]
        st.session_state["ia_historial"] = hist[-MAX_HISTORIAL:]
        st.session_state["ia_ultima"] = ("ok", prompt_usuario, respuesta)


# ──────────────────────────────────────────────────────────────────────
# 4. ANCLAJE FLOTANTE — JavaScript (independiente de la versión)
# ──────────────────────────────────────────────────────────────────────
# components.html usa un iframe srcdoc del MISMO origen, por lo que el
# script puede acceder a window.parent.document y fijar los bloques.
# Se re-aplica cada 350 ms para sobrevivir a los re-renders de Streamlit.
_JS_ANCLAJE = """
<script>
function fijarAsistente() {
    try {
        const doc = window.parent.document;

        // ── BOTÓN flotante (abajo-derecha) ──
        const anclaB = doc.querySelector('div.ancla-boton-ia');
        if (anclaB) {
            const bloque = anclaB.closest('[data-testid="stVerticalBlock"]');
            if (bloque && bloque.dataset.iaFijado !== '1') {
                Object.assign(bloque.style, {
                    position: 'fixed', bottom: '26px', right: '26px',
                    left: 'auto', top: 'auto', width: 'auto',
                    zIndex: '999990', gap: '0px'});
                bloque.dataset.iaFijado = '1';
            }
            const btn = anclaB.closest('[data-testid="stVerticalBlock"]')
                              ?.querySelector('button');
            if (btn && btn.dataset.iaEstilo !== '1') {
                Object.assign(btn.style, {
                    width: '62px', height: '62px', minHeight: '62px',
                    borderRadius: '50%', border: 'none',
                    background: 'linear-gradient(135deg,#1e3a5f,#2c5282)',
                    color: '#ffffff', fontSize: '1.6rem',
                    boxShadow: '0 4px 16px rgba(30,58,95,.5)',
                    cursor: 'pointer'});
                btn.querySelectorAll('p').forEach(p => {
                    p.style.color = '#fff'; p.style.fontSize = '1.5rem';});
                btn.dataset.iaEstilo = '1';
            }
        }

        // ── PANEL flotante (sobre el botón) ──
        const anclaP = doc.querySelector('div.ancla-panel-ia');
        if (anclaP) {
            const panel = anclaP.closest('[data-testid="stVerticalBlock"]');
            if (panel && panel.dataset.iaFijado !== '1') {
                Object.assign(panel.style, {
                    position: 'fixed', bottom: '100px', right: '26px',
                    left: 'auto', top: 'auto',
                    width: '390px', maxWidth: '92vw',
                    maxHeight: '68vh', overflowY: 'auto',
                    background: '#ffffff', borderRadius: '14px',
                    border: '1px solid #e2e8f0',
                    boxShadow: '0 12px 40px rgba(0,0,0,.22)',
                    padding: '14px 16px', zIndex: '999991',
                    gap: '0.4rem'});
                panel.dataset.iaFijado = '1';
            }
        }
    } catch (e) { /* silencioso */ }
}
setInterval(fijarAsistente, 350);
fijarAsistente();
</script>
"""

_CSS_GLOBAL = """
<style>
div.ancla-boton-ia, div.ancla-panel-ia { display:none; }
.ia-saludo {background:linear-gradient(135deg,#1e3a5f10,#2c528215);
    border-left:3px solid #1e3a5f;border-radius:10px;padding:10px 12px;
    font-size:.8rem;color:#1e293b;line-height:1.5;}
.ia-titulo {font-size:.95rem;font-weight:700;color:#1e3a5f;}
.ia-resp {background:#f1f5f9;border-left:3px solid #16a34a;border-radius:8px;
    padding:9px 12px;font-size:.8rem;color:#1e293b;white-space:pre-wrap;
    line-height:1.55;max-height:230px;overflow-y:auto;}
.ia-preg {background:#1e3a5f0d;border-radius:8px;padding:6px 10px;
    font-size:.75rem;color:#334155;font-style:italic;}
</style>
"""


# ──────────────────────────────────────────────────────────────────────
# 5. RENDER PRINCIPAL
# ──────────────────────────────────────────────────────────────────────
def render_asistente(mez, costos, ph, pa, receta_id, modo_innov,
                     LIMITES, HARINAS, semaforo):
    """Botón flotante inferior-derecho + panel del asistente IA."""
    st.markdown(_CSS_GLOBAL, unsafe_allow_html=True)

    contexto = _construir_contexto(mez, costos, ph, pa, receta_id,
                                   modo_innov, LIMITES, HARINAS, semaforo)
    abierto = st.session_state.get("ia_abierto", False)

    # ── BOTÓN flotante 🤖 / ✕ ──
    with st.container():
        st.markdown('<div class="ancla-boton-ia"></div>', unsafe_allow_html=True)
        if st.button("✕" if abierto else "🤖", key="ia_toggle",
                     help="Asistente IA"):
            st.session_state["ia_abierto"] = not abierto
            st.rerun()

    # ── PANEL flotante ──
    if abierto:
        with st.container():
            st.markdown('<div class="ancla-panel-ia"></div>', unsafe_allow_html=True)
            st.markdown('<div class="ia-titulo">🤖 Asistente del Formulador</div>',
                        unsafe_allow_html=True)
            st.markdown(f'<div class="ia-saludo">{SALUDO}</div>',
                        unsafe_allow_html=True)

            # Opciones rápidas
            cols = st.columns(3)
            for col, (clave, (etiqueta, prompt)) in zip(cols, _PROMPTS_RAPIDOS.items()):
                with col:
                    if st.button(etiqueta, key=f"ia_btn_{clave}",
                                 use_container_width=True):
                        _procesar(prompt, contexto)

            # Buscador de preguntas libres
            pregunta = st.text_input("Pregunta libre",
                                     placeholder="¿Qué ocurriría si...?",
                                     key="ia_pregunta",
                                     label_visibility="collapsed")
            if st.button("Preguntar ➤", key="ia_enviar",
                         use_container_width=True, type="primary"):
                if pregunta.strip():
                    _procesar(pregunta.strip(), contexto)
                else:
                    st.session_state["ia_ultima"] = (
                        "error", "", "Escribe una pregunta antes de enviar.")

            # Última respuesta
            ultima = st.session_state.get("ia_ultima")
            if ultima:
                estado, preg, texto = ultima
                if preg:
                    st.markdown(f'<div class="ia-preg">Tú: {preg}</div>',
                                unsafe_allow_html=True)
                if estado == "ok":
                    st.markdown(f'<div class="ia-resp">{texto}</div>',
                                unsafe_allow_html=True)
                else:
                    st.error(texto)

            if st.session_state.get("ia_historial"):
                if st.button("🗑 Limpiar conversación", key="ia_clear",
                             use_container_width=True):
                    st.session_state["ia_historial"] = []
                    st.session_state["ia_ultima"] = None
                    st.rerun()

    # ── Script de anclaje (iframe invisible, mismo origen) ──
    components.html(_JS_ANCLAJE, height=0, width=0)
