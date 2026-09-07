# ✿ Mi Rincón Manhwa ✿

Una app personal, rosita y tierna para llevar el control de todos mis manhwas 💕

Hecha con [Streamlit](https://streamlit.io/).

## ¿Qué hace?

- Guarda tus manhwas con nombre, foto de portada, autor, género, plataforma y capítulo actual.
- Los organiza por secciones: **Leyendo**, **Finalizados**, **En pausa** y **Canceladas**.
- Le pones **rating con estrellas** y un **comentario** a cada uno.
- Un **iconito de carpeta** que abre la carpeta de tu Google Drive con los PDFs.
- Pantalla de bienvenida (opening) y diseño rosa pastel.

## Cómo se ve

Cada manhwa es una tarjeta con su portada, estado, estrellas y comentario. Agregas nuevos desde la barra de la izquierda.

## Correr la app en tu compu (opcional)

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Estructura

```
mi-rincon-manhwa/
├── app.py              # La app
├── requirements.txt    # Lo que necesita para funcionar
├── assets/             # Iconos de los estados (leyendo, finalizado, etc.)
└── data/               # Aquí se guardan tus manhwas y portadas
```

Hecho con mucho amor ♡
