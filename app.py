# -*- coding: utf-8 -*-
"""
✿ Mi Rincón Manhwa ✿
App personal para llevar el control de tus manhwas.
Hecha con Streamlit + mucho amor rosita ♡
"""

import streamlit as st
import json
import os
import base64
from datetime import datetime

# --------------------------------------------------------------------------
# Configuración básica
# --------------------------------------------------------------------------
st.set_page_config(
    page_title="Mi Rincón Manhwa",
    page_icon="🌸",
    layout="wide",
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "manhwas.json")
COVERS_DIR = os.path.join(BASE_DIR, "data", "covers")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
os.makedirs(COVERS_DIR, exist_ok=True)

# Estados con su icono e info
STATUSES = {
    "leyendo":    {"label": "Leyendo",    "icon": "leyendo.png"},
    "finalizado": {"label": "Finalizado", "icon": "finalizado.png"},
    "pausa":      {"label": "En pausa",   "icon": "pausa.png"},
    "cancelada":  {"label": "Cancelada",  "icon": "cancelada.png"},
}

# --------------------------------------------------------------------------
# Utilidades de datos (guardado en archivo JSON local)
# --------------------------------------------------------------------------
def load_manhwas():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def save_manhwas(manhwas):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(manhwas, f, ensure_ascii=False, indent=2)


def next_id(manhwas):
    return (max([m["id"] for m in manhwas]) + 1) if manhwas else 1


def img_to_b64(path):
    """Lee una imagen del disco y la devuelve como data URI base64."""
    try:
        with open(path, "rb") as f:
            b = base64.b64encode(f.read()).decode()
        ext = os.path.splitext(path)[1].lower().replace(".", "") or "png"
        if ext == "jpg":
            ext = "jpeg"
        return f"data:image/{ext};base64,{b}"
    except Exception:
        return ""


# Iconos de estado como data URI (para el HTML)
ICON_URI = {k: img_to_b64(os.path.join(ASSETS_DIR, v["icon"])) for k, v in STATUSES.items()}

# --------------------------------------------------------------------------
# Estilos (rosa pastel + fuentes Baloo 2 / Nunito)
# --------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@500;600;700;800&family=Nunito:wght@400;600;700;800&display=swap');

