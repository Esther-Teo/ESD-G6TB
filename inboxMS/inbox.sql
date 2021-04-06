-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Jan 14, 2019 at 06:42 AM
-- Server version: 5.7.19
-- PHP Version: 7.1.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `book`
--
DROP DATABASE IF EXISTS `inbox`;
CREATE DATABASE IF NOT EXISTS `inbox` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `inbox`;

-- --------------------------------------------------------

--
-- Table structure for table `assignment`
--

DROP TABLE IF EXISTS `rejectedOffer`;
CREATE TABLE IF NOT EXISTS `rejectedOffer` (
  `assignmentId` int NOT NULL,
  `userID` int NOT NULL,
  `tutorID` int NOT NULL,
  `status` varchar(10) NOT NULL,
  `selectedTime` int NOT NULL,
  `expectedPrice` decimal(5,2) NOT NULL,
  `preferredDay` varchar(3) NOT NULL,
  `read` boolean NOT NULL, 
  
  PRIMARY KEY (`assignmentId`, `tutorID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Table structure for table `payment sent`
--



--
-- Dumping data for table `rejectedOffer`
--

INSERT INTO `rejectedOffer` (`assignmentId`, `userID`, `tutorID`, `status`, `selectedTime`,`expectedPrice`, `preferredDay`, `read`) VALUES
(1,2, 1, "rejected",1200, 2.5, "Fri", FALSE),
(7,2, 1, "rejected", 1300, 66, "Sun", FALSE),
(2,4, 1, "rejected",1230, 4, "Sat", FALSE),
(3,6, 1, "rejected", 1400, 3, "Sun", FALSE),
(4,8, 4, "rejected", 1500, 6, "Mon", FALSE),
(5,7, 5, "rejected", 0900, 3.7, "Thu", FALSE),
(6,9, 1, "rejected", 2100, 2, "Wed", FALSE);
COMMIT;

--
-- Dumping data for table `offer`
--



/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;


