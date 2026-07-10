import streamlit as st, pandas as pd, numpy as np, os
from scipy.optimize import minimize

st.set_page_config(page_title="Formulador Harinas — Marraqueta",
                   page_icon="🍞", layout="wide",
                   initial_sidebar_state="expanded")

st.markdown("""<style>
/* ── Tema claro global ── */
[data-testid="stAppViewContainer"] {
    background-color: #f8fafc !important;
}
[data-testid="stSidebar"] {
    background-color: #ffffff !important;
    border-right: 1px solid #e2e8f0;
}
[data-testid="stSidebar"] * {
    color: #1e293b !important;
}
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stCheckbox label,
[data-testid="stSidebar"] .stRadio label,
[data-testid="stSidebar"] .stSelectbox label {
    color: #1e293b !important;
}
/* Texto principal */
h1,h2,h3,p,span,div,label {
    color: #1e293b;
}
/* Botones */
.stButton > button {
    background: #ffffff;
    color: #1e293b;
    border: 1px solid #cbd5e1;
}
.stButton > button:hover {
    background: #f1f5f9;
    border-color: #94a3b8;
}
/* Slider */
.stSlider .st-emotion-cache-1jmve {
    color: #1e293b;
}
/* Dataframe */
[data-testid="stDataFrame"] {
    background: #ffffff;
}
/* Expander */
[data-testid="stExpander"] {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
}
/* Selectbox — fondo blanco, texto oscuro visible */
[data-testid="stSelectbox"] > div > div {
    background-color: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    color: #1e293b !important;
}
[data-testid="stSelectbox"] span {
    color: #1e293b !important;
}
/* Text input */
[data-testid="stTextInput"] input {
    background-color: #ffffff !important;
    color: #1e293b !important;
    border: 1px solid #cbd5e1 !important;
}
/* Number input */
[data-testid="stNumberInput"] input {
    background-color: #ffffff !important;
    color: #1e293b !important;
}
.sec{font-size:.78rem;font-weight:700;color:#1e3a5f;text-transform:uppercase;
  letter-spacing:.06em;border-bottom:1px solid #e2e8f0;padding-bottom:3px;margin:14px 0 8px 0;}
.mcard{background:#ffffff;border-radius:8px;padding:10px 14px;
  border-left:4px solid #1e3a5f;margin-bottom:7px;
  box-shadow:0 1px 3px rgba(0,0,0,0.08);}
.mlabel{font-size:.68rem;color:#64748b;font-weight:600;text-transform:uppercase;}
.mval{font-size:1.25rem;font-weight:700;color:#1e3a5f;}
.munit{font-size:.78rem;color:#94a3b8;margin-left:3px;}
.srow{display:flex;align-items:center;gap:8px;padding:5px 10px;
  border-radius:7px;margin-bottom:4px;}
.slbl{flex:1;font-size:.80rem;font-weight:600;color:#334155;}
.sval{font-size:.80rem;color:#1e3a5f;font-weight:700;width:70px;text-align:right;}
.srng{font-size:.72rem;color:#64748b;width:85px;text-align:center;}
.smsg{font-size:.72rem;width:130px;}
</style>""", unsafe_allow_html=True)

LOGO_UDD_B64 = "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"

EXCEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "DATA_BASE_HARINAS_v3.xlsx")

# ══════════════════════════════════════════════════════════════════════
# B. CACHÉ — datos se cargan una sola vez en memoria
# ══════════════════════════════════════════════════════════════════════
@st.cache_data
def cargar_excel(path):
    df_h = pd.read_excel(path, sheet_name='INFO TIPOS DE HARINAS')
    df_h.columns = df_h.columns.str.strip()
    df_h['ID_Harina'] = df_h['ID_Harina'].astype(str).str.strip()
    df_h.set_index('ID_Harina', inplace=True)
    col_tipo = (df_h['Tipo_Ingrediente'].astype(str).str.strip().str.lower()
                if 'Tipo_Ingrediente' in df_h.columns else None)
    for col in df_h.columns:
        if col != 'Tipo_Ingrediente':
            df_h[col] = pd.to_numeric(df_h[col], errors='coerce').fillna(0)
    tipos = {}
    for nm in df_h.index:
        tipos[nm] = (col_tipo.get(nm, 'alternativa') if col_tipo is not None
                     else ('aditivo' if any(a in nm.lower() for a in
                           ['psyllium','goma','mejorador','ibis'])
                           else 'base' if 'trigo' in nm.lower() else 'alternativa'))

    def prom(nm, a, b):
        return ((float(df_h.at[nm,a]) if a in df_h.columns else 0) +
                (float(df_h.at[nm,b]) if b in df_h.columns else 0)) / 2

    PARES = [('proteina','Proteina_Min','Proteina_Max'),
             ('lipidos','Lipidos_Min','Lipidos_Max'),
             ('fibra','Fibra_Min','Fibra_Max'),
             ('W','Fuerza_panadera_min','Fuerza_panadera_max'),
             ('PL','Equilibrio_PL_min','Equilibrio_PL_max'),
             ('tenacidad','Tenacidad_min','Tenacidad_max'),
             ('extension','Extensibilidad_min','Extensibillidad_max'),
             ('absorcion','Absorcion_agua_C1_min','Absorcion_agua_C1_max'),
             ('cenizas','Cenizas_min','Cenizas_max'),
             ('humedad','Humedad_min','Humedad_max'),
             ('C3','Gelatinización_C3_min','Gelatinización_C3_max'),
             ('C5','Retrogradación_C5_min','Retrogradación_C6_max')]

    harinas, aditivos = {}, {}
    for nm in df_h.index:
        p = {'tipo': tipos.get(nm,'alternativa'),
             'costo_sim':  float(df_h.at[nm,'Costo_simulado_Kg']),
             'costo_real': float(df_h.at[nm,'Costo_real_kg'])}
        for clave, c1, c2 in PARES:
            p[clave] = prom(nm, c1, c2)
        (aditivos if tipos.get(nm)=='aditivo' else harinas)[nm] = p

    df_l = pd.read_excel(path, sheet_name='LIMITES MARRAQUETA')
    df_l.columns = df_l.columns.str.strip()
    df_l['Propiedad'] = df_l['Propiedad'].astype(str).str.strip()
    df_l.set_index('Propiedad', inplace=True)
    limites = {}
    if 'clave_modelo' in df_l.columns:
        for prop, row in df_l.iterrows():
            clave = str(row.get('clave_modelo','')).strip()
            if not clave or clave == 'nan': continue
            tipo_lim = str(row.get('tipo_limite','')).strip().lower()
            limites[clave] = {
                'label':     prop,
                'min':       float(row['bj_min']) if pd.notna(row.get('bj_min')) and row.get('bj_min') else None,
                'max':       float(row['bj_max']) if pd.notna(row.get('bj_max')) and row.get('bj_max') else None,
                'max_innov': float(row['bj_max_innovacion'])
                             if 'bj_max_innovacion' in df_l.columns
                             and pd.notna(row.get('bj_max_innovacion')) else None,
                'tipo':      tipo_lim if tipo_lim else 'normativo',
            }

    df_e = pd.read_excel(path, sheet_name='EFECTOS_ADITIVOS', header=2)
    df_e.columns = df_e.columns.str.strip()
    df_e.dropna(subset=['ID_Aditivo'], inplace=True)
    efectos = {}
    for _, row in df_e.iterrows():
        adi = str(row['ID_Aditivo']).strip()
        prop = str(row['Propiedad_Afectada']).strip()
        val  = float(row['Efecto_por_1pct']) if pd.notna(row['Efecto_por_1pct']) else 0
        if adi not in efectos: efectos[adi] = {}
        efectos[adi][prop] = val

    df_r = pd.read_excel(path, sheet_name='RECETA_BASE', header=2)
    df_r.columns = df_r.columns.str.strip()
    df_r.dropna(subset=['ID_Receta'], inplace=True)
    recetas = {}
    for _, row in df_r.iterrows():
        rid = str(row['ID_Receta']).strip()
        ing = str(row['Ingrediente_Panadero']).strip().lower()
        pct = float(row['Porcentaje_Baker']) if pd.notna(row['Porcentaje_Baker']) else 0
        if rid not in recetas: recetas[rid] = {}
        recetas[rid][ing] = pct

    df_esc = pd.read_excel(path, sheet_name='RECETA_BASE', header=2, usecols="G:J")
    df_esc.columns = ['Parametro','Valor','Unidad','Notas']
    df_esc.dropna(subset=['Parametro'], inplace=True)
    escalado = {str(r['Parametro']).strip(): r['Valor']
                for _, r in df_esc.iterrows() if pd.notna(r['Valor'])}

    # ── Precios de insumos y parámetros económicos
    df_p = pd.read_excel(path, sheet_name='PRECIOS_INSUMOS', header=None)
    precios = {}
    for _, row in df_p.iterrows():
        id_ins = str(row.iloc[0] or '').strip()
        val    = row.iloc[2]
        if (id_ins and id_ins not in ('ID_Insumo','') and
                pd.notna(val) and str(id_ins) != 'nan'):
            try: precios[id_ins] = float(val)
            except: pass

    return harinas, aditivos, limites, efectos, recetas, escalado, precios

try:
    HARINAS, ADITIVOS, LIMITES, EFECTOS, RECETAS, ESCALADO, PRECIOS = cargar_excel(EXCEL_PATH)
except Exception as e:
    st.error(f"❌ Error cargando Excel: {e}")
    st.stop()

RENDIMIENTO  = float(ESCALADO.get('rendimiento_pct', 82.2)) / 100
PESO_PAN_G   = float(ESCALADO.get('peso_pan_g', 210))
KG_H_DEFAULT = float(ESCALADO.get('kg_harina_default', 10.0))
IBIS_KEY     = next((k for k in ADITIVOS
                     if 'ibis' in k.lower() or 'mejorador' in k.lower()), None)
