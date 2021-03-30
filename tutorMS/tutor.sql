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
-- Database: `tutor`
--
CREATE DATABASE IF NOT EXISTS `tutor` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `tutor`;

-- --------------------------------------------------------

--
-- Table structure for table `tutors`
--

DROP TABLE IF EXISTS `tutor`;
CREATE TABLE IF NOT EXISTS `tutor` (
    `tutorID` char(120) NOT NULL,
    `tutorName` varchar(64) NOT NULL,
    `tutorPhone` int(8) NOT NULL,
    `location` varchar(1000) NOT NULL,
    `portfolio` varchar(1000) NOT NULL,
    `teachesPri` tinyint(1) NOT NULL,
    `teachesSec` tinyint(1) NOT NULL,
    `subjects` varchar(1000) NOT NULL,
    `priceRange` int(5) NOT NULL,
    PRIMARY KEY (`tutorID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `tutor`
--

INSERT INTO `tutor` (`tutorID`, `tutorName`, `tutorPhone`, `location`, `portfolio`,`teachesPri`,`teachesSec`, `subjects`, `priceRange`) VALUES
('Bob@gmail.com','Bob', 9001889,'Fort Canning','Taught Sec 3 students for 1 month','1','0', 'English, Math', 100),
('Tom@hotmail.com','Tom', 999,'Dover','Taught Pri 1 students for 1 month','0','1', 'Mother Tongue, Math ', 160),
('SueSUE@gmail.com','Sue', 112,'Marymount','Taught Sec 4 students for 1 month', '1','0','Science, Math ', 105),
('MaryTan@gmail.com','Mary', 123,'Pasir Ris','None', '0','1','English, Math, Social Studies ', 125),
('Janice@gmail.com','Jane', 12311,'River Valley','Mentored before','0','1', 'English, Science ', 130);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;