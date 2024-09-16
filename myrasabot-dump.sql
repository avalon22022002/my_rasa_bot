-- MySQL dump 10.13  Distrib 8.0.31, for Win64 (x86_64)
--
-- Host: localhost    Database: myrasabot
-- ------------------------------------------------------
-- Server version	8.0.31

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
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admin` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `phno` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8672 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin`
--

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
INSERT INTO `admin` VALUES (1,'prasad','admin','8867066062'),(8671,'avalon','admin','8549976690');
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customer` (
  `c_id` int NOT NULL AUTO_INCREMENT,
  `c_name` varchar(50) DEFAULT NULL,
  `c_phno` varchar(10) DEFAULT NULL,
  `c_password` varchar(50) DEFAULT NULL,
  `c_city_name` varchar(50) DEFAULT NULL,
  `c_address` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`c_id`)
) ENGINE=InnoDB AUTO_INCREMENT=281 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer`
--

LOCK TABLES `customer` WRITE;
/*!40000 ALTER TABLE `customer` DISABLE KEYS */;
INSERT INTO `customer` VALUES (12,'patil','8867066062','customer','kalaburagi','manikeshwari colony'),(261,'John Doe','1234567890','password1','New York','123 Main St'),(262,'Jane Smith','2345678901','password2','Los Angeles','456 Elm St'),(263,'Michael Johnson','3456789012','password3','Chicago','789 Oak Ave'),(264,'Emily Brown','4567890123','password4','Houston','321 Pine St'),(265,'William Taylor','5678901234','password5','Philadelphia','987 Maple Rd'),(266,'Sophia Wilson','6789012345','password6','Phoenix','654 Cedar Dr'),(267,'James Anderson','7890123456','password7','San Antonio','789 Walnut Ln'),(268,'Olivia Thomas','8901234567','password8','San Diego','321 Spruce Ave'),(269,'Benjamin Martinez','9012345678','password9','Dallas','987 Birch St'),(270,'Emma Robinson','0123456789','password10','San Jose','654 Oak Ave'),(271,'Daniel Clark','1234509876','password11','Austin','789 Elm St'),(272,'Ava Rodriguez','2345610987','password12','Jacksonville','123 Cedar Dr'),(273,'Alexander Lewis','3456721098','password13','San Francisco','456 Pine St'),(274,'Mia Lee','4567832109','password14','Indianapolis','789 Walnut Ln'),(275,'Jacob Walker','5678943210','password15','Columbus','321 Spruce Ave'),(276,'Isabella Hall','6789054321','password16','Fort Worth','987 Birch St'),(277,'Ethan Green','7890165432','password17','Charlotte','654 Oak Ave'),(278,'Charlotte Young','8901276543','password18','Seattle','789 Elm St'),(279,'Sebastian Hernandez','9012387654','password19','Denver','123 Cedar Dr'),(280,'Harper King','0123498765','password20','Washington','456 Pine St');
/*!40000 ALTER TABLE `customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `delivery_guy`
--

DROP TABLE IF EXISTS `delivery_guy`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `delivery_guy` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `phno` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `delivery_guy`
--

LOCK TABLES `delivery_guy` WRITE;
/*!40000 ALTER TABLE `delivery_guy` DISABLE KEYS */;
INSERT INTO `delivery_guy` VALUES (12,'patil','delivery_guy','8867066062');
/*!40000 ALTER TABLE `delivery_guy` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `feedback`
--

DROP TABLE IF EXISTS `feedback`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `feedback` (
  `f_id` int NOT NULL AUTO_INCREMENT,
  `f_content` varchar(500) DEFAULT NULL,
  `f_p_rating` int DEFAULT NULL,
  `p_id` int NOT NULL,
  `c_id` int NOT NULL,
  PRIMARY KEY (`f_id`),
  KEY `p_id` (`p_id`),
  KEY `c_id` (`c_id`),
  CONSTRAINT `feedback_ibfk_1` FOREIGN KEY (`p_id`) REFERENCES `product` (`p_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `feedback_ibfk_2` FOREIGN KEY (`c_id`) REFERENCES `customer` (`c_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feedback`
--

LOCK TABLES `feedback` WRITE;
/*!40000 ALTER TABLE `feedback` DISABLE KEYS */;
INSERT INTO `feedback` VALUES (3,'The apple juice was not refreshing.',3,138,12),(4,'The mango squash was not delicious.',1,186,261),(5,'The grape squash had a rich flavor.',4,276,262),(6,'The aamras was delicious but not that much',3,391,263),(7,'The lemon squash had a bad taste.',2,574,264),(8,'The orange squash was not at all refreshing.',1,683,265),(9,'The apple juice had a natural flavor.',4,138,266),(10,'The mango squash was delicious!',5,186,267),(11,'The grape squash had a rich flavor.',4,276,268),(12,'The aamras had an authentic taste.',5,391,269),(13,'The lemon squash had a tangy taste.',4,574,270),(14,'The orange squash was refreshing.',5,683,271),(15,'The apple juice was refreshing and had a natural flavor.',5,138,272),(16,'The aamras was delicious and had an authentic taste.',5,391,273),(17,'The mango squash had a delightful flavor.',4,186,274),(18,'The lemon squash had a tangy and refreshing taste.',5,574,275),(19,'The grape squash had a rich and fruity flavor.',4,276,276),(20,'The orange squash was refreshing and had a tangy flavor.',4,683,277),(21,'The apple juice had a refreshing and natural taste.',5,138,278),(22,'The aamras had a delicious and authentic flavor.',5,391,279);
/*!40000 ALTER TABLE `feedback` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `o_id` int NOT NULL AUTO_INCREMENT,
  `o_status` varchar(50) DEFAULT NULL,
  `o_cost` double DEFAULT NULL,
  `o_date` date DEFAULT NULL,
  `o_city_name` varchar(50) DEFAULT NULL,
  `o_address` varchar(500) DEFAULT NULL,
  `o_c_id` int NOT NULL,
  PRIMARY KEY (`o_id`),
  KEY `o_c_id` (`o_c_id`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`o_c_id`) REFERENCES `customer` (`c_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=962 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO `orders` VALUES (942,'Pending',68.5,'2023-05-18','Kalaburagi','Manikeshwari Colony',12),(943,'Pending',90,'2023-05-18','New York','123 Main St',261),(944,'Pending',90,'2023-05-18','New York','123 Main St',261),(945,'Pending',90,'2023-05-18','Los Angeles','456 Elm St',262),(946,'Pending',97,'2023-05-18','Chicago','789 Oak Ave',263),(947,'Pending',48.5,'2023-05-18','Houston','321 Pine St',264),(948,'Pending',40,'2023-05-18','Philadelphia','987 Maple Rd',265),(949,'Pending',40,'2023-05-18','Phoenix','654 Cedar Dr',266),(950,'Pending',45,'2023-05-18','San Antonio','789 Walnut Ln',267),(951,'Pending',45,'2023-05-18','San Diego','321 Spruce Ave',268),(952,'Pending',48.5,'2023-05-18','Dallas','987 Birch St',269),(953,'Pending',48.5,'2023-05-18','San Jose','654 Oak Ave',270),(954,'Pending',40,'2023-05-18','Austin','789 Elm St',271),(955,'Pending',34,'2023-05-18','Jacksonville','123 Cedar Dr',272),(956,'Pending',48.5,'2023-05-18','San Francisco','456 Pine St',273),(957,'Completed',45,'2023-05-18','Indianapolis','789 Walnut Ln',274),(958,'Completed',48.5,'2023-05-18','Columbus','321 Spruce Ave',275),(959,'Completed',34,'2023-05-18','Seattle','789 Elm St',278),(960,'Completed',20,'2023-05-18','Charlotte','654 Oak Ave',277),(961,'Completed',48.5,'2023-05-18','Denver','123 Cedar Dr',279);
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders_detail`
--

DROP TABLE IF EXISTS `orders_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders_detail` (
  `o_id` int NOT NULL,
  `p_id` int NOT NULL,
  `quantity` int DEFAULT NULL,
  KEY `o_id` (`o_id`),
  KEY `p_id` (`p_id`),
  CONSTRAINT `orders_detail_ibfk_1` FOREIGN KEY (`o_id`) REFERENCES `orders` (`o_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `orders_detail_ibfk_2` FOREIGN KEY (`p_id`) REFERENCES `product` (`p_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders_detail`
--

LOCK TABLES `orders_detail` WRITE;
/*!40000 ALTER TABLE `orders_detail` DISABLE KEYS */;
INSERT INTO `orders_detail` VALUES (942,138,2),(943,186,2),(944,276,1),(945,391,2),(946,574,1),(947,683,2),(948,138,1),(949,186,1),(950,276,2),(951,391,1),(952,574,2),(953,683,1),(954,138,3),(955,391,2),(956,186,1),(957,574,1),(958,276,2),(959,683,1),(960,391,1),(961,138,2);
/*!40000 ALTER TABLE `orders_detail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product` (
  `p_id` int NOT NULL AUTO_INCREMENT,
  `p_name` varchar(50) DEFAULT NULL,
  `p_quantity` int DEFAULT NULL,
  `p_rating` double DEFAULT NULL,
  `p_description` text,
  `p_price` double DEFAULT NULL,
  PRIMARY KEY (`p_id`),
  UNIQUE KEY `p_name` (`p_name`)
) ENGINE=InnoDB AUTO_INCREMENT=831 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product`
--

LOCK TABLES `product` WRITE;
/*!40000 ALTER TABLE `product` DISABLE KEYS */;
INSERT INTO `product` VALUES (138,'paper boat apple',14,3.4,'An apple a day keeps the doctor away might just be the main mantra of the Indian parent\'s handbook, no? Which kid wasn\'t raised with sermons on how one must eat apples for health? It\'s a good thing that this biblical fruit is juicy, tasty and fulfilling or else we really have a bone to pick with our parents. Growing up we had a family joke, that no matter what time of the day you tell mom youre hungry she has a standard response, apple khaa lo. In fact, we reached a point where we would ask her just for this automated response and then giggle away to glory. In our household, apples were not just the breakfast fruit, however, because we made warm apple pies and trifle pudding with apple pieces regularly. The unsung hero of fruits, it truly was versatile and is the family\'s go-to snack option to this day!',34),(186,'kissan juicy mango squash',40,3.6,'Ripe Mangoes, handpicked from the farms of South India, are used to make our Juicy Mango Squash. You can taste the burst of juicy Mango with every sip. Enjoy the delightfully juicy Mango taste with water or soda.',45),(276,'kissan juicy grape squash',21,4.5,'Naturally ripened Blue Grapes, handpicked from the renowned vineyards of Karnataka, are used to make our luscious, Juicy Grape Squash. You can taste the fruity burst of Grape with every sip. Enjoy the delightfully rich Grape taste with water or soda.',45),(391,'paper boat aamras',20,4.3,'The one treasure that easily transforms Indian summer into the festivity that it is, is Aamras. An honest treat for an honest day\'s work. A silkesque ale cascading down your throat - Soothing, serenading and more importantly, lingering. Sometimes enveloped in rotis, sometimes guzzled with milk but the best way to go about Aamras is to have it directly as-is. The way the ancients intended. Without preservatives or artificial flavour. Without frills or hassles. Ah! One just cannot help but submit to the tasty tyranny of the one true king of the fruit realm. All hail the mango! Long live the king!',48.5),(574,'kissan juicy lemon squash',10,3.5,'Naturally ripened Lemons, handpicked from the Himalayan Foothills, are used to make our Juicy Lemon Squash. You can taste the burst of lemony flavour with every sip. Enjoy the delightfully zesty Lemon taste with water or soda.',48.5),(683,'kissan juicy orange squash',20,4.5,'Naturally ripened Oranges, handpicked from the renowned farms of Nagpur, are used to make our Juicy Orange Squash. Every sip of Kissan\'s Juicy Orange Squash is enriched with the goodness of Fruit Vitamins A, B, and C. Our Orange Squash has more fruit juice in every sip as compared to Leading Instant Drink Mix. Enjoy the deliciously refreshing Orange taste with water or soda.',20);
/*!40000 ALTER TABLE `product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_images`
--

DROP TABLE IF EXISTS `product_images`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product_images` (
  `p_id` int NOT NULL,
  `image_link` text,
  KEY `p_id` (`p_id`),
  CONSTRAINT `product_images_ibfk_1` FOREIGN KEY (`p_id`) REFERENCES `product` (`p_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_images`
--

LOCK TABLES `product_images` WRITE;
/*!40000 ALTER TABLE `product_images` DISABLE KEYS */;
INSERT INTO `product_images` VALUES (683,'./product_images/kissan_juicy_orange_squash.png'),(574,'./product_images/kissan_juicy_lemon_squash.png'),(391,'./product_images/paper_boat_aamras.png'),(138,'./product_images/paper_boat_apple.png'),(276,'./product_images/kissan_juicy_grape_squash.png'),(186,'./product_images/kissan_juicy_mango_squash.png');
/*!40000 ALTER TABLE `product_images` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-05-18  1:49:57
