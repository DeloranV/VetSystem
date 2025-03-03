-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: vet
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `appointments`
--

DROP TABLE IF EXISTS `appointments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appointments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `pet_id` int NOT NULL,
  `vet_id` int NOT NULL,
  `resource_id` int NOT NULL,
  `appointment_type` char(1) NOT NULL,
  `scheduled` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `pet_id` (`pet_id`),
  KEY `vet_id` (`vet_id`),
  KEY `resource_id` (`resource_id`),
  CONSTRAINT `appointments_ibfk_1` FOREIGN KEY (`pet_id`) REFERENCES `pets` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `appointments_ibfk_2` FOREIGN KEY (`vet_id`) REFERENCES `vets` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `appointments_ibfk_3` FOREIGN KEY (`resource_id`) REFERENCES `resources` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appointments`
--

LOCK TABLES `appointments` WRITE;
/*!40000 ALTER TABLE `appointments` DISABLE KEYS */;
INSERT INTO `appointments` VALUES (13,20,1,3,'k','2025-02-06 14:30:00'),(16,21,7,4,'z','2025-05-25 10:00:00'),(17,22,5,1,'d','2025-01-31 12:35:00');
/*!40000 ALTER TABLE `appointments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `appointments_view`
--

DROP TABLE IF EXISTS `appointments_view`;
/*!50001 DROP VIEW IF EXISTS `appointments_view`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `appointments_view` AS SELECT 
 1 AS `app_id`,
 1 AS `pet_id`,
 1 AS `owner_id`,
 1 AS `pet_name`,
 1 AS `vet_name`,
 1 AS `vet_surname`,
 1 AS `appointment_type`,
 1 AS `scheduled`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `pets`
--

DROP TABLE IF EXISTS `pets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pets` (
  `id` int NOT NULL AUTO_INCREMENT,
  `owner_id` int NOT NULL,
  `name` varchar(32) NOT NULL,
  `type` varchar(15) NOT NULL,
  `age` tinyint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `owner_id` (`owner_id`),
  CONSTRAINT `pets_ibfk_1` FOREIGN KEY (`owner_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pets`
--

LOCK TABLES `pets` WRITE;
/*!40000 ALTER TABLE `pets` DISABLE KEYS */;
INSERT INTO `pets` VALUES (20,14,'Fibi','Pies',13),(21,15,'Azor','Pies',3),(22,16,'Lusia','Kot',7);
/*!40000 ALTER TABLE `pets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `pets_view`
--

DROP TABLE IF EXISTS `pets_view`;
/*!50001 DROP VIEW IF EXISTS `pets_view`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `pets_view` AS SELECT 
 1 AS `id`,
 1 AS `owner_id`,
 1 AS `name`,
 1 AS `type`,
 1 AS `age`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `resources`
--

DROP TABLE IF EXISTS `resources`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `resources` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  `amount` tinyint DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `resources`
--

LOCK TABLES `resources` WRITE;
/*!40000 ALTER TABLE `resources` DISABLE KEYS */;
INSERT INTO `resources` VALUES (1,'Leki',121),(3,'Gumowe rękawiczki',121),(4,'Nożyki chirurgiczne',115);
/*!40000 ALTER TABLE `resources` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  `surname` varchar(32) NOT NULL,
  `password` text NOT NULL,
  `api_key` text NOT NULL,
  `email` varchar(32) NOT NULL,
  `phone` char(9) NOT NULL,
  `role` char(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `un_constr` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (12,'admin','admin','scrypt:32768:8:1$RpTlD1pd2Jehf9Rp$c72bc1765d1cc6c29bc8b92bd4d660174e843d3d657cc22c325bc5ea5231c9cc01040aa254ec00ed1b0000f4d0ad1bd7ef980a76281b9105481409fb8afc02e7','1111','admin@admin.com','344444444','a'),(14,'Roland','Gugala','scrypt:32768:8:1$PkEY86Ymvrb8pt8s$64f01bd78cf8f60e5e9d484ec10ce12fd19d787afb0256c2f2b9d364a7a72c50938a0c48a62fef7997e6e620418b305c03ad70d998d13f87b3db7ed68dbe47a6','aTskft2eakTV1A','rolandgugala@gmail.com','662432208','u'),(15,'Jakub','Mitek','scrypt:32768:8:1$QWw5YVhgCTYWClcg$a32cbe431002e6b22dedd4e46dc57d78df2fed567366ef94c5b82a2277e648eb6790f849d3c44dddc89c467db0f5badf8bff5c22cdec622eb3a54a6384f98937','Ptwj_xSR4G9iXA','jakubmitek@example.com','768936536','u'),(16,'Marta','Falinska','scrypt:32768:8:1$vJynsZsgcqfH76Ns$6b9fdf1a7c7dcba5b56b9a721b8511821e2b4c2919ea1559e5f7f94444d2e94111ad8022524ce49cb08e4aca30ff60c580303bfdb8aa9b26893de9a37d148217','ftgTH5nS92KipA','martafalinska@example.com','865654837','u');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vets`
--

DROP TABLE IF EXISTS `vets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vets` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  `surname` varchar(32) NOT NULL,
  `appointment_type` char(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vets`
--

LOCK TABLES `vets` WRITE;
/*!40000 ALTER TABLE `vets` DISABLE KEYS */;
INSERT INTO `vets` VALUES (1,'Marcin','Kowalski','k'),(5,'Rafal','Bebel','d'),(6,'Jacek','Weterynarz','d'),(7,'Mateusz','Kowalski','z');
/*!40000 ALTER TABLE `vets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Final view structure for view `appointments_view`
--

/*!50001 DROP VIEW IF EXISTS `appointments_view`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = cp852 */;
/*!50001 SET character_set_results     = cp852 */;
/*!50001 SET collation_connection      = cp852_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`vetAdmin`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `appointments_view` AS select `a`.`id` AS `app_id`,`p`.`id` AS `pet_id`,`p`.`owner_id` AS `owner_id`,`p`.`name` AS `pet_name`,`v`.`name` AS `vet_name`,`v`.`surname` AS `vet_surname`,`a`.`appointment_type` AS `appointment_type`,`a`.`scheduled` AS `scheduled` from ((`appointments` `a` join `pets` `p` on((`a`.`pet_id` = `p`.`id`))) join `vets` `v` on((`a`.`vet_id` = `v`.`id`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `pets_view`
--

/*!50001 DROP VIEW IF EXISTS `pets_view`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = cp852 */;
/*!50001 SET character_set_results     = cp852 */;
/*!50001 SET collation_connection      = cp852_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`vetAdmin`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `pets_view` AS select `pets`.`id` AS `id`,`pets`.`owner_id` AS `owner_id`,`pets`.`name` AS `name`,`pets`.`type` AS `type`,`pets`.`age` AS `age` from `pets` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-01-29 23:29:05
