import streamlit as st
import pandas as pd
from database import ejecutar_consulta, ejecutar_comando

st.set_page_config(
    page_title="Spotify CRUD",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# CSS PERSONALIZADO
# ==========================================
st.markdown("""
<style>
    .stApp { background-color: #121212; color: #FFFFFF; }
    header { visibility: hidden; }
    [data-testid="stSidebar"] { display: none; }
    * { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important; }

    /* Contenedores Base */
    .col-left { background-color: #000000; border-radius: 10px; padding: 20px; min-height: 85vh; }
    .col-right { background-color: #181818; border-radius: 10px; padding: 20px; min-height: 85vh; }
    
    /* Textos del Menú */
    .nav-item { color: #B3B3B3; font-size: 16px; font-weight: bold; margin-bottom: 20px; cursor: pointer; }
    .nav-item:hover { color: #FFFFFF; }
    .nav-item.active { color: #FFFFFF; }

    /* Títulos de sección */
    .section-title { font-size: 22px; font-weight: bold; margin: 20px 0 15px 0; color: #FFFFFF; }

    /* Carrusel Horizontal */
    .carousel-container { display: flex; overflow-x: auto; gap: 15px; padding-bottom: 15px; scrollbar-width: none; }
    .carousel-container::-webkit-scrollbar { display: none; }

    /* Tarjetas de Artistas */
    .card-artist { flex: 0 0 130px; text-align: center; }
    .card-artist img { width: 130px; height: 130px; border-radius: 50%; object-fit: cover; margin-bottom: 8px; }
    .card-artist h4 { margin: 0; font-size: 14px; color: #FFFFFF; }
    .card-artist p { margin: 0; font-size: 12px; color: #B3B3B3; }

    /* Tarjetas de Playlists */
    .card-playlist { flex: 0 0 150px; }
    .card-playlist img { width: 150px; height: 150px; border-radius: 8px; object-fit: cover; margin-bottom: 8px; }
    .card-playlist h4 { margin: 0; font-size: 14px; color: #FFFFFF; }
    .card-playlist p { margin: 0; font-size: 12px; color: #B3B3B3; }

    /* Lista de Canciones (Derecha) */
    .song-item { display: flex; align-items: center; gap: 12px; margin-bottom: 12px; padding: 8px; border-radius: 5px; }
    .song-item:hover { background-color: #282828; }
    .song-item img { width: 45px; height: 45px; border-radius: 4px; object-fit: cover; }
    .song-info h4 { margin: 0; font-size: 14px; color: #FFFFFF; }
    .song-info p { margin: 0; font-size: 12px; color: #B3B3B3; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# ESTRUCTURA DE COLUMNAS NATIVA
# ==========================================
col_izq, col_centro, col_der = st.columns([1.2, 4, 1.5])

# --- COLUMNA IZQUIERDA (MENÚ) ---
with col_izq:
    st.markdown("""
    <div class="col-left">
        <div style="font-size: 24px; font-weight: bold; color: white; margin-bottom: 30px;">Spotify</div>
        <div class="nav-item active">Inicio</div>
        <div class="nav-item">Buscar</div>
        <div style="margin-top: 30px; color: #B3B3B3; font-size: 12px; font-weight: bold; letter-spacing: 1px;">TU BIBLIOTECA</div>
        <div class="nav-item" style="font-size: 14px; margin-top: 15px;">Crear Playlist</div>
        <div class="nav-item" style="font-size: 14px;">Artistas Favoritos</div>
    </div>
    """, unsafe_allow_html=True)

# --- COLUMNA CENTRAL (ARTISTAS Y PLAYLISTS) ---
with col_centro:
    st.markdown('<h1 style="color: white; font-size: 32px; margin-bottom: 0;">Buenas tardes</h1>', unsafe_allow_html=True)

    # Artistas
    st.markdown('<div class="section-title">Artistas Populares</div>', unsafe_allow_html=True)
    df_artistas = ejecutar_consulta("SELECT nombre, foto_artista FROM artistas LIMIT 10;")
    
    if not df_artistas.empty:
        html_artistas = '<div class="carousel-container">'
        for _, row in df_artistas.iterrows():
            # Todo el HTML en una sola línea para evitar errores de renderizado
            html_artistas += f'<div class="card-artist"><img src="{row["foto_artista"]}" /><h4>{row["nombre"]}</h4><p>Artista</p></div>'
        html_artistas += '</div>'
        st.markdown(html_artistas, unsafe_allow_html=True)
    else:
        st.info("No hay artistas.")

    # Playlists
    st.markdown('<div class="section-title" style="margin-top: 30px;">Playlists Creadas</div>', unsafe_allow_html=True)
    query_playlists = "SELECT p.nombre AS playlist, u.nombre AS creador FROM playlists p JOIN usuarios u ON p.id_usuario = u.id_usuario LIMIT 10;"
    df_playlists = ejecutar_consulta(query_playlists)
    
    if not df_playlists.empty:
        html_playlists = '<div class="carousel-container">'
        for _, row in df_playlists.iterrows():
            img_default = "https://images.unsplash.com/photo-1614613535308-eb5fbd3d2c17?q=80&w=300&auto=format&fit=crop"
            html_playlists += f'<div class="card-playlist"><img src="{img_default}" /><h4>{row["playlist"]}</h4><p>Por {row["creador"]}</p></div>'
        html_playlists += '</div>'
        st.markdown(html_playlists, unsafe_allow_html=True)
    else:
        st.info("No hay playlists.")

# --- COLUMNA DERECHA (CANCIONES) ---
with col_der:
    st.markdown('<div class="col-right"><h3 style="color: white; margin-top: 0; font-size: 18px;">Canciones Recientes</h3>', unsafe_allow_html=True)
    
    query_canciones = "SELECT c.titulo, a.nombre AS artista, c.foto_portada FROM canciones c JOIN artistas a ON c.id_artista = a.id_artista LIMIT 15;"
    df_canciones = ejecutar_consulta(query_canciones)
    
    if not df_canciones.empty:
        for _, row in df_canciones.iterrows():
            # Todo en una sola línea
            st.markdown(f'<div class="song-item"><img src="{row["foto_portada"]}" /><div class="song-info"><h4>{row["titulo"]}</h4><p>{row["artista"]}</p></div></div>', unsafe_allow_html=True)
    else:
        st.info("No hay canciones.")
    st.markdown('</div>', unsafe_allow_html=True)


# ==========================================
# BOTÓN PARA CREAR PLAYLIST
# ==========================================
st.markdown("<br>", unsafe_allow_html=True)
col_b1, col_b2, col_b3 = st.columns([4, 1, 4])
with col_b2:
    if st.button("Crear Playlist", use_container_width=True):
        st.session_state.mostrar_modal = True

if st.session_state.get("mostrar_modal", False):
    with st.form("form_crear_playlist"):
        st.markdown("### Nueva Playlist")
        nombre_pl = st.text_input("Nombre de la playlist")
        id_usuario = st.number_input("ID del usuario creador", min_value=1, step=1)
        col_s, col_c = st.columns(2)
        with col_s:
            submitted = st.form_submit_button("Crear")
        with col_c:
            cancelar = st.form_submit_button("Cancelar")
            
        if submitted and nombre_pl:
            if ejecutar_comando("INSERT INTO playlists (nombre, id_usuario) VALUES (%s, %s);", (nombre_pl, id_usuario)):
                st.success("Playlist creada")
                st.session_state.mostrar_modal = False
                st.rerun()
        if cancelar:
            st.session_state.mostrar_modal = False
            st.rerun()