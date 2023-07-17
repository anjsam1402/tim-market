# ************************************************************
# Sequel Ace SQL dump
# Version 20046
#
# https://sequel-ace.com/
# https://github.com/Sequel-Ace/Sequel-Ace
#
# Host: localhost (MySQL 8.0.33)
# Database: tim_market
# Generation Time: 2023-07-17 11:12:30 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
SET NAMES utf8mb4;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE='NO_AUTO_VALUE_ON_ZERO', SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table cart
# ------------------------------------------------------------

CREATE TABLE `cart` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` int NOT NULL,
  `updated_at` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `cart` WRITE;
/*!40000 ALTER TABLE `cart` DISABLE KEYS */;

INSERT INTO `cart` (`id`, `created_at`, `updated_at`)
VALUES
	(1,1689252635,1689512411),
	(2,1689282968,1689515583),
	(4,1689283252,1689283252),
	(5,1689283344,1689283344),
	(6,1689283413,1689283413),
	(7,1689283474,1689283474),
	(8,1689283502,1689283502),
	(9,1689283637,1689283637),
	(10,1689283677,1689283677),
	(11,1689283754,1689283754),
	(12,1689283768,1689283768),
	(13,1689283817,1689283817),
	(14,1689283839,1689283839),
	(15,1689283864,1689283864),
	(16,1689283903,1689283903),
	(17,1689284003,1689284003),
	(18,1689284014,1689284014),
	(19,1689284090,1689284090),
	(20,1689284178,1689284178),
	(21,1689284219,1689284219),
	(22,1689322193,1689322193),
	(23,1689322281,1689322281),
	(24,1689322359,1689322359),
	(25,1689345307,1689345307),
	(26,1689345312,1689345312),
	(27,1689345361,1689345361),
	(28,1689514167,1689514167),
	(29,1689515355,1689586817),
	(30,1689527490,1689527490);

/*!40000 ALTER TABLE `cart` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table cart_price_map
# ------------------------------------------------------------

CREATE TABLE `cart_price_map` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `cart_id` bigint NOT NULL,
  `total_price` decimal(10,2) unsigned DEFAULT NULL,
  `net_total_price` decimal(10,2) unsigned DEFAULT NULL,
  `vat_percent` decimal(5,2) unsigned DEFAULT NULL,
  `vat_tax_price` decimal(10,2) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `cart_id` (`cart_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `cart_price_map` WRITE;
/*!40000 ALTER TABLE `cart_price_map` DISABLE KEYS */;

INSERT INTO `cart_price_map` (`id`, `cart_id`, `total_price`, `net_total_price`, `vat_percent`, `vat_tax_price`)
VALUES
	(1,25,0.00,0.00,0.00,0.00),
	(2,26,0.00,0.00,0.00,0.00),
	(3,27,0.00,0.00,0.00,0.00),
	(4,1,0.00,0.00,0.00,0.00),
	(5,28,0.00,0.00,0.00,0.00),
	(6,29,1098.52,1007.82,9.00,90.70),
	(7,30,0.00,0.00,0.00,0.00);

/*!40000 ALTER TABLE `cart_price_map` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table cart_product_map
# ------------------------------------------------------------

CREATE TABLE `cart_product_map` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `cart_id` int NOT NULL,
  `product_id` int NOT NULL,
  `quantity` int unsigned DEFAULT '1',
  `category_id` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `cart_product_map` WRITE;
/*!40000 ALTER TABLE `cart_product_map` DISABLE KEYS */;

INSERT INTO `cart_product_map` (`id`, `cart_id`, `product_id`, `quantity`, `category_id`)
VALUES
	(23,2,51,18,4),
	(26,29,51,18,4);

/*!40000 ALTER TABLE `cart_product_map` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table cart_user_map
# ------------------------------------------------------------

CREATE TABLE `cart_user_map` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `cart_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `platform` varchar(26) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `cart_user_map` WRITE;
/*!40000 ALTER TABLE `cart_user_map` DISABLE KEYS */;

INSERT INTO `cart_user_map` (`id`, `cart_id`, `user_id`, `platform`)
VALUES
	(1,1,1,'ios'),
	(28,28,5,'web'),
	(29,29,6,'web'),
	(30,30,7,'web');

/*!40000 ALTER TABLE `cart_user_map` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table category
# ------------------------------------------------------------

CREATE TABLE `category` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `category` WRITE;
/*!40000 ALTER TABLE `category` DISABLE KEYS */;