/* Fondo general */
.stApp {
    background: linear-gradient(160deg,#fff6fa 0%,#ffeaf3 100%);
}
html, body, [class*="css"], .stMarkdown, p, span, div, label {
    font-family:'Nunito','Segoe UI',sans-serif;
    color:#5b3a4a;
}
h1,h2,h3,.baloo { font-family:'Baloo 2','Nunito',sans-serif !important; }

/* Encabezado */
.app-header{
    text-align:center;padding:26px 20px 16px;
    background:linear-gradient(135deg,#ffd9e8 0%,#ffc4dd 100%);
    border-radius:24px;margin-bottom:8px;border:2px solid #ffb9d6;
}
.app-header h1{margin:2px 0;font-size:34px;color:#c94b81;text-shadow:0 2px 0 #fff;font-family:'Baloo 2',sans-serif;}
.app-header p{margin:0;color:#c06390;font-size:14px;font-weight:600;}

/* Tarjetas */
.card{
    background:#fff;border-radius:22px;padding:0 0 14px;overflow:hidden;
    box-shadow:0 8px 24px rgba(255,111,165,.15);border:1.5px solid #ffd6e6;
    margin-bottom:18px;
}
.cover{height:170px;background:linear-gradient(135deg,#ffd9e8,#ffc4dd);
    background-size:cover;background-position:center;position:relative;}
.status-badge{
    position:absolute;top:10px;left:10px;background:#ffffffdd;color:#e85f96;
    padding:4px 11px 4px 8px;border-radius:20px;font-size:11px;font-weight:700;
    display:flex;align-items:center;gap:5px;box-shadow:0 2px 8px rgba(200,75,129,.2);
}
.status-badge img{width:15px;height:15px;object-fit:contain;}
.genre-tag{
    position:absolute;bottom:10px;right:10px;background:#ffffffdd;color:#e85f96;
    padding:3px 10px;border-radius:20px;font-size:10px;font-weight:700;
}
.card-pad{padding:12px 16px 0;}
.card-title{font-size:17px;font-weight:700;color:#5b3a4a;font-family:'Baloo 2',sans-serif;
    display:flex;align-items:center;gap:8px;line-height:1.2;}
.drive-ico{width:26px;height:26px;border-radius:8px;background:#ffe9f2;display:inline-flex;
    align-items:center;justify-content:center;text-decoration:none;font-size:14px;flex-shrink:0;}
.drive-ico:hover{background:#ff9ec4;}
.card-author{font-size:12px;color:#9c7688;margin:2px 0 6px;}
.chip{display:inline-block;background:#ffe9f2;color:#e85f96;padding:3px 9px;border-radius:14px;
    font-size:11px;font-weight:700;margin:0 4px 4px 0;}
.stars{color:#ffc93c;font-size:16px;letter-spacing:2px;margin:4px 0;}
.stars .empty{color:#ffe1a8;}
.comment{font-size:12px;color:#9c7688;font-style:italic;background:#ffe9f2;
    padding:7px 10px;border-radius:12px;margin-top:4px;line-height:1.35;}

/* Botones Streamlit */
.stButton>button{
    background:linear-gradient(135deg,#ff6fa5,#e85f96);color:#fff;border:none;
    border-radius:16px;font-weight:700;font-family:'Baloo 2',sans-serif;
    padding:8px 16px;transition:.15s;
}
.stButton>button:hover{transform:translateY(-2px);box-shadow:0 6px 18px rgba(255,111,165,.35);color:#fff;}

/* Tabs */
.stTabs [data-baseweb="tab-list"]{gap:8px;justify-content:center;}
.stTabs [data-baseweb="tab"]{
    background:#fff;border-radius:24px;padding:6px 18px;font-weight:700;
    border:1.5px solid #ffd6e6;color:#9c7688;font-family:'Baloo 2',sans-serif;
}
.stTabs [aria-selected="true"]{
    background:linear-gradient(135deg,#ff6fa5,#e85f96)!important;color:#fff!important;border-color:transparent!important;
}

/* Inputs */
.stTextInput input,.stNumberInput input,.stTextArea textarea,.stSelectbox div[data-baseweb="select"]>div{
    border-radius:14px!important;border-color:#ffd6e6!important;
}
#MainMenu,footer{visibility:hidden;}
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------------------------------
# Opening / pantalla de bienvenida (solo la primera vez en la sesión)
# --------------------------------------------------------------------------
if "seen_splash" not in st.session_state:
    st.session_state.seen_splash = True
    splash = st.empty()
    splash.markdown("""
    <div style="position:fixed;inset:0;z-index:9999;
        background:linear-gradient(160deg,#ffd9e8,#ffc4dd 55%,#ffb0d1);
        display:flex;align-items:center;justify-content:center;text-align:center;">
      <div>
        <div style="font-size:70px;color:#fff;animation:beat 1.4s ease-in-out infinite;">✿</div>
        <h1 style="font-family:'Baloo 2',sans-serif;font-size:38px;color:#c94b81;
            text-shadow:0 2px 0 #fff;margin:10px 0 4px;">Mi Rincón Manhwa</h1>
        <p style="color:#c06390;font-weight:700;">Tu biblioteca personal ♡</p>
      </div>
    </div>
    <style>@keyframes beat{0%,100%{transform:scale(1)}50%{transform:scale(1.18)}}</style>
    """, unsafe_allow_html=True)
    import time
    time.sleep(2.2)
    splash.empty()


# --------------------------------------------------------------------------
# Encabezado
# --------------------------------------------------------------------------
st.markdown("""
<div class="app-header">
  <h1>✿ Mi Rincón Manhwa ✿</h1>
  <p>Tu biblioteca personal ♡ hecha con amor</p>
</div>
""", unsafe_allow_html=True)


# --------------------------------------------------------------------------
# Cargar datos
# --------------------------------------------------------------------------
manhwas = load_manhwas()


# --------------------------------------------------------------------------
# Formulario para agregar (en la barra lateral)
# --------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### ✿ Agregar un manhwa")
    with st.form("add_form", clear_on_submit=True):
        title = st.text_input("Nombre *", placeholder="Ej. Our sunny days")
        cover_file = st.file_uploader("Foto de portada", type=["png", "jpg", "jpeg", "webp"])
        author = st.text_input("Autor", placeholder="Ej. Hajin")
        genre = st.text_input("Género", placeholder="Ej. Romance, BL, Fantasía...")
        platform = st.text_input("Plataforma", placeholder="Ej. Webtoon, Telegram...")
        chapter = st.number_input("Capítulo actual", min_value=0, step=1, value=0)
        status = st.selectbox("Estado", options=list(STATUSES.keys()),
                              format_func=lambda k: STATUSES[k]["label"])
        rating = st.slider("Rating ⭐", 0, 5, 0)
        drive = st.text_input("Link de la carpeta en Drive",
                              placeholder="Pega aquí el link (opcional)")
        comment = st.text_area("Comentario", placeholder="¿Qué te pareció? ♡")

        submitted = st.form_submit_button("Guardar ♡")
        if submitted:
            if not title.strip():
                st.warning("Ponle un nombre al manhwa ♡")
            else:
                cover_path = ""
                if cover_file is not None:
                    ext = cover_file.name.split(".")[-1].lower()
                    fname = f"cover_{next_id(manhwas)}_{int(datetime.now().timestamp())}.{ext}"
                    fpath = os.path.join(COVERS_DIR, fname)
                    with open(fpath, "wb") as f:
                        f.write(cover_file.getbuffer())
                    cover_path = os.path.join("data", "covers", fname)

                manhwas.append({
                    "id": next_id(manhwas),
                    "title": title.strip(),
                    "cover": cover_path,
                    "author": author.strip(),
                    "genre": genre.strip(),
                    "platform": platform.strip(),
                    "chapter": int(chapter),
                    "status": status,
                    "rating": int(rating),
                    "drive": drive.strip(),
                    "comment": comment.strip(),
                })
                save_manhwas(manhwas)
                st.success(f"¡'{title.strip()}' agregado! ♡")
                st.rerun()


# --------------------------------------------------------------------------
# Helpers de render
# --------------------------------------------------------------------------
def stars_html(n):
    s = ""
    for i in range(1, 6):
        s += "★" if i <= n else '<span class="empty">★</span>'
    return f'<div class="stars">{s}</div>'


def cover_uri(m):
    if m.get("cover"):
        p = os.path.join(BASE_DIR, m["cover"])
        if os.path.exists(p):
            return img_to_b64(p)
    return ""


def render_card(m):
    st_info = STATUSES.get(m["status"], STATUSES["leyendo"])
    cov = cover_uri(m)
    cover_style = f"background-image:url('{cov}')" if cov else ""
    genre_tag = f'<span class="genre-tag">{m["genre"]}</span>' if m.get("genre") else ""
    drive_ico = (f'<a class="drive-ico" href="{m["drive"]}" target="_blank" '
                 f'title="Abrir carpeta en Drive">📁</a>') if m.get("drive") else ""
    author = f'<div class="card-author">✍️ {m["author"]}</div>' if m.get("author") and m["author"] != "—" else ""
    chips = ""
    if m.get("platform"):
        chips += f'<span class="chip">▶ {m["platform"]}</span>'
    if m.get("chapter"):
        chips += f'<span class="chip">Cap. {m["chapter"]}</span>'
    comment = f'<div class="comment">💬 {m["comment"]}</div>' if m.get("comment") else ""

    st.markdown(f"""
    <div class="card">
      <div class="cover" style="{cover_style}">
        <span class="status-badge"><img src="{ICON_URI[m['status']]}"> {st_info['label']}</span>
        {genre_tag}
      </div>
      <div class="card-pad">
        <div class="card-title">{m['title']} {drive_ico}</div>
        {author}
        <div>{chips}</div>
        {stars_html(m.get('rating', 0))}
        {comment}
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Controles: cambiar estado + eliminar
    c1, c2 = st.columns([3, 1])
    with c1:
        new_status = st.selectbox(
            "Estado", options=list(STATUSES.keys()),
            index=list(STATUSES.keys()).index(m["status"]),
            format_func=lambda k: STATUSES[k]["label"],
            key=f"status_{m['id']}", label_visibility="collapsed",
        )
        if new_status != m["status"]:
            m["status"] = new_status
            save_manhwas(manhwas)
            st.rerun()
    with c2:
        if st.button("🗑", key=f"del_{m['id']}", help="Eliminar"):
            manhwas.remove(m)
            save_manhwas(manhwas)
            st.rerun()


def render_grid(items):
    if not items:
        st.markdown(
            "<div style='text-align:center;padding:50px;color:#9c7688;'>"
            "<div style='font-size:46px'>🌸</div>"
            "No hay manhwas aquí todavía.<br>¡Agrega uno desde la barra de la izquierda!</div>",
            unsafe_allow_html=True)
        return
    cols = st.columns(3)
    for i, m in enumerate(items):
        with cols[i % 3]:
            render_card(m)


# --------------------------------------------------------------------------
# Secciones (tabs)
# --------------------------------------------------------------------------
def count(status):
    return sum(1 for m in manhwas if m["status"] == status)

tab_labels = [
    f"✿ Todos ({len(manhwas)})",
    f"📖 Leyendo ({count('leyendo')})",
    f"✅ Finalizados ({count('finalizado')})",
    f"⏸ En pausa ({count('pausa')})",
    f"✖ Canceladas ({count('cancelada')})",
]
tabs = st.tabs(tab_labels)

with tabs[0]:
    render_grid(manhwas)
with tabs[1]:
    render_grid([m for m in manhwas if m["status"] == "leyendo"])
with tabs[2]:
    render_grid([m for m in manhwas if m["status"] == "finalizado"])
with tabs[3]:
    render_grid([m for m in manhwas if m["status"] == "pausa"])
with tabs[4]:
    render_grid([m for m in manhwas if m["status"] == "cancelada"])
