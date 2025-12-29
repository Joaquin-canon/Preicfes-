-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 29-12-2025 a las 05:31:20
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
  `contexto` longtext DEFAULT NULL,
  `enunciado` text NOT NULL,
  `opciones` longtext DEFAULT NULL,
  `respuesta_correcta` int(11) DEFAULT NULL,
  `activa` tinyint(1) DEFAULT 1,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `creado_por` int(11) DEFAULT NULL,
  `actualizado_por` int(11) DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL ON UPDATE current_timestamp(),
  `tipo_pregunta_id` int(11) NOT NULL,
  `imagen_url` varchar(255) DEFAULT NULL,
  `idioma` enum('ES','EN') NOT NULL DEFAULT 'ES'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `pregunta_diagnostico`
--

INSERT INTO `pregunta_diagnostico` (`id_pregunta_diagnostico`, `area_id`, `dificultad`, `contexto`, `enunciado`, `opciones`, `respuesta_correcta`, `activa`, `created_at`, `creado_por`, `actualizado_por`, `updated_at`, `tipo_pregunta_id`, `imagen_url`, `idioma`) VALUES
(1, 1, 'Baja', NULL, '¿Cuánto es 6 + 4?', '[\"8\",\"9\",\"10\",\"11\"]', 2, 1, '2025-12-29 00:16:48', 6, NULL, NULL, 1, NULL, 'ES'),
(2, 1, 'Baja', NULL, '¿Cuánto es 5 × 3?', '[\"10\",\"15\",\"20\",\"25\"]', 1, 1, '2025-12-29 00:16:48', 6, NULL, NULL, 1, NULL, 'ES'),
(3, 1, 'Media', NULL, '¿Resultado de 18 ÷ 3?', '[\"4\",\"5\",\"6\",\"7\"]', 2, 1, '2025-12-29 00:16:48', 6, NULL, NULL, 1, NULL, 'ES'),
(4, 1, 'Alta', NULL, '¿Cuánto es 2³ + 1?', '[\"7\",\"8\",\"9\",\"10\"]', 2, 1, '2025-12-29 00:16:48', 6, NULL, NULL, 1, NULL, 'ES'),
(5, 1, 'Media', NULL, 'Un cuadrado tiene lado 4 cm. ¿Cuál es su perímetro?', '[\"12\",\"14\",\"16\",\"18\"]', 2, 1, '2025-12-29 00:16:48', 6, NULL, NULL, 2, NULL, 'ES'),
(6, 1, 'Alta', NULL, 'Si un triángulo tiene base 6 y altura 4, ¿cuál es su área?', '[\"10\",\"12\",\"14\",\"16\"]', 1, 1, '2025-12-29 00:16:48', 6, NULL, NULL, 2, NULL, 'ES'),
(7, 1, 'Media', NULL, 'I. 2 es primo. II. 4 es primo. ¿Cuál es correcta?', '[\"Solo I\",\"Solo II\",\"Ambas\",\"Ninguna\"]', 0, 1, '2025-12-29 00:16:48', 6, NULL, NULL, 3, NULL, 'ES'),
(8, 1, 'Alta', NULL, 'I. √9=3. II. √16=5. ¿Cuál es correcta?', '[\"Solo I\",\"Solo II\",\"Ambas\",\"Ninguna\"]', 0, 1, '2025-12-29 00:16:48', 6, NULL, NULL, 3, NULL, 'ES'),
(9, 1, 'Media', NULL, 'Observa la gráfica y selecciona el valor mayor.', '[\"2\",\"4\",\"6\",\"8\"]', 3, 1, '2025-12-29 00:16:48', 6, NULL, NULL, 4, NULL, 'ES'),
(10, 1, 'Alta', NULL, 'Según la tabla de valores, ¿cuál es el promedio?', '[\"4\",\"5\",\"6\",\"7\"]', 1, 1, '2025-12-29 00:16:48', 6, NULL, NULL, 5, NULL, 'ES'),
(11, 2, 'Baja', NULL, '¿Qué es un sinónimo?', '[\"Contrario\",\"Igual significado\",\"Ejemplo\",\"Título\"]', 1, 1, '2025-12-29 00:17:05', 6, NULL, NULL, 1, NULL, 'ES'),
(12, 2, 'Baja', NULL, 'La idea principal de un texto es:', '[\"Tema central\",\"Detalle\",\"Opinión\",\"Imagen\"]', 0, 1, '2025-12-29 00:17:05', 6, NULL, NULL, 1, NULL, 'ES'),
(13, 2, 'Media', NULL, '¿Qué busca un texto argumentativo?', '[\"Narrar\",\"Convencer\",\"Describir\",\"Enumerar\"]', 1, 1, '2025-12-29 00:17:05', 6, NULL, NULL, 1, NULL, 'ES'),
(14, 2, 'Alta', NULL, '¿Qué es una inferencia?', '[\"Dato explícito\",\"Opinión\",\"Conclusión implícita\",\"Resumen\"]', 2, 1, '2025-12-29 00:17:05', 6, NULL, NULL, 1, NULL, 'ES'),
(15, 2, 'Media', NULL, 'El autor menciona datos para:', '[\"Confundir\",\"Convencer\",\"Narrar\",\"Repetir\"]', 1, 1, '2025-12-29 00:17:05', 6, NULL, NULL, 2, NULL, 'ES'),
(16, 2, 'Alta', NULL, 'Según el texto, la intención principal es:', '[\"Informar\",\"Criticar\",\"Describir\",\"Entretener\"]', 0, 1, '2025-12-29 00:17:05', 6, NULL, NULL, 2, NULL, 'ES'),
(17, 2, 'Media', NULL, 'I. El texto tiene introducción. II. Tiene conclusión.', '[\"Solo I\",\"Solo II\",\"Ambas\",\"Ninguna\"]', 2, 1, '2025-12-29 00:17:05', 6, NULL, NULL, 3, NULL, 'ES'),
(18, 2, 'Alta', NULL, 'I. Es objetivo. II. Usa opiniones.', '[\"Solo I\",\"Solo II\",\"Ambas\",\"Ninguna\"]', 3, 1, '2025-12-29 00:17:05', 6, NULL, NULL, 3, NULL, 'ES'),
(19, 2, 'Media', NULL, 'Según la imagen, el mensaje principal es:', '[\"Ambiental\",\"Político\",\"Cultural\",\"Social\"]', 0, 1, '2025-12-29 00:17:05', 6, NULL, NULL, 4, NULL, 'ES'),
(20, 2, 'Alta', NULL, 'Según la tabla, el texto más largo es:', '[\"A\",\"B\",\"C\",\"D\"]', 2, 1, '2025-12-29 00:17:05', 6, NULL, NULL, 5, NULL, 'ES'),
(21, 3, 'Baja', NULL, '¿Cuál es un ser vivo?', '[\"Piedra\",\"Mesa\",\"Árbol\",\"Libro\"]', 2, 1, '2025-12-29 00:20:16', 6, NULL, NULL, 1, NULL, 'ES'),
(22, 3, 'Baja', NULL, '¿Qué órgano bombea la sangre?', '[\"Pulmón\",\"Riñón\",\"Corazón\",\"Hígado\"]', 2, 1, '2025-12-29 00:20:16', 6, NULL, NULL, 1, NULL, 'ES'),
(23, 3, 'Media', NULL, '¿Qué gas respiramos principalmente?', '[\"CO₂\",\"Oxígeno\",\"Nitrógeno\",\"Helio\"]', 1, 1, '2025-12-29 00:20:16', 6, NULL, NULL, 1, NULL, 'ES'),
(24, 3, 'Alta', NULL, '¿Qué proceso realizan las plantas para producir alimento?', '[\"Respiración\",\"Fotosíntesis\",\"Digestión\",\"Evaporación\"]', 1, 1, '2025-12-29 00:20:16', 6, NULL, NULL, 1, NULL, 'ES'),
(25, 3, 'Media', NULL, 'Las plantas usan la luz solar para:', '[\"Respirar\",\"Fotosintetizar\",\"Moverse\",\"Reproducirse\"]', 1, 1, '2025-12-29 00:20:16', 6, NULL, NULL, 2, NULL, 'ES'),
(26, 3, 'Alta', NULL, 'El agua cambia de estado sólido a líquido mediante:', '[\"Evaporación\",\"Condensación\",\"Fusión\",\"Sublimación\"]', 2, 1, '2025-12-29 00:20:16', 6, NULL, NULL, 2, NULL, 'ES'),
(27, 3, 'Media', NULL, 'I. El corazón bombea sangre. II. Los pulmones producen sangre.', '[\"Solo I\",\"Solo II\",\"Ambas\",\"Ninguna\"]', 0, 1, '2025-12-29 00:20:16', 6, NULL, NULL, 3, NULL, 'ES'),
(28, 3, 'Alta', NULL, 'I. El ADN contiene información genética. II. Está solo en animales.', '[\"Solo I\",\"Solo II\",\"Ambas\",\"Ninguna\"]', 0, 1, '2025-12-29 00:20:16', 6, NULL, NULL, 3, NULL, 'ES'),
(29, 3, 'Media', NULL, 'Según la imagen del sistema solar, ¿qué planeta es el tercero?', '[\"Mercurio\",\"Venus\",\"Tierra\",\"Marte\"]', 2, 1, '2025-12-29 00:20:16', 6, NULL, NULL, 4, NULL, 'ES'),
(30, 3, 'Alta', NULL, 'Según la tabla de temperaturas, ¿cuál es la más alta?', '[\"20°C\",\"25°C\",\"30°C\",\"35°C\"]', 3, 1, '2025-12-29 00:20:16', 6, NULL, NULL, 5, NULL, 'ES'),
(31, 4, 'Baja', NULL, '¿Qué es una norma?', '[\"Regla\",\"Castigo\",\"Derecho\",\"Opinión\"]', 0, 1, '2025-12-29 00:20:25', 6, NULL, NULL, 1, NULL, 'ES'),
(32, 4, 'Baja', NULL, '¿Quién elige al presidente?', '[\"El rey\",\"El pueblo\",\"El congreso\",\"Los jueces\"]', 1, 1, '2025-12-29 00:20:25', 6, NULL, NULL, 1, NULL, 'ES'),
(33, 4, 'Media', NULL, '¿Qué es la democracia?', '[\"Dictadura\",\"Gobierno del pueblo\",\"Monarquía\",\"Anarquía\"]', 1, 1, '2025-12-29 00:20:25', 6, NULL, NULL, 1, NULL, 'ES'),
(34, 4, 'Alta', NULL, '¿Qué derecho protege la libertad de expresión?', '[\"Político\",\"Civil\",\"Económico\",\"Cultural\"]', 1, 1, '2025-12-29 00:20:25', 6, NULL, NULL, 1, NULL, 'ES'),
(35, 4, 'Media', NULL, 'Una comunidad organizada busca principalmente:', '[\"Conflicto\",\"Bien común\",\"Competencia\",\"Desigualdad\"]', 1, 1, '2025-12-29 00:20:25', 6, NULL, NULL, 2, NULL, 'ES'),
(36, 4, 'Alta', NULL, 'El respeto a la ley permite:', '[\"Caos\",\"Orden social\",\"Anarquía\",\"Confusión\"]', 1, 1, '2025-12-29 00:20:25', 6, NULL, NULL, 2, NULL, 'ES'),
(37, 4, 'Media', NULL, 'I. Votar es un derecho. II. Votar es un deber.', '[\"Solo I\",\"Solo II\",\"Ambas\",\"Ninguna\"]', 2, 1, '2025-12-29 00:20:25', 6, NULL, NULL, 3, NULL, 'ES'),
(38, 4, 'Alta', NULL, 'I. La ley es obligatoria. II. La ley es opcional.', '[\"Solo I\",\"Solo II\",\"Ambas\",\"Ninguna\"]', 0, 1, '2025-12-29 00:20:25', 6, NULL, NULL, 3, NULL, 'ES'),
(39, 4, 'Media', NULL, 'Según la imagen del semáforo, el color rojo indica:', '[\"Avanzar\",\"Precaución\",\"Detenerse\",\"Girar\"]', 2, 1, '2025-12-29 00:20:25', 6, NULL, NULL, 4, NULL, 'ES'),
(40, 4, 'Alta', NULL, 'Según la tabla de votaciones, ¿qué opción ganó?', '[\"A\",\"B\",\"C\",\"D\"]', 1, 1, '2025-12-29 00:20:25', 6, NULL, NULL, 5, NULL, 'ES'),
(41, 5, 'Baja', NULL, 'What is the translation of \"house\"?', '[\"Car\",\"House\",\"Tree\",\"Dog\"]', 1, 1, '2025-12-29 00:20:36', 6, NULL, NULL, 1, NULL, 'ES'),
(42, 5, 'Baja', NULL, 'Choose the correct color: Red', '[\"Rojo\",\"Azul\",\"Verde\",\"Amarillo\"]', 0, 1, '2025-12-29 00:20:36', 6, NULL, NULL, 1, NULL, 'ES'),
(43, 5, 'Media', NULL, 'Choose the correct verb: I ___ a student.', '[\"am\",\"is\",\"are\",\"be\"]', 0, 1, '2025-12-29 00:20:36', 6, NULL, NULL, 1, NULL, 'ES'),
(44, 5, 'Alta', NULL, 'Choose the correct sentence:', '[\"She go school\",\"She goes to school\",\"She going school\",\"She gone school\"]', 0, 1, '2025-12-29 00:20:36', 6, NULL, '2025-12-29 01:22:16', 1, NULL, 'ES'),
(45, 5, 'Media', NULL, 'According to the text, John is:', '[\"Teacher\",\"Student\",\"Doctor\",\"Driver\"]', 1, 1, '2025-12-29 00:20:36', 6, NULL, NULL, 2, NULL, 'ES'),
(46, 5, 'Alta', NULL, 'The text says Mary likes:', '[\"Apples\",\"Bananas\",\"Oranges\",\"Grapes\"]', 2, 1, '2025-12-29 00:20:36', 6, NULL, NULL, 2, NULL, 'ES'),
(47, 5, 'Media', NULL, 'I. \"Dog\" is an animal. II. \"Dog\" is a color.', '[\"Solo I\",\"Solo II\",\"Ambas\",\"Ninguna\"]', 0, 1, '2025-12-29 00:20:36', 6, NULL, NULL, 3, NULL, 'ES'),
(48, 5, 'Alta', NULL, 'I. \"She\" is a pronoun. II. \"She\" is a verb.', '[\"Solo I\",\"Solo II\",\"Ambas\",\"Ninguna\"]', 0, 1, '2025-12-29 00:20:36', 6, NULL, NULL, 3, NULL, 'ES'),
(49, 5, 'Media', NULL, 'According to the image, the person is:', '[\"Running\",\"Eating\",\"Sleeping\",\"Reading\"]', 0, 1, '2025-12-29 00:20:36', 6, NULL, '2025-12-29 01:21:47', 4, NULL, 'ES'),
(50, 5, 'Alta', NULL, 'According to the table, the correct answer is:', '[\"A\", \"z\", \"C\", \"D\"]', 1, 0, '2025-12-29 00:20:36', 6, NULL, '2025-12-29 01:22:51', 5, NULL, 'ES'),
(54, 2, 'Media', 'Lea el siguiente texto:\n\n\"El desarrollo sostenible busca equilibrar el crecimiento económico con la protección del medio ambiente y el bienestar social.\"', 'Según el texto, ¿cuál es el objetivo principal del desarrollo sostenible?', '[\r\n        \"Promover únicamente el crecimiento económico\",\r\n        \"Equilibrar economía, medio ambiente y sociedad\",\r\n        \"Reducir el uso de recursos naturales\",\r\n        \"Aumentar la industrialización\"\r\n    ]', 1, 1, '2025-12-29 02:58:39', 6, NULL, NULL, 1, NULL, 'ES'),
(55, 4, 'Alta', 'Read the following text carefully:\nMary likes different fruits depending on the season.', 'Which fruit does Mary prefer in summer?', '[\"Apples\",\"Bananas\",\"Oranges\",\"Grapes\"]', 2, 1, '2025-12-29 03:14:36', NULL, NULL, NULL, 2, NULL, 'ES'),
(56, 4, 'Media', 'Mary is talking about the fruits she usually eats for breakfast.', 'According to the text, which fruit does Mary like the most?', '[\r\n        {\"letra\":\"A\",\"texto\":\"Apples\"},\r\n        {\"letra\":\"B\",\"texto\":\"Bananas\"},\r\n        {\"letra\":\"C\",\"texto\":\"Oranges\"},\r\n        {\"letra\":\"D\",\"texto\":\"Grapes\"}\r\n    ]', 1, 1, '2025-12-29 03:16:58', 6, NULL, NULL, 2, NULL, 'ES'),
(57, 5, 'Media', 'En un barrio de una ciudad, los vecinos se organizaron para limpiar un parque que estaba en mal estado.\r\n     Algunos aportaron herramientas, otros tiempo y otros coordinaron las actividades.', '¿Qué valor ciudadano se evidencia principalmente en la situación descrita?', '[\"\", \"\", \"\", \"\"]', 1, 1, '2025-12-29 03:25:10', 6, NULL, '2025-12-29 04:06:29', 2, NULL, 'ES'),
(58, 1, 'Baja', NULL, '123123', '[\"12312354\", \"1231\", \"2131\", \"12333\"]', 0, 1, '2025-12-29 04:29:01', NULL, NULL, NULL, 1, NULL, 'ES'),
(59, 1, 'Baja', NULL, 'cual es el area ', '[\"asdsad1\", \"1233\", \"4415\", \"1122222222\"]', 0, 1, '2025-12-29 04:29:29', NULL, NULL, NULL, 4, NULL, 'ES');

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
  MODIFY `id_pregunta_diagnostico` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=60;

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
