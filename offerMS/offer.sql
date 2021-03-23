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
-- Database: `offer`
--
CREATE DATABASE IF NOT EXISTS `offer` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `offer`;

-- --------------------------------------------------------

--
-- Table structure for table `offers`
--

DROP TABLE IF EXISTS `offer`;
CREATE TABLE IF NOT EXISTS `offer` (
  `assignmentId` INT NOT NULL,
  `tutorId` INT NOT NULL,
  `status` VARCHAR(6) NOT NULL,
  `selectedTime` INT NOT NULL,
  `expectedPrice` INT NOT NULL,
  `preferredDay` VARCHAR(3) NOT NULL,
  PRIMARY KEY (`assignmentid`, `tutorId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `book`
--

INSERT INTO `offer` (`assignmentId`, `tutorId`, `status`, `selectedTime`, `expectedPrice`, `preferredDay`) VALUES
('1000', '1000', 'open', '1500', '30', 'sun'),
('2000', '2000', 'closed', '0900', '50', 'sat'),
('3000', '3000', 'closed', '2000', '35', 'fri'),
('4000', '4000', 'open', '1900', '20', 'wed'),
('5000', '5000', 'closed', '1500', '25', 'tue');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

