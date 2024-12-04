-- MySQL dump 10.13  Distrib 8.0.38, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: artflowdb
-- ------------------------------------------------------
-- Server version	8.0.39

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
-- Table structure for table `api_achievement`
--

DROP TABLE IF EXISTS `api_achievement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_achievement` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` longtext NOT NULL,
  `icon` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_achievement`
--

LOCK TABLES `api_achievement` WRITE;
/*!40000 ALTER TABLE `api_achievement` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_achievement` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_achievement_users`
--

DROP TABLE IF EXISTS `api_achievement_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_achievement_users` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `achievement_id` bigint NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `api_achievement_users_achievement_id_user_id_a43f9596_uniq` (`achievement_id`,`user_id`),
  KEY `api_achievement_users_user_id_2c200067_fk_auth_user_id` (`user_id`),
  CONSTRAINT `api_achievement_user_achievement_id_87219b97_fk_api_achie` FOREIGN KEY (`achievement_id`) REFERENCES `api_achievement` (`id`),
  CONSTRAINT `api_achievement_users_user_id_2c200067_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_achievement_users`
--

LOCK TABLES `api_achievement_users` WRITE;
/*!40000 ALTER TABLE `api_achievement_users` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_achievement_users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_comment`
--

DROP TABLE IF EXISTS `api_comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_comment` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `content` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `is_private` tinyint(1) NOT NULL,
  `post_id` bigint NOT NULL,
  `user_id` int NOT NULL,
  `parent_comment_id` bigint DEFAULT NULL,
  `edited_at` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `api_comment_post_id_251fc0c3_fk_api_post_id` (`post_id`),
  KEY `api_comment_user_id_14315666_fk_auth_user_id` (`user_id`),
  KEY `api_comment_parent_comment_id_775aa873_fk_api_comment_id` (`parent_comment_id`),
  CONSTRAINT `api_comment_parent_comment_id_775aa873_fk_api_comment_id` FOREIGN KEY (`parent_comment_id`) REFERENCES `api_comment` (`id`),
  CONSTRAINT `api_comment_post_id_251fc0c3_fk_api_post_id` FOREIGN KEY (`post_id`) REFERENCES `api_post` (`id`),
  CONSTRAINT `api_comment_user_id_14315666_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_comment`
--

LOCK TABLES `api_comment` WRITE;
/*!40000 ALTER TABLE `api_comment` DISABLE KEYS */;
INSERT INTO `api_comment` VALUES (1,'desenhos muito legais','2024-09-24 19:05:43.647680',0,15,1,NULL,NULL),(2,'Continuem com o bom trabalho amigo','2024-09-24 20:52:50.879116',0,15,3,NULL,NULL),(3,'Realmente','2024-09-25 18:17:10.712902',0,15,1,NULL,'2024-11-10 21:46:39.510312'),(5,'Muito bom trabalho amigo','2024-09-26 12:47:38.792072',0,15,2,NULL,NULL),(9,'Realmente amigo','2024-09-26 13:10:25.612366',0,15,1,2,'2024-11-10 21:42:10.829929'),(10,'Muito bonito os desenhos','2024-09-28 23:42:14.044142',0,14,1,NULL,NULL),(11,'estou pensado no desenho que vou fazer ainda','2024-09-29 18:19:44.322528',0,17,1,NULL,NULL),(12,'vc gosta de usar realmente ne','2024-10-01 18:04:43.328217',0,15,4,9,NULL),(13,'Caraca','2024-10-30 15:26:20.284850',0,15,3,NULL,NULL),(14,'Muito legal!!','2024-11-12 23:19:19.634146',0,11,1,NULL,NULL);
/*!40000 ALTER TABLE `api_comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_comment_likes`
--

DROP TABLE IF EXISTS `api_comment_likes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_comment_likes` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `comment_id` bigint NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `api_comment_likes_comment_id_user_id_4704215b_uniq` (`comment_id`,`user_id`),
  KEY `api_comment_likes_user_id_430966d2_fk_auth_user_id` (`user_id`),
  CONSTRAINT `api_comment_likes_comment_id_00463fb1_fk_api_comment_id` FOREIGN KEY (`comment_id`) REFERENCES `api_comment` (`id`),
  CONSTRAINT `api_comment_likes_user_id_430966d2_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_comment_likes`
--

LOCK TABLES `api_comment_likes` WRITE;
/*!40000 ALTER TABLE `api_comment_likes` DISABLE KEYS */;
INSERT INTO `api_comment_likes` VALUES (11,1,1),(14,2,1),(7,3,1),(8,5,1),(17,9,1),(15,12,1);
/*!40000 ALTER TABLE `api_comment_likes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_follower`
--

DROP TABLE IF EXISTS `api_follower`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_follower` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `follower_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `api_follower_user_id_follower_id_016f653d_uniq` (`user_id`,`follower_id`),
  KEY `api_follower_follower_id_6102f642_fk_api_userdata_id` (`follower_id`),
  CONSTRAINT `api_follower_follower_id_6102f642_fk_api_userdata_id` FOREIGN KEY (`follower_id`) REFERENCES `api_userdata` (`id`),
  CONSTRAINT `api_follower_user_id_f7b69a27_fk_api_userdata_id` FOREIGN KEY (`user_id`) REFERENCES `api_userdata` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_follower`
--

LOCK TABLES `api_follower` WRITE;
/*!40000 ALTER TABLE `api_follower` DISABLE KEYS */;
INSERT INTO `api_follower` VALUES (25,2,1),(22,4,1),(37,1,2),(34,1,4);
/*!40000 ALTER TABLE `api_follower` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_friendrequest`
--

DROP TABLE IF EXISTS `api_friendrequest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_friendrequest` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `is_accepted` tinyint(1) NOT NULL,
  `from_user_id` bigint NOT NULL,
  `to_user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `api_friendrequest_from_user_id_3f131d59_fk_api_userdata_id` (`from_user_id`),
  KEY `api_friendrequest_to_user_id_40db48db_fk_api_userdata_id` (`to_user_id`),
  CONSTRAINT `api_friendrequest_from_user_id_3f131d59_fk_api_userdata_id` FOREIGN KEY (`from_user_id`) REFERENCES `api_userdata` (`id`),
  CONSTRAINT `api_friendrequest_to_user_id_40db48db_fk_api_userdata_id` FOREIGN KEY (`to_user_id`) REFERENCES `api_userdata` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_friendrequest`
--

LOCK TABLES `api_friendrequest` WRITE;
/*!40000 ALTER TABLE `api_friendrequest` DISABLE KEYS */;
INSERT INTO `api_friendrequest` VALUES (8,'2024-09-13 17:00:11.453113',0,2,1),(25,'2024-09-14 13:43:53.884566',0,1,4),(27,'2024-09-14 14:53:40.035888',0,4,3);
/*!40000 ALTER TABLE `api_friendrequest` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_interaction`
--

DROP TABLE IF EXISTS `api_interaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_interaction` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `interaction_type` varchar(20) NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `post_id` bigint NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `api_interaction_post_id_c318ccd6_fk_api_post_id` (`post_id`),
  KEY `api_interaction_user_id_792d430c_fk_auth_user_id` (`user_id`),
  CONSTRAINT `api_interaction_post_id_c318ccd6_fk_api_post_id` FOREIGN KEY (`post_id`) REFERENCES `api_post` (`id`),
  CONSTRAINT `api_interaction_user_id_792d430c_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=117 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_interaction`
--

LOCK TABLES `api_interaction` WRITE;
/*!40000 ALTER TABLE `api_interaction` DISABLE KEYS */;
INSERT INTO `api_interaction` VALUES (1,'favorite','2024-09-23 21:12:30.126358',17,1),(2,'favorite','2024-09-23 21:12:30.466069',14,1),(3,'favorite','2024-09-23 21:12:30.471067',16,1),(4,'favorite','2024-09-23 21:12:30.528065',15,1),(5,'favorite','2024-09-23 21:12:30.534070',13,1),(6,'favorite','2024-09-23 21:12:30.544071',12,1),(7,'favorite','2024-09-23 21:12:30.547064',11,1),(8,'favorite','2024-09-23 21:12:30.553066',9,1),(9,'favorite','2024-09-23 21:12:30.622192',10,1),(10,'favorite','2024-09-23 21:12:30.646190',8,1),(11,'favorite','2024-09-23 21:12:30.830140',16,1),(12,'favorite','2024-09-23 21:12:31.028663',17,1),(13,'favorite','2024-09-23 21:12:31.029661',13,1),(14,'favorite','2024-09-23 21:12:31.039779',14,1),(15,'favorite','2024-09-23 21:12:31.041780',15,1),(16,'favorite','2024-09-23 21:12:31.045778',12,1),(17,'favorite','2024-09-23 21:12:31.077781',11,1),(18,'favorite','2024-09-23 21:12:31.155778',9,1),(19,'favorite','2024-09-23 21:12:31.156778',8,1),(20,'favorite','2024-09-23 21:12:31.290628',10,1),(21,'favorite','2024-09-23 21:12:46.269984',17,1),(22,'favorite','2024-09-23 21:12:46.275986',12,1),(23,'favorite','2024-09-23 21:12:46.276986',16,1),(24,'favorite','2024-09-23 21:12:46.277987',15,1),(25,'favorite','2024-09-23 21:12:46.277987',13,1),(26,'favorite','2024-09-23 21:12:46.278987',14,1),(27,'favorite','2024-09-23 21:12:46.379983',9,1),(28,'favorite','2024-09-23 21:12:46.386985',11,1),(29,'favorite','2024-09-23 21:12:46.394571',10,1),(30,'favorite','2024-09-23 21:12:46.406565',8,1),(31,'favorite','2024-09-23 21:12:47.607657',16,1),(32,'favorite','2024-09-23 21:12:47.653662',17,1),(33,'favorite','2024-09-23 21:12:47.707000',14,1),(34,'favorite','2024-09-23 21:12:47.713993',15,1),(35,'favorite','2024-09-23 21:12:47.716995',13,1),(36,'favorite','2024-09-23 21:12:47.722995',11,1),(37,'favorite','2024-09-23 21:12:47.730993',12,1),(38,'favorite','2024-09-23 21:12:47.757998',10,1),(39,'favorite','2024-09-23 21:12:47.850995',9,1),(40,'favorite','2024-09-23 21:12:47.861992',8,1),(41,'favorite','2024-09-23 21:12:48.052065',14,1),(42,'favorite','2024-09-23 21:12:48.055066',16,1),(43,'favorite','2024-09-23 21:12:48.062063',15,1),(44,'favorite','2024-09-23 21:12:48.076066',17,1),(45,'favorite','2024-09-23 21:12:48.081065',12,1),(46,'favorite','2024-09-23 21:12:48.095063',13,1),(47,'favorite','2024-09-23 21:12:48.195309',9,1),(48,'favorite','2024-09-23 21:12:48.195309',11,1),(49,'favorite','2024-09-23 21:12:48.197306',10,1),(50,'favorite','2024-09-23 21:12:48.205310',8,1),(51,'favorite','2024-09-23 21:12:48.423986',13,1),(52,'favorite','2024-09-23 21:12:48.427987',15,1),(53,'favorite','2024-09-23 21:12:48.436988',17,1),(54,'favorite','2024-09-23 21:12:48.437989',14,1),(55,'favorite','2024-09-23 21:12:48.491140',11,1),(56,'favorite','2024-09-23 21:12:48.497138',16,1),(57,'favorite','2024-09-23 21:12:48.506138',9,1),(58,'favorite','2024-09-23 21:12:48.520568',8,1),(59,'favorite','2024-09-23 21:12:48.534567',12,1),(60,'favorite','2024-09-23 21:12:48.541567',10,1),(61,'favorite','2024-09-23 21:12:48.802096',16,1),(62,'favorite','2024-09-23 21:12:48.876095',15,1),(63,'favorite','2024-09-23 21:12:48.897096',17,1),(64,'favorite','2024-09-23 21:12:49.060265',11,1),(65,'favorite','2024-09-23 21:12:49.062265',10,1),(66,'favorite','2024-09-23 21:12:49.063268',12,1),(67,'favorite','2024-09-23 21:12:49.063268',13,1),(68,'favorite','2024-09-23 21:12:49.063268',14,1),(69,'favorite','2024-09-23 21:12:49.072266',9,1),(70,'favorite','2024-09-23 21:12:49.270499',8,1),(71,'favorite','2024-09-23 21:12:49.510658',16,1),(72,'favorite','2024-09-23 21:12:49.712884',17,1),(73,'favorite','2024-09-23 21:12:49.751563',14,1),(74,'favorite','2024-09-23 21:12:49.751563',15,1),(75,'favorite','2024-09-23 21:12:49.842946',12,1),(76,'favorite','2024-09-23 21:12:49.857489',10,1),(77,'favorite','2024-09-23 21:12:49.863151',11,1),(78,'favorite','2024-09-23 21:12:49.896629',13,1),(79,'favorite','2024-09-23 21:12:49.959918',9,1),(80,'favorite','2024-09-23 21:12:49.976474',8,1),(81,'like','2024-09-23 21:15:47.477037',17,1),(82,'favorite','2024-09-23 21:16:12.301080',15,1),(83,'favorite','2024-09-23 21:16:29.927971',14,1),(84,'like','2024-09-23 21:16:52.037370',16,1),(85,'like','2024-09-23 21:26:29.680344',13,1),(86,'favorite','2024-09-23 21:26:30.713329',13,1),(87,'comment','2024-09-24 19:05:43.665834',15,1),(88,'comment','2024-09-24 20:52:50.897939',15,3),(89,'like','2024-09-24 21:46:10.986478',15,1),(90,'like','2024-09-25 13:03:11.374603',9,1),(91,'like','2024-09-25 14:24:09.327879',12,1),(92,'comment','2024-09-25 18:17:10.743847',15,1),(93,'comment','2024-09-25 18:18:17.790976',15,1),(94,'comment','2024-09-26 12:47:38.801914',15,2),(95,'comment','2024-09-26 12:51:26.114862',15,1),(96,'comment','2024-09-26 12:55:35.323165',15,1),(97,'comment','2024-09-26 12:57:06.847250',15,1),(98,'favorite','2024-09-26 16:31:55.590919',9,1),(99,'comment','2024-09-28 23:42:14.054235',14,1),(100,'favorite','2024-09-29 17:55:54.679663',12,1),(101,'like','2024-09-29 17:56:08.061534',10,1),(102,'comment','2024-09-29 18:19:44.331160',17,1),(103,'like','2024-09-30 16:54:38.820738',15,4),(104,'favorite','2024-09-30 16:54:41.520265',15,4),(105,'like','2024-09-30 16:54:46.598555',17,4),(106,'like','2024-10-23 14:15:55.950403',16,1),(107,'favorite','2024-10-26 00:41:38.718576',10,1),(108,'like','2024-10-29 17:22:10.433407',28,3),(109,'comment','2024-10-30 15:26:20.293752',15,3),(110,'favorite','2024-11-03 22:04:50.538723',16,1),(111,'like','2024-11-03 22:10:49.324181',14,1),(112,'like','2024-11-12 23:11:10.239213',16,1),(113,'comment','2024-11-12 23:19:19.645608',11,1),(114,'favorite','2024-11-12 23:50:29.294112',13,1),(115,'like','2024-11-12 23:57:41.859863',20,1),(116,'favorite','2024-11-12 23:57:48.416398',20,1);
/*!40000 ALTER TABLE `api_interaction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_message`
--

DROP TABLE IF EXISTS `api_message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_message` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `content` longtext NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `is_read` tinyint(1) NOT NULL,
  `sender_id` int NOT NULL,
  `room_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `api_message_sender_id_fa6d8ff2_fk_auth_user_id` (`sender_id`),
  KEY `api_message_room_id_5e8f449d_fk_api_room_id` (`room_id`),
  CONSTRAINT `api_message_room_id_5e8f449d_fk_api_room_id` FOREIGN KEY (`room_id`) REFERENCES `api_room` (`id`),
  CONSTRAINT `api_message_sender_id_fa6d8ff2_fk_auth_user_id` FOREIGN KEY (`sender_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=77 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_message`
--

LOCK TABLES `api_message` WRITE;
/*!40000 ALTER TABLE `api_message` DISABLE KEYS */;
INSERT INTO `api_message` VALUES (1,'ola','2024-11-11 19:28:55.253104',0,1,1),(2,'po','2024-11-11 19:45:51.340644',0,1,2),(3,'teste','2024-11-11 19:51:34.358937',0,1,3),(4,'osa','2024-11-11 20:01:49.892132',0,1,2),(5,'ol','2024-11-11 20:04:19.038414',0,1,3),(6,'op','2024-11-11 22:08:49.349102',0,1,2),(7,'opa','2024-11-11 22:08:49.409652',0,1,2),(8,'ola','2024-11-11 22:59:21.982326',0,4,3),(9,'opa','2024-11-11 23:05:51.894934',0,4,3),(10,'oese','2024-11-11 23:08:00.991810',0,4,3),(11,'deser','2024-11-11 23:12:24.246612',0,1,2),(12,'op','2024-11-12 00:03:14.186092',0,1,3),(13,'como vai amigo','2024-11-12 01:04:05.420351',0,1,3),(14,'como vai','2024-11-12 01:12:16.452944',0,1,3),(15,'comova ','2024-11-12 01:12:42.886555',0,1,3),(16,'heheeh','2024-11-12 01:13:35.021476',0,1,3),(17,'medeus','2024-11-12 01:14:02.544308',0,1,3),(18,'para de da erro','2024-11-12 01:14:14.510007',0,1,3),(19,'fucsd','2024-11-12 01:20:41.375363',0,1,3),(20,'sdfs','2024-11-12 01:20:56.690825',0,1,3),(21,'esdf','2024-11-12 01:22:00.867885',0,1,3),(22,'eds','2024-11-12 01:22:42.767776',0,1,3),(23,'dsfs','2024-11-12 01:25:25.372007',0,1,3),(24,'s','2024-11-12 01:26:02.754772',0,1,3),(25,'sd','2024-11-12 01:27:56.077771',0,1,3),(26,'opsd','2024-11-12 01:32:36.033700',0,1,3),(27,'dsdfeesf','2024-11-12 01:34:23.807788',0,1,3),(28,'dsfsdfe','2024-11-12 01:38:25.032589',0,1,3),(29,'dsfdsdfes','2024-11-12 01:40:23.829080',0,1,3),(30,'esfsdfesdf','2024-11-12 01:40:59.218372',0,1,3),(31,'ola','2024-11-12 16:48:26.774033',0,1,2),(32,'ola','2024-11-12 16:48:26.822276',0,1,2),(33,'ola','2024-11-12 16:48:26.829356',0,1,2),(34,'ola','2024-11-12 16:48:26.837848',0,1,2),(35,'Como vai','2024-11-12 16:59:31.784329',0,4,3),(36,'Como vai','2024-11-12 16:59:31.832888',0,4,3),(37,'hehehe','2024-11-12 17:01:54.013587',0,1,3),(38,'hehehe','2024-11-12 17:01:54.056638',0,1,3),(39,'hehehe','2024-11-12 17:01:54.072157',0,1,3),(40,'hehehe','2024-11-12 17:01:54.080075',0,1,3),(41,'s','2024-11-12 17:02:31.911589',0,4,3),(42,'s','2024-11-12 17:02:31.917115',0,4,3),(43,'s','2024-11-12 17:02:31.917115',0,4,3),(44,'como','2024-11-12 17:09:07.376117',0,1,3),(45,'isso mesmo','2024-11-12 17:09:20.705411',0,4,3),(46,'realmente','2024-11-12 17:11:09.240433',0,4,3),(47,'como eu posso dizer','2024-11-12 17:15:22.507296',0,4,3),(48,'E isso ae','2024-11-12 17:15:30.760057',0,1,3),(49,'pera','2024-11-12 17:16:31.519363',0,4,3),(50,'isso ae','2024-11-12 17:21:25.019002',0,4,3),(51,'ok é isso','2024-11-12 17:24:53.401478',0,1,3),(52,'kskksksks','2024-11-12 18:04:23.377751',0,1,3),(53,'e','2024-11-12 18:11:43.806476',0,4,3),(54,'esfesfs','2024-11-12 18:24:44.239710',0,1,3),(55,'olah','2024-11-12 18:29:52.959510',0,4,3),(56,'cosfsds','2024-11-12 18:30:12.711177',0,1,3),(57,'ess','2024-11-12 18:31:56.773299',0,4,3),(58,'como ssims','2024-11-12 18:32:03.285531',0,1,3),(59,'dsdfssdfsesd','2024-11-12 18:34:32.637746',0,4,3),(60,'como sasess','2024-11-12 18:34:45.686890',0,1,3),(61,'dsfs','2024-11-12 18:35:13.348198',0,4,3),(62,'cfsfsdssdf','2024-11-12 18:37:46.696354',0,4,3),(63,'dsfs','2024-11-12 18:40:56.996321',0,1,3),(64,'dsfesdfe','2024-11-12 18:41:42.422269',0,1,3),(65,'dsfsefsdfeg','2024-11-12 18:46:50.487445',0,4,3),(66,'sefsdeee','2024-11-12 18:48:11.802651',0,1,3),(67,'fesdfes','2024-11-12 18:48:44.456743',0,4,3),(68,'esfsdfe','2024-11-12 18:49:18.582605',0,4,3),(69,'sfsd','2024-11-12 18:49:42.825807',0,1,3),(70,'ldsfsefs','2024-11-12 18:50:53.634091',0,1,3),(71,'kfsjf9osejfosjdfoesjd\\','2024-11-12 18:51:50.787461',0,4,3),(72,'lmlihon','2024-11-12 18:52:24.926428',0,1,3),(73,'dsfes','2024-11-12 18:53:44.999813',0,1,3),(74,'dsfesdfedsss','2024-11-12 18:54:10.741656',0,4,3),(75,'dedsfdfses','2024-11-12 18:54:34.675724',0,1,3),(76,'op','2024-11-14 18:08:58.940282',0,1,1);
/*!40000 ALTER TABLE `api_message` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_notification`
--

DROP TABLE IF EXISTS `api_notification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_notification` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `notification_type` varchar(20) NOT NULL,
  `content` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `is_read` tinyint(1) NOT NULL,
  `user_id` int NOT NULL,
  `sender_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `api_notification_user_id_6cede59e_fk_auth_user_id` (`user_id`),
  CONSTRAINT `api_notification_user_id_6cede59e_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_notification`
--

LOCK TABLES `api_notification` WRITE;
/*!40000 ALTER TABLE `api_notification` DISABLE KEYS */;
INSERT INTO `api_notification` VALUES (7,'friend_accepted','teste aceitou sua solicitação de amizade.','2024-09-13 17:01:45.326432',0,2,NULL),(29,'friend_request','Google_uwu enviou uma solicitação de amizade.','2024-09-14 14:53:40.040748',1,3,4);
/*!40000 ALTER TABLE `api_notification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_post`
--

DROP TABLE IF EXISTS `api_post`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_post` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `caption` longtext,
  `created_at` datetime(6) NOT NULL,
  `is_sensitive` tinyint(1) NOT NULL,
  `user_id` int NOT NULL,
  `comments_count` int NOT NULL,
  `is_private` tinyint(1) NOT NULL,
  `last_edited_at` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `api_post_user_id_580bae2a_fk_auth_user_id` (`user_id`),
  CONSTRAINT `api_post_user_id_580bae2a_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_post`
--

LOCK TABLES `api_post` WRITE;
/*!40000 ALTER TABLE `api_post` DISABLE KEYS */;
INSERT INTO `api_post` VALUES (1,'teste postegem','2024-09-11 22:25:55.454417',0,3,0,1,NULL),(5,'Explorando novas ideias para o próximo projeto de arte! ?✨ Fico sempre inspirado pela natureza e pelas formas abstratas. Alguma sugestão para o próximo desenho? #Arte #Criatividade #Inspiração #Desenho #ArtFlow','2024-09-21 22:51:44.397799',0,1,0,0,NULL),(6,'Entre o bem e o mal, só há espaço para coragem, Não é apenas um duelo, é sobrevivência em um mundo cheio de maldições. ? #GojoSatoru #JujutsuKaisenArt ? #Sukuna #JujutsuKaisen','2024-09-22 16:59:37.715384',0,4,0,0,NULL),(8,'Toji Fushiguro  a força bruta e a destreza de um verdadeiro assassino sem maldição. ?⚔️ #TojiFushiguro #JujutsuKaisen #PoderSemLimites','2024-09-22 17:03:53.365580',0,3,0,0,NULL),(9,'Transformando o sonho em realidade! ✨✨ Arima Kana como Tsurugi, mostrando que a força vem do coração e da determinação. #ArimaKana #Tsurugi #AnimeArt #OshiNoKo','2024-09-22 17:13:23.770288',0,3,0,0,NULL),(10,'Uma viagem pelo mundo dos animes! ?✨ Cada traço conta uma história e cada personagem traz uma lembrança. Quem mais ama essa mistura mágica? #AnimeArt #MúltiplosUniversos #FanAr','2024-09-22 17:14:25.136336',0,3,0,0,NULL),(11,'Uma viagem pelo mundo dos animes! ?✨ Cada traço conta uma história e cada personagem traz uma lembrança. Quem mais ama essa mistura mágica? #AnimeArt #MúltiplosUniversos #FanArt','2024-09-22 18:34:39.700913',0,1,1,0,'2024-11-12 23:19:19.642587'),(12,'Depois de assistir ao novo filme, só posso dizer: Deadpool e Wolverine juntos são pura loucura! ?? Não resisti e fiz essa arte para homenagear o Mercenário Tagarela e o Carcaju. Quem mais está ansioso para ver mais dessa dupla? ??️ #Deadpool #Wolverine #FanArt #DuplaImprovável','2024-09-23 16:41:09.572845',0,4,0,0,NULL),(13,'Explosões de poder e batalhas épicas! ?? Não importa quantos anos passem, Dragon Ball Z sempre vai ser uma fonte infinita de inspiração. Essa arte é uma homenagem aos guerreiros que moldaram minha infância. Quem mais está pronto para outra rodada de Kamehameha? ?✨ #DragonBallZ #Saiyajins #FanArt #NostalgiaDBZ','2024-09-23 16:46:31.203538',0,4,0,0,NULL),(14,'?✨ Desenho Geek do Dia ✨? Todo dia, uma nova arte para alimentar sua paixão pelo mundo geek! Desde heróis épicos até criaturas fantásticas, vou compartilhar um pouco de tudo que faz a cultura pop ser tão incrível. Fique ligado para mais criatividade e fandom! ??️ #GeekArt #ArteDiária #CulturaPop #FanArt','2024-09-23 16:55:39.839653',0,4,1,0,NULL),(15,'?? A brutalidade e caos de Chainsaw Man capturados em cada traço! Denji e sua serra mortal enfrentando o inferno com estilo. Quem mais tá hypado por essa insanidade? ?? #ChainsawMan #Denji #DevilHunter #ArteInsana','2024-09-23 16:57:36.510685',0,4,7,0,'2024-11-10 21:46:39.553436'),(16,'Cada dia evoluído pai já é o Picasso 2 ','2024-09-23 16:59:49.931618',0,4,0,0,'2024-11-06 14:13:15.557578'),(17,'?✨ E aí, galera! Como estão indo no Desafio de Desenho deste mês? Já mandaram ver nos rabiscos? Quero ver o progresso de vocês, compartilhem suas criações aqui! ?️? #DesafioDeArte #ArtFlow #DesenhoDoMês\"','2024-09-23 17:01:44.841529',0,3,1,0,NULL),(20,'','2024-10-18 13:50:54.298957',0,1,0,0,NULL),(21,'Hora de aventura','2024-10-18 13:53:19.638129',0,1,0,0,'2024-10-21 14:12:54.556938'),(24,'','2024-10-18 20:36:40.732635',0,1,0,0,NULL),(28,'teste de editar postagem, 2','2024-10-20 23:31:23.531812',0,1,0,0,'2024-10-21 01:05:29.566762');
/*!40000 ALTER TABLE `api_post` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_post_favorites`
--

DROP TABLE IF EXISTS `api_post_favorites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_post_favorites` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `post_id` bigint NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `api_post_favorites_post_id_user_id_722d2fbf_uniq` (`post_id`,`user_id`),
  KEY `api_post_favorites_user_id_8a7ba9d3_fk_auth_user_id` (`user_id`),
  CONSTRAINT `api_post_favorites_post_id_db2ddc01_fk_api_post_id` FOREIGN KEY (`post_id`) REFERENCES `api_post` (`id`),
  CONSTRAINT `api_post_favorites_user_id_8a7ba9d3_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=91 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_post_favorites`
--

LOCK TABLES `api_post_favorites` WRITE;
/*!40000 ALTER TABLE `api_post_favorites` DISABLE KEYS */;
INSERT INTO `api_post_favorites` VALUES (84,9,1),(87,10,1),(85,12,1),(82,14,1),(81,15,1),(86,15,4),(88,16,1),(90,20,1);
/*!40000 ALTER TABLE `api_post_favorites` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_post_likes`
--

DROP TABLE IF EXISTS `api_post_likes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_post_likes` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `post_id` bigint NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `api_post_likes_post_id_user_id_d89a6e65_uniq` (`post_id`,`user_id`),
  KEY `api_post_likes_user_id_85624e4f_fk_auth_user_id` (`user_id`),
  CONSTRAINT `api_post_likes_post_id_6cd04b3a_fk_api_post_id` FOREIGN KEY (`post_id`) REFERENCES `api_post` (`id`),
  CONSTRAINT `api_post_likes_user_id_85624e4f_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_post_likes`
--

LOCK TABLES `api_post_likes` WRITE;
/*!40000 ALTER TABLE `api_post_likes` DISABLE KEYS */;
INSERT INTO `api_post_likes` VALUES (5,9,1),(7,10,1),(6,12,1),(3,13,1),(12,14,1),(4,15,1),(8,15,4),(13,16,1),(1,17,1),(9,17,4),(14,20,1),(11,28,3);
/*!40000 ALTER TABLE `api_post_likes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_postmedia`
--

DROP TABLE IF EXISTS `api_postmedia`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_postmedia` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `file` varchar(255) NOT NULL,
  `post_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `api_postmedia_post_id_299d25e1_fk_api_post_id` (`post_id`),
  CONSTRAINT `api_postmedia_post_id_299d25e1_fk_api_post_id` FOREIGN KEY (`post_id`) REFERENCES `api_post` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_postmedia`
--

LOCK TABLES `api_postmedia` WRITE;
/*!40000 ALTER TABLE `api_postmedia` DISABLE KEYS */;
INSERT INTO `api_postmedia` VALUES (1,'https://res.cloudinary.com/dynymtlrt/image/upload/v1726093601/yjmwrka7zfarynbp6r61.png',1),(2,'https://res.cloudinary.com/dynymtlrt/image/upload/v1726093601/k1itxacxpevdp5d8y6hm.jpg',1),(5,'https://res.cloudinary.com/dynymtlrt/image/upload/v1726959160/vmdm0xgmmkwtbzlfg9jr.jpg',5),(6,'https://res.cloudinary.com/dynymtlrt/image/upload/v1726959160/ydnfleybggt026aw5hbw.jpg',5),(7,'https://res.cloudinary.com/dynymtlrt/image/upload/v1727024433/ckayb0ntb5muji5vbxu7.jpg',6),(8,'https://res.cloudinary.com/dynymtlrt/image/upload/v1727024434/mqu8g2aspjwij7ncebo3.jpg',6),(9,'https://res.cloudinary.com/dynymtlrt/video/upload/v1727024690/ehiqlraxxpjjzzrp4kpe.mp4',8),(10,'https://res.cloudinary.com/dynymtlrt/image/upload/v1727025258/ld7iqzqoigczhwkpwlaf.jpg',9),(11,'https://res.cloudinary.com/dynymtlrt/video/upload/v1727025260/yenwiyxtfotfia9xnbha.mp4',9),(12,'https://res.cloudinary.com/dynymtlrt/image/upload/v1727025319/tod2kerh7jlxi82qq5wc.jpg',10),(13,'https://res.cloudinary.com/dynymtlrt/image/upload/v1727025320/alxl79xjyotrz4pb3iev.jpg',10),(14,'https://res.cloudinary.com/dynymtlrt/image/upload/v1727025321/sfaykwdiws8uwkdvxxgy.jpg',10),(15,'https://res.cloudinary.com/dynymtlrt/image/upload/v1727025323/pht8eqffz2vowwoq58en.gif',10),(16,'https://res.cloudinary.com/dynymtlrt/image/upload/v1727025324/uaenmqinybozgmxsncpr.gif',10),(17,'https://res.cloudinary.com/dynymtlrt/image/upload/v1727030135/vz7llsr4cjmmrxaqc6ss.jpg',11),(18,'https://res.cloudinary.com/dynymtlrt/image/upload/v1727030136/hgymjg8rtcaijzj7fli3.jpg',11),(19,'https://res.cloudinary.com/dynymtlrt/image/upload/v1727030136/qijul0jd8xma04fgrzh9.jpg',11),(20,'https://res.cloudinary.com/dynymtlrt/image/upload/v1727109727/eduk9gdijlmjh1mhxdu9.jpg',12),(21,'https://res.cloudinary.com/dynymtlrt/image/upload/v1727109727/gwbbaxcqgpmgef0dzbzf.jpg',12),(22,'https://res.cloudinary.com/dynymtlrt/image/upload/v1727109728/oy0k0vcdvannfzzhsev0.jpg',12),(23,'https://res.cloudinary.com/dynymtlrt/image/upload/v1727109729/vp4s0qfhytjbo2fcz5ny.jpg',12),(24,'https://res.cloudinary.com/dynymtlrt/image/upload/v1727110047/m7yfo3o84iilnkjlqsfs.jpg',13),(25,'https://res.cloudinary.com/dynymtlrt/video/upload/v1727110048/w0guaqlvog0rritrgwly.mp4',13),(26,'https://res.cloudinary.com/dynymtlrt/video/upload/v1727110049/qdzapbjwweefqiq9ltcx.mp4',13),(27,'https://res.cloudinary.com/dynymtlrt/image/upload/v1727110595/qovt3w9xhammnrf9pyit.jpg',14),(28,'https://res.cloudinary.com/dynymtlrt/image/upload/v1727110596/gkjrmjjsqkki0uvhx8gw.jpg',14),(29,'https://res.cloudinary.com/dynymtlrt/image/upload/v1727110597/ks5i20vr7sscay1pqiw2.jpg',14),(30,'https://res.cloudinary.com/dynymtlrt/image/upload/v1727110597/ip7wqi8kiccxozlaxhmn.jpg',14),(31,'https://res.cloudinary.com/dynymtlrt/image/upload/v1727110712/pchgq5sjbmvp5hbfci9u.jpg',15),(32,'https://res.cloudinary.com/dynymtlrt/image/upload/v1727110713/smyf2vxbcigamlch11pf.jpg',15),(33,'https://res.cloudinary.com/dynymtlrt/image/upload/v1727110713/tjyecamcn4ysxllobvy3.jpg',15),(34,'https://res.cloudinary.com/dynymtlrt/image/upload/v1727110845/anz7hxhg2afzsqhyfab2.jpg',16),(35,'https://res.cloudinary.com/dynymtlrt/image/upload/v1727110846/fgitwzhobgdcxocm3s5l.jpg',16),(40,'https://res.cloudinary.com/dynymtlrt/image/upload/v1729259537/kzagmoz30bskmhbedm96.jpg',20),(41,'https://res.cloudinary.com/dynymtlrt/image/upload/v1729259538/nr6blxwgm9wigutdgxmk.jpg',20),(42,'https://res.cloudinary.com/dynymtlrt/image/upload/v1729259682/wygaackefpfvpfcqkyty.gif',21),(44,'https://res.cloudinary.com/dynymtlrt/image/upload/v1729283884/vzq2yrvpd99xplh9awys.gif',24),(54,'https://res.cloudinary.com/dynymtlrt/image/upload/v1729467339/seozaj4uefg1ys9jdw07.gif',28),(56,'https://res.cloudinary.com/dynymtlrt/image/upload/v1729468385/koxenrxozzqoij27biac.gif',28);
/*!40000 ALTER TABLE `api_postmedia` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_room`
--

DROP TABLE IF EXISTS `api_room`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_room` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_room`
--

LOCK TABLES `api_room` WRITE;
/*!40000 ALTER TABLE `api_room` DISABLE KEYS */;
INSERT INTO `api_room` VALUES (2,'1_2'),(1,'1_3'),(3,'1_4');
/*!40000 ALTER TABLE `api_room` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_room_participants`
--

DROP TABLE IF EXISTS `api_room_participants`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_room_participants` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `room_id` bigint NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `api_room_participants_room_id_user_id_a02d8b94_uniq` (`room_id`,`user_id`),
  KEY `api_room_participants_user_id_292ecf97_fk_auth_user_id` (`user_id`),
  CONSTRAINT `api_room_participants_room_id_2b4cb5c0_fk_api_room_id` FOREIGN KEY (`room_id`) REFERENCES `api_room` (`id`),
  CONSTRAINT `api_room_participants_user_id_292ecf97_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_room_participants`
--

LOCK TABLES `api_room_participants` WRITE;
/*!40000 ALTER TABLE `api_room_participants` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_room_participants` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_userdata`
--

DROP TABLE IF EXISTS `api_userdata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_userdata` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_tag` varchar(30) NOT NULL,
  `bio` longtext,
  `birth_date` date NOT NULL,
  `user_id` int NOT NULL,
  `profile_picture_url` varchar(200) DEFAULT NULL,
  `is_online` tinyint(1) NOT NULL,
  `banner_picture_id` varchar(255) DEFAULT NULL,
  `banner_picture_url` varchar(200) DEFAULT NULL,
  `displayname` varchar(100) NOT NULL,
  `profile_picture_id` varchar(255) DEFAULT NULL,
  `is_private` tinyint(1) NOT NULL,
  `recovery_email` varchar(254) DEFAULT NULL,
  `two_factor_code` varchar(6) DEFAULT NULL,
  `two_factor_enabled` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_tag` (`user_tag`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `api_userdata_user_id_afd981ee_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_userdata`
--

LOCK TABLES `api_userdata` WRITE;
/*!40000 ALTER TABLE `api_userdata` DISABLE KEYS */;
INSERT INTO `api_userdata` VALUES (1,'@artflow_oficial','Teste de perfil artFlow','2000-02-20',1,'https://res.cloudinary.com/dynymtlrt/image/upload/v1728658256/vc0tdf9myxuhtb5y8olj.png',0,'d83d0qzqfcvvgxj4hrij','https://res.cloudinary.com/dynymtlrt/image/upload/v1728667511/d83d0qzqfcvvgxj4hrij.png','ArtFlows_Oficial',NULL,1,'gogleuser49@gmail.com',NULL,0),(2,'@Jaker_E2','','2000-02-21',2,'https://res.cloudinary.com/dynymtlrt/image/upload/v1724900246/default-img-perfil/uitqsvayiua7nbh8dcru.jpg',0,NULL,NULL,'Jaker_oWo',NULL,0,NULL,NULL,0),(3,'VonEarthy@8040','','2003-03-01',3,'https://res.cloudinary.com/dynymtlrt/image/upload/v1730830960/fczkvdrbtercxfczjenb.png',0,'wb2q7gib7rfrrcrkftuy','https://res.cloudinary.com/dynymtlrt/image/upload/v1730830961/wb2q7gib7rfrrcrkftuy.png','','fczkvdrbtercxfczjenb',0,NULL,NULL,0),(4,'Google_uwu@2593','Opa Amigos opa','2000-02-10',4,'https://res.cloudinary.com/dynymtlrt/image/upload/v1730835844/c1fxdhbyhyqwshasbjgm.png',1,'fj9mg8ybs0ey5ndjzrho','https://res.cloudinary.com/dynymtlrt/image/upload/v1730903269/fj9mg8ybs0ey5ndjzrho.png','GoATgoogle','c1fxdhbyhyqwshasbjgm',1,NULL,NULL,1),(5,'@Manitos1152','','2000-12-01',5,'https://res.cloudinary.com/dynymtlrt/image/upload/v1724900246/default-img-perfil/uitqsvayiua7nbh8dcru.jpg',1,NULL,NULL,'',NULL,0,NULL,NULL,0);
/*!40000 ALTER TABLE `api_userdata` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_userdata_friends`
--

DROP TABLE IF EXISTS `api_userdata_friends`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_userdata_friends` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `from_userdata_id` bigint NOT NULL,
  `to_userdata_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `api_userdata_friends_from_userdata_id_to_user_9cab7857_uniq` (`from_userdata_id`,`to_userdata_id`),
  KEY `api_userdata_friends_to_userdata_id_82ae95a1_fk_api_userdata_id` (`to_userdata_id`),
  CONSTRAINT `api_userdata_friends_from_userdata_id_72e06f0a_fk_api_userd` FOREIGN KEY (`from_userdata_id`) REFERENCES `api_userdata` (`id`),
  CONSTRAINT `api_userdata_friends_to_userdata_id_82ae95a1_fk_api_userdata_id` FOREIGN KEY (`to_userdata_id`) REFERENCES `api_userdata` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_userdata_friends`
--

LOCK TABLES `api_userdata_friends` WRITE;
/*!40000 ALTER TABLE `api_userdata_friends` DISABLE KEYS */;
INSERT INTO `api_userdata_friends` VALUES (13,1,2),(54,1,3),(58,1,4),(14,2,1),(53,3,1),(57,4,1);
/*!40000 ALTER TABLE `api_userdata_friends` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=69 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add achievement',7,'add_achievement'),(26,'Can change achievement',7,'change_achievement'),(27,'Can delete achievement',7,'delete_achievement'),(28,'Can view achievement',7,'view_achievement'),(29,'Can add post',8,'add_post'),(30,'Can change post',8,'change_post'),(31,'Can delete post',8,'delete_post'),(32,'Can view post',8,'view_post'),(33,'Can add user data',9,'add_userdata'),(34,'Can change user data',9,'change_userdata'),(35,'Can delete user data',9,'delete_userdata'),(36,'Can view user data',9,'view_userdata'),(37,'Can add comment',10,'add_comment'),(38,'Can change comment',10,'change_comment'),(39,'Can delete comment',10,'delete_comment'),(40,'Can view comment',10,'view_comment'),(41,'Can add post media',11,'add_postmedia'),(42,'Can change post media',11,'change_postmedia'),(43,'Can delete post media',11,'delete_postmedia'),(44,'Can view post media',11,'view_postmedia'),(45,'Can add friend request',12,'add_friendrequest'),(46,'Can change friend request',12,'change_friendrequest'),(47,'Can delete friend request',12,'delete_friendrequest'),(48,'Can view friend request',12,'view_friendrequest'),(49,'Can add follower',13,'add_follower'),(50,'Can change follower',13,'change_follower'),(51,'Can delete follower',13,'delete_follower'),(52,'Can view follower',13,'view_follower'),(53,'Can add notification',14,'add_notification'),(54,'Can change notification',14,'change_notification'),(55,'Can delete notification',14,'delete_notification'),(56,'Can view notification',14,'view_notification'),(57,'Can add interaction',15,'add_interaction'),(58,'Can change interaction',15,'change_interaction'),(59,'Can delete interaction',15,'delete_interaction'),(60,'Can view interaction',15,'view_interaction'),(61,'Can add room',16,'add_room'),(62,'Can change room',16,'change_room'),(63,'Can delete room',16,'delete_room'),(64,'Can view room',16,'view_room'),(65,'Can add message',17,'add_message'),(66,'Can change message',17,'change_message'),(67,'Can delete message',17,'delete_message'),(68,'Can view message',17,'view_message');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$870000$H3bwIHnLQnatANrGY4a2bn$kojVPyMF0OTwCMHhEEM7lSjyfD5G/uwDmtXHejCZFLs=','2024-10-02 23:03:36.054105',0,'teste','','','teste55@gmail.com',0,1,'2024-09-11 22:16:26.246943'),(2,'pbkdf2_sha256$870000$vIhzS108PVGDuRkVRvN2qr$mLZYR8KjkcFvZp8tQLtwIqtZ6UpZ9o7swD+dQ0Sl3x4=',NULL,0,'jakepudim1236','','','jakepumdr@gmail.com',0,1,'2024-09-11 22:19:42.362190'),(3,'pbkdf2_sha256$870000$xYSFBCsV3iBPzKSHSlVCuh$8NdmWmLAicD+/jWxElq9qb2TVApgkQMneyKpNNQdrRU=',NULL,0,'VonEarthy','','','meutste@gmail.com',0,1,'2024-09-11 22:21:53.056259'),(4,'pbkdf2_sha256$870000$l9F1DWzSFlvRrtOiAGeJlF$35e0pK8+WrXGI4Lgot83k7nZX9AoDTRJTn8UPuYpgBo=',NULL,0,'Google_uwu','','','gogleuser49@gmail.com',0,1,'2024-09-12 19:22:38.159919'),(5,'pbkdf2_sha256$870000$m4XaQrVWlbtMVWuuDfbuw4$+b1ntAHhK0XecPBVbKbHFgOzzFIh6SQPRBIBkuliI9E=',NULL,0,'Manitos','','','teste6@gmail.com',0,1,'2024-10-22 22:45:42.028102');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(7,'api','achievement'),(10,'api','comment'),(13,'api','follower'),(12,'api','friendrequest'),(15,'api','interaction'),(17,'api','message'),(14,'api','notification'),(8,'api','post'),(11,'api','postmedia'),(16,'api','room'),(9,'api','userdata'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2024-09-11 22:13:39.957688'),(2,'auth','0001_initial','2024-09-11 22:13:40.905365'),(3,'admin','0001_initial','2024-09-11 22:13:41.097177'),(4,'admin','0002_logentry_remove_auto_add','2024-09-11 22:13:41.107686'),(5,'admin','0003_logentry_add_action_flag_choices','2024-09-11 22:13:41.117415'),(6,'contenttypes','0002_remove_content_type_name','2024-09-11 22:13:41.231140'),(7,'auth','0002_alter_permission_name_max_length','2024-09-11 22:13:41.319092'),(8,'auth','0003_alter_user_email_max_length','2024-09-11 22:13:41.349387'),(9,'auth','0004_alter_user_username_opts','2024-09-11 22:13:41.357790'),(10,'auth','0005_alter_user_last_login_null','2024-09-11 22:13:41.444132'),(11,'auth','0006_require_contenttypes_0002','2024-09-11 22:13:41.448149'),(12,'auth','0007_alter_validators_add_error_messages','2024-09-11 22:13:41.456665'),(13,'auth','0008_alter_user_username_max_length','2024-09-11 22:13:41.549923'),(14,'auth','0009_alter_user_last_name_max_length','2024-09-11 22:13:41.647645'),(15,'auth','0010_alter_group_name_max_length','2024-09-11 22:13:41.674479'),(16,'auth','0011_update_proxy_permissions','2024-09-11 22:13:41.682886'),(17,'auth','0012_alter_user_first_name_max_length','2024-09-11 22:13:41.776755'),(18,'api','0001_initial','2024-09-11 22:13:42.209559'),(19,'api','0002_userprofile_delete_user','2024-09-11 22:13:42.392398'),(20,'api','0003_achievement_post_userdata_delete_userprofile','2024-09-11 22:13:42.887274'),(21,'api','0004_remove_userdata_profile_picture_and_more','2024-09-11 22:13:42.944443'),(22,'api','0005_remove_post_image_post_comments_post_is_private_and_more','2024-09-11 22:13:43.806028'),(23,'api','0006_rename_comments_post_comments_count','2024-09-11 22:13:43.850290'),(24,'api','0007_userdata_followers_userdata_friends','2024-09-11 22:13:44.354229'),(25,'api','0008_friendrequest','2024-09-11 22:13:44.555485'),(26,'api','0009_rename_is_accepted_friendrequest_accepted_and_more','2024-09-11 22:13:45.187502'),(27,'api','0010_rename_accepted_friendrequest_is_accepted_and_more','2024-09-11 22:13:46.043380'),(28,'api','0011_alter_userdata_followers','2024-09-11 22:13:46.057232'),(29,'api','0012_alter_userdata_followers','2024-09-11 22:13:46.384667'),(30,'api','0013_alter_userdata_followers','2024-09-11 22:13:46.700646'),(31,'sessions','0001_initial','2024-09-11 22:13:46.752611'),(32,'api','0014_alter_userdata_followers_alter_userdata_friends','2024-09-12 14:01:44.560343'),(33,'api','0015_remove_userdata_followers_remove_userdata_friends_and_more','2024-09-12 14:33:02.184339'),(34,'api','0016_userdata_friends','2024-09-12 14:41:02.252770'),(35,'api','0017_notification','2024-09-12 18:18:13.816877'),(36,'api','0018_notification_sender_id','2024-09-12 20:59:25.357728'),(37,'api','0019_userdata_is_online_and_more','2024-09-15 18:03:43.023321'),(38,'api','0020_interaction','2024-09-21 22:51:11.833964'),(39,'api','0021_post_favorites_alter_interaction_interaction_type','2024-09-23 21:10:47.728127'),(40,'api','0022_comment_likes_comment_parent_comment','2024-09-25 14:59:57.200995'),(41,'api','0023_userdata_banner_picture_id_and_more','2024-10-10 18:19:46.407950'),(42,'api','0024_userdata_is_private','2024-10-16 15:19:57.084890'),(43,'api','0025_post_last_edited_at','2024-10-21 01:03:44.647309'),(44,'api','0026_comment_edited_at','2024-11-04 15:34:20.469975'),(45,'api','0027_userdata_recovery_email_userdata_two_factor_code_and_more','2024-11-06 19:05:22.126778'),(46,'api','0028_room_message','2024-11-11 15:58:24.787152');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('uk7z5cvx350m5way7mfbk82ufl0201n7','.eJxVjMEOwiAQRP-FsyGyCAWP3vsNhGUXqRpISnsy_rtt0oNe5jDvzbxFiOtSwtp5DhOJq1Di9NthTE-uO6BHrPcmU6vLPKHcFXnQLsdG_Lod7t9Bib1s65wBmc_gk1VMZgsTLWhmVhGSH4DBKrQ4eMWayKRsrXPITme8aGPE5wsClzht:1sw8Nc:CDx10tar7non7ouBKqKNE4tvmDR65y-8O_aMoIUFL7A','2024-10-16 23:03:36.108619');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-11-14 18:34:07
