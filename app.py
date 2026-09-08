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
 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
 
# Icono de la app incrustado (base64) — no necesita archivos externos
APP_ICON_URI = "data:image/png;base64,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"
 
st.set_page_config(
    page_title="Mi Rincon Manhwa",
    page_icon=APP_ICON_URI if APP_ICON_URI.startswith("data:") else "🌸",
    layout="wide",
)
 
# ---- Icono para "Agregar a pantalla de inicio" en el telefono (iOS/Android) ----
def _inject_app_icon():
    if not APP_ICON_URI.startswith("data:"):
        return
    components.html(
        "<script>"
        "var h=window.parent.document.head;"
        "h.querySelectorAll(\"link[rel*='icon']\").forEach(function(x){x.parentNode.removeChild(x);});"
        "function add(rel){var l=window.parent.document.createElement('link');l.rel=rel;"
        "l.setAttribute('sizes','180x180');l.href='" + APP_ICON_URI + "';h.appendChild(l);}"
        "['apple-touch-icon','apple-touch-icon-precomposed','icon','shortcut icon'].forEach(add);"
        "var m=window.parent.document.createElement('meta');"
        "m.name='apple-mobile-web-app-title';m.content='Mi Rincon Manhwa';h.appendChild(m);"
        "var m2=window.parent.document.createElement('meta');"
        "m2.name='apple-mobile-web-app-capable';m2.content='yes';h.appendChild(m2);"
        "</script>",
        height=0,
    )
 
_inject_app_icon()
 
 
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
 
