-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: language_learning
-- ------------------------------------------------------
-- Server version	8.0.42

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
INSERT INTO `alembic_version` VALUES ('8c31d6b4ddb8');
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
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `levels`
--

LOCK TABLES `levels` WRITE;
/*!40000 ALTER TABLE `levels` DISABLE KEYS */;
INSERT INTO `levels` VALUES (17,'A1 – Beginner','You can understand and use very simple words and sentences in everyday situations.',NULL,'2025-06-04 15:07:24','2025-06-08 21:06:17'),(35,'A2 – Elementary','You can communicate in simple tasks and understand basic phrases about personal and familiar topics.',NULL,'2025-06-08 00:06:02','2025-06-08 21:06:33'),(36,'B1 – Intermediate','You can understand and express ideas clearly on everyday matters like work, school, and travel.',NULL,'2025-06-08 03:11:15','2025-06-08 21:06:47'),(43,'B2 – Upper-Intermediate','You can speak and write with confidence on most topics, including giving opinions and explaining your ideas.',NULL,'2025-06-08 21:05:15','2025-06-08 21:06:59'),(44,'C1 – Advanced','You can use English fluently and flexibly for social, academic, and professional purposes.',NULL,'2025-06-08 21:05:18','2025-06-08 21:07:11'),(45,'C2 – Proficient','You can understand and express yourself precisely and naturally, like a native speaker, even in complex situations.',NULL,'2025-06-08 21:05:21','2025-06-08 21:07:23');
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
  `choice_type` enum('TEXT','IMAGE','AUDIO') NOT NULL,
  `content` varchar(255) NOT NULL,
  `is_correct` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `question_id` (`question_id`),
  CONSTRAINT `question_choices_ibfk_1` FOREIGN KEY (`question_id`) REFERENCES `questions` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=90 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `question_choices`
--

LOCK TABLES `question_choices` WRITE;
/*!40000 ALTER TABLE `question_choices` DISABLE KEYS */;
INSERT INTO `question_choices` VALUES (49,32,'TEXT','Red',1,'2025-06-08 03:41:56','2025-06-08 03:41:56'),(50,32,'TEXT','Blue',1,'2025-06-08 03:41:56','2025-06-08 03:41:56'),(51,32,'TEXT','Green',1,'2025-06-08 03:41:56','2025-06-08 03:41:56'),(52,32,'TEXT','Orange',1,'2025-06-08 03:41:56','2025-06-08 03:41:56'),(53,32,'TEXT','Yellow',1,'2025-06-08 03:41:56','2025-06-08 03:41:56'),(54,32,'TEXT','Black',1,'2025-06-08 03:41:56','2025-06-08 03:41:56'),(55,32,'TEXT','Brown',1,'2025-06-08 03:41:56','2025-06-08 03:41:56'),(56,32,'TEXT','Purple',1,'2025-06-08 03:41:56','2025-06-08 03:41:56'),(57,32,'TEXT','Sky Blue',1,'2025-06-08 03:41:56','2025-06-08 03:41:56'),(58,32,'TEXT','Pink',1,'2025-06-08 03:41:56','2025-06-08 03:41:56'),(61,34,'TEXT','Orange',1,'2025-06-08 03:47:38','2025-06-08 03:47:38'),(62,34,'TEXT','Green',1,'2025-06-08 03:47:38','2025-06-08 03:47:38'),(63,34,'TEXT','Black',1,'2025-06-08 03:47:38','2025-06-08 03:47:38'),(64,34,'TEXT','Pink',1,'2025-06-08 03:47:38','2025-06-08 03:47:38'),(67,35,'TEXT','Black',1,'2025-06-08 03:49:40','2025-06-08 03:49:40'),(68,35,'TEXT','Brown',1,'2025-06-08 03:49:40','2025-06-08 03:49:40'),(69,36,'TEXT','Blue',1,'2025-06-08 03:54:23','2025-06-08 03:54:23'),(70,36,'TEXT','Red',1,'2025-06-08 03:54:23','2025-06-08 03:54:23'),(71,36,'TEXT','Green',1,'2025-06-08 03:54:23','2025-06-08 03:54:23'),(72,36,'TEXT','Brown',1,'2025-06-08 03:54:23','2025-06-08 03:54:23'),(73,36,'TEXT','Pink',1,'2025-06-08 03:54:23','2025-06-08 03:54:23'),(74,36,'TEXT','Yellow',1,'2025-06-08 03:54:23','2025-06-08 03:54:23');
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
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `questions`
--

