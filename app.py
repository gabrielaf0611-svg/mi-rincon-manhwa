# -*- coding: utf-8 -*-
"""
Mi Rincon Manhwa - app personal para llevar el control de tus manhwas.
El diseno esta incrustado como HTML para verse identico al modelo.
"""
import streamlit as st
import streamlit.components.v1 as components
import json, os, base64, html
from datetime import datetime
from icons import ICON
 
st.set_page_config(page_title="Mi Rincon Manhwa", page_icon="🌸", layout="wide")
 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "manhwas.json")
COVERS_DIR = os.path.join(BASE_DIR, "data", "covers")
os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
os.makedirs(COVERS_DIR, exist_ok=True)
 
STATUSES = {"leyendo": "Leyendo", "finalizado": "Finalizado",
            "pausa": "En pausa", "cancelada": "Cancelada"}
 
 
def load():
    if os.path.exists(DATA_FILE):
        try:
            return json.load(open(DATA_FILE, encoding="utf-8"))
        except Exception:
            return []
    return []
 
 
def save(ms):
    json.dump(ms, open(DATA_FILE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
 
 
def new_id(ms):
    return (max([m["id"] for m in ms]) + 1) if ms else 1
 
 
def cover_uri(m):
    c = m.get("cover") or ""
    if not c:
        return ""
    # nuevo formato: ya es un data URI base64 guardado en el JSON
    if c.startswith("data:"):
        return c
    # formato antiguo: ruta a archivo
    p = os.path.join(BASE_DIR, c)
    if os.path.exists(p):
        ext = os.path.splitext(p)[1].lower().replace(".", "") or "png"
        if ext == "jpg":
            ext = "jpeg"
        return "data:image/" + ext + ";base64," + base64.b64encode(open(p, "rb").read()).decode()
    return ""
 
 
manhwas = load()
 
# ---- acciones por query params (vienen del iframe de tarjetas) ----
qp = st.query_params
if "tab" in qp:
    t = qp["tab"]
    if t in STATUSES or t == "todos":
        st.session_state.active_tab = t
    st.query_params.clear()
    st.rerun()
if "open" in qp:
    try:
        st.session_state.opening_id = int(qp["open"])
    except Exception:
        pass
    st.query_params.clear()
    st.rerun()
 
# ---- CSS para la parte de Streamlit ----
st.markdown(
    "<style>"
    "@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700;800&family=Nunito:wght@400;600;700&display=swap');"
    ".stApp{background:linear-gradient(160deg,#fff6fa,#ffeaf3);}"
    "html,body,[class*='css'],p,span,div,label{font-family:'Nunito','Segoe UI',sans-serif;color:#5b3a4a;}"
    ".stButton>button,.stFormSubmitButton>button{background:linear-gradient(135deg,#ff6fa5,#e85f96)!important;"
    "color:#fff!important;border:none!important;border-radius:26px!important;font-weight:800!important;"
    "font-family:'Baloo 2',sans-serif!important;padding:12px 26px!important;"
    "box-shadow:0 6px 18px rgba(255,111,165,.28)!important;}"
    ".stButton>button *,.stFormSubmitButton>button *{font-family:'Baloo 2',sans-serif!important;font-weight:800!important;color:#fff!important;}"
    ".stButton>button:hover,.stFormSubmitButton>button:hover{color:#fff!important;transform:translateY(-2px);}"
    ".stTextInput input,.stNumberInput input,.stTextArea textarea{border-radius:26px!important;border-color:#ffd6e6!important;"
    "font-family:'Nunito',sans-serif!important;color:#5b3a4a!important;padding:11px 18px!important;background:#fff!important;}"
    ".stTextInput input::placeholder{color:#d6a7bc!important;}"
    "[data-testid='stSelectbox'] div[data-baseweb='select']>div{border-radius:14px!important;border-color:#ffd6e6!important;}"
    "[data-testid='stDialog'] div[role='dialog']{border-radius:26px;border:2px solid #ffd9e8;background:#fff;}"
    "[data-testid='stFeedback'] button{color:#ffc93c!important;font-size:26px!important;background:transparent!important;"
    "box-shadow:none!important;padding:2px 4px!important;transform:none!important;}"
    "[data-testid='stFeedback'] button:hover{color:#ffb400!important;transform:scale(1.15)!important;}"
    "#MainMenu,footer,header[data-testid='stHeader']{visibility:hidden;}"
    "div.block-container{padding-top:1rem;max-width:1100px;}"
    "iframe{margin-bottom:0!important;}"
    "div[data-testid='stVerticalBlock']{gap:.5rem;}"
    ".stButton{display:flex;align-items:center;height:100%;}"
    "</style>",
    unsafe_allow_html=True,
)
 
# ---- Opening / pantalla de bienvenida (solo la primera vez) ----
if "seen_splash" not in st.session_state:
    st.session_state.seen_splash = True
    splash = st.empty()
    splash.markdown(
        "<div style='position:fixed;inset:0;z-index:99999;"
        "background:linear-gradient(160deg,#ffd9e8,#ffc4dd 55%,#ffb0d1);"
        "display:flex;align-items:center;justify-content:center;text-align:center;'>"
        "<div>"
        "<div style='font-size:72px;color:#fff;animation:beat 1.4s ease-in-out infinite;'>✿</div>"
        "<div style='font-family:Baloo 2,sans-serif;font-size:40px;color:#c94b81;"
        "text-shadow:0 2px 0 #fff;margin:10px 0 4px;font-weight:800;'>Mi Rincon Manhwa</div>"
        "<div style='color:#c06390;font-weight:700;font-family:Nunito,sans-serif;'>Tu biblioteca personal ♡</div>"
        "</div></div>"
        "<style>@keyframes beat{0%,100%{transform:scale(1)}50%{transform:scale(1.18)}}</style>",
        unsafe_allow_html=True,
    )
    import time
    time.sleep(2.2)
    splash.empty()
 
 
# ---- Diálogo: agregar o editar un manhwa ----
def file_to_datauri(cover_file):
    """Convierte la foto subida en un data URI base64 (se guarda dentro del JSON)."""
    ext = cover_file.name.split(".")[-1].lower()
    if ext == "jpg":
        ext = "jpeg"
    if ext not in ("png", "jpeg", "webp", "gif"):
        ext = "png"
    b = base64.b64encode(cover_file.getvalue()).decode()
    return "data:image/" + ext + ";base64," + b
 
 
def manhwa_dialog(editing=None):
    """editing = dict del manhwa a editar, o None para uno nuevo."""
    is_edit = editing is not None
    d = editing or {}
    rk = "rating_edit_" + str(d.get("id", "new"))
    # inicializar el rating del widget con el valor actual (solo la primera vez que abre)
    if rk not in st.session_state:
        r0 = int(d.get("rating", 0))
        st.session_state[rk] = (r0 - 1) if r0 > 0 else None
 
    with st.form("mform", clear_on_submit=False):
        title = st.text_input("Nombre *", value=d.get("title", ""), placeholder="Ej. Our sunny days")
        cover_file = st.file_uploader("Foto de portada", type=["png", "jpg", "jpeg", "webp"])
        if is_edit and d.get("cover"):
            st.caption("Ya tiene portada. Sube otra solo si quieres cambiarla.")
        author = st.text_input("Autor", value=d.get("author", ""), placeholder="Ej. Hajin")
        genre = st.text_input("Genero", value=d.get("genre", ""), placeholder="Ej. Romance, BL, Fantasia...")
        platform = st.text_input("Plataforma", value=d.get("platform", ""), placeholder="Ej. Webtoon, Telegram...")
        chapter = st.number_input("Capitulo actual", min_value=0, step=1, value=int(d.get("chapter", 0)))
        _stkeys = list(STATUSES.keys())
        status = st.selectbox("Estado", _stkeys,
                              index=_stkeys.index(d.get("status", "leyendo")) if d.get("status") in _stkeys else 0,
                              format_func=lambda k: STATUSES[k])
        st.markdown("**Rating** (opcional, ponlo cuando ya lo hayas leido)")
        rating_sel = st.feedback("stars", key=rk)
        rating = (rating_sel + 1) if rating_sel is not None else 0
        drive = st.text_input("Link de la carpeta en Drive", value=d.get("drive", ""),
                              placeholder="Pega aqui el link (opcional)")
        comment = st.text_area("Comentario", value=d.get("comment", ""), placeholder="Que te parecio?")
        submitted = st.form_submit_button("Guardar ♡")
 
    if submitted:
        if not title.strip():
            st.warning("Ponle un nombre al manhwa")
            return
        # portada: nueva subida -> base64; si no, conservar la que tenia
        cover_val = d.get("cover", "")
        if cover_file is not None:
            cover_val = file_to_datauri(cover_file)
 
        record = {
            "id": d.get("id", new_id(manhwas)),
            "title": title.strip(), "cover": cover_val,
            "author": author.strip(), "genre": genre.strip(), "platform": platform.strip(),
            "chapter": int(chapter), "status": status, "rating": int(rating),
            "drive": drive.strip(), "comment": comment.strip(),
        }
        if is_edit:
            for i, mm in enumerate(manhwas):
                if mm["id"] == d["id"]:
                    manhwas[i] = record
                    break
        else:
            manhwas.append(record)
        save(manhwas)
        if rk in st.session_state:
            del st.session_state[rk]
        st.rerun()
 
 
@st.dialog("✿ Nuevo manhwa")
def add_dialog():
    manhwa_dialog(editing=None)
 
 
@st.dialog("✏️ Editar manhwa")
def edit_dialog(m):
    manhwa_dialog(editing=m)
 
 
@st.dialog("Opciones")
def options_dialog(m):
    st.markdown("<div style='font-family:Baloo 2,sans-serif;font-size:20px;color:#c94b81;"
                "font-weight:800;margin-bottom:4px;'>" + esc(m["title"]) + "</div>",
                unsafe_allow_html=True)
    st.caption("¿Qué quieres hacer con este manhwa?")
 
    if not st.session_state.get("opt_confirm_del"):
        o1, o2 = st.columns(2)
        with o1:
            if st.button("✏️ Editar", use_container_width=True, key="opt_edit"):
                st.session_state.editing_now = m["id"]
                st.rerun()
        with o2:
            if st.button("🗑 Eliminar", use_container_width=True, key="opt_del"):
                st.session_state.opt_confirm_del = True
                st.rerun()
    else:
        st.warning("¿Seguro que quieres eliminar **" + m["title"] + "**? Esto no se puede deshacer.")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Sí, eliminar", use_container_width=True, key="opt_del_yes"):
                manhwas[:] = [x for x in manhwas if x["id"] != m["id"]]
                save(manhwas)
                st.session_state.pop("opt_confirm_del", None)
                st.rerun()
        with c2:
            if st.button("Cancelar", use_container_width=True, key="opt_del_no"):
                st.session_state.pop("opt_confirm_del", None)
                st.rerun()
 
 
# ---- Abrir el diálogo correcto según lo que se haya pedido ----
# Si desde la ventanita de opciones se pulsó "Editar":
if "editing_now" in st.session_state:
    _eid = st.session_state.pop("editing_now")
    st.session_state.pop("opening_id", None)
    _t = next((m for m in manhwas if m["id"] == _eid), None)
    if _t:
        edit_dialog(_t)
# Si se pulsó el lapicito de una tarjeta (?open=ID):
elif "opening_id" in st.session_state:
    _oid = st.session_state.opening_id
    _t = next((m for m in manhwas if m["id"] == _oid), None)
    if _t:
        options_dialog(_t)
    else:
        st.session_state.pop("opening_id", None)
 
 
 
# ---- helpers para el HTML ----
TRASH_SVG = ("<svg viewBox='0 0 24 24' width='15' height='15' fill='none' stroke='currentColor' "
             "stroke-width='2' stroke-linecap='round' stroke-linejoin='round'>"
             "<polyline points='3 6 5 6 21 6'></polyline>"
             "<path d='M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2'></path>"
             "<line x1='10' y1='11' x2='10' y2='17'></line><line x1='14' y1='11' x2='14' y2='17'></line></svg>")
 
PENCIL_SVG = ("<svg viewBox='0 0 24 24' width='15' height='15' fill='none' stroke='currentColor' "
              "stroke-width='2' stroke-linecap='round' stroke-linejoin='round'>"
              "<path d='M12 20h9'></path>"
              "<path d='M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4 12.5-12.5z'></path></svg>")
 
 
def esc(s):
    return html.escape(str(s if s is not None else ""))
 
 
def stars(n):
    out = ""
    for i in range(1, 6):
        out += "★" if i <= n else "<span class='empty'>★</span>"
    return out
 
 
def card_html(m):
    cov = cover_uri(m)
    cover_style = ("background-image:url('" + cov + "')") if cov else ""
    genre = ("<span class='genre-tag'>" + esc(m.get("genre")) + "</span>") if m.get("genre") else ""
    drive = ("<a class='drive-ico' href='" + esc(m.get("drive")) + "' target='_blank' title='Abrir en Drive'>📁</a>") if m.get("drive") else ""
    author = ("<div class='card-author'>✍️ " + esc(m.get("author")) + "</div>") if m.get("author") and m.get("author") != "—" else ""
    chips = ""
    if m.get("platform"):
        chips += "<span class='chip'>▶ " + esc(m.get("platform")) + "</span>"
    if m.get("chapter"):
        chips += "<span class='chip'>Cap. " + esc(m.get("chapter")) + "</span>"
    comment = ("<div class='comment'>💬 " + esc(m.get("comment")) + "</div>") if m.get("comment") else ""
    mid = str(m["id"])
    q_attr = esc((str(m.get("title", "")) + " " + str(m.get("author", ""))).lower())
    return (
        "<div class='card' data-q='" + q_attr + "'>"
        "<div class='cover' style='" + cover_style + "'>"
        "<span class='badge'><img src='" + ICON[m["status"]] + "'> " + STATUSES[m["status"]] + "</span>"
        "<button class='edit-fab' onclick='openManhwa(" + mid + ")' title='Editar o eliminar'>" + PENCIL_SVG + "</button>"
        + genre + "</div>"
        "<div class='body'>"
        "<div class='title-row'><div class='title'>" + esc(m["title"]) + "</div>" + drive + "</div>"
        + author + "<div>" + chips + "</div>"
        "<div class='stars'>" + stars(m.get("rating", 0)) + "</div>"
        + comment +
        "</div></div>"
    )
 
 
def grid(items):
    if not items:
        return ("<div class='empty'><div class='big'>🌸</div>"
                "No hay manhwas aqui todavia.<br>Agrega uno desde la barra de la izquierda!</div>")
    return "<div class='grid'>" + "".join(card_html(m) for m in items) + "</div>"
 
 
def count(s):
    return sum(1 for m in manhwas if m["status"] == s)
 
 
tabs_def = [
    ("todos", "<span style='font-size:16px'>✿</span> Todos", len(manhwas)),
    ("leyendo", "<img src='" + ICON["leyendo"] + "'> Leyendo", count("leyendo")),
    ("finalizado", "<img src='" + ICON["finalizado"] + "'> Finalizados", count("finalizado")),
    ("pausa", "<img src='" + ICON["pausa"] + "'> En pausa", count("pausa")),
    ("cancelada", "<img src='" + ICON["cancelada"] + "'> Canceladas", count("cancelada")),
]
active = st.session_state.get("active_tab", "todos")
tabs_html = "".join(
    "<button class='tab" + (" active" if k == active else "") + "' onclick=\"goTab('" + k + "')\">" + lbl +
    "<span class='cnt'>" + str(c) + "</span></button>"
    for k, lbl, c in tabs_def
)
 
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700;800&family=Nunito:wght@400;600;700;800&display=swap');
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:'Nunito',sans-serif;color:#5b3a4a;background:transparent;}
.header{text-align:center;padding:30px 20px 18px;background:linear-gradient(135deg,#ffd9e8,#ffc4dd);
  border-radius:24px;border:2px solid #ffb9d6;margin-bottom:18px;position:relative;overflow:hidden;}
.header::before{content:'❀ ❀ ❀ ❀ ❀ ❀ ❀ ❀ ❀ ❀ ❀ ❀';position:absolute;top:7px;left:0;right:0;
  color:rgba(255,255,255,.55);font-size:13px;letter-spacing:14px;white-space:nowrap;overflow:hidden;}
.header h1{font-family:'Baloo 2',sans-serif;font-size:34px;color:#c94b81;text-shadow:0 2px 0 #fff;}
.header p{color:#c06390;font-weight:700;font-size:14px;margin-top:2px;}
.heart{color:#e85f96;}
/* Toolbar: buscar + agregar */
.toolbar{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:18px;}
.add-btn{background:linear-gradient(135deg,#ff6fa5,#e85f96);color:#fff;border:none;padding:12px 22px;
  border-radius:30px;font-size:14px;font-weight:800;font-family:'Baloo 2',sans-serif;cursor:pointer;
  box-shadow:0 6px 18px rgba(255,111,165,.28);transition:.2s;text-decoration:none;display:inline-block;}
.add-btn:hover{transform:translateY(-2px);box-shadow:0 10px 26px rgba(255,111,165,.38);}
.search{flex:1;min-width:180px;max-width:340px;border:1.5px solid #ffd6e6;border-radius:30px;
  padding:11px 18px;font-size:14px;background:#fff;color:#5b3a4a;outline:none;font-family:'Nunito',sans-serif;}
.search::placeholder{color:#d6a7bc;}
.tabs{display:flex;gap:10px;flex-wrap:wrap;justify-content:center;margin-bottom:18px;}
.tab{border:none;cursor:pointer;background:#fff;color:#9c7688;padding:9px 18px;border-radius:30px;
  font-size:14px;font-weight:700;font-family:'Baloo 2',sans-serif;box-shadow:0 6px 16px rgba(255,111,165,.15);
  border:1.5px solid #ffd6e6;display:flex;align-items:center;gap:7px;transition:.2s;}
.tab img{width:18px;height:18px;object-fit:contain;}
.tab:hover{transform:translateY(-2px);}
.tab.active{background:linear-gradient(135deg,#ff6fa5,#e85f96);color:#fff;border-color:transparent;}
.tab .cnt{background:#ffe9f2;color:#e85f96;border-radius:20px;padding:0 8px;font-size:12px;}
.tab.active .cnt{background:rgba(255,255,255,.27);color:#fff;}
.section{display:none;}
.section.show{display:block;}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:20px;}
.card{background:#fff;border-radius:22px;box-shadow:0 8px 24px rgba(255,111,165,.15);
  border:1.5px solid #ffd6e6;overflow:visible;display:flex;flex-direction:column;transition:.2s;}
.card:hover{transform:translateY(-4px);box-shadow:0 12px 32px rgba(255,111,165,.28);}
.cover{height:175px;background:linear-gradient(135deg,#ffd9e8,#ffc4dd);background-size:cover;
  background-position:center;position:relative;border-radius:22px 22px 0 0;}
.badge{position:absolute;top:10px;left:10px;background:rgba(255,255,255,.87);color:#e85f96;
  padding:4px 11px 4px 8px;border-radius:20px;font-size:11px;font-weight:800;display:flex;
  align-items:center;gap:5px;box-shadow:0 2px 8px rgba(200,75,129,.2);}
.badge img{width:15px;height:15px;object-fit:contain;}
.genre-tag{position:absolute;bottom:10px;right:10px;background:rgba(255,255,255,.87);color:#e85f96;
  padding:3px 10px;border-radius:20px;font-size:10px;font-weight:800;}
.edit-fab{position:absolute;top:10px;right:10px;width:32px;height:32px;border:none;cursor:pointer;
  background:rgba(255,255,255,.9);color:#e85f96;border-radius:50%;display:flex;align-items:center;
  justify-content:center;box-shadow:0 2px 8px rgba(200,75,129,.25);transition:.15s;}
.edit-fab:hover{background:#fff;color:#c94b81;transform:scale(1.12);}
.body{padding:14px;display:flex;flex-direction:column;gap:8px;flex:1;}
.title-row{display:flex;align-items:flex-start;gap:8px;}
.title{font-size:16px;font-weight:700;font-family:'Baloo 2',sans-serif;color:#5b3a4a;line-height:1.2;flex:1;}
.drive-ico{flex-shrink:0;width:30px;height:30px;border-radius:10px;background:#ffe9f2;display:flex;
  align-items:center;justify-content:center;text-decoration:none;font-size:15px;transition:.15s;}
.drive-ico:hover{background:#ff9ec4;transform:scale(1.08);}
.card-author{font-size:12px;color:#9c7688;margin-top:-4px;}
.chip{display:inline-block;background:#ffe9f2;color:#e85f96;padding:3px 9px;border-radius:14px;
  font-size:11px;font-weight:700;margin:0 4px 4px 0;}
.stars{color:#ffc93c;font-size:16px;letter-spacing:2px;}
.stars .empty{color:#ffe1a8;}
.comment{font-size:12px;color:#9c7688;font-style:italic;background:#ffe9f2;padding:8px 10px;
  border-radius:12px;line-height:1.35;}
.foot{display:flex;gap:6px;margin-top:auto;padding-top:6px;position:relative;}
.picker{flex:1;position:relative;}
.trigger{width:100%;border:1.5px solid #ffd6e6;border-radius:16px;padding:7px 10px;font-size:12px;
  color:#5b3a4a;background:#ffe9f2;cursor:pointer;font-weight:700;display:flex;align-items:center;gap:6px;}
.trigger:hover{background:#ffdcea;}
.trigger img{width:16px;height:16px;object-fit:contain;}
.trigger .caret{margin-left:auto;color:#e85f96;transition:.2s;}
.picker.open .caret{transform:rotate(180deg);}
.menu{position:absolute;bottom:calc(100% + 8px);left:0;right:0;z-index:30;background:#fff;border-radius:18px;
  padding:6px;box-shadow:0 12px 30px rgba(200,75,129,.28);border:2px solid #ffd9e8;opacity:0;
  transform:translateY(8px) scale(.96);pointer-events:none;transform-origin:bottom center;
  transition:opacity .18s ease,transform .18s cubic-bezier(.34,1.56,.64,1);}
.picker.open .menu{opacity:1;transform:translateY(0) scale(1);pointer-events:auto;}
.menu::after{content:'';position:absolute;bottom:-9px;left:24px;width:16px;height:16px;background:#fff;
  border-right:2px solid #ffd9e8;border-bottom:2px solid #ffd9e8;transform:rotate(45deg);border-radius:0 0 4px 0;}
.opt{display:flex;align-items:center;gap:9px;padding:9px 11px;border-radius:13px;cursor:pointer;
  font-size:13px;font-weight:700;color:#5b3a4a;transition:.12s;}
.opt:hover{background:#ffe9f2;}
.opt.sel{background:linear-gradient(135deg,#ff6fa5,#e85f96);color:#fff;}
.opt img{width:20px;height:20px;object-fit:contain;}
.opt .chk{margin-left:auto;}
.iconbtn{width:38px;display:flex;align-items:center;justify-content:center;background:#ffe9f2;
  border-radius:14px;text-decoration:none;color:#e85f96;transition:.15s;flex-shrink:0;}
.iconbtn:hover{background:#ffccdd;color:#c94b81;}
.iconbtn.edit:hover{background:#ffe0b8;color:#d98a2b;}
.empty{text-align:center;padding:50px 20px;color:#9c7688;}
.empty .big{font-size:46px;margin-bottom:8px;}
</style>
"""
 
JS = """
<script>
function goTab(k){ window.top.location.href='?tab='+k; }
</script>
"""
 
JS_TABS = JS  # (usa goTab en los botones de pestaña)
 
JS_CARDS = """
<script>
function openManhwa(id){ window.top.location.href = '?open=' + id; }
</script>
"""
 
HEADER = ("<div class='header'><h1>✿ Mi Rincon Manhwa ✿</h1>"
          "<p>Tu biblioteca personal <span class='heart'>♡</span> hecha con amor</p></div>")
 
# 1) HEADER + TABS como primer componente (las tabs solo cambian de vista con JS)
PAGE_TOP = CSS + HEADER + "<div class='tabs'>" + tabs_html + "</div>" + JS_TABS
components.html(PAGE_TOP, height=210, scrolling=False)
 
# 2) Fila nativa: botón agregar + buscador (donde estaba, debajo de las secciones/pestañas)
c_add, c_search = st.columns([1, 2], vertical_alignment="center")
with c_add:
    if st.button("＋ Agregar manhwa", use_container_width=True):
        add_dialog()
with c_search:
    query = st.text_input("buscar", value="", placeholder="🔍 Buscar por nombre o autor...",
                          label_visibility="collapsed")
 
# 3) Filtrar por búsqueda y mostrar SOLO la sección activa
active = st.session_state.get("active_tab", "todos")
if query.strip():
    q = query.strip().lower()
    visible = [m for m in manhwas
               if q in (str(m.get("title", "")) + " " + str(m.get("author", ""))).lower()]
else:
    visible = manhwas
if active != "todos":
    visible = [m for m in visible if m["status"] == active]
 
PAGE_CARDS = CSS + grid(visible) + JS_CARDS
rows = max(1, (len(visible) + 2) // 3)
height = 120 + rows * 430
components.html(PAGE_CARDS, height=height, scrolling=True)
 