INSERT INTO `category` (`id`, `name`)
VALUES
	(1,'category-5'),
	(2,'category-1'),
	(3,'category1'),
	(4,'men\'s clothing'),
	(5,'jewelery'),
	(6,'electronics'),
	(7,'women\'s clothing');

/*!40000 ALTER TABLE `category` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table core_user
# ------------------------------------------------------------

CREATE TABLE `core_user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `is_superuser` tinyint(1) NOT NULL,
  `password` varchar(128) NOT NULL,
  `username` varchar(150) NOT NULL,
  `name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` int NOT NULL,
  `is_active` int NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `core_user` WRITE;
/*!40000 ALTER TABLE `core_user` DISABLE KEYS */;

INSERT INTO `core_user` (`id`, `is_superuser`, `password`, `username`, `name`, `email`, `is_staff`, `is_active`, `date_joined`, `last_login`)
VALUES
	(1,1,'pbkdf2_sha256$600000$xi8GSBpL8uWIdp2LybtDAS$rDxiSbXLPN6h3OWGj4YPdigN/Q+aBJDGp0YbM8/Zxww=','admin','admin','admin@gmail.com',1,1,'2023-07-15 23:42:44.097511','2023-07-15 23:52:35.096187'),
	(5,0,'password123','newuser2','new user2','new2@gmail.com',0,1,'2023-07-16 13:29:27.175598',NULL),
	(6,0,'pbkdf2_sha256$600000$ukRfDbbsIOwYb9QRPPABpP$K7vs+ct7dwdIm/0lMmOobrUrnPoFRXZRWWnXlwDDVrQ=','newuser3','newuser3','newuser3@gmail.com',0,1,'2023-07-16 13:49:15.796010',NULL),
	(7,0,'pbkdf2_sha256$600000$ZnpNbkrAu80rrH9n1twp2i$Dug7vnYX7RdfdV6VzZZjJFxuppLJJOm5LEa0AW9+gg8=','newuser4','newuser4','newuser4@gmail.com',0,1,'2023-07-16 17:11:30.339504','2023-07-16 17:12:15.876248');

/*!40000 ALTER TABLE `core_user` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table core_user_groups
# ------------------------------------------------------------

CREATE TABLE `core_user_groups` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `core_user_groups_user_id_group_id_c82fcad1_uniq` (`user_id`,`group_id`),
  KEY `core_user_groups_group_id_fe8c697f_fk_auth_group_id` (`group_id`),
  CONSTRAINT `core_user_groups_group_id_fe8c697f_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `core_user_groups_user_id_70b4d9b8_fk_core_user_id` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



# Dump of table core_user_user_permissions
# ------------------------------------------------------------

CREATE TABLE `core_user_user_permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `core_user_user_permissions_user_id_permission_id_73ea0daa_uniq` (`user_id`,`permission_id`),
  KEY `core_user_user_permi_permission_id_35ccf601_fk_auth_perm` (`permission_id`),
  CONSTRAINT `core_user_user_permi_permission_id_35ccf601_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `core_user_user_permissions_user_id_085123d3_fk_core_user_id` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



# Dump of table order_product_map
# ------------------------------------------------------------

CREATE TABLE `order_product_map` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `product_id` bigint NOT NULL,
  `order_id` bigint NOT NULL,
  `quantity` int DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `unq_order_product` (`order_id`,`product_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `order_product_map` WRITE;
/*!40000 ALTER TABLE `order_product_map` DISABLE KEYS */;

INSERT INTO `order_product_map` (`id`, `product_id`, `order_id`, `quantity`)
VALUES
	(1,33,1,6),
	(2,33,2,2),
	(3,53,3,10),
	(4,51,4,18),
	(5,51,5,9);

/*!40000 ALTER TABLE `order_product_map` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table order_status
# ------------------------------------------------------------

CREATE TABLE `order_status` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `order_id` bigint NOT NULL,
  `status` enum('placed','processing','shipped','delivered') DEFAULT NULL,
  `created_at` int NOT NULL,
  `updated_at` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `order_id` (`order_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `order_status` WRITE;
/*!40000 ALTER TABLE `order_status` DISABLE KEYS */;

INSERT INTO `order_status` (`id`, `order_id`, `status`, `created_at`, `updated_at`)
VALUES
	(1,2,'placed',1689371390,1689371390),
	(2,3,'placed',1689512428,1689512428),
	(3,4,'placed',1689515832,1689515832),
	(4,5,'placed',1689549865,1689549865);