IBIS_DOSIS   = 0.4
MAX_ALT      = {'Maíz':20,'Arroz':15,'Garbanzos':15,'Lentejas':10}
# ── PESOS DE PENALIZACIÓN para la función objetivo del optimizador ──────────
# Justificación metodológica (documentar en tesis, Anexo metodológico):
#
# El peso de cada restricción refleja dos criterios combinados:
#   (1) ESTRECHEZ DEL RANGO NORMATIVO: límites más estrechos → mayor penalización,
#       porque pequeñas violaciones tienen impacto proporcional mayor.
#   (2) IMPACTO TECNOLÓGICO EN MARRAQUETA: propiedades más críticas para la
#       calidad del producto final reciben mayor peso.
#
# Propiedad      Peso  Rango normativo   Justificación
# ─────────────────────────────────────────────────────────────────────────────
# cenizas          25  ≤ 0.65%           Rango muy estrecho (0.05% de margen).
#                                        Harinas leguminosas tienen 2-3% →
#                                        cualquier sustitución lo viola.
#                                        Impacto: color miga, sabor residual.
#                                        Fuente: NCh 1237; justificación empírica
#                                        iterativa (calibración del modelo).
#
# absorcion        20  58 – 63%          Rango estrecho (5%). Absorción fuera de
#                                        rango afecta directamente la consistencia
#                                        de la masa y el proceso de amasado.
#                                        Impacto operacional directo (Farinógrafo).
#                                        Fuente: AACC 54-21; peso iterativo.
#
# W               15  200 – 260          Rango amplio (60 unidades). Peso alto
#                                        porque W es el parámetro más relevante
#                                        para la aptitud panadera de la harina
#                                        (Alveógrafo Chopin). Sin W mínimo la
#                                        marraqueta no desarrolla volumen.
#                                        Fuente: NCh 1237; literatura reológica.
#
# PL              12  0.7 – 1.6          Rango moderado. Equilibrio P/L define
#                                        la maquinabilidad de la masa. Peso menor
#                                        que W porque en mezclas con harinas sin
#                                        gluten el P/L se recalcula indirectamente
#                                        desde tenacidad/extensibilidad.
#
# proteina        12  7 – 15%            Rango amplio (8%). La proteína mínima
#                                        (7%) es fácilmente alcanzable con trigo
#                                        pero las leguminosas aportan proteína
#                                        no-gluten que eleva el valor proyectado
#                                        sin mejorar la red reológica.
#                                        Peso moderado: menos crítico que W.
#
# NOTA: Los pesos fueron calibrados iterativamente para que la función objetivo
# produzca soluciones factibles en los rangos 5-35% de sustitución. No provienen
# de literatura directa sino de optimización de hiperparámetros del modelo DSS.
# ─────────────────────────────────────────────────────────────────────────────
PESOS_PEN = {'W': 15, 'PL': 12, 'absorcion': 20, 'proteina': 12, 'cenizas': 25}

# Precios leídos desde hoja PRECIOS_INSUMOS del Excel
# Fallback a valores por defecto si falta alguna fila
P = PRECIOS
PRECIO_LEVADURA  = P.get('levadura_fresca',        2500)
PRECIO_SAL       = P.get('sal_fina',                150)
PRECIO_IBIS      = P.get('mejorador_ibis',          3500)
PRECIO_AGUA      = P.get('agua_potable',              5)
PRECIO_VENTA     = P.get('precio_venta_marraqueta', 250)
MARGEN_OBJ       = P.get('margen_objetivo_pct',      35) / 100
MERMA_PCT        = P.get('factor_merma_proceso',      3) / 100
COSTO_MO         = P.get('mano_obra_por_kg_pan',    180)
COSTO_ENERGIA    = P.get('energia_horneado_por_kg',  45)
COSTO_PACKAGING  = P.get('packaging_por_unidad',      8)

# ══════════════════════════════════════════════════════════════════════
# FUNCIONES DE CÁLCULO
# ══════════════════════════════════════════════════════════════════════
def calcular_mezcla(ph, pa):
    th = sum(ph.values()); ta = sum(pa.values()); tot = th + ta
    if tot == 0: return {}
    fh = {k: v/tot for k,v in ph.items()}
    fa = {k: v/tot for k,v in pa.items()}
    PROPS = ['proteina','lipidos','fibra','W','PL','tenacidad','extension',
             'absorcion','cenizas','humedad','C3','C5']
    base = {}
    for p in PROPS:
        val = sum(fh[h]*HARINAS[h].get(p,0) for h in ph)
        base[p] = val*(tot/th) if th > 0 else 0.0
    for adi, frac in fa.items():
        pct = frac*100
        for prop, delta in EFECTOS.get(adi,{}).items():
            if prop in base: base[prop] += pct*delta
    # Proteger extensibilidad: no puede ser negativa ni cero
    # Los aditivos (especialmente XG a dosis altas) pueden reducir L.
    # Mínimo físico razonable: 10mm (masa muy tenaz pero aún extensible)
    base['extension'] = max(base.get('extension', 0), 10.0)
    if base.get('extension', 0) > 0:
        base['PL'] = base['tenacidad'] / base['extension']
    cs = (sum(fh[h]*HARINAS[h]['costo_sim']  for h in ph) +
          sum(fa[a]*ADITIVOS[a]['costo_sim']  for a in pa))
    cr = (sum(fh[h]*HARINAS[h]['costo_real'] for h in ph) +
          sum(fa[a]*ADITIVOS[a]['costo_real'] for a in pa))
    pct_alt = sum(ph[h] for h in ph if HARINAS[h]['tipo']=='alternativa')/tot*100
    return {**base,'costo_sim':cs,'costo_real':cr,
            'pct_alt':pct_alt,'pct_adi':ta/tot*100}

def semaforo(val, clave, innov=False):
    lim = LIMITES.get(clave)
    if not lim: return "—","#f8fafc","#94a3b8","Sin límite"
    vmin,vmax,vmaxi = lim['min'],lim['max'],lim.get('max_innov')
    tipo = lim.get('tipo','normativo')
    if tipo == 'referencia':
        if vmin and val < vmin: return "📊","#f0f9ff","#0369a1","Bajo ref."
        if vmax and val > vmax: return "📊","#fff7ed","#c2410c","Sobre ref."
        return "📊","#f0fdf4","#15803d","En rango ref."
    # Normativo: falla solo si está FUERA del rango
    if vmin and val < vmin: return "❌","#fef2f2","#ef4444","↓ Bajo mínimo"
    if vmax and val > vmax:
        if innov and vmaxi and val <= vmaxi:
            return "⚡","#fffbeb","#d97706","Rango innovación"
        return "❌","#fef2f2","#ef4444","↑ Sobre máximo"
    # Dentro de rango — marginal usa 5% del RANGO (no del valor)
    # Esto evita que propiedades con rangos amplios sean falsamente marginal
    rango = (vmax - vmin) if (vmin and vmax) else (vmax or vmin or 1)
    mn = (val - vmin) / rango if vmin else 1.0
    mx = (vmax - val) / rango if vmax else 1.0
    if min(mn, mx) < 0.05: return "⚠️","#fffbeb","#d97706","Marginal"
    return "✅","#f0fdf4","#16a34a","Dentro de rango"

def rango_str(clave):
    lim = LIMITES.get(clave)
    if not lim: return "—"
    vmin,vmax = lim['min'],lim['max']
    if vmin and vmax: return f"{vmin} – {vmax}"
    if vmin: return f"≥ {vmin}"
    if vmax: return f"≤ {vmax}"
    return "—"

def calcular_costos_totales(ph, pa, rec_id, absorcion):
    rec      = RECETAS.get(rec_id, {})
    agua_pct = rec.get('agua',0) or absorcion
    lev_pct  = rec.get('levadura', 1.75)
    sal_pct  = rec.get('sal', 2.0)
    ibis_pct = rec.get('mejorador ibis', 0.4)
    tot = sum(ph.values()) + sum(pa.values())
    fh  = {k: v/tot for k,v in ph.items()} if tot > 0 else {}
    fa  = {k: v/tot for k,v in pa.items()} if tot > 0 else {}

    # Costo de harinas (objetivo central de la tesis)
    c_h_sim  = sum(fh[h]*HARINAS[h]['costo_sim']  for h in ph) if ph else 0
    c_h_real = sum(fh[h]*HARINAS[h]['costo_real'] for h in ph) if ph else 0

    # Insumos panaderos — precios desde Excel (PRECIOS_INSUMOS)
    c_lev  = (lev_pct/100)  * PRECIO_LEVADURA
    c_sal  = (sal_pct/100)  * PRECIO_SAL
    c_ibis = (ibis_pct/100) * PRECIO_IBIS
    c_agua = (agua_pct/100) * PRECIO_AGUA
    c_ins  = c_lev + c_sal + c_ibis + c_agua

    # Factor de masa: kg masa por cada kg harina
    masa_f = 1 + agua_pct/100 + lev_pct/100 + sal_pct/100 + ibis_pct/100

    # Panes por kg de harina (aplicando rendimiento y merma)
    panes_por_kg = masa_f * RENDIMIENTO * (1 - MERMA_PCT) * 1000 / PESO_PAN_G

    # Costos por unidad de producción
    c_masa_sim  = (c_h_sim  + c_ins) / masa_f
    c_masa_real = (c_h_real + c_ins) / masa_f
    c_pan_sim   = (c_h_sim  + c_ins) / panes_por_kg
    c_pan_real  = (c_h_real + c_ins) / panes_por_kg

    # Costo total por marraqueta (incluyendo operacionales desde Excel)
    c_op_por_pan = (COSTO_MO + COSTO_ENERGIA) * (PESO_PAN_G/1000) + COSTO_PACKAGING
    c_total_pan_sim  = c_pan_sim  + c_op_por_pan
    c_total_pan_real = c_pan_real + c_op_por_pan

    # Margen bruto
    margen_sim  = PRECIO_VENTA - c_total_pan_sim
    margen_real = PRECIO_VENTA - c_total_pan_real
    margen_pct_sim  = margen_sim  / PRECIO_VENTA * 100 if PRECIO_VENTA > 0 else 0
    margen_pct_real = margen_real / PRECIO_VENTA * 100 if PRECIO_VENTA > 0 else 0

    return {
        'c_h_sim':  c_h_sim,   'c_h_real':  c_h_real,
        'c_ins':    c_ins,
        'c_masa_sim':  c_masa_sim,  'c_masa_real':  c_masa_real,
        'c_pan_sim':   c_pan_sim,   'c_pan_real':   c_pan_real,
        'c_op_por_pan': c_op_por_pan,
        'c_total_pan_sim':  c_total_pan_sim,
        'c_total_pan_real': c_total_pan_real,
        'margen_sim':      margen_sim,
        'margen_real':     margen_real,
        'margen_pct_sim':  margen_pct_sim,
        'margen_pct_real': margen_pct_real,
        'precio_venta':    PRECIO_VENTA,
        'merma_pct':       MERMA_PCT * 100,
        'desglose': {
            'Levadura':       c_lev,
            'Sal':            c_sal,
            'Mejorador IBIS': c_ibis,
            'Agua':           c_agua,
        },
        'desglose_op': {
            'Mano de obra':  COSTO_MO * (PESO_PAN_G/1000),
            'Energía horno': COSTO_ENERGIA * (PESO_PAN_G/1000),
            'Packaging':     COSTO_PACKAGING,
        },
    }

