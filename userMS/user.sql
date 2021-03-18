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
CREATE DATABASE IF NOT EXISTS `user` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `user`;

-- --------------------------------------------------------

--
-- Table structure for table `offers`
--

DROP TABLE IF EXISTS `User`;
CREATE TABLE IF NOT EXISTS `User` (
  `UserID` INT NOT NULL,
  `UserName` VARCHAR(100) NOT NULL,
  `UserPhone` INT NOT NULL,
  `Location` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`UserID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `book`
--

INSERT INTO `user` (`UserID`, `UserName`, `UserPhone`, `Location`) VALUES
('0001', 'Michael Scarn', '12354678', 'Jurong East'),
('0002', 'Dwight Snoot', '96857412', 'Yishun'),
('0003', 'Nard Dog', '21325465', 'Sengkang'),
('0004', 'Mary Juana', '78459865', 'Tampines'),
('0005', 'Jimothy Halpert', '01472558', 'Woodlands');
COMMIT;

DROP TABLE IF EXISTS `Child`;
CREATE TABLE IF NOT EXISTS `Child` (
  `UserID` INT NOT NULL,
  `ChildID` INT NOT NULL,
  `School` VARCHAR(100) NOT NULL,
  `Level` VARCHAR(100) NOT NULL,
  `Subjects` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`UserID`, `ChildID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `child`
--

INSERT INTO `user` (`UserID`, `ChildID`, `School`, `Level`, `Subjects`) VALUES
('0001', '1' 'Raffles Primary School', '4', 'Mathematics'),
('0001', '2', 'Nanyang Girls High School', '8', 'Additional Mathematics'),
('0002', '1', 'Dunman High School ', '9', 'Chemistry'),
('0002', '2', 'Rosyth School', '3', 'Chinese'),
('0003', '1', 'Clementi Primary School', '2', 'Science'),
('0004', '1', 'Yishun Primary School', '5', 'Tamil'),
('0005', '1', 'Anderson Secondary School', '8', 'Physics');
COMMIT;


/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;