/*!40000 ALTER TABLE `order_status` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table order_table
# ------------------------------------------------------------

CREATE TABLE `order_table` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `cart_id` bigint NOT NULL,
  `total_price` decimal(10,2) unsigned DEFAULT NULL,
  `net_total_price` decimal(10,2) unsigned DEFAULT NULL,
  `vat_percent` decimal(5,2) unsigned DEFAULT NULL,
  `vat_tax_price` decimal(10,2) unsigned DEFAULT NULL,
  `created_at` int NOT NULL,
  `updated_at` int NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `order_table` WRITE;
/*!40000 ALTER TABLE `order_table` DISABLE KEYS */;

INSERT INTO `order_table` (`id`, `cart_id`, `total_price`, `net_total_price`, `vat_percent`, `vat_tax_price`, `created_at`, `updated_at`, `description`)
VALUES
	(2,1,21.80,20.00,9.00,1.80,1689371390,1689371390,NULL),
	(3,1,1154.96,1059.60,9.00,95.36,1689512428,1689512428,NULL),
	(4,29,1098.52,1007.82,9.00,90.70,1689515832,1689515832,NULL),
	(5,29,549.26,503.91,9.00,45.35,1689549865,1689549865,NULL);

/*!40000 ALTER TABLE `order_table` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table product
# ------------------------------------------------------------

CREATE TABLE `product` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `product` WRITE;
/*!40000 ALTER TABLE `product` DISABLE KEYS */;

INSERT INTO `product` (`id`, `name`)
VALUES
	(5,'product-5'),
	(33,'product-5'),
	(34,'DANVOUY Womens T Shirt Casual Cotton Short'),
	(35,'Opna Women\'s Short Sleeve Moisture'),
	(36,'MBJ Women\'s Solid Short Sleeve Boat Neck V '),
	(37,'Rain Jacket Women Windbreaker Striped Climbing Raincoats'),
	(38,'Lock and Love Women\'s Removable Hooded Faux Leather Moto Biker Jacket'),
	(39,'BIYLACLESEN Women\'s 3-in-1 Snowboard Jacket Winter Coats'),
	(40,'Samsung 49-Inch CHG90 144Hz Curved Gaming Monitor (LC49HG90DMNXZA) – Super Ultrawide Screen QLED '),
	(41,'Acer SB220Q bi 21.5 inches Full HD (1920 x 1080) IPS Ultra-Thin'),
	(42,'WD 4TB Gaming Drive Works with Playstation 4 Portable External Hard Drive'),
	(43,'Silicon Power 256GB SSD 3D NAND A55 SLC Cache Performance Boost SATA III 2.5'),
	(44,'SanDisk SSD PLUS 1TB Internal SSD - SATA III 6 Gb/s'),
	(45,'WD 2TB Elements Portable External Hard Drive - USB 3.0 '),
	(46,'Pierced Owl Rose Gold Plated Stainless Steel Double'),
	(47,'White Gold Plated Princess'),
	(48,'Solid Gold Petite Micropave '),
	(49,'John Hardy Women\'s Legends Naga Gold & Silver Dragon Station Chain Bracelet'),
	(50,'Mens Casual Slim Fit'),
	(51,'Mens Cotton Jacket'),
	(52,'Mens Casual Premium Slim Fit T-Shirts '),
	(53,'Fjallraven - Foldsack No. 1 Backpack, Fits 15 Laptops'),
	(56,'new_product'),
	(57,'new_product_2');

/*!40000 ALTER TABLE `product` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table product_category_map
# ------------------------------------------------------------

CREATE TABLE `product_category_map` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `product_id` int NOT NULL,
  `category_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unq_product_category` (`product_id`,`category_id`)
) ENGINE=InnoDB AUTO_INCREMENT=55 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `product_category_map` WRITE;
/*!40000 ALTER TABLE `product_category_map` DISABLE KEYS */;

INSERT INTO `product_category_map` (`id`, `product_id`, `category_id`)
VALUES
	(2,5,1),
	(30,33,3),
	(32,34,7),
	(33,35,7),
	(34,36,7),
	(35,37,7),
	(36,38,7),
	(37,39,7),
	(38,40,6),
	(39,41,6),
	(40,42,6),
	(41,43,6),
	(42,44,6),
	(43,45,6),
	(44,46,5),
	(45,47,5),
	(46,48,5),
	(47,49,5),
	(48,50,4),
	(49,51,4),
	(50,52,4),
	(51,53,4),
	(52,56,1),
	(54,57,4);

