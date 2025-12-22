-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 22-12-2025 a las 10:34:28
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.4.13

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `pre_icfes`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `areas`
--

CREATE TABLE `areas` (
  `id_area` int(11) NOT NULL,
  `codigo` varchar(30) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `activa` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `areas`
--

INSERT INTO `areas` (`id_area`, `codigo`, `nombre`, `activa`) VALUES
(1, 'MAT', 'Matemáticas', 1),
(2, 'LEC', 'Lectura Crítica', 1),
(3, 'CIE', 'Ciencias Naturales', 1),
(4, 'SOC', 'Sociales y Ciudadanas', 1),
(5, 'ING', 'Inglés', 1),
(6, 'SOCIO', 'Destrezas Socio-Ocupacionales', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estudiante`
--

CREATE TABLE `estudiante` (
  `id_usuario` int(11) NOT NULL,
  `institucion` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `lecciones`
--

CREATE TABLE `lecciones` (
  `id_leccion` int(11) NOT NULL,
  `area_id` int(11) NOT NULL,
  `titulo` varchar(150) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `nivel_recomendado` enum('Bajo','Medio','Alto') NOT NULL,
  `activa` tinyint(1) DEFAULT 1,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `creado_por` int(11) NOT NULL,
  `actualizado_por` int(11) DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pregunta_diagnostico`
--

CREATE TABLE `pregunta_diagnostico` (
  `id_pregunta_diagnostico` int(11) NOT NULL,
  `area_id` int(11) NOT NULL,
  `dificultad` enum('Baja','Media','Alta') NOT NULL,
  `enunciado` text NOT NULL,
  `opciones` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`opciones`)),
  `respuesta_correcta` int(11) NOT NULL,
  `activa` tinyint(1) DEFAULT 1,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `creado_por` int(11) NOT NULL,
  `actualizado_por` int(11) DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL ON UPDATE current_timestamp(),
  `tipo_pregunta_id` int(11) NOT NULL,
  `imagen_url` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `pregunta_diagnostico`
--

INSERT INTO `pregunta_diagnostico` (`id_pregunta_diagnostico`, `area_id`, `dificultad`, `enunciado`, `opciones`, `respuesta_correcta`, `activa`, `created_at`, `creado_por`, `actualizado_por`, `updated_at`, `tipo_pregunta_id`, `imagen_url`) VALUES
(54, 1, 'Baja', '¿Cuánto es 8 × 7?', '[\"54\",\"56\",\"48\",\"64\"]', 1, 1, '2025-12-22 09:28:53', 6, NULL, NULL, 1, NULL),
(55, 1, 'Baja', '¿Cuánto es 15 − 9?', '[\"4\",\"5\",\"6\",\"7\"]', 2, 1, '2025-12-22 09:28:53', 6, NULL, NULL, 1, NULL),
(56, 1, 'Media', '¿Cuál es el área de un cuadrado de lado 5?', '[\"10\",\"20\",\"25\",\"30\"]', 2, 1, '2025-12-22 09:28:53', 6, NULL, NULL, 1, NULL),
(57, 1, 'Media', '¿Cuánto es 12 ÷ 3?', '[\"2\",\"3\",\"4\",\"6\"]', 2, 1, '2025-12-22 09:28:53', 6, NULL, NULL, 1, NULL),
(58, 1, 'Alta', '¿Resultado de 2³ + 4?', '[\"10\",\"12\",\"8\",\"6\"]', 0, 1, '2025-12-22 09:28:53', 6, NULL, NULL, 1, NULL),
(59, 1, 'Alta', '¿Raíz cuadrada de 81?', '[\"7\",\"8\",\"9\",\"10\"]', 2, 1, '2025-12-22 09:28:53', 6, NULL, NULL, 1, NULL),
(60, 1, 'Media', '¿Perímetro de un cuadrado de lado 4?', '[\"8\",\"12\",\"16\",\"20\"]', 2, 1, '2025-12-22 09:28:53', 6, NULL, NULL, 1, NULL),
(61, 1, 'Baja', '¿Cuánto es 9 + 6?', '[\"13\",\"14\",\"15\",\"16\"]', 2, 1, '2025-12-22 09:28:53', 6, NULL, NULL, 1, NULL),
(62, 1, 'Media', '¿Cuánto es 7 × 6?', '[\"36\",\"42\",\"48\",\"56\"]', 1, 1, '2025-12-22 09:28:53', 6, NULL, NULL, 1, NULL),
(63, 1, 'Alta', '¿Resultado de (10 − 2) × 3?', '[\"18\",\"21\",\"24\",\"30\"]', 0, 1, '2025-12-22 09:28:53', 6, NULL, NULL, 1, NULL),
(64, 2, 'Baja', '¿Cuál es la idea principal de un texto?', '[\"El tema central\",\"Un ejemplo\",\"Una opinión\",\"Un detalle\"]', 0, 1, '2025-12-22 09:29:04', 6, NULL, NULL, 1, NULL),
(65, 2, 'Baja', '¿Qué es un sinónimo?', '[\"Palabra opuesta\",\"Palabra similar\",\"Frase larga\",\"Texto\"]', 1, 1, '2025-12-22 09:29:04', 6, NULL, NULL, 1, NULL),
(66, 2, 'Media', '¿Cuál es la intención del autor?', '[\"Informar\",\"Confundir\",\"Copiar\",\"Decorar\"]', 0, 1, '2025-12-22 09:29:04', 6, NULL, NULL, 1, NULL),
(67, 2, 'Media', 'Un texto argumentativo busca:', '[\"Narrar\",\"Describir\",\"Convencer\",\"Enumerar\"]', 2, 1, '2025-12-22 09:29:04', 6, NULL, NULL, 1, NULL),
(68, 2, 'Alta', '¿Qué es una inferencia?', '[\"Opinión directa\",\"Conclusión implícita\",\"Dato explícito\",\"Resumen\"]', 1, 1, '2025-12-22 09:29:04', 6, NULL, NULL, 1, NULL),
(69, 2, 'Media', '¿Qué función cumple un título?', '[\"Decorar\",\"Anticipar el tema\",\"Confundir\",\"Cerrar el texto\"]', 1, 1, '2025-12-22 09:29:04', 6, NULL, NULL, 1, NULL),
(70, 2, 'Baja', '¿Qué es un texto narrativo?', '[\"Cuenta hechos\",\"Da instrucciones\",\"Enumera datos\",\"Explica reglas\"]', 0, 1, '2025-12-22 09:29:04', 6, NULL, NULL, 1, NULL),
(71, 2, 'Alta', '¿Qué es coherencia textual?', '[\"Orden lógico\",\"Ortografía\",\"Longitud\",\"Cantidad de palabras\"]', 0, 1, '2025-12-22 09:29:04', 6, NULL, NULL, 1, NULL),
(72, 2, 'Media', '¿Un argumento se apoya en?', '[\"Opiniones\",\"Datos\",\"Errores\",\"Imágenes\"]', 1, 1, '2025-12-22 09:29:04', 6, NULL, NULL, 1, NULL),
(73, 2, 'Alta', '¿Qué es un punto de vista?', '[\"Lugar\",\"Opinión\",\"Título\",\"Autor\"]', 1, 1, '2025-12-22 09:29:04', 6, NULL, NULL, 1, NULL),
(74, 3, 'Baja', '¿Cuál es el estado líquido del agua?', '[\"Hielo\",\"Vapor\",\"Agua\",\"Nube\"]', 2, 1, '2025-12-22 09:29:13', 6, NULL, NULL, 1, NULL),
(75, 3, 'Baja', '¿Cuál es un ser vivo?', '[\"Piedra\",\"Mesa\",\"Árbol\",\"Libro\"]', 2, 1, '2025-12-22 09:29:13', 6, NULL, NULL, 1, NULL),
(76, 3, 'Media', '¿Qué órgano bombea la sangre?', '[\"Pulmón\",\"Riñón\",\"Corazón\",\"Hígado\"]', 2, 1, '2025-12-22 09:29:13', 6, NULL, NULL, 1, NULL),
(77, 3, 'Media', '¿Qué gas respiramos?', '[\"CO₂\",\"Oxígeno\",\"Nitrógeno\",\"Helio\"]', 1, 1, '2025-12-22 09:29:13', 6, NULL, NULL, 1, NULL),
(78, 3, 'Alta', '¿Qué es la fotosíntesis?', '[\"Respiración\",\"Digestión\",\"Producción de alimento\",\"Movimiento\"]', 2, 1, '2025-12-22 09:29:13', 6, NULL, NULL, 1, NULL),
(79, 3, 'Media', '¿Qué planeta es rojo?', '[\"Tierra\",\"Marte\",\"Venus\",\"Júpiter\"]', 1, 1, '2025-12-22 09:29:13', 6, NULL, NULL, 1, NULL),
(80, 3, 'Baja', '¿Qué necesitan las plantas?', '[\"Luz\",\"Sombras\",\"Humo\",\"Plástico\"]', 0, 1, '2025-12-22 09:29:13', 6, NULL, NULL, 1, NULL),
(81, 3, 'Alta', '¿Qué estudia la biología?', '[\"Rocas\",\"Seres vivos\",\"Números\",\"Idiomas\"]', 1, 1, '2025-12-22 09:29:13', 6, NULL, NULL, 1, NULL),
(82, 3, 'Media', '¿Qué es un ecosistema?', '[\"Un animal\",\"Un lugar\",\"Relación de seres vivos\",\"Un planeta\"]', 2, 1, '2025-12-22 09:29:13', 6, NULL, NULL, 1, NULL),
(83, 3, 'Alta', '¿Qué es ADN?', '[\"Proteína\",\"Material genético\",\"Órgano\",\"Célula\"]', 1, 1, '2025-12-22 09:29:13', 6, NULL, NULL, 1, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipo_pregunta`
--

CREATE TABLE `tipo_pregunta` (
  `id_tipo_pregunta` int(11) NOT NULL,
  `codigo` varchar(30) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `activa` tinyint(1) DEFAULT 1,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `tipo_pregunta`
--

INSERT INTO `tipo_pregunta` (`id_tipo_pregunta`, `codigo`, `nombre`, `descripcion`, `activa`, `created_at`) VALUES
(1, 'SMUR', 'Selección múltiple única respuesta', 'Pregunta con 4 opciones y una sola correcta', 1, '2025-12-21 04:18:09'),
(2, 'SMUR_CONTEXTO', 'Selección múltiple con contexto', 'Pregunta basada en un texto, caso o situación', 1, '2025-12-21 04:18:09'),
(3, 'AFIRMACIONES', 'Pregunta por afirmaciones', 'Se evalúan combinaciones de afirmaciones', 1, '2025-12-21 04:18:09'),
(4, 'IMAGEN', 'Selección múltiple con imagen', 'Incluye una imagen o gráfico', 1, '2025-12-21 04:18:09'),
(5, 'TABLA', 'Selección múltiple con tabla', 'Incluye una tabla de datos', 1, '2025-12-21 04:18:09');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--

CREATE TABLE `usuario` (
  `id_usuario` int(11) NOT NULL,
  `nombres` varchar(100) NOT NULL,
  `apellidos` varchar(100) NOT NULL,
  `tipo_documento` enum('CC','CE','TI') NOT NULL,
  `numero_documento` varchar(20) NOT NULL,
  `correo` varchar(150) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `fecha_nacimiento` date NOT NULL,
  `rol` enum('estudiante','docente','coordinador','admin') NOT NULL,
  `activo` tinyint(1) DEFAULT 1,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuario`
--

INSERT INTO `usuario` (`id_usuario`, `nombres`, `apellidos`, `tipo_documento`, `numero_documento`, `correo`, `password_hash`, `fecha_nacimiento`, `rol`, `activo`, `created_at`, `updated_at`) VALUES
(5, 'Harol', 'Pardo ', 'CC', '145225478', 'harol@hotmail.com', '$2b$12$eSLJT9yMQVcazHlHQXyl1O5cFESfo03rFR9yL/UTIcyuQC25qKGS2', '2000-12-17', 'estudiante', 1, '2025-12-17 14:48:20', '2025-12-17 14:48:20'),
(6, 'Daniel', 'cañon', 'CC', '1012443507', 'danielcf97@hotmail.com', '$2b$12$kJJwQqN1hyAghx6gc4gX/.w0g2bC4FBGk.O5PBJbdhLLaeI0i2IHq', '1997-06-01', 'admin', 1, '2025-12-17 15:55:48', '2025-12-17 15:55:48');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `areas`
--
ALTER TABLE `areas`
  ADD PRIMARY KEY (`id_area`),
  ADD UNIQUE KEY `codigo` (`codigo`);

--
-- Indices de la tabla `estudiante`
--
ALTER TABLE `estudiante`
  ADD PRIMARY KEY (`id_usuario`);

--
-- Indices de la tabla `lecciones`
--
ALTER TABLE `lecciones`
  ADD PRIMARY KEY (`id_leccion`),
  ADD KEY `fk_leccion_area` (`area_id`),
  ADD KEY `fk_leccion_creado_por` (`creado_por`),
  ADD KEY `fk_leccion_actualizado_por` (`actualizado_por`);

--
-- Indices de la tabla `pregunta_diagnostico`
--
ALTER TABLE `pregunta_diagnostico`
  ADD PRIMARY KEY (`id_pregunta_diagnostico`),
  ADD KEY `fk_pregunta_area` (`area_id`),
  ADD KEY `fk_pd_creado_por` (`creado_por`),
  ADD KEY `fk_pd_actualizado_por` (`actualizado_por`),
  ADD KEY `fk_pregunta_tipo` (`tipo_pregunta_id`);

--
-- Indices de la tabla `tipo_pregunta`
--
ALTER TABLE `tipo_pregunta`
  ADD PRIMARY KEY (`id_tipo_pregunta`),
  ADD UNIQUE KEY `codigo` (`codigo`);

--
-- Indices de la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`id_usuario`),
  ADD UNIQUE KEY `numero_documento` (`numero_documento`),
  ADD UNIQUE KEY `correo` (`correo`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `areas`
--
ALTER TABLE `areas`
  MODIFY `id_area` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `lecciones`
--
ALTER TABLE `lecciones`
  MODIFY `id_leccion` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `pregunta_diagnostico`
--
ALTER TABLE `pregunta_diagnostico`
  MODIFY `id_pregunta_diagnostico` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=84;

--
-- AUTO_INCREMENT de la tabla `tipo_pregunta`
--
ALTER TABLE `tipo_pregunta`
  MODIFY `id_tipo_pregunta` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `usuario`
--
ALTER TABLE `usuario`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `estudiante`
--
ALTER TABLE `estudiante`
  ADD CONSTRAINT `estudiante_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id_usuario`) ON DELETE CASCADE;

--
-- Filtros para la tabla `lecciones`
--
ALTER TABLE `lecciones`
  ADD CONSTRAINT `fk_leccion_actualizado_por` FOREIGN KEY (`actualizado_por`) REFERENCES `usuario` (`id_usuario`),
  ADD CONSTRAINT `fk_leccion_creado_por` FOREIGN KEY (`creado_por`) REFERENCES `usuario` (`id_usuario`);

--
-- Filtros para la tabla `pregunta_diagnostico`
--
ALTER TABLE `pregunta_diagnostico`
  ADD CONSTRAINT `fk_pd_actualizado_por` FOREIGN KEY (`actualizado_por`) REFERENCES `usuario` (`id_usuario`),
  ADD CONSTRAINT `fk_pd_creado_por` FOREIGN KEY (`creado_por`) REFERENCES `usuario` (`id_usuario`),
  ADD CONSTRAINT `fk_pregunta_area` FOREIGN KEY (`area_id`) REFERENCES `areas` (`id_area`),
  ADD CONSTRAINT `fk_pregunta_tipo` FOREIGN KEY (`tipo_pregunta_id`) REFERENCES `tipo_pregunta` (`id_tipo_pregunta`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
