SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

CREATE DATABASE IF NOT EXISTS `sensei-scraper_items` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `sensei-scraper_items`;

DROP TABLE IF EXISTS `hoteles`;
CREATE TABLE `hoteles` (
  `id` int(9) NOT NULL,
  `nombre` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `url` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `imagen` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `estrellas` int(1) NOT NULL,
  `estrellas_ta` int(1) NOT NULL,
  `url_listing` varchar(1000) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `hoteles` (`id`, `nombre`, `url`, `imagen`, `estrellas`, `estrellas_ta`, `url_listing`) VALUES
(1, 'Encantos Torres', 'https://www.example.com/hoteles/detalle/8826a58/{{from}}/{{to}}/0/2/encantos-torres', 'https://halo-images.s3.amazonaws.com/BR/B/dfe6a73f45e933abdaffecdac6b890c3.jpg', 3, 4, 'https://www.example.com/hoteles/resultados/ciudad/3vqz/{{from}}/{{to}}/0/2/torres_brasil'),
(2, 'Copacabana Rio Hotel', 'https://www.example.com/hoteles/detalle/26867c5/{{from}}/{{to}}/0/2/copacabana-rio-hotel', 'https://storage.googleapis.com/halo_images/BR/M/69341201.jpg', 3, 0, 'https://www.example.com/hoteles/resultados/ciudad/3tkt/{{from}}/{{to}}/0/2/rio-de-janeiro_brasil'),
(3, 'Hotel Villa Rica', 'https://www.example.com/hoteles/detalle/99db6f8/{{from}}/{{to}}/0/2/hotel-villa-rica', 'https://halo-images.s3.amazonaws.com/BR/B/602b250343b1bdd132f2c39e8050c85a.jpg', 2, 3, 'https://www.example.com/hoteles/resultados/ciudad/3tkt/{{from}}/{{to}}/0/2/rio-de-janeiro_brasil'),
(4, 'Hotel Plaza Spania', 'https://www.example.com/hoteles/detalle/c82482d/{{from}}/{{to}}/0/2/hotel-plaza-spania', 'https://halo-images.s3.amazonaws.com/BR/B/5f137e3fd259200904979cea13b8a1de.jpg', 3, 0, 'https://www.example.com/hoteles/resultados/ciudad/3tkt/{{from}}/{{to}}/0/2/rio-de-janeiro_brasil'),
(5, 'Angrense Hotel', 'https://www.example.com/hoteles/detalle/f832d3e/{{from}}/{{to}}/0/2/angrense-hotel', 'https://halo-images.s3.amazonaws.com/BR/B/3f88abd3faebf5787a624c544ac74cdf.jpg', 3, 0, 'https://www.example.com/hoteles/resultados/ciudad/3tkt/{{from}}/{{to}}/0/2/rio-de-janeiro_brasil');

DROP TABLE IF EXISTS `tags`;
CREATE TABLE `tags` (
  `id` int(9) NOT NULL,
  `tag` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `id_hotel` int(9) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `tags` (`id`, `tag`, `id_hotel`) VALUES
(1, 'torres brasil', 1),
(2, 'wififree', 1),
(3, 'air', 1),
(4, 'secbox', 1),
(5, 'mibar', 1),
(6, 'babysit', 1),
(7, 'rio de janeiro', 2),
(8, 'wififree', 2),
(9, 'swpool', 2),
(10, 'air', 2),
(11, 'park', 2),
(12, 'secbox', 2),
(13, 'rio de janeiro', 3),
(14, 'wififree', 3),
(15, 'air', 3),
(16, 'park', 3),
(17, 'mibar', 3),
(18, 'peal', 3),
(19, 'rio de janeiro', 4),
(20, 'wififree', 4),
(21, 'air', 4),
(22, 'tv', 4),
(23, 'hairdry', 4),
(24, 'tv', 4),
(25, 'rio de janeiro', 5),
(26, 'wififree', 5),
(27, 'air', 5),
(28, 'park', 5),
(29, 'mibar', 5),
(30, 'tourassis', 5);


ALTER TABLE `hoteles`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `tags`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_hotel` (`id_hotel`);


ALTER TABLE `hoteles`
  MODIFY `id` int(9) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

ALTER TABLE `tags`
  MODIFY `id` int(9) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