/*!40000 ALTER TABLE `product_category_map` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table product_category_price_map
# ------------------------------------------------------------

CREATE TABLE `product_category_price_map` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `product_category_id` int NOT NULL,
  `price` decimal(10,2) unsigned DEFAULT '0.00',
  PRIMARY KEY (`id`),
  UNIQUE KEY `product_category_id` (`product_category_id`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `product_category_price_map` WRITE;
/*!40000 ALTER TABLE `product_category_price_map` DISABLE KEYS */;

INSERT INTO `product_category_price_map` (`id`, `product_category_id`, `price`)
VALUES
	(2,2,10.00),
	(30,30,10.00),
	(31,32,12.99),
	(32,33,7.95),
	(33,34,9.85),
	(34,35,39.85),
	(35,36,49.95),
	(36,37,69.95),
	(37,38,999.95),
	(38,39,599.95),
	(39,40,115.00),
	(40,41,100.00),
	(41,42,105.00),
	(42,43,68.00),
	(43,44,10.99),
	(44,45,7.99),
	(45,46,199.23),
	(46,47,345.89),
	(47,48,15.89),
	(48,49,55.99),
	(49,50,25.99),
	(50,51,105.96),
	(51,52,105.96),
	(52,54,105.96);

/*!40000 ALTER TABLE `product_category_price_map` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table product_inventory_map
# ------------------------------------------------------------

CREATE TABLE `product_inventory_map` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `product_category_id` int NOT NULL,
  `quantity` int unsigned DEFAULT '1',
  `weight` decimal(5,2) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `product_category_id` (`product_category_id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `product_inventory_map` WRITE;
/*!40000 ALTER TABLE `product_inventory_map` DISABLE KEYS */;

INSERT INTO `product_inventory_map` (`id`, `product_category_id`, `quantity`, `weight`)
VALUES
	(1,2,10,0.00),
	(2,30,4,0.00),
	(3,32,145,0.00),
	(4,33,146,0.00),
	(5,34,130,0.00),
	(6,35,179,0.00),
	(7,36,140,0.00),
	(8,37,150,0.00),
	(9,38,180,0.00),
	(10,39,180,0.00),
	(11,40,400,0.00),
	(12,41,200,0.00),
	(13,42,130,0.00),
	(14,43,158,0.00),
	(15,44,120,0.00),
	(16,45,80,0.00),
	(17,46,80,0.00),
	(18,47,50,0.00),
	(19,48,150,0.00),
	(20,49,95,0.00),
	(21,50,48,0.00),
	(22,51,20,0.00),
	(23,52,0,0.00),
	(24,54,0,0.00);

/*!40000 ALTER TABLE `product_inventory_map` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table user
# ------------------------------------------------------------

CREATE TABLE `user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `last_name` varchar(255) DEFAULT NULL,
  `first_name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;

INSERT INTO `user` (`id`, `last_name`, `first_name`)
VALUES
	(1,'name','admin'),
	(8,'password','username'),
	(9,'password','username'),
	(10,'password','username'),
	(11,'password','username'),
	(12,'password','username'),
	(13,'password','username'),
	(14,'password','username'),
	(15,'password','username'),
	(16,'password','username'),
	(17,'password','username'),
	(18,'password','username'),
	(19,'password','username'),
	(20,'password','username'),
	(21,'password','username'),
	(22,'password','username'),
	(23,'password','username'),
	(24,'password','username'),
	(25,'password','username'),
	(26,'password','username'),
	(27,'password','username'),
	(28,'password','username'),
	(29,'password','username'),
	(30,'password','new'),
	(31,'new','new'),
	(32,'new','new'),
	(33,'new','new'),
	(34,'new','new');

/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table user_order_map
# ------------------------------------------------------------

CREATE TABLE `user_order_map` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `order_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unq_user_order` (`user_id`,`order_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `user_order_map` WRITE;
/*!40000 ALTER TABLE `user_order_map` DISABLE KEYS */;

INSERT INTO `user_order_map` (`id`, `user_id`, `order_id`)
VALUES
	(1,1,1),
	(2,1,2),
	(3,1,3),
	(4,6,4),
	(5,6,5);

/*!40000 ALTER TABLE `user_order_map` ENABLE KEYS */;
UNLOCK TABLES;



/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
