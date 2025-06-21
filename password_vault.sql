-- MySQL dump 10.13  Distrib 9.1.0, for Win64 (x86_64)
--
-- Host: localhost    Database: password_vault
-- ------------------------------------------------------
-- Server version	8.0.42

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
-- Table structure for table `credentials`
--

DROP TABLE IF EXISTS `credentials`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `credentials` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `site_name` varchar(100) NOT NULL,
  `site_username` varchar(100) NOT NULL,
  `site_password_encrypted` text NOT NULL,
  `notes` text,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `credentials_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `credentials`
--

LOCK TABLES `credentials` WRITE;
/*!40000 ALTER TABLE `credentials` DISABLE KEYS */;
INSERT INTO `credentials` VALUES (12,1,'gmail','barath.bala2004@gmail.com','gAAAAABoVsL1lh5WAjQd8bkiCop9G-poSXz7wynbRah95xzLmACTpcqpdLndrNMJm8l09BHAH8TJK1SiSjVAUxAhFErfaPe4vQ==','Personal mail'),(13,1,'gmail','barathworkspace@gmail.com','gAAAAABoVsH_rwMske0oyP4CSei0R86vOT5I9q4aOMssGXjWQmOxseqLdV6eS1yG5gV9tuLa2bOQsa6ZK-eqjBfpIveG3DSrtA==','Official gmail'),(14,1,'linkedin','barathbala','gAAAAABoVsIp4dxcHx0aJO5jPWVEMj75q3mjJ4FpFofyuwEya0fmGXOVSJCS9AIQpR-9cBNE4IZ5O488YsgvjsE8-osfRcgi3w==','Linked In\r\n'),(15,1,'instagram','barath.bala07','gAAAAABoVsJP4h_l4EL1FSnlW_7WTeON_btJOxZ2wTb9FjVn4fMgPKr9cpYs8x_w4Rgsg9RqMh4-ZNKUsXDFUaw4U21Zmzaqdg==','insta public acc'),(17,2,'gmail','bala07','gAAAAABoVsQATHRLVnuLsuE7SUq2J4Nz0sYiEz8o5dU3iuxsNH4oPjOI0deE57eAzHJyFAnS78SpywEeTNM_udGEX_kxCUA5nQ==','personal mail'),(18,2,'linkedin','bala007','gAAAAABoVsQXkRj-IpZv6RYxT4E-Xo_IGNgscW2Uq1zWKNAgRMYY4J35qosS8ExVSikb0XB8mKKRVhn3C5b1kkmKKOYcgQkdqg==','linked in'),(19,2,'instagram','bala0704','gAAAAABoVsQ21Klc1M24Hz0mdANdO3pa8KhxkMk0hpImUsR2VmrHafoUE4LcNY_BbBG2U87ENgKbFt3K0m5XUgp9Ffn1jktPGQ==','insta public acc');
/*!40000 ALTER TABLE `credentials` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password_hash` varchar(200) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'barath','scrypt:32768:8:1$dtqKaCk6vNtfJlrl$a9688a0c246c83de95390e5f48f3dd1940807ce7263e4af273b683102535803c5e736ee2fd13b060aad0beaafe43502388f14c94a0bd0252b3f8009f82119642'),(2,'bala','scrypt:32768:8:1$DLx7vvFUEGCQhPNI$2fa0efc66de262b97e9a0f6a2172a74b06c80846cc9292f009cf0d1612a67c56de8fa97eed5142f42edaa2ffba7f13625db88a61ac8099322e5f763593af7aae');
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

-- Dump completed on 2025-06-21 21:00:57
