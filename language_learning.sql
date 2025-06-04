-- MySQL dump 10.13  Distrib 8.0.36, for Linux (x86_64)
--
-- Host: localhost    Database: language_learning
-- ------------------------------------------------------
-- Server version	8.0.41-0ubuntu0.24.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

USE language_learning;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('47584f0cdd70');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `levels`
--

DROP TABLE IF EXISTS `levels`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `levels` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` text,
  `image_url` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `levels`
--

LOCK TABLES `levels` WRITE;
/*!40000 ALTER TABLE `levels` DISABLE KEYS */;
INSERT INTO `levels` VALUES (5,'Test Level 456','',NULL,'2025-05-06 08:50:28','2025-05-06 08:50:28'),(8,'level 222','level 1',NULL,'2025-05-06 11:31:30','2025-05-06 11:31:30'),(11,'level 222s','level 1','uploads/levels/cbd766c7ac3e4dccace0c2d5a8ebc1d6.png','2025-05-06 11:34:41','2025-05-06 11:34:41'),(12,'level 222ssss','level 1','uploads/levels/6e110508e9614c7e8a9952abad37d1d4.png','2025-05-06 11:39:36','2025-05-06 11:39:36'),(13,'level 2ss22','level 1',NULL,'2025-05-06 11:39:44','2025-05-06 11:39:44'),(14,'level 2sdds22','level 1',NULL,'2025-05-06 11:40:27','2025-05-06 11:40:27');
/*!40000 ALTER TABLE `levels` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `question_choices`
--

DROP TABLE IF EXISTS `question_choices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `question_choices` (
  `id` int NOT NULL AUTO_INCREMENT,
  `question_id` int NOT NULL,
  `choice_type` enum('TEXT','IMAGE','VOICE') NOT NULL,
  `content` varchar(255) NOT NULL,
  `is_correct` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `question_id` (`question_id`),
  CONSTRAINT `question_choices_ibfk_1` FOREIGN KEY (`question_id`) REFERENCES `questions` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `question_choices`
--

LOCK TABLES `question_choices` WRITE;
/*!40000 ALTER TABLE `question_choices` DISABLE KEYS */;
INSERT INTO `question_choices` VALUES (20,15,'IMAGE','uploads/questions/33ef8e4e7b724e17a7e1ac69dbcdf67a.png',0,'2025-05-06 18:01:09','2025-05-06 18:01:09');
/*!40000 ALTER TABLE `question_choices` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `questions`
--

DROP TABLE IF EXISTS `questions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `questions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `section_id` int NOT NULL,
  `question_type` enum('TEXT','IMAGE','AUDIO') NOT NULL,
  `question_content` varchar(255) NOT NULL,
  `answer_type` enum('MULTIPLE_CHOICE','FILL_IN_BLANK') NOT NULL,
  `correct_answer` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `section_id` (`section_id`),
  CONSTRAINT `questions_ibfk_1` FOREIGN KEY (`section_id`) REFERENCES `sections` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `questions`
--

LOCK TABLES `questions` WRITE;
/*!40000 ALTER TABLE `questions` DISABLE KEYS */;
INSERT INTO `questions` VALUES (12,18,'IMAGE','uploads/questions/198da73ef495475db86d9f5215e1a3e4.png','MULTIPLE_CHOICE',NULL,'2025-05-06 17:56:13','2025-05-06 17:56:13'),(13,18,'IMAGE','uploads/questions/ed5a03c93d5b434fbea90a950a363a3a.png','MULTIPLE_CHOICE',NULL,'2025-05-06 17:56:23','2025-05-06 17:56:23'),(14,18,'IMAGE','uploads/questions/ae2e564aa01c4415b09161958e951432.png','MULTIPLE_CHOICE',NULL,'2025-05-06 17:57:16','2025-05-06 17:57:16'),(15,18,'IMAGE','uploads/questions/f7f4ac95fda1492eb5cbf73e26144baf.png','MULTIPLE_CHOICE',NULL,'2025-05-06 17:57:28','2025-05-06 17:57:28');
/*!40000 ALTER TABLE `questions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sections`
--

DROP TABLE IF EXISTS `sections`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sections` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` text,
  `image` varchar(255) DEFAULT NULL,
  `level_id` int NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `level_id` (`level_id`),
  CONSTRAINT `sections_ibfk_1` FOREIGN KEY (`level_id`) REFERENCES `levels` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sections`
--

LOCK TABLES `sections` WRITE;
/*!40000 ALTER TABLE `sections` DISABLE KEYS */;
INSERT INTO `sections` VALUES (18,'cdndjnkcnd','dkkdkskm',NULL,8,'2025-05-06 12:04:58','2025-05-06 12:04:58'),(22,'ssss','dkkdkskm',NULL,8,'2025-05-06 12:11:55','2025-05-06 12:11:55'),(28,'ssss22','dkkdkskm','uploads/sections/89b7e3b53ddc4cb89a6d2f84bed47af7.png',5,'2025-05-06 12:16:11','2025-05-06 12:16:11'),(30,'ssss22dd','dkkdkskmddd','uploads/sections/ae79954eac19402b8e0820d268f08303.png',5,'2025-05-06 12:43:08','2025-05-06 12:43:08');
/*!40000 ALTER TABLE `sections` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(120) NOT NULL,
  `username` varchar(80) NOT NULL,
  `password_hash` varchar(255) DEFAULT NULL,
  `role` enum('USER','ADMIN') NOT NULL,
  `is_verified` tinyint(1) DEFAULT NULL,
  `verification_code` varchar(6) DEFAULT NULL,
  `verification_code_expires` datetime DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'yousefmyou@gmail.com','jo','scrypt:32768:8:1$te21KqAbThXbR2Kv$b7bb4027cdf14a12d2ad0b1473c9b80c8a7ab593511e163fb11f3a62d43cd50cd9fb5f24fb8a54989215875d5f2e71c740c3b8b675a5ea5b65c358e8552fb30f','ADMIN',1,NULL,NULL,'2025-05-06 07:58:53','2025-05-06 07:58:53');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-07 21:35:42