def escalar(ph, pa, rec_id, abs_opt, kg):
    rec  = RECETAS.get(rec_id, {})
    agua = rec.get('agua',0) or abs_opt
    lev  = rec.get('levadura', 1.75)
    sal  = rec.get('sal', 2.0)
    ibis = rec.get('mejorador ibis', 0.4)
    ings = {}
    for h,f in ph.items():
        if f > 0: ings[h] = round(f*kg*1000, 1)
    for a,f in pa.items():
        if f > 0 and (IBIS_KEY is None or a != IBIS_KEY):
            ings[a] = round(f*kg*1000, 1)
    ings[f'Mejorador IBIS ({ibis}%)'] = round(ibis/100*kg*1000, 1)
    ings[f'Agua ({agua:.1f}%)']       = round(agua/100*kg*1000, 1)
    ings[f'Levadura ({lev}%)']        = round(lev/100*kg*1000, 1)
    ings[f'Sal ({sal}%)']             = round(sal/100*kg*1000, 1)
    masa_kg = kg*(100+agua+lev+sal+ibis)/100
    pan_kg  = masa_kg * RENDIMIENTO
    return {'ingredientes':ings,'masa_kg':round(masa_kg,3),
            'pan_kg':round(pan_kg,3),'unidades':int(pan_kg*1000/PESO_PAN_G),
            'agua_pct':agua}

# ══════════════════════════════════════════════════════════════════════
# A. MOTOR DE OPTIMIZACIÓN — Simplex / SLSQP
# ══════════════════════════════════════════════════════════════════════
def optimizar_receta(nivel_alt_target, usar_ibis_opt, tipo_costo='sim',
                     harina_forzada=None, nivel_forzado=None,
                     harinas_permitidas=None):
    """
    Minimiza el costo de la mezcla de harinas sujeto a restricciones reológicas.

    Args:
        nivel_alt_target:  fracción mínima total de harinas alternativas (0–0.4)
        usar_ibis_opt:     si el mejorador IBIS está activo
        tipo_costo:        'sim' (ODEPA) o 'real' (mercado)
        harina_forzada:    nombre de harina que debe incluirse al nivel_forzado
        nivel_forzado:     fracción mínima de harina_forzada
        harinas_permitidas: lista de harinas alternativas permitidas.
                            Si se especifica, las demás quedan bloqueadas (bound=0).
                            Permite hacer recetas binarias o combinaciones específicas.
    """
    nombres_h = list(HARINAS.keys())
    n = len(nombres_h)
    idx_alt   = [i for i,nm in enumerate(nombres_h) if HARINAS[nm]['tipo']=='alternativa']
    idx_base  = [i for i,nm in enumerate(nombres_h) if HARINAS[nm]['tipo']=='base']

    # Vectores de propiedades
    def vec(prop):
        return np.array([HARINAS[nm].get(prop,0) for nm in nombres_h])

    v_costo  = vec('costo_sim') if tipo_costo=='sim' else vec('costo_real')
    v_W      = vec('W'); v_PL = vec('PL'); v_prot = vec('proteina')
    v_abs    = vec('absorcion'); v_cen = vec('cenizas')
    v_ten    = vec('tenacidad'); v_ext = vec('extension')

    # Efectos del IBIS sobre la mezcla (a dosis fija 0.4%)
    ibis_efx = EFECTOS.get(IBIS_KEY, {}) if usar_ibis_opt and IBIS_KEY else {}
    ibis_dosis_f = IBIS_DOSIS/100 if usar_ibis_opt else 0

    def props_mezcla(x):
        """Calcula propiedades de la mezcla + efectos IBIS."""
        W   = float(np.dot(x, v_W))   + ibis_efx.get('W',0)   * ibis_dosis_f * 100
        PL  = float(np.dot(x, v_PL))
        ten = float(np.dot(x, v_ten)) + ibis_efx.get('tenacidad',0) * ibis_dosis_f * 100
        ext = float(np.dot(x, v_ext)) + ibis_efx.get('extension',0) * ibis_dosis_f * 100
        # Clamp: extensibilidad nunca negativa ni cero (mínimo físico 10mm)
        ext = max(ext, 10.0)
        if ext > 0: PL = ten/ext
        prot= float(np.dot(x, v_prot))
        ab  = float(np.dot(x, v_abs)) + ibis_efx.get('absorcion',0) * ibis_dosis_f * 100
        cen = float(np.dot(x, v_cen))
        return {'W':W,'PL':PL,'proteina':prot,'absorcion':ab,'cenizas':cen}

    def fo(x):
        """Función objetivo: costo + penalización por violación de límites."""
        costo = float(np.dot(x, v_costo))
        p = props_mezcla(x)
        pen = 0.0
        def pnl(val, vmin, vmax, w):
            r = 0.0
            if vmin and val < vmin: r += w*((vmin-val)/vmin)**2
            if vmax and val > vmax: r += w*((val-vmax)/vmax)**2
            return r
        pen += pnl(p['proteina'],   LIMITES.get('proteina',{}).get('min'),
                                    LIMITES.get('proteina',{}).get('max'), PESOS_PEN['proteina'])
        pen += pnl(p['W'],          LIMITES.get('W',{}).get('min'),
                                    LIMITES.get('W',{}).get('max'), PESOS_PEN['W'])
        pen += pnl(p['PL'],         LIMITES.get('PL',{}).get('min'),
                                    LIMITES.get('PL',{}).get('max'), PESOS_PEN['PL'])
        pen += pnl(p['absorcion'],  LIMITES.get('absorcion',{}).get('min'),
                                    LIMITES.get('absorcion',{}).get('max'), PESOS_PEN['absorcion'])
        pen += pnl(p['cenizas'],    None,
                                    LIMITES.get('cenizas',{}).get('max'), PESOS_PEN['cenizas'])
        return costo + pen * max(costo*3, 1500)

    # Bounds: base 0-100%, alt según MAX_ALT
    # Si harinas_permitidas está definido, bloquear las alternativas no incluidas
    bounds = []
    for nm in nombres_h:
        if HARINAS[nm]['tipo'] == 'base':
            bounds.append((0.0, 1.0))
        elif HARINAS[nm]['tipo'] == 'alternativa':
            if harinas_permitidas is not None and nm not in harinas_permitidas:
                bounds.append((0.0, 0.0))   # bloqueada
            else:
                lim_ind = MAX_ALT.get(nm, 0.20) / 100
                bounds.append((0.0, lim_ind))
        else:
            bounds.append((0.0, MAX_ALT.get(nm, 0.20) / 100))

    constraints = [
        {'type':'eq',   'fun': lambda x: np.sum(x) - 1.0},
        {'type':'ineq', 'fun': lambda x, t=nivel_alt_target:
            sum(x[i] for i in idx_alt) - t},
        {'type':'ineq', 'fun': lambda x, t=nivel_alt_target:
            t + 0.02 - sum(x[i] for i in idx_alt)},
    ]

    # Si se especifica harina_forzada, agregar restricción de nivel mínimo
    i_forzada = None
    if harina_forzada and harina_forzada in nombres_h:
        i_forzada = nombres_h.index(harina_forzada)
        nivel_f   = nivel_forzado if nivel_forzado else nivel_alt_target
        constraints.append({
            'type': 'ineq',
            'fun':  lambda x, i=i_forzada, nf=nivel_f: x[i] - nf * 0.8
        })

    mejor = None; mejor_val = np.inf
    rng = np.random.default_rng(42)
    for intento in range(30):
        x0 = np.zeros(n)
        # Si hay harina forzada, el punto de partida la incluye directamente
        if i_forzada is not None:
            nf = nivel_forzado if nivel_forzado else nivel_alt_target
            x0[i_forzada] = nf
            resto = 1.0 - nf
            if idx_base and resto > 0: x0[idx_base[0]] = resto
        elif idx_alt:
            pcts = rng.dirichlet(np.ones(len(idx_alt))) * nivel_alt_target
            pcts = np.clip(pcts, 0, [bounds[i][1] for i in idx_alt])
            for k,i in enumerate(idx_alt): x0[i] = pcts[k]
            resto = 1.0 - x0.sum()
            if idx_base and resto > 0: x0[idx_base[0]] = resto
        x0 = np.clip(x0, [b[0] for b in bounds], [b[1] for b in bounds])
        x0 = x0/x0.sum() if x0.sum()>0 else np.ones(n)/n
        try:
            res = minimize(fo, x0, method='SLSQP', bounds=bounds,
                           constraints=constraints,
                           options={'ftol':1e-10,'maxiter':3000})
            if res.success and res.fun < mejor_val:
                mejor_val = res.fun; mejor = res
        except Exception as e:
            print(f"[OPT] Intento {intento+1}/30 falló: {type(e).__name__}: {e}")

    if mejor is None: return None
    x_opt = np.clip(mejor.x, 0, 1); x_opt /= x_opt.sum()
    p_opt = props_mezcla(x_opt)
    return {
        'proporciones': dict(zip(nombres_h, x_opt)),
        'costo_sim':  float(np.dot(x_opt, vec('costo_sim'))),
        'costo_real': float(np.dot(x_opt, vec('costo_real'))),
        **p_opt,
        'pct_alt': sum(x_opt[i] for i in idx_alt)*100,
    }

