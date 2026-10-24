import streamlit as st
import pandas as pd
from database import ejecutar_consulta, ejecutar_comando

st.set_page_config(
    page_title="Spotify CRUD",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .stApp { background-color: #121212; color: #FFFFFF; }
    header { visibility: hidden; }
    [data-testid="stSidebar"] { display: none; }
    
    /* Corrección de fuentes para evitar el texto encimado en los iconos */
    body, .stApp { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important; }
    [data-testid="stIconMaterial"], .material-icons { font-family: 'Material Icons' !important; }

    .block-container { padding-top: 1rem !important; padding-bottom: 1rem !important; }

    /* Menú Superior */
    div[data-testid="stVerticalBlockBorderWrapper"]:nth-of-type(1) > div {
        background-color: #000000; border-radius: 10px; padding: 10px 20px; margin-bottom: 15px;
    }
    div[data-testid="stVerticalBlockBorderWrapper"]:nth-of-type(1) button {
        background-color: transparent !important; color: #B3B3B3 !important; border: none !important;
        font-size: 16px !important; font-weight: bold !important; text-align: left !important; padding: 0 !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"]:nth-of-type(1) button:hover { color: #FFFFFF !important; }

    /* Contenedores Principales */
    div[data-testid="stVerticalBlockBorderWrapper"]:nth-of-type(2) > div {
        background-color: #000000; border-radius: 10px; padding: 20px; min-height: 75vh;
    }
    div[data-testid="stVerticalBlockBorderWrapper"]:nth-of-type(3) > div {
        background-color: #181818; border-radius: 10px; padding: 20px; min-height: 75vh;
    }

    /* Botones de la barra lateral (Biblioteca) */
    div[data-testid="stVerticalBlockBorderWrapper"] button {
        background-color: transparent !important; color: #B3B3B3 !important; border: none !important;
        text-align: left !important; font-size: 14px !important; padding: 5px 0 !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] button:hover { color: #FFFFFF !important; }

    .section-title { font-size: 22px; font-weight: bold; margin: 20px 0 15px 0; color: #FFFFFF; }
    .carousel-container { display: flex; overflow-x: auto; gap: 15px; padding-bottom: 15px; scrollbar-width: none; }
    .carousel-container::-webkit-scrollbar { display: none; }
    
    .card-artist { flex: 0 0 130px; text-align: center; }
    .card-artist img { width: 130px; height: 130px; border-radius: 50%; object-fit: cover; margin-bottom: 8px; }
    .card-artist h4 { margin: 0; font-size: 14px; color: #FFFFFF; }
    .card-artist p { margin: 0; font-size: 12px; color: #B3B3B3; }
    
    /* Playlists en la Biblioteca */
    .sidebar-playlist {
        display: flex; align-items: center; gap: 10px; margin-bottom: 10px; padding: 5px; border-radius: 5px;
    }
    .sidebar-playlist:hover { background-color: #282828; }
    .sidebar-playlist img { width: 40px; height: 40px; border-radius: 4px; object-fit: cover; }
    .sidebar-playlist-info h4 { margin: 0; font-size: 13px; color: #FFFFFF; }
    .sidebar-playlist-info p { margin: 0; font-size: 11px; color: #B3B3B3; }

    .song-item { display: flex; align-items: center; gap: 12px; margin-bottom: 12px; padding: 8px; border-radius: 5px; }
    .song-item:hover { background-color: #282828; }
    .song-item img { width: 45px; height: 45px; border-radius: 4px; object-fit: cover; }
    .song-info h4 { margin: 0; font-size: 14px; color: #FFFFFF; }
    .song-info p { margin: 0; font-size: 12px; color: #B3B3B3; }

    /* Recuadro para gestionar registros */
    .gestion-box {
        background-color: #282828; padding: 15px; border-radius: 8px; margin-bottom: 10px; cursor: pointer;
        border-left: 4px solid #1DB954;
    }
</style>
""", unsafe_allow_html=True)

# Inicializar estados
if "vista_actual" not in st.session_state:
    st.session_state.vista_actual = "Inicio"
if "mostrar_modal" not in st.session_state:
    st.session_state.mostrar_modal = False
if "playlist_actual" not in st.session_state:
    st.session_state.playlist_actual = None
if "mostrar_lista_playlists" not in st.session_state:
    st.session_state.mostrar_lista_playlists = False

# Estados para gestionar qué registro estamos editando
if "edit_artista_id" not in st.session_state: st.session_state.edit_artista_id = None
if "edit_cancion_id" not in st.session_state: st.session_state.edit_cancion_id = None
if "edit_playlist_id" not in st.session_state: st.session_state.edit_playlist_id = None

# MENÚ SUPERIOR
with st.container(border=True):
    col_logo, col_m1, col_m2, col_m3, col_m4, col_resto = st.columns([2, 1, 1, 2, 1.5, 3])
    with col_logo:
        st.markdown('<div style="font-size: 24px; font-weight: 900; color: #1DB954;">Spotify</div>', unsafe_allow_html=True)
    with col_m1:
        if st.button("Inicio", key="menu_inicio"):
            st.session_state.vista_actual = "Inicio"
            st.session_state.playlist_actual = None
            st.rerun()
    with col_m2:
        if st.button("Buscar", key="menu_buscar"):
            st.session_state.vista_actual = "Buscar"
            st.session_state.playlist_actual = None
            st.rerun()
    with col_m3:
        if st.button("Crear Playlist", key="menu_crear"):
            st.session_state.mostrar_modal = True
            st.session_state.vista_actual = "Inicio"
            st.session_state.playlist_actual = None
            st.rerun()
    with col_m4:
        if st.button("Gestionar", key="menu_gestionar"):
            st.session_state.vista_actual = "Gestionar"
            st.session_state.playlist_actual = None
            # Limpiamos las selecciones al entrar
            st.session_state.edit_artista_id = None
            st.session_state.edit_cancion_id = None
            st.session_state.edit_playlist_id = None
            st.rerun()

col_izq, col_centro, col_der = st.columns([1.5, 4, 1.5])

# COLUMNA IZQUIERDA (Biblioteca)
with col_izq:
    with st.container(border=True):
        st.markdown('<div style="color: #B3B3B3; font-size: 12px; font-weight: bold; letter-spacing: 1px; margin-bottom: 15px;">TU BIBLIOTECA</div>', unsafe_allow_html=True)
        
        if st.button("Artistas Favoritos"):
            st.session_state.vista_actual = "Artistas Favoritos"
            st.session_state.playlist_actual = None
            st.rerun()
            
        st.markdown('<hr style="border: 1px solid #282828; margin: 10px 0;">', unsafe_allow_html=True)
        
        texto_boton = "Ocultar Playlists" if st.session_state.mostrar_lista_playlists else "Tus Playlists"
        if st.button(texto_boton, key="btn_toggle_playlists"):
            st.session_state.mostrar_lista_playlists = not st.session_state.mostrar_lista_playlists
            st.rerun()

        if st.session_state.mostrar_lista_playlists:
            df_playlists_sidebar = ejecutar_consulta("SELECT id_playlist, nombre FROM playlists ORDER BY id_playlist DESC;")
            if not df_playlists_sidebar.empty:
                for _, row in df_playlists_sidebar.iterrows():
                    img_default = "https://images.unsplash.com/photo-1614613535308-eb5fbd3d2c17?q=80&w=100&auto=format&fit=crop"
                    st.markdown(f'''
                    <div class="sidebar-playlist">
                        <img src="{img_default}" />
                        <div class="sidebar-playlist-info">
                            <h4>{row["nombre"]}</h4>
                            <p>Playlist</p>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
                    if st.button(f"Abrir", key=f"sb_pl_{row['id_playlist']}"):
                        st.session_state.playlist_actual = int(row["id_playlist"])
                        st.session_state.vista_actual = "Detalle_Playlist"
                        st.rerun()
            else:
                st.info("No hay playlists.")

# COLUMNA CENTRAL (Contenido)
with col_centro:
    if st.session_state.mostrar_modal:
        st.markdown("### Nueva Playlist")
        with st.form("form_crear_playlist"):
            nombre_pl = st.text_input("Nombre de la playlist")
            id_usuario = st.number_input("ID del usuario creador", min_value=1, step=1)
            col_s, col_c = st.columns(2)
            with col_s:
                submitted = st.form_submit_button("Crear")
            with col_c:
                cancelar = st.form_submit_button("Cancelar")
                
            if submitted and nombre_pl:
                if ejecutar_comando("INSERT INTO playlists (nombre, id_usuario) VALUES (%s, %s);", (nombre_pl, int(id_usuario))):
                    df_nueva = ejecutar_consulta("SELECT id_playlist FROM playlists ORDER BY id_playlist DESC LIMIT 1;")
                    if not df_nueva.empty:
                        st.session_state.playlist_actual = int(df_nueva.iloc[0]["id_playlist"])
                        st.session_state.mostrar_modal = False
                        st.session_state.vista_actual = "Detalle_Playlist"
                        st.session_state.mostrar_lista_playlists = True
                        st.rerun()
            if cancelar:
                st.session_state.mostrar_modal = False
                st.rerun()

    elif st.session_state.vista_actual == "Detalle_Playlist" and st.session_state.playlist_actual is not None:
        id_pl = int(st.session_state.playlist_actual)
        
        df_info = ejecutar_consulta(f"SELECT p.nombre, u.nombre AS creador FROM playlists p JOIN usuarios u ON p.id_usuario = u.id_usuario WHERE p.id_playlist = {id_pl};")
        if not df_info.empty:
            st.markdown(f'<h1 style="color: white; font-size: 32px; margin-bottom: 0;">{df_info.iloc[0]["nombre"]}</h1>', unsafe_allow_html=True)
            st.markdown(f'<p style="color: #B3B3B3;">Creada por {df_info.iloc[0]["creador"]}</p>', unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["Agregar Canción Existente", "Crear y Agregar Canción Nueva"])

        with tab1:
            st.markdown("#### Selecciona una canción de la base de datos")
            df_disponibles = ejecutar_consulta("SELECT id_cancion, titulo FROM canciones;")
            if not df_disponibles.empty:
                opciones = {row['titulo']: int(row['id_cancion']) for _, row in df_disponibles.iterrows()}
                with st.form("form_agregar_existente"):
                    cancion_sel = st.selectbox("Canciones disponibles", list(opciones.keys()))
                    btn_agregar = st.form_submit_button("Agregar a la Playlist")
                    if btn_agregar:
                        id_cancion = int(opciones[cancion_sel])
                        df_existe = ejecutar_consulta(f"SELECT * FROM playlist_canciones WHERE id_playlist = {id_pl} AND id_cancion = {id_cancion};")
                        if df_existe.empty:
                            if ejecutar_comando("INSERT INTO playlist_canciones (id_playlist, id_cancion) VALUES (%s, %s);", (id_pl, id_cancion)):
                                st.success("Canción agregada a la playlist")
                                st.rerun()
                        else:
                            st.warning("Esta canción ya está en la playlist.")
            else:
                st.info("No hay canciones en la base de datos.")

        with tab2:
            st.markdown("#### Agrega una canción nueva y añádela directamente")
            with st.form("form_nueva_cancion_pl"):
                titulo = st.text_input("Título de la canción")
                duracion = st.number_input("Duración en segundos", min_value=1, step=1)
                id_artista = st.number_input("ID del artista", min_value=1, step=1)
                foto = st.text_input("URL de la portada")
                btn_crear = st.form_submit_button("Crear y Agregar")
                if btn_crear and titulo:
                    if ejecutar_comando("INSERT INTO canciones (titulo, duracion, foto_portada, id_artista) VALUES (%s, %s, %s, %s);", (titulo, int(duracion), foto, int(id_artista))):
                        df_c = ejecutar_consulta("SELECT id_cancion FROM canciones ORDER BY id_cancion DESC LIMIT 1;")
                        if not df_c.empty:
                            id_c = int(df_c.iloc[0]["id_cancion"])
                            ejecutar_comando("INSERT INTO playlist_canciones (id_playlist, id_cancion) VALUES (%s, %s);", (id_pl, id_c))
                            st.success("Canción creada y agregada a la playlist")
                            st.rerun()

        st.markdown("---")
        st.markdown("#### Canciones en esta Playlist")
        df_pl_canciones = ejecutar_consulta(f"SELECT c.titulo, a.nombre AS artista, c.foto_portada FROM playlist_canciones pc JOIN canciones c ON pc.id_cancion = c.id_cancion JOIN artistas a ON c.id_artista = a.id_artista WHERE pc.id_playlist = {id_pl};")
        if not df_pl_canciones.empty:
            for _, row in df_pl_canciones.iterrows():
                st.markdown(f'<div class="song-item"><img src="{row["foto_portada"]}" /><div class="song-info"><h4>{row["titulo"]}</h4><p>{row["artista"]}</p></div></div>', unsafe_allow_html=True)
        else:
            st.info("Esta playlist aún no tiene canciones.")

        if st.button("Volver al Inicio"):
            st.session_state.vista_actual = "Inicio"
            st.session_state.playlist_actual = None
            st.rerun()

    elif st.session_state.vista_actual == "Gestionar":
        st.markdown('<h1 style="color: white; font-size: 32px; margin-bottom: 0;">Gestionar Base de Datos</h1>', unsafe_allow_html=True)
        
        tab_art, tab_can, tab_pl = st.tabs(["Artistas", "Canciones", "Playlists"])
        
        # --- PESTAÑA ARTISTAS ---
        with tab_art:
            with st.expander("Agregar Nuevo Artista"):
                with st.form("add_art"):
                    n = st.text_input("Nombre")
                    p = st.text_input("Pais")
                    f = st.text_input("URL Foto")
                    if st.form_submit_button("Guardar"):
                        ejecutar_comando("INSERT INTO artistas (nombre, pais, foto_artista) VALUES (%s, %s, %s);", (n, p, f))
                        st.success("Agregado")
                        st.rerun()

            st.markdown("### Selecciona un artista para editar")
            df_art = ejecutar_consulta("SELECT id_artista, nombre, pais, foto_artista FROM artistas ORDER BY nombre;")
            if not df_art.empty:
                for _, row in df_art.iterrows():
                    if st.session_state.edit_artista_id == row['id_artista']:
                        with st.form(f"edit_art_{row['id_artista']}"):
                            st.markdown(f"**Editando: {row['nombre']}**")
                            nn = st.text_input("Nombre", value=row['nombre'])
                            np = st.text_input("Pais", value=row['pais'])
                            nf = st.text_input("URL Foto", value=row['foto_artista'])
                            c1, c2 = st.columns(2)
                            with c1:
                                if st.form_submit_button("Actualizar"):
                                    ejecutar_comando("UPDATE artistas SET nombre=%s, pais=%s, foto_artista=%s WHERE id_artista=%s;", (nn, np, nf, int(row['id_artista'])))
                                    st.session_state.edit_artista_id = None
                                    st.rerun()
                            with c2:
                                if st.form_submit_button("Eliminar"):
                                    ejecutar_comando("DELETE FROM artistas WHERE id_artista=%s;", (int(row['id_artista']),))
                                    st.session_state.edit_artista_id = None
                                    st.rerun()
                    else:
                        st.markdown(f'<div class="gestion-box">{row["nombre"]}</div>', unsafe_allow_html=True)
                        if st.button("Editar", key=f"btn_edit_art_{row['id_artista']}"):
                            st.session_state.edit_artista_id = row['id_artista']
                            st.rerun()

        # --- PESTAÑA CANCIONES ---
        with tab_can:
            with st.expander("Agregar Nueva Canción"):
                with st.form("add_can"):
                    t = st.text_input("Titulo")
                    d = st.number_input("Duracion (seg)", min_value=1)
                    ia = st.number_input("ID Artista", min_value=1)
                    f = st.text_input("URL Portada")
                    if st.form_submit_button("Guardar"):
                        ejecutar_comando("INSERT INTO canciones (titulo, duracion, foto_portada, id_artista) VALUES (%s, %s, %s, %s);", (t, int(d), f, int(ia)))
                        st.success("Agregado")
                        st.rerun()

            st.markdown("### Selecciona una canción para editar")
            df_can = ejecutar_consulta("SELECT id_cancion, titulo, duracion, foto_portada, id_artista FROM canciones ORDER BY titulo;")
            if not df_can.empty:
                for _, row in df_can.iterrows():
                    if st.session_state.edit_cancion_id == row['id_cancion']:
                        with st.form(f"edit_can_{row['id_cancion']}"):
                            st.markdown(f"**Editando: {row['titulo']}**")
                            nt = st.text_input("Titulo", value=row['titulo'])
                            nd = st.number_input("Duracion", value=int(row['duracion']))
                            nf = st.text_input("URL Portada", value=row['foto_portada'])
                            nia = st.number_input("ID Artista", value=int(row['id_artista']))
                            c1, c2 = st.columns(2)
                            with c1:
                                if st.form_submit_button("Actualizar"):
                                    ejecutar_comando("UPDATE canciones SET titulo=%s, duracion=%s, foto_portada=%s, id_artista=%s WHERE id_cancion=%s;", (nt, int(nd), nf, int(nia), int(row['id_cancion'])))
                                    st.session_state.edit_cancion_id = None
                                    st.rerun()
                            with c2:
                                if st.form_submit_button("Eliminar"):
                                    ejecutar_comando("DELETE FROM canciones WHERE id_cancion=%s;", (int(row['id_cancion']),))
                                    st.session_state.edit_cancion_id = None
                                    st.rerun()
                    else:
                        st.markdown(f'<div class="gestion-box">{row["titulo"]}</div>', unsafe_allow_html=True)
                        if st.button("Editar", key=f"btn_edit_can_{row['id_cancion']}"):
                            st.session_state.edit_cancion_id = row['id_cancion']
                            st.rerun()

        # --- PESTAÑA PLAYLISTS ---
        with tab_pl:
            with st.expander("Agregar Nueva Playlist"):
                with st.form("add_pl"):
                    n = st.text_input("Nombre Playlist")
                    iu = st.number_input("ID Usuario Creador", min_value=1)
                    if st.form_submit_button("Guardar"):
                        ejecutar_comando("INSERT INTO playlists (nombre, id_usuario) VALUES (%s, %s);", (n, int(iu)))
                        st.success("Agregado")
                        st.rerun()

            st.markdown("### Selecciona una playlist para editar")
            df_pl = ejecutar_consulta("SELECT id_playlist, nombre, id_usuario FROM playlists ORDER BY nombre;")
            if not df_pl.empty:
                for _, row in df_pl.iterrows():
                    if st.session_state.edit_playlist_id == row['id_playlist']:
                        with st.form(f"edit_pl_{row['id_playlist']}"):
                            st.markdown(f"**Editando: {row['nombre']}**")
                            nn = st.text_input("Nombre", value=row['nombre'])
                            niu = st.number_input("ID Usuario", value=int(row['id_usuario']))
                            c1, c2 = st.columns(2)
                            with c1:
                                if st.form_submit_button("Actualizar"):
                                    ejecutar_comando("UPDATE playlists SET nombre=%s, id_usuario=%s WHERE id_playlist=%s;", (nn, int(niu), int(row['id_playlist'])))
                                    st.session_state.edit_playlist_id = None
                                    st.rerun()
                            with c2:
                                if st.form_submit_button("Eliminar"):
                                    ejecutar_comando("DELETE FROM playlists WHERE id_playlist=%s;", (int(row['id_playlist']),))
                                    st.session_state.edit_playlist_id = None
                                    st.rerun()
                    else:
                        st.markdown(f'<div class="gestion-box">{row["nombre"]}</div>', unsafe_allow_html=True)
                        if st.button("Editar", key=f"btn_edit_pl_{row['id_playlist']}"):
                            st.session_state.edit_playlist_id = row['id_playlist']
                            st.rerun()

    elif st.session_state.vista_actual == "Inicio":
        st.markdown('<h1 style="color: white; font-size: 32px; margin-bottom: 0;">Buenas tardes</h1>', unsafe_allow_html=True)

        st.markdown('<div class="section-title">Artistas Populares</div>', unsafe_allow_html=True)
        df_artistas = ejecutar_consulta("SELECT id_artista, nombre, foto_artista FROM artistas LIMIT 10;")
        
        if not df_artistas.empty:
            html_artistas = '<div class="carousel-container">'
            for _, row in df_artistas.iterrows():
                html_artistas += f'<div class="card-artist"><img src="{row["foto_artista"]}" /><h4>{row["nombre"]}</h4><p>Artista</p></div>'
            html_artistas += '</div>'
            st.markdown(html_artistas, unsafe_allow_html=True)

    elif st.session_state.vista_actual == "Buscar":
        st.markdown('<h1 style="color: white; font-size: 32px; margin-bottom: 0;">Buscar Canciones</h1>', unsafe_allow_html=True)
        busqueda = st.text_input("Escribe el nombre de una canción o artista...")
        if busqueda:
            query_buscar = f"SELECT c.titulo, a.nombre AS artista, c.foto_portada FROM canciones c JOIN artistas a ON c.id_artista = a.id_artista WHERE c.titulo ILIKE '%{busqueda}%' OR a.nombre ILIKE '%{busqueda}%';"
            df_busqueda = ejecutar_consulta(query_buscar)
            if not df_busqueda.empty:
                for _, row in df_busqueda.iterrows():
                    st.markdown(f'<div class="song-item"><img src="{row["foto_portada"]}" /><div class="song-info"><h4>{row["titulo"]}</h4><p>{row["artista"]}</p></div></div>', unsafe_allow_html=True)
            else:
                st.info("No se encontraron resultados.")
                
    elif st.session_state.vista_actual == "Artistas Favoritos":
        st.markdown('<h1 style="color: white; font-size: 32px; margin-bottom: 0;">Todos los Artistas</h1>', unsafe_allow_html=True)
        df_todos = ejecutar_consulta("SELECT nombre, pais, foto_artista FROM artistas;")
        if not df_todos.empty:
            html_todos = '<div class="carousel-container" style="flex-wrap: wrap; overflow-x: hidden;">'
            for _, row in df_todos.iterrows():
                html_todos += f'<div class="card-artist" style="margin: 10px;"><img src="{row["foto_artista"]}" /><h4>{row["nombre"]}</h4><p>{row["pais"]}</p></div>'
            html_todos += '</div>'
            st.markdown(html_todos, unsafe_allow_html=True)

# COLUMNA DERECHA (Canciones Recientes)
with col_der:
    with st.container(border=True):
        st.markdown('<h3 style="color: white; margin-top: 0; font-size: 18px;">Canciones Recientes</h3>', unsafe_allow_html=True)
        query_canciones = "SELECT c.titulo, a.nombre AS artista, c.foto_portada FROM canciones c JOIN artistas a ON c.id_artista = a.id_artista LIMIT 15;"
        df_canciones = ejecutar_consulta(query_canciones)
        if not df_canciones.empty:
            for _, row in df_canciones.iterrows():
                st.markdown(f'<div class="song-item"><img src="{row["foto_portada"]}" /><div class="song-info"><h4>{row["titulo"]}</h4><p>{row["artista"]}</p></div></div>', unsafe_allow_html=True)
        else:
            st.info("No hay canciones.")