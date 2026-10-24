-- 1. TABLA USUARIOS
CREATE TABLE usuarios (
    id_usuario SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    foto_perfil TEXT,
    fecha_registro DATE DEFAULT CURRENT_DATE
);

-- 2. TABLA ARTISTAS
CREATE TABLE artistas (
    id_artista SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    pais VARCHAR(50),
    foto_artista TEXT
);

-- 3. TABLA GENEROS
CREATE TABLE generos (
    id_genero SERIAL PRIMARY KEY,
    nombre_genero VARCHAR(50) UNIQUE NOT NULL
);

-- 4. TABLA CANCIONES
CREATE TABLE canciones (
    id_cancion SERIAL PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    duracion INT CHECK (duracion > 0),
    foto_portada TEXT,
    id_artista INT NOT NULL,
    CONSTRAINT fk_cancion_artista FOREIGN KEY (id_artista) 
        REFERENCES artistas(id_artista) ON DELETE CASCADE
);

-- 5. TABLA PLAYLISTS
CREATE TABLE playlists (
    id_playlist SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    id_usuario INT NOT NULL,
    fecha_creacion DATE DEFAULT CURRENT_DATE,
    CONSTRAINT fk_playlist_usuario FOREIGN KEY (id_usuario) 
        REFERENCES usuarios(id_usuario) ON DELETE CASCADE
);

-- 6. TABLA INTERMEDIA: PLAYLIST_CANCIONES (Relación Muchos a Muchos)
CREATE TABLE playlist_canciones (
    id_playlist INT NOT NULL,
    id_cancion INT NOT NULL,
    fecha_agregado DATE DEFAULT CURRENT_DATE,
    PRIMARY KEY (id_playlist, id_cancion),
    CONSTRAINT fk_pc_playlist FOREIGN KEY (id_playlist) 
        REFERENCES playlists(id_playlist) ON DELETE CASCADE,
    CONSTRAINT fk_pc_cancion FOREIGN KEY (id_cancion) 
        REFERENCES canciones(id_cancion) ON DELETE CASCADE
);

-- 7. TABLA INTERMEDIA: CANCION_GENERO (Relación Muchos a Muchos)
CREATE TABLE cancion_genero (
    id_cancion INT NOT NULL,
    id_genero INT NOT NULL,
    PRIMARY KEY (id_cancion, id_genero),
    CONSTRAINT fk_cg_cancion FOREIGN KEY (id_cancion) 
        REFERENCES canciones(id_cancion) ON DELETE CASCADE,
    CONSTRAINT fk_cg_genero FOREIGN KEY (id_genero) 
        REFERENCES generos(id_genero) ON DELETE CASCADE
);

-- USUARIOS (10 registros)
INSERT INTO usuarios (nombre, email, foto_perfil) VALUES
('Ana Garcia', 'ana@mail.com', 'https://i.pravatar.cc/150?img=1'),
('Luis Perez', 'luis@mail.com', 'https://i.pravatar.cc/150?img=2'),
('Maria Lopez', 'maria@mail.com', 'https://i.pravatar.cc/150?img=3'),
('Carlos Ruiz', 'carlos@mail.com', 'https://i.pravatar.cc/150?img=4'),
('Sofia Diaz', 'sofia@mail.com', 'https://i.pravatar.cc/150?img=5'),
('Jorge Torres', 'jorge@mail.com', 'https://i.pravatar.cc/150?img=6'),
('Elena Vargas', 'elena@mail.com', 'https://i.pravatar.cc/150?img=7'),
('Pedro Mendez', 'pedro@mail.com', 'https://i.pravatar.cc/150?img=8'),
('Lucia Castro', 'lucia@mail.com', 'https://i.pravatar.cc/150?img=9'),
('Diego Silva', 'diego@mail.com', 'https://i.pravatar.cc/150?img=10');

-- ARTISTAS (10 registros)
INSERT INTO artistas (nombre, pais, foto_artista) VALUES
('The Weeknd', 'Canada', 'https://i.pravatar.cc/150?img=11'),
('Dua Lipa', 'Reino Unido', 'https://i.pravatar.cc/150?img=12'),
('Bad Bunny', 'Puerto Rico', 'https://i.pravatar.cc/150?img=13'),
('Taylor Swift', 'EEUU', 'https://i.pravatar.cc/150?img=14'),
('Coldplay', 'Reino Unido', 'https://i.pravatar.cc/150?img=15'),
('Shakira', 'Colombia', 'https://i.pravatar.cc/150?img=16'),
('Ed Sheeran', 'Reino Unido', 'https://i.pravatar.cc/150?img=17'),
('Billie Eilish', 'EEUU', 'https://i.pravatar.cc/150?img=18'),
('Karol G', 'Colombia', 'https://i.pravatar.cc/150?img=19'),
('Drake', 'Canada', 'https://i.pravatar.cc/150?img=20');

-- GENEROS (10 registros)
INSERT INTO generos (nombre_genero) VALUES
('Pop'), ('Rock'), ('Reggaeton'), ('Hip Hop'), ('R&B'),
('Electronica'), ('Jazz'), ('Clasica'), ('Indie'), ('Latina');

-- CANCIONES (12 registros)
INSERT INTO canciones (titulo, duracion, foto_portada, id_artista) VALUES
('Blinding Lights', 200, 'https://picsum.photos/seed/1/200', 1),
('Levitating', 203, 'https://picsum.photos/seed/2/200', 2),
('Tití Me Preguntó', 243, 'https://picsum.photos/seed/3/200', 3),
('Anti-Hero', 200, 'https://picsum.photos/seed/4/200', 4),
('Yellow', 266, 'https://picsum.photos/seed/5/200', 5),
('Hips Don''t Lie', 218, 'https://picsum.photos/seed/6/200', 6),
('Shape of You', 233, 'https://picsum.photos/seed/7/200', 7),
('Bad Guy', 194, 'https://picsum.photos/seed/8/200', 8),
('PROVENZA', 210, 'https://picsum.photos/seed/9/200', 9),
('God''s Plan', 198, 'https://picsum.photos/seed/10/200', 10),
('Save Your Tears', 215, 'https://picsum.photos/seed/11/200', 1),
('Physical', 194, 'https://picsum.photos/seed/12/200', 2);

-- PLAYLISTS (10 registros)
INSERT INTO playlists (nombre, id_usuario) VALUES
('Favoritas 2024', 1), ('Para Estudiar', 2), ('Fiesta Total', 3),
('Road Trip', 4), ('Relax', 5), ('Hits del Momento', 6),
('Rock Clasico', 7), ('Pop Latino', 8), ('Indie Vibes', 9),
('Workout', 10);

-- PLAYLIST_CANCIONES (Relacion muchos a muchos)
INSERT INTO playlist_canciones (id_playlist, id_cancion) VALUES
(1, 1), (1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (4, 8),
(5, 9), (6, 10), (7, 11), (8, 12), (9, 1), (10, 2);

-- CANCION_GENERO (Relacion muchos a muchos)
INSERT INTO cancion_genero (id_cancion, id_genero) VALUES
(1, 1), (2, 1), (3, 3), (4, 1), (5, 2), (6, 3), (7, 1),
(8, 9), (9, 3), (10, 4), (11, 1), (12, 1);