# ══════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🍞 Formulador\n*Marraqueta · DSS*")
    st.markdown(
        '<div style="background:#1e3a5f18;border-radius:7px;padding:7px 10px;'
        'font-size:.73rem;color:#475569;margin-bottom:8px;">'
        '⚡ <b>Modo Innovación:</b> relaja límites normativos — '
        'cenizas ≤1%, absorción ≤70%, proteína ≤20%</div>',
        unsafe_allow_html=True)
    modo_innov = st.toggle("⚡ Modo Innovación", False)
    usar_ibis  = st.toggle("🧪 Mejorador IBIS (0.4%)", True,
        help="Lesaffre: CaCO₃ + ácido ascórbico + complejo enzimático. Dosis fija 0.4%.")
    receta_id  = st.selectbox("Receta base", list(RECETAS.keys()))

    harinas_base = {k:v for k,v in HARINAS.items() if v['tipo']=='base'}
    harinas_alt  = {k:v for k,v in HARINAS.items() if v['tipo']=='alternativa'}
    sl_h, sl_a   = {}, {}

    st.markdown('<div class="sec">Harinas Base</div>', unsafe_allow_html=True)
    for nm in harinas_base:
        val_key = f"val_{nm}"   # clave de valor (separada del widget)
        default = st.session_state.get(val_key, 85 if 'trigo' in nm.lower() else 50)
        sl_h[nm] = st.slider(f"{nm} (%)", 0, 100, int(default), 1, key=f"sl_{nm}",
                             on_change=lambda n=nm: st.session_state.update(
                                 {f"val_{n}": st.session_state[f"sl_{n}"]}))

    st.markdown('<div class="sec">Harinas Alternativas</div>', unsafe_allow_html=True)
    for nm in harinas_alt:
        val_key = f"val_{nm}"
        default = st.session_state.get(val_key, 0)
        sl_h[nm] = st.slider(f"{nm} (%)", 0, MAX_ALT.get(nm,20),
                             int(default), 1, key=f"sl_{nm}",
                             on_change=lambda n=nm: st.session_state.update(
                                 {f"val_{n}": st.session_state[f"sl_{n}"]}))

    st.markdown('<div class="sec">Aditivos (máx 3%)</div>', unsafe_allow_html=True)
    for nm in ADITIVOS:
        if IBIS_KEY and nm == IBIS_KEY: continue
        val_key = f"val_{nm}"
        default = st.session_state.get(val_key, 0.0)
        sl_a[nm] = st.slider(f"{nm} (%)", 0.0, 3.0, float(default), 0.1,
                             key=f"sl_{nm}",
                             on_change=lambda n=nm: st.session_state.update(
                                 {f"val_{n}": st.session_state[f"sl_{n}"]}))

    st.markdown('<div class="sec">Escalado</div>', unsafe_allow_html=True)
    kg_harina = st.number_input("Base de harina (kg)", 0.5, 500.0, KG_H_DEFAULT, 0.5)

    if st.button("🔄 Recargar Excel", use_container_width=True):
        st.cache_data.clear(); st.rerun()

# ── Proporciones manuales
ph = {k: v/100 for k,v in sl_h.items()}
pa = {k: v/100 for k,v in sl_a.items()}
if usar_ibis and IBIS_KEY:
    pa[IBIS_KEY] = IBIS_DOSIS/100

total_harinas = sum(sl_h.values()) + sum(sl_a.values())
total_adi     = sum(sl_a.values())
mez     = calcular_mezcla(ph, pa)
rec_esc = escalar(ph, pa, receta_id, mez.get('absorcion',60), kg_harina)
costos  = calcular_costos_totales(ph, pa, receta_id, mez.get('absorcion',60))

# ══════════════════════════════════════════════════════════════════════
# CABECERA
# ══════════════════════════════════════════════════════════════════════
st.markdown(
    f'<div style="display:flex;align-items:center;gap:18px;'
    f'padding-bottom:10px;border-bottom:2px solid #e67e22;margin-bottom:4px;">'
    f'<img src="data:image/png;base64,{LOGO_UDD_B64}" '
    f'style="height:52px;width:auto;object-fit:contain;" '
    f'alt="Universidad del Desarrollo — Facultad de Ingeniería"/>'
    f'<div>'
    f'<div style="font-size:1.35rem;font-weight:700;color:#1e3a5f;line-height:1.2;">'
    f'Formulador de Mezclas de Harinas</div>'
    f'<div style="font-size:.82rem;color:#64748b;">'
    f'Innovación en Panificación Chilena · Marraqueta · '
    f'<code style="font-size:.75rem;color:#16a34a;">{os.path.basename(EXCEL_PATH)}</code>'
    f'</div></div></div>',
    unsafe_allow_html=True)

dif = abs(total_harinas - 100)
if total_adi > 3.0:
    st.error(f"❌ Aditivos variables: {total_adi:.1f}% — supera el máximo normativo (3%)")

# ══════════════════════════════════════════════════════════════════════
# TRES COLUMNAS
# ══════════════════════════════════════════════════════════════════════
c1, c2, c3 = st.columns([1.05, 1.45, 1.05], gap="large")

