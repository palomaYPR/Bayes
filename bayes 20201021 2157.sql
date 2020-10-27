-- MySQL Administrator dump 1.4
--
-- ------------------------------------------------------
-- Server version	5.1.45-community


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


--
-- Create schema bayes
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ bayes;
USE bayes;

--
-- Table structure for table `bayes`.`prueba3`
--

DROP TABLE IF EXISTS `prueba3`;
CREATE TABLE `prueba3` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `edad` varchar(45) DEFAULT '',
  `hijos` varchar(45) DEFAULT '',
  `deporte` varchar(45) DEFAULT '',
  `salario` varchar(45) DEFAULT '',
  `buencliente` varchar(45) DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `bayes`.`prueba3`
--

/*!40000 ALTER TABLE `prueba3` DISABLE KEYS */;
INSERT INTO `prueba3` (`id`,`edad`,`hijos`,`deporte`,`salario`,`buencliente`) VALUES 
 (1,'joven','si','no','alto','si'),
 (2,'joven','no','no','medio','no'),
 (3,'joven','si','si','medio','no'),
 (4,'joven','si','no','bajo','si'),
 (5,'mayor','si','no','bajo','si'),
 (6,'mayor','no','si','medio','si'),
 (7,'joven','no','si','medio','si'),
 (8,'joven','si','si','alto','si'),
 (9,'mayor','si','no','medio','si'),
 (10,'mayor','no','no','bajo','no'),
 (11,'joven','si','no','medio','si'),
 (12,'mayor','no','si','alto','no'),
 (13,'mayor','si','no','alto','no');
/*!40000 ALTER TABLE `prueba3` ENABLE KEYS */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