# ---- CSS para la parte de Streamlit ----
st.markdown(
    '<link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700;800&family=Nunito:wght@400;600;700;800&display=swap" rel="stylesheet">'
    "<style>"
    "@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700;800&family=Nunito:wght@400;600;700;800&display=swap');"
    ".stApp{background:linear-gradient(160deg,#fff6fa,#ffeaf3);}"
    # Nunito para TODO el texto de la app (con !important para ganar a Streamlit)
    ".stApp,.stApp p,.stApp span,.stApp div,.stApp label,.stApp li,.stApp a,"
    ".stApp input,.stApp textarea,.stApp [data-testid='stMarkdownContainer']{"
    "font-family:'Nunito','Segoe UI',sans-serif!important;}"
    # Baloo 2 para titulos y botones
    ".stApp h1,.stApp h2,.stApp h3,.stButton button,.stButton button *,"
    ".stFormSubmitButton button,.stFormSubmitButton button *,[data-testid='stPopover'] button{"
    "font-family:'Baloo 2','Nunito',sans-serif!important;}"
    # Base para TODOS los botones: forma redondeada
    ".stButton>button,.stFormSubmitButton>button{border-radius:26px!important;font-weight:800!important;"
    "padding:10px 18px!important;}"
    # Botones ROSA sólido: guardar (form) y agregar
    ".stFormSubmitButton>button,.st-key-addbtn button{"
    "background:linear-gradient(135deg,#ff6fa5,#e85f96)!important;color:#fff!important;border:none!important;"
    "box-shadow:0 6px 18px rgba(255,111,165,.28)!important;}"
    ".stFormSubmitButton>button *,.st-key-addbtn button *{color:#fff!important;}"
    ".stFormSubmitButton>button:hover,.st-key-addbtn button:hover{color:#fff!important;transform:translateY(-2px);}"
    # Pestañas: base blanca con texto rosita (la activa se pinta rosa aparte)
    "[class*='st-key-tab_'] button{background:#fff!important;color:#9c7688!important;"
    "border:1.5px solid #ffd6e6!important;box-shadow:0 4px 12px rgba(255,111,165,.12)!important;}"
    "[class*='st-key-tab_'] button *{color:#9c7688!important;}"
    "[class*='st-key-tab_'] button:hover{background:#ffe9f2!important;border-color:#ffb9d6!important;}"
    "[class*='st-key-tab_'] button:hover *{color:#c94b81!important;}"
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
    # key ÚNICA por apertura del diálogo (evita que el widget de estrellas se trabe)
    _dn = st.session_state.get("dlg_nonce", 0)
    rk = "rating_" + str(d.get("id", "new")) + "_" + str(_dn)
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
        st.rerun()
 
 
@st.dialog("✿ Nuevo manhwa")
def add_dialog():
    manhwa_dialog(editing=None)
 
 
@st.dialog("✏️ Editar manhwa")
def edit_dialog(m):
    manhwa_dialog(editing=m)
 
 
 
 
 
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
    # solo las estrellas seleccionadas (sin las vacías)
    return "★" * int(n)
 
 
def count(s):
    return sum(1 for m in manhwas if m["status"] == s)
 
 
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
  border:1.5px solid #ffd6e6;overflow:visible;display:flex;flex-direction:column;transition:.2s;position:relative;}
.card:hover{transform:translateY(-4px);box-shadow:0 12px 32px rgba(255,111,165,.28);}
.cover{height:175px;background:linear-gradient(135deg,#ffd9e8,#ffc4dd);
  position:relative;border-radius:22px 22px 0 0;overflow:hidden;}
.cover-img{position:absolute!important;inset:0;width:100%!important;height:100%!important;
  object-fit:cover!important;display:block!important;max-width:none!important;border-radius:0!important;}
.badge{position:absolute;top:10px;left:10px;z-index:3;background:rgba(255,255,255,.92);color:#e85f96!important;
  padding:4px 11px 4px 8px;border-radius:20px;font-size:11px;font-weight:800;display:inline-flex;
  align-items:center;gap:5px;box-shadow:0 2px 8px rgba(200,75,129,.2);text-decoration:none!important;cursor:pointer;transition:.15s;}
.badge:hover{background:#fff;box-shadow:0 4px 12px rgba(200,75,129,.3);}
.badge .bcaret{opacity:.7;font-size:10px;}
.statusmenu{position:absolute;top:44px;left:10px;z-index:20;background:#fff;border-radius:16px;padding:6px;
  box-shadow:0 12px 30px rgba(200,75,129,.3);border:2px solid #ffd9e8;min-width:160px;
  animation:smpop .18s cubic-bezier(.34,1.56,.64,1);}
@keyframes smpop{from{opacity:0;transform:translateY(-8px) scale(.96);}to{opacity:1;transform:translateY(0) scale(1);}}
.statusmenu::before{content:'';position:absolute;top:-9px;left:22px;width:15px;height:15px;background:#fff;
  border-left:2px solid #ffd9e8;border-top:2px solid #ffd9e8;transform:rotate(45deg);border-radius:4px 0 0 0;}
.smopt{display:flex;align-items:center;gap:9px;padding:8px 10px;border-radius:11px;cursor:pointer;
  font-size:13px;font-weight:700;color:#5b3a4a!important;text-decoration:none!important;transition:.12s;}
.smopt:hover{background:#ffe9f2;}
.smopt.sel{background:linear-gradient(135deg,#ff6fa5,#e85f96);}
.smopt.sel,.smopt.sel span{color:#fff!important;}
.smopt img{width:19px;height:19px;object-fit:contain;}
.smopt .smchk{margin-left:auto;font-size:12px;}
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
 
# CSS para las tarjetas cuando se renderizan de forma NATIVA (sin iframe)
CARD_CSS = (CSS.replace("<style>", "").replace("</style>", "") +
            ".ncard{margin-bottom:14px;}"
            "div[data-testid='stColumn']{position:relative;}"
            # posicion: badge de ESTADO arriba-izquierda, OPCIONES arriba-derecha
            "[class*='st-key-stbadge_']{position:absolute!important;top:10px;left:10px;z-index:11;width:auto!important;margin:0!important;}"
            "[class*='st-key-optpop_']{position:absolute!important;top:10px;right:12px;z-index:10;width:auto!important;margin:0!important;}"
            # badge de estado: pastilla blanca con tu icono + nombre
            "[class*='st-key-stbadge_'] button[data-testid='stPopoverButton']{background:rgba(255,255,255,.92)!important;"
            "color:#e85f96!important;border:1.5px solid #ffd6e6!important;border-radius:20px!important;"
            "padding:3px 10px!important;min-height:0!important;height:auto!important;font-size:11px!important;font-weight:800!important;"
            "box-shadow:0 2px 8px rgba(200,75,129,.2)!important;}"
            "[class*='st-key-stbadge_'] button[data-testid='stPopoverButton']:hover{background:#fff!important;}"
            "[class*='st-key-stbadge_'] button[data-testid='stPopoverButton'] img{width:14px!important;height:14px!important;"
            "object-fit:contain;vertical-align:middle;margin-right:3px;display:inline-block;}"
            # opciones: iconito redondo
            "[class*='st-key-optpop_'] button[data-testid='stPopoverButton']{width:32px!important;min-width:32px!important;"
            "height:32px!important;padding:0!important;background:rgba(255,255,255,.92)!important;color:#e85f96!important;"
            "border:1.5px solid #ffd6e6!important;border-radius:50%!important;"
            "box-shadow:0 2px 8px rgba(200,75,129,.25)!important;display:flex;align-items:center;justify-content:center;}"
            "[class*='st-key-optpop_'] button[data-testid='stPopoverButton']:hover{background:#fff!important;color:#c94b81!important;transform:scale(1.1);}"
            # ocultar el chevron 'expand_more' en ambos
            "div[data-testid='stPopover'] [data-testid='stIconMaterial']{display:none!important;}"
            "button[data-testid='stPopoverButton'] div[aria-hidden='true']{display:none!important;}"
            "button[data-testid='stPopoverButton'] p{margin:0!important;}"
            # botones de estado dentro del menu: icono + texto a la izquierda
            "[class*='st-key-stset_'] button{justify-content:flex-start!important;text-align:left!important;}"
            "[class*='st-key-stset_'] button img{width:18px!important;height:18px!important;object-fit:contain;margin-right:6px;vertical-align:middle;}")
 
 
HEADER = ("<div class='header'><h1>✿ Mi Rincon Manhwa ✿</h1>"
          "<p>Tu biblioteca personal <span class='heart'>♡</span> hecha con amor</p></div>")
 
# 1) HEADER (solo visual) en un componente
components.html(CSS + HEADER, height=140, scrolling=False)
 
# Pestañas NATIVAS con TUS iconos encima de cada botón (funcionan seguro)
active = st.session_state.get("active_tab", "todos")
tab_defs = [
    ("todos", None, "Todos", len(manhwas)),
    ("leyendo", ICON["leyendo"], "Leyendo", count("leyendo")),
    ("finalizado", ICON["finalizado"], "Finalizados", count("finalizado")),
    ("pausa", ICON["pausa"], "En pausa", count("pausa")),
    ("cancelada", ICON["cancelada"], "Canceladas", count("cancelada")),
]
# CSS dinámico: mete TU icono dentro de cada botón (a la izquierda del texto, como la lupa)
# y pinta de rosa la pestaña activa.
_tab_css = "<style>"
for k, icon_uri, lbl, cnt in tab_defs:
    if icon_uri:
        _tab_css += (".st-key-tab_" + k + " button p::before{content:'';display:inline-block;"
                     "width:18px;height:18px;background:url('" + icon_uri + "') center/contain no-repeat;"
                     "margin-right:7px;vertical-align:-4px;}")
    else:
        _tab_css += ".st-key-tab_todos button p::before{content:'✿ ';}"
_tab_css += (".st-key-tab_" + active + " button{background:linear-gradient(135deg,#ff6fa5,#e85f96)!important;"
             "color:#fff!important;border:none!important;box-shadow:0 6px 18px rgba(255,111,165,.28)!important;}"
             ".st-key-tab_" + active + " button *{color:#fff!important;}")
_tab_css += "</style>"
st.markdown(_tab_css, unsafe_allow_html=True)
 
tab_cols = st.columns(5)
for tcol, (k, icon_uri, lbl, cnt) in zip(tab_cols, tab_defs):
    with tcol:
        if st.button(lbl + " (" + str(cnt) + ")", key="tab_" + k, use_container_width=True):
            st.session_state.active_tab = k
            st.rerun()
active = st.session_state.get("active_tab", "todos")
 
# 2) Fila nativa: botón agregar + buscador
c_add, c_search = st.columns([1, 2], vertical_alignment="center")
with c_add:
    if st.button("＋ Agregar manhwa", use_container_width=True, key="addbtn"):
        st.session_state["dlg_nonce"] = st.session_state.get("dlg_nonce", 0) + 1  # rating fresco
        add_dialog()
with c_search:
    query = st.text_input("buscar", value="", placeholder="🔍 Buscar por nombre o autor...",
                          label_visibility="collapsed")
 
# 3) Filtrar por búsqueda y por sección activa
if query.strip():
    q = query.strip().lower()
    visible = [m for m in manhwas
               if q in (str(m.get("title", "")) + " " + str(m.get("author", ""))).lower()]
else:
    visible = manhwas
if active != "todos":
    visible = [m for m in visible if m["status"] == active]
 
# 4) Mostrar las tarjetas (nativas, 3 por fila) con popover de opciones que SÍ funciona
def card_inner_html(m):
    """El contenido visual de la tarjeta (sin el botón de opciones, que es nativo)."""
    cov = cover_uri(m)
    cover_img = ("<img class='cover-img' src='" + cov + "'>") if cov else ""
    drive = ("<a class='drive-ico' href='" + esc(m.get("drive")) + "' target='_blank' title='Abrir en Drive'>📁</a>") if m.get("drive") else ""
    author = ("<div class='card-author'>✍️ " + esc(m.get("author")) + "</div>") if m.get("author") and m.get("author") != "—" else ""
    chips = ""
    if m.get("genre"):
        chips += "<span class='chip'>" + esc(m.get("genre")) + "</span>"
    if m.get("platform"):
        chips += "<span class='chip'>📱 " + esc(m.get("platform")) + "</span>"
    if m.get("chapter"):
        chips += "<span class='chip'>Cap. " + esc(m.get("chapter")) + "</span>"
    comment = ("<div class='comment'>💬 " + esc(m.get("comment")) + "</div>") if m.get("comment") else ""
    # las estrellas solo salen si hay rating
    stars_html = ("<div class='stars'>" + stars(m.get("rating", 0)) + "</div>") if m.get("rating", 0) else ""
    return (
        "<div class='card ncard'>"
        "<div class='cover'>" + cover_img + "</div>"
        "<div class='body'>"
        "<div class='title-row'><div class='title'>" + esc(m["title"]) + "</div>" + drive + "</div>"
        + author + "<div class='chips'>" + chips + "</div>"
        + stars_html
        + comment +
        "</div></div>"
    )
 
# CSS de tarjetas para el render nativo (una vez)
st.markdown("<style>" + CARD_CSS + "</style>", unsafe_allow_html=True)
 
if not visible:
    st.markdown("<div class='empty'><div class='big'>🌸</div>"
                "No hay manhwas aqui todavia.<br>Agrega uno con el boton de arriba!</div>",
                unsafe_allow_html=True)
else:
    for row_start in range(0, len(visible), 3):
        cols = st.columns(3)
        for col, m in zip(cols, visible[row_start:row_start + 3]):
            with col:
                mid = str(m["id"])
                # ---- Popover de ESTADO (arriba izquierda, con tu icono) — nativo, sin recarga ----
                with st.container(key="stbadge_" + mid):
                    with st.popover("![](" + ICON[m["status"]] + ") " + STATUSES[m["status"]],
                                    use_container_width=False):
                        st.markdown("**Cambiar estado**")
                        for k, lbl in STATUSES.items():
                            marca = "✓ " if m["status"] == k else ""
                            if st.button("![](" + ICON[k] + ") " + marca + lbl,
                                         key="stset_" + mid + "_" + k, use_container_width=True):
                                for _m in manhwas:
                                    if _m["id"] == m["id"]:
                                        _m["status"] = k
                                save(manhwas)
                                st.rerun()
                # ---- Popover de OPCIONES (arriba derecha) ----
                # el nonce cambia la key al abrir "Editar" -> fuerza que el popover se cierre
                _pn = st.session_state.get("optpop_nonce", 0)
                with st.container(key="optpop_" + mid + "_" + str(_pn)):
                    with st.popover("✏️", use_container_width=False):
                        st.markdown("**" + m["title"] + "**")
                        pc1, pc2 = st.columns(2)
                        with pc1:
                            if st.button("✏️ Editar", key="ed_" + mid, use_container_width=True):
                                st.session_state["open_edit_id"] = m["id"]
                                st.session_state["optpop_nonce"] = _pn + 1  # cierra el popover
                                st.session_state["dlg_nonce"] = st.session_state.get("dlg_nonce", 0) + 1  # rating fresco
                                st.rerun()
                        with pc2:
                            if st.button("🗑 Eliminar", key="dl_" + mid, use_container_width=True):
                                st.session_state["confirm_del_" + mid] = True
                                st.rerun()
                        if st.session_state.get("confirm_del_" + mid):
                            st.warning("¿Seguro? Esto no se puede deshacer.")
                            if st.button("Sí, eliminar", key="dy_" + mid, use_container_width=True):
                                manhwas[:] = [x for x in manhwas if x["id"] != m["id"]]
                                save(manhwas)
                                st.session_state.pop("confirm_del_" + mid, None)
                                st.rerun()
                st.markdown(card_inner_html(m), unsafe_allow_html=True)
 
# Abrir el diálogo de editar DESPUÉS de cerrar el recuadro de opciones
if st.session_state.get("open_edit_id") is not None:
    _eid = st.session_state.pop("open_edit_id")
    _target = next((x for x in manhwas if x["id"] == _eid), None)
    if _target:
        edit_dialog(_target)
 