# ── COL 1
with c1:
    # Propiedades normativas determinantes (en orden de importancia)
    # Cenizas queda fuera del conteo normativo — pasa a referencia informativa
    PROPS_MODELO = {'W','PL','tenacidad','extension','absorcion','proteina'}
    PROPS_REFERENCIA_EXTRA = {'cenizas','humedad','fibra','lipidos','C3','C5'}

    n_ok = n_falla = n_sem = 0
    for clave in ['W','PL','tenacidad','extension','absorcion','proteina']:
        if clave not in LIMITES: continue
        val = mez.get(clave, 0)
        if val == 0 and clave in ('W','PL','tenacidad','extension'): continue
        ico,_,_,_ = semaforo(val, clave, modo_innov)
        n_sem += 1
        if ico == "❌": n_falla += 1
        elif ico in ("✅","⚠️","⚡"): n_ok += 1

    n_cumple  = n_sem - n_falla
    n_marginal = sum(1 for clave in PROPS_MODELO
                     if clave in LIMITES
                     and mez.get(clave,0) != 0
                     and semaforo(mez.get(clave,0), clave, modo_innov)[0] == "⚠️")

    # Veredicto rediseñado: positivo cuando cumple, informativo cuando no
    if n_falla == 0:
        col_r = "#22c55e"
        icono_v = "✅"
        titulo_v = "Receta viable para marraqueta"
        sub_v = (f"{n_cumple}/{n_sem} propiedades dentro de rango normativo"
                 + (f" · {n_marginal} cerca del límite" if n_marginal else ""))
    elif n_falla <= 2:
        col_r = "#f59e0b"
        icono_v = "⚠️"
        titulo_v = f"Receta con {n_falla} propiedad{'es' if n_falla>1 else ''} fuera de rango"
        sub_v = f"{n_cumple}/{n_sem} cumplen · ajusta los sliders o activa Modo Innovación"
    else:
        col_r = "#ef4444"
        icono_v = "🔴"
        titulo_v = f"{n_cumple}/{n_sem} propiedades dentro de rango"
        sub_v = f"{n_falla} fuera de norma · revisa el semáforo para ver cuáles ajustar"

    st.markdown(
        f'<div style="background:{col_r}12;border:2px solid {col_r};'
        f'border-radius:9px;padding:10px 15px;margin-bottom:10px;">'
        f'<div style="font-size:1.0rem;font-weight:700;color:{col_r};">'
        f'{icono_v} {titulo_v}</div>'
        f'<div style="font-size:.72rem;color:#475569;margin-top:2px;">{sub_v}</div>'
        f'</div>', unsafe_allow_html=True)

    # ── Guardar formulación
    st.markdown('<div class="sec">Guardar esta formulación</div>', unsafe_allow_html=True)
    nombre_form = st.text_input("Nombre de la receta", placeholder="Ej: Marraqueta 15% garbanzo",
                                label_visibility="collapsed")
    if st.button("💾 Guardar formulación", use_container_width=True):
        if nombre_form.strip():
            if 'formulaciones' not in st.session_state:
                st.session_state['formulaciones'] = {}
            st.session_state['formulaciones'][nombre_form.strip()] = {
                'nombre':      nombre_form.strip(),
                'composicion': {k: round(v*100,2) for k,v in ph.items() if v > 0.001},
                'aditivos':    {k: round(v*100,2) for k,v in pa.items() if v > 0.001},
                'propiedades': {k: round(mez.get(k,0),3)
                                for k in ['proteina','W','PL','absorcion','cenizas','fibra']},
                'costo_sim':   round(costos['c_h_sim'],0),
                'costo_real':  round(costos['c_h_real'],0),
                'costo_pan_sim':  round(costos['c_total_pan_sim'],1),
                'costo_pan_real': round(costos['c_total_pan_real'],1),
                'margen_sim':  round(costos['margen_pct_sim'],1),
                'viable':      n_falla == 0,
                'n_cumple':    n_cumple,
                'n_sem':       n_sem,
                'pct_alt':     round(mez.get('pct_alt',0),1),
            }
            st.success(f"✓ Guardada: {nombre_form.strip()}")
        else:
            st.warning("Escribe un nombre para la formulación antes de guardar.")

    st.markdown('<div class="sec">Composición</div>', unsafe_allow_html=True)
    filas = [{"Ingrediente": nm, "%": pct, "Tipo": HARINAS[nm]['tipo'].capitalize()}
             for nm, pct in sl_h.items() if pct > 0]
    filas += [{"Ingrediente": nm, "%": round(v*100,1), "Tipo": "Aditivo"}
              for nm, v in pa.items() if v > 0]
    if filas:
        st.dataframe(pd.DataFrame(filas), use_container_width=True,
                     hide_index=True, height=190)
        st.markdown(f"**Alt:** {mez.get('pct_alt',0):.1f}% · **Aditivos:** {mez.get('pct_adi',0):.1f}%")

    st.markdown('<div class="sec">Costo de harinas</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:.71rem;color:#64748b;margin-bottom:5px;">Solo mezcla harinas + aditivos</div>', unsafe_allow_html=True)
    ca, cb = st.columns(2)
    with ca:
        st.markdown(f'<div class="mcard"><div class="mlabel">Simulado (ODEPA)</div><div class="mval">${costos["c_h_sim"]:,.0f}<span class="munit">/kg</span></div></div>', unsafe_allow_html=True)
    with cb:
        st.markdown(f'<div class="mcard"><div class="mlabel">Real Mercado</div><div class="mval">${costos["c_h_real"]:,.0f}<span class="munit">/kg</span></div></div>', unsafe_allow_html=True)

    st.markdown('<div class="sec">Costo total producción</div>', unsafe_allow_html=True)
    st.markdown(
        '<div style="font-size:.71rem;color:#64748b;margin-bottom:7px;">'
        'Desglose por ítem — costo simulado por marraqueta</div>',
        unsafe_allow_html=True)

    # Costo total por marraqueta simulado (desglosado)
    c_pan_s = costos['c_pan_sim']
    c_op    = costos['c_op_por_pan']
    c_total = costos['c_total_pan_sim']

    items_costo = [
        ("Harinas y aditivos", costos['c_h_sim'] * (rec_esc['masa_kg']/kg_harina) * (PESO_PAN_G/1000) * RENDIMIENTO
         if rec_esc else c_pan_s - costos['c_ins'] * (PESO_PAN_G/1000),
         "#1e3a5f"),
        ("Insumos (agua, lev., sal, IBIS)", costos['c_ins'] * (PESO_PAN_G / 1000),
         "#2563eb"),
        ("Mano de obra", costos['desglose_op'].get('Mano de obra', 0), "#7c3aed"),
        ("Energía horneado",               costos['desglose_op'].get('Energía horno', 0), "#0891b2"),
        ("Packaging",                      costos['desglose_op'].get('Packaging', 0),     "#059669"),
    ]
    # Recalcular harinas correctamente
    masa_f_local = rec_esc['masa_kg'] / kg_harina if rec_esc and kg_harina > 0 else 1.0
    panes_por_kg = masa_f_local * RENDIMIENTO * 1000 / PESO_PAN_G
    items_costo[0] = ("Harinas y aditivos",
                      costos['c_h_sim'] / panes_por_kg if panes_por_kg > 0 else 0,
                      "#1e3a5f")
    items_costo[1] = ("Insumos (agua, lev., sal, IBIS)",
                      costos['c_ins'] / panes_por_kg if panes_por_kg > 0 else 0,
                      "#2563eb")

    max_val = max(v for _,v,_ in items_costo) if items_costo else 1

    barra_rows = ""
    for label, val, color in items_costo:
        pct_bar = val / c_total * 100 if c_total > 0 else 0
        ancho   = val / max_val * 100 if max_val > 0 else 0
        barra_rows += (
            f'<tr>'
            f'<td style="padding:3px 8px;font-size:.75rem;color:#334155;width:44%;">{label}</td>'
            f'<td style="padding:3px 8px;width:36%;">'
            f'<div style="background:#e2e8f0;border-radius:4px;height:10px;overflow:hidden;">'
            f'<div style="background:{color};width:{ancho:.0f}%;height:10px;border-radius:4px;"></div>'
            f'</div></td>'
            f'<td style="padding:3px 8px;font-size:.75rem;font-weight:600;color:{color};'
            f'text-align:right;width:10%;">${val:.1f}</td>'
            f'<td style="padding:3px 8px;font-size:.72rem;color:#94a3b8;'
            f'text-align:right;width:10%;">{pct_bar:.0f}%</td>'
            f'</tr>')

    st.markdown(
        f'<table style="width:100%;border-collapse:collapse;">{barra_rows}</table>'
        f'<div style="border-top:1px solid #e2e8f0;margin-top:4px;padding-top:4px;'
        f'display:flex;justify-content:space-between;align-items:center;">'
        f'<span style="font-size:.77rem;font-weight:700;color:#1e293b;">Total / marraqueta</span>'
        f'<span style="font-size:.88rem;font-weight:700;color:#1e3a5f;">${c_total:.1f} sim</span>'
        f'<span style="font-size:.77rem;color:#64748b;">${costos["c_total_pan_real"]:.1f} real</span>'
        f'</div>', unsafe_allow_html=True)

    # Margen bruto
    col_ms = "#22c55e" if costos['margen_sim'] > 0 else "#ef4444"
    col_mr = "#22c55e" if costos['margen_real'] > 0 else "#ef4444"
    st.markdown(
        f'<div style="background:#f8fafc;border-radius:7px;padding:8px 10px;'
        f'margin-top:6px;font-size:.77rem;">'
        f'💰 <b>Precio venta:</b> ${costos["precio_venta"]:,.0f}/unidad '
        f'<span style="color:#94a3b8;">(editar en Excel)</span><br>'
        f'📈 <b>Margen bruto:</b> '
        f'<span style="color:{col_ms};font-weight:700;">'
        f'${costos["margen_sim"]:,.1f} ({costos["margen_pct_sim"]:.1f}%)</span> sim · '
        f'<span style="color:{col_mr};">'
        f'${costos["margen_real"]:,.1f} ({costos["margen_pct_real"]:.1f}%)</span> real<br>'
        f'<span style="color:#94a3b8;font-size:.69rem;">'
        f'Merma proceso: {costos["merma_pct"]:.0f}% · '
        f'Objetivo: {MARGEN_OBJ*100:.0f}% · '
        f'Todos los precios desde Excel → hoja PRECIOS_INSUMOS</span>'
        f'</div>', unsafe_allow_html=True)

    with st.expander("Ver desglose insumos y operacionales"):
        st.markdown("**Insumos panaderos:**")
        for ins, c in costos['desglose'].items():
            st.markdown(f'<div style="display:flex;justify-content:space-between;font-size:.77rem;padding:2px 4px;color:#475569;"><span>{ins}</span><span>${c:,.0f}/kg har.</span></div>', unsafe_allow_html=True)
        st.markdown("**Costos operacionales:**")
        for ins, c in costos['desglose_op'].items():
            st.markdown(f'<div style="display:flex;justify-content:space-between;font-size:.77rem;padding:2px 4px;color:#475569;"><span>{ins}</span><span>${c:,.1f}/unid.</span></div>', unsafe_allow_html=True)
        st.markdown('<div style="font-size:.69rem;color:#94a3b8;margin-top:4px;">Todos los precios editables en Excel → hoja PRECIOS_INSUMOS</div>', unsafe_allow_html=True)

# ── COL 2: Semáforo + Optimizador
with c2:
    st.markdown('<div class="sec">Propiedades Proyectadas + Semáforo</div>', unsafe_allow_html=True)

    adi_activos = {nm: round(v*100,1) for nm,v in pa.items() if v > 0}
    if adi_activos:
        efx = [f"{p} {'+' if d*pct>0 else ''}{d*pct:.1f}"
               for nm,pct in adi_activos.items()
               for p,d in EFECTOS.get(nm,{}).items() if d != 0]
        st.markdown(
            f'<div style="background:#eff6ff;border-radius:7px;padding:7px 11px;'
            f'font-size:.73rem;color:#1e40af;margin-bottom:7px;">'
            f'⚗️ <b>Efectos aditivos:</b> {" | ".join(efx)}</div>',
            unsafe_allow_html=True)

    st.markdown(
        f'<div style="display:flex;gap:8px;padding:5px 10px;background:#1e3a5f;'
        f'border-radius:7px 7px 0 0;margin-bottom:2px;">'
        f'<span style="width:22px;"></span>'
        f'<span style="flex:1;font-size:.72rem;font-weight:700;color:white;">Propiedad</span>'
        f'<span style="width:70px;font-size:.72rem;font-weight:700;color:white;text-align:right;">Valor</span>'
        f'<span style="width:85px;font-size:.72rem;font-weight:700;color:#94a3b8;text-align:center;">Rango</span>'
        f'<span style="width:130px;font-size:.72rem;font-weight:700;color:white;">Estado</span></div>',
        unsafe_allow_html=True)

    st.markdown('<div style="font-size:.69rem;color:#64748b;padding:2px 10px;background:#f1f5f9;border-left:3px solid #1e3a5f;margin-bottom:3px;">NORMATIVOS (NCh 1237) — propiedades determinantes</div>', unsafe_allow_html=True)
    for clave, label, unidad in [
        ("W",         "Fuerza W",          ""),
        ("PL",        "Relación P/L",      ""),
        ("tenacidad", "Tenacidad P",       "mm"),
        ("extension", "Extensibilidad L",  "mm"),
        ("absorcion", "Absorción agua",    "%"),
        ("proteina",  "Proteína",          "%"),
    ]:
        val = mez.get(clave, 0)
        rng = rango_str(clave)
        if val == 0 and clave in ('W','PL','tenacidad','extension'):
            ico,bg,ct,msg = "—","#f1f5f9","#94a3b8","Dilución del trigo"
        else:
            ico,bg,ct,msg = semaforo(val, clave, modo_innov)
        st.markdown(f'<div class="srow" style="background:{bg};"><span style="font-size:.9rem;width:22px;">{ico}</span><span class="slbl">{label}</span><span class="sval">{val:.2f}{unidad}</span><span class="srng">{rng}</span><span class="smsg" style="color:{ct};">{msg}</span></div>', unsafe_allow_html=True)

    st.markdown('<div style="font-size:.69rem;color:#0369a1;padding:2px 10px;background:#f0f9ff;border-left:3px solid #0369a1;margin:5px 0 3px 0;">📊 REFERENCIA (informativo, sin impacto en veredicto)</div>', unsafe_allow_html=True)
    for clave, label, unidad in [
        ("cenizas",  "Cenizas",           "%"),
        ("fibra",    "Fibra total",       "%"),
        ("lipidos",  "Lípidos",           "%"),
        ("C3",       "Gelatinización C3", ""),
        ("C5",       "Retrogradación C5", ""),
    ]:
        val = mez.get(clave, 0)
        ico,bg,ct,msg = semaforo(val, clave, modo_innov)
        st.markdown(f'<div class="srow" style="background:{bg};"><span style="font-size:.9rem;width:22px;">{ico}</span><span class="slbl">{label}</span><span class="sval">{val:.2f}{unidad}</span><span class="srng">{rango_str(clave)}</span><span class="smsg" style="color:{ct};">{msg}</span></div>', unsafe_allow_html=True)

    if modo_innov:
        st.markdown('<div style="background:#fff7ed;border:1px solid #f59e0b;border-radius:7px;padding:7px 11px;font-size:.77rem;color:#92400e;margin-top:6px;">⚡ Modo Innovación: cenizas ≤1.0%, absorción ≤70%, proteína ≤20%</div>', unsafe_allow_html=True)

    # ── MOTOR DE OPTIMIZACIÓN (compacto con expander)
    st.markdown('<div class="sec" style="margin-top:14px;">Motor de Optimización</div>',
                unsafe_allow_html=True)
    st.markdown(
        '<div style="font-size:.71rem;color:#64748b;margin-bottom:8px;">'
        'Encuentra la mezcla de menor costo que cumple los límites normativos.</div>',
        unsafe_allow_html=True)

    with st.expander("⚙️ Configurar optimización", expanded=False):
        col_opt1, col_opt2 = st.columns(2)
        with col_opt1:
            nivel_opt = st.slider("Mín. harinas alternativas (%)", 0, 40, 15, 5,
                help="Sin este mínimo el algoritmo elige 100% trigo.")
        with col_opt2:
            costo_opt = st.radio("Minimizar", ["Simulado","Real"], horizontal=True)

    if st.button("🔍 Optimizar Receta", use_container_width=True, type="primary"):
        with st.spinner("Optimizando..."):
            res_opt = optimizar_receta(
                nivel_alt_target=nivel_opt/100,
                usar_ibis_opt=usar_ibis,
                tipo_costo='sim' if costo_opt=="Simulado" else 'real'
            )
        if res_opt:
            st.session_state['res_opt'] = res_opt
            for nm in list(HARINAS.keys()):
                st.session_state[f"val_{nm}"] = 0
            for nm, frac in res_opt['proporciones'].items():
                if nm in HARINAS:
                    pct = round(frac * 100)
                    max_sl = 100 if HARINAS[nm]['tipo']=='base' else MAX_ALT.get(nm,20)
                    st.session_state[f"val_{nm}"] = min(pct, max_sl)
            st.rerun()
        else:
            st.error("Sin solución. Prueba reducir el % mínimo de alternativas.")

