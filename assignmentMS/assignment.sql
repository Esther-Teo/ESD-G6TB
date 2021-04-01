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
CREATE DATABASE IF NOT EXISTS `assignment` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `assignment`;

-- --------------------------------------------------------

--
-- Table structure for table `assignment`
--

DROP TABLE IF EXISTS `assignment`;
CREATE TABLE IF NOT EXISTS `assignment` (
  `assignmentId` int NOT NULL,
  `userID` int NOT NULL,
  `childName` varchar(64) NOT NULL,
  `subject` varchar(30) NOT NULL,
  `expectedPrice` decimal(5,2) NOT NULL,
  `preferredDay` int NOT NULL,
  `tutorId` int default 0,
  PRIMARY KEY (`assignmentId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `book`
--

INSERT INTO `assignment` (`assignmentId`, `userID`, `childName`, `subject`, `expectedPrice`, `preferredDay`) VALUES
(1, 1, "meep", 'Pri_Math', '6.50', 3),
(2, 2, "oof", 'Pri_Math', '6.50', 2),
(3, 2, "lostcause", 'Sec_Math', '6.50', 3),
(4, 4, "prettyBaby", 'Pri_Eng', '6.50', 1),
(5, 5, "yourmom", 'Sec_Physics', '6.50', 2),
(6, 1, "meep", 'Pri_Math', '6.50', 5);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;


