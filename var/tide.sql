-- MySQL dump 10.13  Distrib 5.5.24, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: tide
-- ------------------------------------------------------
-- Server version	5.5.24-0ubuntu0.12.04.1-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `area`
--

DROP TABLE IF EXISTS `area`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `area` (
  `areaid` int(9) unsigned NOT NULL AUTO_INCREMENT,
  `areaname` varchar(45) NOT NULL,
  `location` varchar(45) NOT NULL,
  `longitude` decimal(9,6) NOT NULL DEFAULT '0.000000',
  `latitude` decimal(9,6) NOT NULL DEFAULT '0.000000',
  `updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`areaid`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `area`
--

LOCK TABLES `area` WRITE;
/*!40000 ALTER TABLE `area` DISABLE KEYS */;
INSERT INTO `area` VALUES (1,'清水港','shimizuminato',138.496666,35.009900,'2012-07-24 08:35:45'),(2,'内浦','uchiura',138.898172,35.022458,'2012-07-24 07:20:06'),(3,'石廊崎','irousaki',138.846567,34.606597,'2012-07-24 08:36:24'),(4,'御前崎','omaezaki',138.226805,34.594675,'2012-07-24 08:36:39'),(5,'舞阪','maisaka',0.000000,0.000000,'2012-07-31 09:22:39'),(6,'小田原','odawara',0.000000,0.000000,'2012-07-31 10:54:41'),(7,'横須賀','yokosuka',0.000000,0.000000,'2012-07-31 10:55:21'),(8,'横浜','yokohama',0.000000,0.000000,'2012-07-31 10:56:03');
/*!40000 ALTER TABLE `area` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `area_has_state`
--

DROP TABLE IF EXISTS `area_has_state`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `area_has_state` (
  `areaid` int(9) unsigned NOT NULL,
  `stateid` tinyint(3) unsigned NOT NULL,
  PRIMARY KEY (`areaid`,`stateid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `area_has_state`
--

LOCK TABLES `area_has_state` WRITE;
/*!40000 ALTER TABLE `area_has_state` DISABLE KEYS */;
INSERT INTO `area_has_state` VALUES (1,22),(2,22),(3,22),(4,22),(5,22),(6,14),(7,14),(8,14);
/*!40000 ALTER TABLE `area_has_state` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `location_code`
--

DROP TABLE IF EXISTS `location_code`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `location_code` (
  `location` varchar(45) NOT NULL,
  `codename` varchar(45) NOT NULL,
  `codenamejp` varchar(45) DEFAULT NULL,
  `updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`location`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `location_code`
--

LOCK TABLES `location_code` WRITE;
/*!40000 ALTER TABLE `location_code` DISABLE KEYS */;
INSERT INTO `location_code` VALUES ('irousaki','G9','???','2012-08-17 03:58:43'),('maisaka','MI',NULL,'2012-08-03 04:10:52'),('odawara','OD','???','2012-08-17 03:59:03'),('omaezaki','OM',NULL,'2012-08-03 03:55:21'),('shimizuminato','SM',NULL,'2012-08-03 04:10:08'),('uchiura','UC',NULL,'2012-08-03 04:09:40'),('yokohama','QS',NULL,'2012-08-03 04:14:39'),('yokosuka','QN',NULL,'2012-08-03 04:14:11');
/*!40000 ALTER TABLE `location_code` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `state`
--

DROP TABLE IF EXISTS `state`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `state` (
  `stateid` tinyint(3) unsigned NOT NULL,
  `statename` varchar(45) NOT NULL,
  `updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`stateid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `state`
--

LOCK TABLES `state` WRITE;
/*!40000 ALTER TABLE `state` DISABLE KEYS */;
INSERT INTO `state` VALUES (1,'北海道','2012-07-24 09:42:23'),(2,'青森県','2012-07-24 09:42:23'),(3,'岩手県','2012-07-24 09:42:23'),(4,'宮城県','2012-07-24 09:42:23'),(5,'秋田県','2012-07-24 09:42:23'),(6,'山形県','2012-07-24 09:42:23'),(7,'福島県','2012-07-24 09:42:23'),(8,'茨城県','2012-07-24 09:42:23'),(9,'栃木県','2012-07-24 09:42:23'),(10,'群馬県','2012-07-24 09:42:23'),(11,'埼玉県','2012-07-24 09:42:23'),(12,'千葉県','2012-07-24 09:42:23'),(13,'東京都','2012-07-24 09:42:23'),(14,'神奈川県','2012-07-24 09:42:23'),(15,'新潟県','2012-07-24 09:42:23'),(16,'富山県','2012-07-24 09:42:23'),(17,'石川県','2012-07-24 09:42:23'),(18,'福井県','2012-07-24 09:42:23'),(19,'山梨県','2012-07-24 09:42:23'),(20,'長野県','2012-07-24 09:42:23'),(21,'岐阜県','2012-07-24 09:42:23'),(22,'静岡県','2012-07-24 09:42:23'),(23,'愛知県','2012-07-24 09:42:23'),(24,'三重県','2012-07-24 09:42:23'),(25,'滋賀県','2012-07-24 09:42:23'),(26,'京都府','2012-07-24 09:42:23'),(27,'大阪府','2012-07-24 09:42:23'),(28,'兵庫県','2012-07-24 09:42:23'),(29,'奈良県','2012-07-24 09:42:23'),(30,'和歌山県','2012-07-24 09:42:23'),(31,'鳥取県','2012-07-24 09:42:23'),(32,'島根県','2012-07-24 09:42:23'),(33,'岡山県','2012-07-24 09:42:23'),(34,'広島県','2012-07-24 09:42:24'),(35,'山口県','2012-07-24 09:42:24'),(36,'徳島県','2012-07-24 09:42:24'),(37,'香川県','2012-07-24 09:42:24'),(38,'愛媛県','2012-07-24 09:42:24'),(39,'高知県','2012-07-24 09:42:24'),(40,'福岡県','2012-07-24 09:42:24'),(41,'佐賀県','2012-07-24 09:42:24'),(42,'長崎県','2012-07-24 09:42:24'),(43,'熊本県','2012-07-24 09:42:24'),(44,'大分県','2012-07-24 09:42:24'),(45,'宮崎県','2012-07-24 09:42:24'),(46,'鹿児島県','2012-07-24 09:42:24'),(47,'沖縄県','2012-07-24 09:42:24');
/*!40000 ALTER TABLE `state` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `state_has_tenkijpPref`
--

DROP TABLE IF EXISTS `state_has_tenkijpPref`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `state_has_tenkijpPref` (
  `stateid` tinyint(3) unsigned NOT NULL,
  `prefid` tinyint(3) unsigned NOT NULL,
  PRIMARY KEY (`stateid`,`prefid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `state_has_tenkijpPref`
--

LOCK TABLES `state_has_tenkijpPref` WRITE;
/*!40000 ALTER TABLE `state_has_tenkijpPref` DISABLE KEYS */;
INSERT INTO `state_has_tenkijpPref` VALUES (1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0),(11,0),(12,0),(13,0),(14,17),(15,0),(16,0),(17,0),(18,0),(19,0),(20,0),(21,0),(22,25),(23,0),(24,0),(25,0),(26,0),(27,0),(28,0),(29,0),(30,0),(31,0),(32,0),(33,0),(34,0),(35,0),(36,0),(37,0),(38,0),(39,0),(40,0),(41,0),(42,0),(43,0),(44,0),(45,0),(46,0),(47,0);
/*!40000 ALTER TABLE `state_has_tenkijpPref` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2012-08-17  4:06:20