# ── COL 3: Receta
with c3:
    st.markdown(f'<div class="sec">Receta: {receta_id} · {kg_harina:.1f} kg</div>', unsafe_allow_html=True)
    if rec_esc:
        st.markdown(f'<div style="font-size:.72rem;color:#64748b;margin-bottom:5px;">Agua: <b>{rec_esc["agua_pct"]:.1f}%</b> · Receta Lefersa · sin manteca</div>', unsafe_allow_html=True)
        rows = ""
        for ing, g in rec_esc['ingredientes'].items():
            nm_c = ing.split('(')[0].strip()
            if nm_c in HARINAS:
                bg_i = "#dbeafe" if HARINAS[nm_c]['tipo']=='base' else "#dcfce7"
            elif nm_c in ADITIVOS or 'ibis' in ing.lower() or 'mejorador' in ing.lower():
                bg_i = "#fef3c7"
            else: bg_i = "#f1f5f9"
            rows += (f'<tr style="background:{bg_i};"><td style="padding:4px 8px;font-size:.79rem;color:#1e293b;">{ing}</td>'
                     f'<td style="padding:4px 8px;font-size:.79rem;text-align:right;font-weight:600;color:#1e293b;">{g:,.1f} g</td></tr>')
        st.markdown(f'<table style="width:100%;border-collapse:collapse;"><tr style="background:#1e3a5f;color:white;"><th style="padding:5px 8px;text-align:left;font-size:.76rem;">Ingrediente</th><th style="padding:5px 8px;text-align:right;font-size:.76rem;">Cantidad</th></tr>{rows}</table>', unsafe_allow_html=True)

        # ── Desglose paso a paso — proceso real de elaboración de marraqueta
        masa_cruda     = rec_esc['masa_kg']
        pan_final      = rec_esc['pan_kg']
        unidades       = rec_esc['unidades']
        g_por_bollo    = PESO_PAN_G / 2
        pct_ferm       = 2.0
        masa_post_ferm = masa_cruda * (1 - pct_ferm/100)

        pasos = [
            ("#dbeafe","#1d4ed8","① Amasado",
             f"{masa_cruda:.3f} kg",
             "Secos → agua → levadura al final. Amasar hasta desarrollo completo."),
            ("#dcfce7","#15803d","② Sobado y bollado",
             f"{unidades} bollos × {g_por_bollo:.0f}g",
             f"Sobadora 5–6 veces. Bollos {g_por_bollo:.0f}–{g_por_bollo+10:.0f}g. Unir de a dos."),
            ("#fef9c3","#854d0e","③ 1ª fermentación",
             "30–40 min",
             "Tablas enharinadas. Tiempo según temperatura ambiente."),
            ("#fed7aa","#c2410c","④ Doblado + 2ª ferm.",
             "45–90 min",
             "Dobladora → género → reposar hasta que esté 'gordita'."),
            ("#fce7f3","#9d174d","⑤ Cocción",
             f"{pan_final:.3f} kg → {unidades} un.",
             f"195–200°C · 10 min + vaporazo + 5 min. Rendimiento: {pan_final/masa_cruda*100:.1f}%."),
        ]

        cards_html = '<div style="display:flex;flex-direction:column;gap:5px;margin-top:9px;">'
        for bg_p, txt_p, etapa, resultado, detalle in pasos:
            cards_html += (
                f'<div style="background:{bg_p};border-radius:7px;padding:7px 10px;'
                f'display:flex;align-items:flex-start;gap:8px;">'
                f'<div style="min-width:120px;">'
                f'<div style="font-size:.76rem;font-weight:700;color:{txt_p};">{etapa}</div>'
                f'<div style="font-size:.78rem;font-weight:600;color:#1e293b;margin-top:1px;">'
                f'{resultado}</div></div>'
                f'<div style="font-size:.70rem;color:#475569;line-height:1.4;">{detalle}</div>'
                f'</div>')
        cards_html += (
            f'</div><div style="font-size:.67rem;color:#94a3b8;margin-top:4px;">'
            f'Fuente: proceso documentado · {g_por_bollo:.0f}–{g_por_bollo+10:.0f}g/bollo · '
            f'195-200°C con vaporazo</div>')

        st.markdown(cards_html, unsafe_allow_html=True)

st.divider()

# ══════════════════════════════════════════════════════════════════════
# SECCIÓN: MEJOR RECETA POR HARINA ALTERNATIVA
# ══════════════════════════════════════════════════════════════════════


# ══════════════════════════════════════════════════════════════════════
# SECCIÓN: MEJOR RECETA POR HARINA ALTERNATIVA

st.markdown("### 🌾 Mejor receta por harina alternativa")
st.markdown(
    '<div style="font-size:.79rem;color:#64748b;margin-bottom:14px;">'
    'Selecciona una o varias harinas alternativas y presiona <b>Optimizar selección</b>. '
    'El sistema encontrará la mejor receta usando solo esas harinas + trigo + aditivos, '
    'evaluando niveles de 5% a 20% de sustitución total.</div>',
    unsafe_allow_html=True)

cfg1, cfg2 = st.columns(2)
with cfg1:
    costo_sec = st.radio("Minimizar costo", ["Simulado (ODEPA)","Real (Mercado)"],
                          horizontal=True, key="costo_sec")
with cfg2:
    ibis_sec = st.checkbox("Incluir Mejorador IBIS (0.4%)", value=True, key="ibis_sec")

st.markdown("")

# Checkboxes de selección por harina
NIVELES_SEC = [0.05, 0.10, 0.15, 0.20]
harinas_alt_lista = [k for k,v in HARINAS.items() if v['tipo']=='alternativa']

# Inicializar selección en session_state
if 'sel_harinas' not in st.session_state:
    st.session_state['sel_harinas'] = []

st.markdown(
    '<div style="font-size:.77rem;color:#475569;margin-bottom:6px;">'
    'Selecciona las harinas a incluir:</div>', unsafe_allow_html=True)

check_cols = st.columns(len(harinas_alt_lista))
for col_c, harina_obj in zip(check_cols, harinas_alt_lista):
    with col_c:
        sel = st.checkbox(
            harina_obj,
            value=(harina_obj in st.session_state['sel_harinas']),
            key=f"check_{harina_obj}")
        if sel and harina_obj not in st.session_state['sel_harinas']:
            st.session_state['sel_harinas'].append(harina_obj)
        elif not sel and harina_obj in st.session_state['sel_harinas']:
            st.session_state['sel_harinas'].remove(harina_obj)

sel_actual = st.session_state['sel_harinas']

# Mostrar etiqueta de combinación seleccionada
if sel_actual:
    combo_label = " + ".join(sel_actual)
    st.markdown(
        f'<div style="background:#eff6ff;border-radius:7px;padding:7px 12px;'
        f'font-size:.78rem;color:#1e40af;margin:6px 0;">'
        f'🔬 Combinación seleccionada: <b>{combo_label} + Trigo</b></div>',
        unsafe_allow_html=True)
