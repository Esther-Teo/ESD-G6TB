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
DROP DATABASE IF EXISTS `assignment`;
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
  `primary` boolean NOT NULL,
  `level` int NOT NULL,
  `subject` varchar(30) NOT NULL,
  `expectedPrice` decimal(5,2) NOT NULL,
  `preferredDay` varchar(90) NOT NULL,
  `tutorID` int default 0,
  PRIMARY KEY (`assignmentId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Table structure for table `offer`
--

DROP TABLE IF EXISTS `offer`;
CREATE TABLE IF NOT EXISTS `offer` (
  `assignmentId` INT NOT NULL,
  `userID` INT NOT NULL,
  `tutorID` INT NOT NULL,
  `tutorName` VARCHAR(40) NOT NULL,
  `status` VARCHAR(20) NOT NULL,
  `selectedTime` INT NOT NULL,
  `expectedPrice` decimal(5,2) NOT NULL,
  `preferredDay` varchar(3) NOT NULL,
  PRIMARY KEY (`assignmentId`, `tutorID`),
  CONSTRAINT FK_assignementId FOREIGN KEY (`assignmentId`)
  REFERENCES assignment(`assignmentId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `assignment`
--

INSERT INTO `assignment` (`assignmentId`, `userID`, `childName`, `primary`, `level`, `subject`, `expectedPrice`, `preferredDay`) VALUES
(1, 1, "meep",1, 2, 'Math', '6.50', "friday"),
(7, 1, "zaikia", 0, 2, 'A_Math', '6.50', "friday"),
(2, 2, "oof",1, 4, 'Math', '6.50', "tuesday"),
(3, 2, "lostcause", 0, 3, 'Math', '6.50', "Sunday"),
(4, 4, "prettyBaby", 1, 6, 'Eng', '6.50', "Someday"),
(5, 5, "yourmom", 0, 3, 'Physics', '6.50', "Monday"),
(6, 1, "meep", 1, 2, 'Chinese', '6.50', "Friday");
COMMIT;

--
-- Dumping data for table `offer`
--

INSERT INTO `offer` (`assignmentId`, `userID`, `tutorID`, `tutorName`, `status`, `selectedTime`, `expectedPrice`, `preferredDay`) VALUES
(1, 1, 1, "Bob", 'pending', 1500, 7, "Fri"),
(1, 1, 2, "Tom", 'pending', 1200, 7, "Mon"),
(1, 1, 4, "Mary", 'pending', 1900, 7, "Wed"),
(1, 1, 5, "Jane", 'accepted', 1900, 7, "Wed"),
(7, 1, 3, "Sue", 'accepted', 0800, 7, "Fri"),
(7, 1, 4, "Mary", 'pending', 1900, 7, "Wed"),
(2, 2, 2, "Tom", 'accepted', 0900, 6.5, "Sun"),
(1, 1, 3, "Sue", 'rejected', 2000, 6.5, "Sat"),
(3, 2, 4, "Mary", 'pending', 1900, 7, "Mon"),
(2, 2, 5, "Jane", 'rejected', 1500, 8, "Tue");
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;