LOCK TABLES `questions` WRITE;
/*!40000 ALTER TABLE `questions` DISABLE KEYS */;
INSERT INTO `questions` VALUES (32,48,'TEXT','Click the image to confirm the color','MULTIPLE_CHOICE',NULL,'2025-06-08 03:40:01','2025-06-08 03:41:56'),(34,51,'TEXT','Click the image to hear the color','MULTIPLE_CHOICE',NULL,'2025-06-08 03:47:38','2025-06-08 03:47:38'),(35,52,'TEXT','Read the shown colors','MULTIPLE_CHOICE',NULL,'2025-06-08 03:49:40','2025-06-08 03:49:40'),(36,53,'TEXT','Choose the colors that match the images','MULTIPLE_CHOICE',NULL,'2025-06-08 03:54:23','2025-06-08 03:54:23');
/*!40000 ALTER TABLE `questions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quiz_choices`
--

DROP TABLE IF EXISTS `quiz_choices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `quiz_choices` (
  `id` int NOT NULL AUTO_INCREMENT,
  `quiz_question_id` int NOT NULL,
  `choice_type` enum('TEXT','IMAGE','AUDIO') NOT NULL,
  `content` varchar(255) NOT NULL,
  `is_correct` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `quiz_question_id` (`quiz_question_id`),
  CONSTRAINT `quiz_choices_ibfk_1` FOREIGN KEY (`quiz_question_id`) REFERENCES `quiz_questions` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=60 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quiz_choices`
--

LOCK TABLES `quiz_choices` WRITE;
/*!40000 ALTER TABLE `quiz_choices` DISABLE KEYS */;
INSERT INTO `quiz_choices` VALUES (20,13,'TEXT','Blue',0,'2025-06-08 19:33:29','2025-06-08 19:33:29'),(21,13,'TEXT','Green',0,'2025-06-08 19:33:29','2025-06-08 19:33:29'),(22,13,'TEXT','Yellow',1,'2025-06-08 19:33:29','2025-06-08 19:33:29'),(23,13,'TEXT','Red',0,'2025-06-08 19:33:29','2025-06-08 19:33:29'),(24,14,'TEXT','3',0,'2025-06-08 20:45:23','2025-06-08 20:45:23'),(25,14,'TEXT','5',1,'2025-06-08 20:45:23','2025-06-08 20:45:23'),(26,14,'TEXT','6',0,'2025-06-08 20:45:23','2025-06-08 20:45:23'),(27,14,'TEXT','2',0,'2025-06-08 20:45:23','2025-06-08 20:45:23'),(28,15,'TEXT','Run',0,'2025-06-08 20:58:14','2025-06-08 20:58:14'),(29,15,'TEXT','Drink',0,'2025-06-08 20:58:14','2025-06-08 20:58:14'),(30,15,'TEXT','Eat',1,'2025-06-08 20:58:14','2025-06-08 20:58:14'),(31,15,'TEXT','Sleep',0,'2025-06-08 20:58:14','2025-06-08 20:58:14'),(32,16,'TEXT','Carrot',0,'2025-06-08 20:58:55','2025-06-08 20:58:55'),(33,16,'TEXT','Banana',1,'2025-06-08 20:58:55','2025-06-08 20:58:55'),(34,16,'TEXT','Potato',0,'2025-06-08 20:58:55','2025-06-08 20:58:55'),(35,16,'TEXT','Broccoli',0,'2025-06-08 20:58:55','2025-06-08 20:58:55'),(36,17,'TEXT','B',0,'2025-06-08 20:59:16','2025-06-08 20:59:16'),(37,17,'TEXT','C',0,'2025-06-08 20:59:16','2025-06-08 20:59:16'),(38,17,'TEXT','A',1,'2025-06-08 20:59:16','2025-06-08 20:59:16'),(39,17,'TEXT','D',0,'2025-06-08 20:59:16','2025-06-08 20:59:16'),(40,18,'TEXT','Cake',0,'2025-06-08 20:59:40','2025-06-08 20:59:40'),(41,18,'TEXT','Water',1,'2025-06-08 20:59:40','2025-06-08 20:59:40'),(42,18,'TEXT','Rice',0,'2025-06-08 20:59:40','2025-06-08 20:59:40'),(43,18,'TEXT','Apple',0,'2025-06-08 20:59:40','2025-06-08 20:59:40'),(44,19,'TEXT','Chair',0,'2025-06-08 21:00:08','2025-06-08 21:00:08'),(45,19,'TEXT','Jump',1,'2025-06-08 21:00:08','2025-06-08 21:00:08'),(46,19,'TEXT','Milk',0,'2025-06-08 21:00:08','2025-06-08 21:00:08'),(47,19,'TEXT','Table',0,'2025-06-08 21:00:08','2025-06-08 21:00:08'),(48,20,'TEXT','Purple',0,'2025-06-08 21:00:42','2025-06-08 21:00:42'),(49,20,'TEXT','Orange',1,'2025-06-08 21:00:42','2025-06-08 21:00:42'),(50,20,'TEXT','Red',0,'2025-06-08 21:00:42','2025-06-08 21:00:42'),(51,20,'TEXT','Blue',0,'2025-06-08 21:00:42','2025-06-08 21:00:42'),(52,21,'TEXT','Sandwich',0,'2025-06-08 21:01:25','2025-06-08 21:01:25'),(53,21,'TEXT','Lollipop',1,'2025-06-08 21:01:25','2025-06-08 21:01:25'),(54,21,'TEXT','Water',0,'2025-06-08 21:01:25','2025-06-08 21:01:25'),(55,21,'TEXT','Tomato',0,'2025-06-08 21:01:25','2025-06-08 21:01:25'),(56,22,'TEXT','5',0,'2025-06-08 21:01:46','2025-06-08 21:01:46'),(57,22,'TEXT','9',0,'2025-06-08 21:01:46','2025-06-08 21:01:46'),(58,22,'TEXT','10',1,'2025-06-08 21:01:46','2025-06-08 21:01:46'),(59,22,'TEXT','12',0,'2025-06-08 21:01:46','2025-06-08 21:01:46');
/*!40000 ALTER TABLE `quiz_choices` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quiz_questions`
--

DROP TABLE IF EXISTS `quiz_questions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `quiz_questions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `quiz_id` int NOT NULL,
  `question_type` enum('TEXT','IMAGE','AUDIO') NOT NULL,
  `question_content` varchar(255) NOT NULL,
  `answer_type` enum('MULTIPLE_CHOICE','FILL_IN_BLANK') NOT NULL,
  `correct_answer` varchar(255) DEFAULT NULL,
  `order_in_quiz` int NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `_quiz_question_order_uc` (`quiz_id`,`order_in_quiz`),
  CONSTRAINT `quiz_questions_ibfk_1` FOREIGN KEY (`quiz_id`) REFERENCES `quizzes` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quiz_questions`
--

LOCK TABLES `quiz_questions` WRITE;
/*!40000 ALTER TABLE `quiz_questions` DISABLE KEYS */;
INSERT INTO `quiz_questions` VALUES (13,2,'TEXT','What is the color of the sun?','MULTIPLE_CHOICE',NULL,1,'2025-06-08 19:33:29','2025-06-08 19:33:29'),(14,2,'TEXT','What number comes after 4?','MULTIPLE_CHOICE',NULL,2,'2025-06-08 20:45:23','2025-06-08 20:45:23'),(15,2,'TEXT','What do you do when you are hungry?','MULTIPLE_CHOICE',NULL,3,'2025-06-08 20:58:14','2025-06-08 20:58:14'),(16,2,'TEXT','Which one is a fruit?','MULTIPLE_CHOICE',NULL,4,'2025-06-08 20:58:55','2025-06-08 20:58:55'),(17,2,'TEXT','What is the first letter of the word apple?','MULTIPLE_CHOICE',NULL,5,'2025-06-08 20:59:16','2025-06-08 20:59:16'),(18,2,'TEXT','Which of these is a drink?\n','MULTIPLE_CHOICE',NULL,6,'2025-06-08 20:59:40','2025-06-08 20:59:40'),(19,2,'TEXT','Which word is a verb?','MULTIPLE_CHOICE',NULL,7,'2025-06-08 21:00:08','2025-06-08 21:00:08'),(20,2,'TEXT','What color is a carrot?','MULTIPLE_CHOICE',NULL,8,'2025-06-08 21:00:42','2025-06-08 21:00:42'),(21,2,'TEXT','What is a candy?','MULTIPLE_CHOICE',NULL,9,'2025-06-08 21:01:25','2025-06-08 21:01:25'),(22,2,'TEXT','What number is the word ten?','MULTIPLE_CHOICE',NULL,10,'2025-06-08 21:01:46','2025-06-08 21:01:46');
/*!40000 ALTER TABLE `quiz_questions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quizzes`
--

DROP TABLE IF EXISTS `quizzes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `quizzes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `level_id` int NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` text,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `level_id` (`level_id`),
  CONSTRAINT `quizzes_ibfk_1` FOREIGN KEY (`level_id`) REFERENCES `levels` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quizzes`
--

LOCK TABLES `quizzes` WRITE;
/*!40000 ALTER TABLE `quizzes` DISABLE KEYS */;
INSERT INTO `quizzes` VALUES (2,17,'Quiz 1','L1','2025-06-08 18:59:22','2025-06-08 19:01:38');
/*!40000 ALTER TABLE `quizzes` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=69 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sections`
--

LOCK TABLES `sections` WRITE;
/*!40000 ALTER TABLE `sections` DISABLE KEYS */;
INSERT INTO `sections` VALUES (48,'Vocabulary','A1',NULL,17,'2025-06-08 03:12:14','2025-06-08 21:07:31'),(51,'Listening','A1',NULL,17,'2025-06-08 03:34:17','2025-06-08 21:07:35'),(52,'Reading','A1',NULL,17,'2025-06-08 03:34:40','2025-06-08 21:07:38'),(53,'Memory','A1',NULL,17,'2025-06-08 03:34:48','2025-06-08 21:07:42'),(55,'Vocabulary','A2',NULL,35,'2025-06-08 03:35:18','2025-06-08 21:07:48'),(56,'Listening','A2',NULL,35,'2025-06-08 03:35:31','2025-06-08 21:07:51'),(57,'Reading ','A2',NULL,35,'2025-06-08 03:35:42','2025-06-08 21:07:58'),(58,'Memory','A2',NULL,35,'2025-06-08 03:35:54','2025-06-08 21:08:02');
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
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'yousefmyou@gmail.com','jo','scrypt:32768:8:1$te21KqAbThXbR2Kv$b7bb4027cdf14a12d2ad0b1473c9b80c8a7ab593511e163fb11f3a62d43cd50cd9fb5f24fb8a54989215875d5f2e71c740c3b8b675a5ea5b65c358e8552fb30f','ADMIN',1,NULL,NULL,'2025-05-06 07:58:53','2025-05-06 07:58:53'),(31,'okms968@gmail.com','omar3125','pbkdf2:sha256:260000$0umZG49ATvCleNuw$5824f66570e6eac5cd15c5f0ef6847f1b3e64270f8a3098a37c56403c9911d6b','ADMIN',0,NULL,NULL,'2025-06-08 18:08:41','2025-06-08 18:08:41');
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

-- Dump completed on 2025-06-09  0:12:58