else:
    st.markdown(
        '<div style="background:#f8fafc;border-radius:7px;padding:7px 12px;'
        'font-size:.78rem;color:#94a3b8;margin:6px 0;">'
        'Selecciona al menos una harina alternativa</div>',
        unsafe_allow_html=True)

btn_disabled = len(sel_actual) == 0
if st.button("🔍 Optimizar selección", use_container_width=True,
             type="primary", disabled=btn_disabled):
    tipo_c2 = 'sim' if 'Simulado' in costo_sec else 'real'
    mejores2 = []
    with st.spinner(f"Optimizando {' + '.join(sel_actual)}..."):
        # Nivel total de alternativas a evaluar
        niveles_a_probar = NIVELES_SEC
        # Para combinaciones de 2+ harinas, probar también niveles más altos
        if len(sel_actual) >= 2:
            niveles_a_probar = [0.10, 0.15, 0.20, 0.25]

        for nivel in niveles_a_probar:
            # Verificar que el nivel sea factible con las harinas seleccionadas
            max_posible = sum(MAX_ALT.get(h, 20)/100 for h in sel_actual)
            if nivel > max_posible: continue

            res2 = optimizar_receta(
                nivel_alt_target=nivel,
                usar_ibis_opt=ibis_sec,
                tipo_costo=tipo_c2,
                harinas_permitidas=sel_actual,   # solo estas alternativas
            )
            if res2:
                n_f2 = sum(
                    1 for clave in ['W','PL','tenacidad','extension','absorcion','proteina']
                        if clave in LIMITES
                    and res2.get(clave,0) != 0
                    and semaforo(res2.get(clave,0), clave, False)[0] == "❌"
                )
                mejores2.append({'nivel': nivel, 'res': res2, 'n_fallas': n_f2,
                                 'combo': list(sel_actual)})

    if mejores2:
        mejor2 = min(mejores2, key=lambda r: (r['n_fallas'], r['res']['costo_sim']))
        st.session_state['sec_resultado'] = mejor2
        if 'sec_historial' not in st.session_state:
            st.session_state['sec_historial'] = []
        st.session_state['sec_historial'].append(mejor2)

        # ── Actualizar sliders para que toda la app se sincronice
        mz_opt = mejor2['res']
        # Sincronizar sliders via val_ (no modificar sl_ directamente)
        for nm in list(HARINAS.keys()):
            st.session_state[f"val_{nm}"] = 0
        for nm, frac in mz_opt['proporciones'].items():
            if nm in HARINAS:
                pct = round(frac * 100)
                max_sl = 100 if HARINAS[nm]['tipo'] == 'base' else MAX_ALT.get(nm, 20)
                st.session_state[f"val_{nm}"] = min(pct, max_sl)
        st.rerun()   # recarga toda la app con los nuevos valores
    else:
        st.session_state['sec_resultado'] = None
        st.error("Sin solución factible para esta combinación. Prueba otras harinas.")

# Mostrar resultado actual
if 'sec_resultado' in st.session_state and st.session_state['sec_resultado']:
    dato = st.session_state['sec_resultado']
    mz2   = dato['res']; niv2 = dato['nivel']; n_f2 = dato['n_fallas']
    combo = dato.get('combo', sel_actual)
    col_v2 = "#22c55e" if n_f2==0 else "#f59e0b" if n_f2<=2 else "#ef4444"
    viab2  = "✅ Viable" if n_f2==0 else f"⚠️ {n_f2} prop. fuera de rango"

    rc1, rc2, rc3 = st.columns([1.2, 1.2, 1])
    with rc1:
        rows2 = "".join(
            f'<tr style="background:{"#dbeafe" if HARINAS.get(nm,{}).get("tipo")=="base" else "#dcfce7"};">'
            f'<td style="padding:4px 9px;font-size:.80rem;color:#1e293b;">{nm}</td>'
            f'<td style="padding:4px 9px;font-size:.80rem;font-weight:600;'
            f'color:#1e293b;text-align:right;">{round(frac*100,1):.1f}%</td></tr>'
            for nm,frac in mz2['proporciones'].items() if frac > 0.005)
        st.markdown(
            f'<div style="border:2px solid {col_v2};border-radius:9px;padding:12px 13px;">'
            f'<div style="font-size:.82rem;font-weight:700;color:{col_v2};margin-bottom:7px;">'
            f'{viab2} · {niv2*100:.0f}% alternativas · {" + ".join(combo)}</div>'
            f'<table style="width:100%;border-collapse:collapse;">'
            f'<tr style="background:#1e3a5f;color:white;">'
            f'<th style="padding:4px 9px;font-size:.74rem;text-align:left;">Harina</th>'
            f'<th style="padding:4px 9px;font-size:.74rem;text-align:right;">%</th>'
            f'</tr>{rows2}</table></div>', unsafe_allow_html=True)
    with rc2:
        st.markdown(
            f'<div style="background:#f8fafc;border-radius:9px;padding:12px 13px;'
            f'font-size:.79rem;color:#475569;line-height:2.0;height:100%;">'
            f'<b style="color:#1e3a5f;">Propiedades proyectadas</b><br>'
            f'W: <b>{mz2["W"]:.0f}</b> · P/L: <b>{mz2["PL"]:.2f}</b><br>'
            f'Proteína: <b>{mz2["proteina"]:.2f}%</b><br>'
            f'Absorción: <b>{mz2["absorcion"]:.1f}%</b><br>'
            f'Cenizas: <b>{mz2["cenizas"]:.3f}%</b><br>'
            f'<b style="color:#1e3a5f;">Costos (harinas)</b><br>'
            f'Sim: <b>${mz2["costo_sim"]:,.0f}/kg</b><br>'
            f'Real: <b>${mz2["costo_real"]:,.0f}/kg</b>'
            f'</div>', unsafe_allow_html=True)
    with rc3:
        st.markdown('<div style="padding-top:4px;">', unsafe_allow_html=True)
        nombre_guard = st.text_input(
            "Nombre para guardar", placeholder="Ej: Lentejas 15%",
            key="nombre_sec_guard", label_visibility="collapsed")
        if st.button("💾 Guardar esta receta", use_container_width=True,
                     key="guardar_sec"):
            nm_g = nombre_guard.strip() or f"{' + '.join(combo)} {niv2*100:.0f}%"
            if 'formulaciones' not in st.session_state:
                st.session_state['formulaciones'] = {}
            st.session_state['formulaciones'][nm_g] = {
                'nombre': nm_g,
                'composicion': {k: round(v*100,2) for k,v in mz2['proporciones'].items() if v > 0.001},
                'aditivos': {},
                'propiedades': {k: round(mz2.get(k,0),3)
                                for k in ['proteina','W','PL','absorcion','cenizas','fibra']},
                'costo_sim':   round(mz2['costo_sim'],0),
                'costo_real':  round(mz2['costo_real'],0),
                'costo_pan_sim':  0,
                'costo_pan_real': 0,
                'margen_sim': 0,
                'viable':  n_f2 == 0,
                'n_cumple': max(0, len(PROPS_MODELO) - n_f2),
                'n_sem':    len(PROPS_MODELO),
                'pct_alt':  round(mz2.get('pct_alt',0),1),
            }
            st.success(f"✓ Guardada: {nm_g}")
        st.markdown('</div>', unsafe_allow_html=True)

# Historial de combinaciones evaluadas
if 'sec_historial' in st.session_state and len(st.session_state['sec_historial']) >= 2:
    st.markdown("**Historial de combinaciones evaluadas:**")
    filas_hist = []
    for dato_h in st.session_state['sec_historial']:
        mz_h = dato_h['res']; n_f_h = dato_h['n_fallas']
        filas_hist.append({
            'Combinación':      " + ".join(dato_h.get('combo',[])),
            '% sust.':          round(dato_h['nivel']*100),
            'W':                round(mz_h['W']),
            'P/L':              round(mz_h['PL'],3),
            'Proteína (%)':     round(mz_h['proteina'],2),
            'Cenizas (%)':      round(mz_h['cenizas'],3),
            'Costo sim ($/kg)': round(mz_h['costo_sim']),
            'Viable':           "✅" if n_f_h==0 else f"⚠️ {n_f_h}",
        })
    st.dataframe(pd.DataFrame(filas_hist), use_container_width=True, hide_index=True)

    if st.button("🗑 Limpiar historial", key="limpiar_historial"):
        st.session_state['sec_historial'] = []
        st.session_state.pop('sec_resultado', None)
        st.rerun()

st.divider()

# ══════════════════════════════════════════════════════════════════════
# SECCIÓN INFERIOR: COMPARADOR DE FORMULACIONES + TOP RECETAS
# ══════════════════════════════════════════════════════════════════════
if 'formulaciones' in st.session_state and st.session_state['formulaciones']:
    forms = st.session_state['formulaciones']

    tab1, tab2, tab3 = st.tabs([
        "📊 Comparador de formulaciones guardadas",
        "🏆 Top recetas guardadas por harina",
        "🔬 Mejores combinaciones (optimizador)"
    ])

    # ── TAB 1: Comparador
    with tab1:
        st.markdown("### Comparador de formulaciones guardadas")
        st.markdown(
            f'<div style="font-size:.79rem;color:#64748b;margin-bottom:10px;">'
            f'{len(forms)} formulación(es) guardada(s). '
            f'Las propiedades son proyecciones del modelo — requieren validación experimental.</div>',
            unsafe_allow_html=True)

        filas_cmp = []
        for nm, f in forms.items():
            viab = "✅ Viable" if f['viable'] else f"⚠️ {f['n_cumple']}/{f['n_sem']} cumplen"
            filas_cmp.append({
                'Nombre':             nm,
                '% Alt.':             f['pct_alt'],
                'Proteína (%)':       f['propiedades'].get('proteina',0),
                'W':                  f['propiedades'].get('W',0),
                'P/L':                f['propiedades'].get('PL',0),
                'Absorción (%)':      f['propiedades'].get('absorcion',0),
                'Cenizas (%)':        f['propiedades'].get('cenizas',0),
                'Costo har. sim ($)': f['costo_sim'],
                'Total/pan sim ($)':  f['costo_pan_sim'],
                'Margen sim (%)':     f['margen_sim'],
                'Viabilidad':         viab,
            })
        df_cmp = pd.DataFrame(filas_cmp)
        st.dataframe(df_cmp, use_container_width=True, hide_index=True,
                     column_config={
                         'Margen sim (%)':     st.column_config.NumberColumn(format="%.1f%%"),
                         'Costo har. sim ($)': st.column_config.NumberColumn(format="$%.0f"),
                         'Total/pan sim ($)':  st.column_config.NumberColumn(format="$%.1f"),
                     })
        if len(forms) >= 2:
            st.markdown("**Comparación visual — propiedades clave:**")
            props_g = ['W','PL','proteina','absorcion','cenizas']
            labels_g = ['W','P/L','Proteína%','Absorción%','Cenizas%']
            df_g = pd.DataFrame([
                {'Formulación': nm,
                 **{l: f['propiedades'].get(p,0) for p,l in zip(props_g,labels_g)}}
                for nm,f in forms.items()
            ]).set_index('Formulación')
            st.bar_chart(df_g)

        if st.button("🗑 Limpiar formulaciones guardadas"):
            st.session_state['formulaciones'] = {}
            st.rerun()

    # ── TAB 2: Top recetas guardadas por harina
    with tab2:
        st.markdown("### Top recetas guardadas por harina alternativa")
        harinas_alt_nms = [k for k,v in HARINAS.items() if v['tipo']=='alternativa']
        alguna = False
        for harina_alt in harinas_alt_nms:
            grupo = {nm: f for nm,f in forms.items()
                     if any(harina_alt.lower() in ing.lower()
                            for ing in f['composicion'].keys())}
            if not grupo: continue
            alguna = True
            st.markdown(f"**🌾 {harina_alt}**")
            ordenado = sorted(grupo.items(),
                              key=lambda x: (0 if x[1]['viable'] else 1, x[1]['costo_sim']))
            for nm, f in ordenado[:3]:
                col_b = "#22c55e" if f['viable'] else "#f59e0b"
                comp_str = ", ".join(f"{h}: {p}%" for h,p in f['composicion'].items()
                                     if p > 0.5 and h != 'Trigo')
                st.markdown(
                    f'<div style="background:#f8fafc;border-radius:8px;padding:9px 13px;'
                    f'margin-bottom:6px;border-left:4px solid {col_b};">'
                    f'<b style="font-size:.82rem;color:#1e293b;">{nm}</b><br>'
                    f'<span style="font-size:.75rem;color:#475569;">'
                    f'Alt: {f["pct_alt"]}% · {comp_str}<br>'
                    f'Costo: <b>${f["costo_sim"]:,.0f}/kg</b> · '
                    f'Pan: <b>${f["costo_pan_sim"]:,.1f}</b> · '
                    f'Margen: <b>{f["margen_sim"]:.1f}%</b></span></div>',
                    unsafe_allow_html=True)
        if not alguna:
            st.info("Guarda formulaciones con harinas alternativas para ver el ranking.")

    # ── TAB 3: Mejor receta por harina (botón por harina)
    with tab3:
        st.markdown("### Mejor receta óptima por harina alternativa")
        st.markdown(
            '<div style="font-size:.79rem;color:#64748b;margin-bottom:14px;">'
            'Presiona el botón de cada harina para que el optimizador encuentre '
            'automáticamente la mejor receta usando solo esa harina alternativa + trigo + aditivos. '
            'Evalúa niveles de 5% a 20% y selecciona el de menor costo que cumpla '
            'los límites normativos (o el mejor disponible si ninguno es completamente viable).'
            '</div>', unsafe_allow_html=True)

        # Configuración
        cc1, cc2 = st.columns(2)
        with cc1:
            costo_opt3 = st.radio("Minimizar costo", ["Simulado (ODEPA)","Real (Mercado)"],
                                   horizontal=True, key="costo_opt3")
        with cc2:
            ibis_opt3 = st.checkbox("Incluir Mejorador IBIS (0.4%)", value=True,
                                     key="ibis_opt3")

        st.divider()

        harinas_alt_nms = [k for k,v in HARINAS.items() if v['tipo']=='alternativa']
        NIVELES_EVALUAR = [0.05, 0.10, 0.15, 0.20]

        # Un botón por harina alternativa — en columnas de 2
        pares = [harinas_alt_nms[i:i+2] for i in range(0, len(harinas_alt_nms), 2)]
        for par in pares:
            cols_btn = st.columns(len(par))
            for col_b, harina_obj in zip(cols_btn, par):
                with col_b:
                    key_res = f"opt_{harina_obj}"
                    if st.button(f"🌾 Optimizar con {harina_obj}",
                                 use_container_width=True, key=f"btn_{harina_obj}"):
                        tipo_c = 'sim' if 'Simulado' in costo_opt3 else 'real'
                        mejores = []
                        with st.spinner(f"Buscando mejor receta con {harina_obj}..."):
                            for nivel in NIVELES_EVALUAR:
                                max_h = MAX_ALT.get(harina_obj, 20) / 100
                                if nivel > max_h: continue
                                res = optimizar_receta(
                                    nivel_alt_target=nivel,
                                    usar_ibis_opt=ibis_opt3,
                                    tipo_costo=tipo_c,
                                    harina_forzada=harina_obj,
                                    nivel_forzado=nivel,
                                )
                                if res:
                                    # Contar fallas normativas
                                    n_f = sum(
                                        1 for clave in ['W','PL','tenacidad','extension','absorcion','proteina']
                        if clave in LIMITES
                                        and res.get(clave,0) != 0
                                        and semaforo(res.get(clave,0), clave, False)[0] == "❌"
                                    )
                                    mejores.append({'nivel': nivel, 'res': res, 'n_fallas': n_f})

                        if mejores:
                            # Seleccionar: viable primero, luego menor costo
                            mejor = min(mejores,
                                        key=lambda r: (r['n_fallas'], r['res']['costo_sim']))
                            st.session_state[key_res] = mejor
                        else:
                            st.session_state[key_res] = None

                    # Mostrar resultado si existe
                    if key_res in st.session_state:
                        dato = st.session_state[key_res]
                        if dato is None:
                            st.error("Sin solución encontrada.")
                        else:
                            mz  = dato['res']
                            niv = dato['nivel']
                            n_f = dato['n_fallas']
                            col_v = "#22c55e" if n_f==0 else "#f59e0b" if n_f<=2 else "#ef4444"
                            viab  = "✅ Viable" if n_f==0 else f"⚠️ {n_f} prop. fuera de rango"

                            # Composición
                            comp = [(nm, round(frac*100,1))
                                    for nm,frac in mz['proporciones'].items()
                                    if frac > 0.005]
                            rows_opt = "".join(
                                f'<tr style="background:{"#dbeafe" if HARINAS.get(nm,{}).get("tipo")=="base" else "#dcfce7"};">'
                                f'<td style="padding:3px 8px;font-size:.78rem;color:#1e293b;">{nm}</td>'
                                f'<td style="padding:3px 8px;font-size:.78rem;font-weight:600;'
                                f'color:#1e293b;text-align:right;">{p:.1f}%</td></tr>'
                                for nm,p in comp
                            )
                            st.markdown(
                                f'<div style="border:2px solid {col_v};border-radius:9px;'
                                f'padding:10px 12px;margin-top:8px;">'
                                f'<div style="font-size:.8rem;font-weight:700;color:{col_v};'
                                f'margin-bottom:6px;">{viab} · {niv*100:.0f}% {harina_obj}</div>'
                                f'<table style="width:100%;border-collapse:collapse;">'
                                f'<tr style="background:#1e3a5f;color:white;">'
                                f'<th style="padding:4px 8px;font-size:.73rem;text-align:left;">Harina</th>'
                                f'<th style="padding:4px 8px;font-size:.73rem;text-align:right;">%</th>'
                                f'</tr>{rows_opt}</table>'
                                f'<div style="font-size:.74rem;color:#475569;margin-top:7px;line-height:1.8;">'
                                f'W: <b>{mz["W"]:.0f}</b> · P/L: <b>{mz["PL"]:.2f}</b> · '
                                f'Proteína: <b>{mz["proteina"]:.2f}%</b><br>'
                                f'Absorción: <b>{mz["absorcion"]:.1f}%</b> · '
                                f'Cenizas: <b>{mz["cenizas"]:.3f}%</b><br>'
                                f'Costo har: <b>${mz["costo_sim"]:,.0f}/kg</b> sim · '
                                f'<b>${mz["costo_real"]:,.0f}/kg</b> real'
                                f'</div></div>',
                                unsafe_allow_html=True)

                            # Botón para cargar esta receta en los sliders
                            if st.button(f"⬆ Cargar en formulador",
                                         key=f"load_{harina_obj}", use_container_width=True):
                                for nm, frac in mz['proporciones'].items():
                                    if nm in st.session_state:
                                        st.session_state[nm] = round(frac*100)
                                st.rerun()

else:
    st.markdown(
        '<div style="background:#f8fafc;border-radius:9px;padding:16px 20px;'
        'text-align:center;border:1px dashed #cbd5e1;">'
        '<div style="font-size:.85rem;color:#64748b;">'
        '💾 Guarda formulaciones desde el panel izquierdo para comparar recetas '
        'y ver el ranking por harina alternativa.</div></div>',
        unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# ASISTENTE VIRTUAL IA — botón flotante inferior-derecho (Groq)
# ══════════════════════════════════════════════════════════════════════
from asistente_ia import render_asistente
render_asistente(mez=mez, costos=costos, ph=ph, pa=pa,
                 receta_id=receta_id, modo_innov=modo_innov,
                 LIMITES=LIMITES, HARINAS=HARINAS, semaforo=semaforo)

st.divider()
st.markdown(
    '<div style="text-align:center;font-size:.7rem;color:#94a3b8;">'
    'DSS reemplazo de ingredientes · Proyecto de título Ingeniería Civil Industrial'
    'los valores proyectados requieren validación experimental.</div>',
    unsafe_allow_html=True)
