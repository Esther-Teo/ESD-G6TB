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
-- Database: `user`
--
CREATE DATABASE IF NOT EXISTS `user` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `user`;

-- --------------------------------------------------------

--
-- 
--

DROP TABLE IF EXISTS `Users`;
CREATE TABLE IF NOT EXISTS `Users` (
  `userID` INT NOT NULL,
  `userName` VARCHAR(100) NOT NULL,
  `userPhone` INT NOT NULL,
  `location` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`UserID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 
--

INSERT INTO `Users` (`userID`, `userName`, `userPhone`, `location`) VALUES
('0001', 'Michael Scarn', '12354678', 'Jurong East'),
('0002', 'Dwight Snoot', '96857412', 'Yishun'),
('0003', 'Nard Dog', '21325465', 'Sengkang'),
('0004', 'Mary Juana', '78459865', 'Tampines'),
('0005', 'Jimothy Halpert', '01472558', 'Woodlands');
COMMIT;

DROP TABLE IF EXISTS `Child`;
CREATE TABLE IF NOT EXISTS `Child` (
  `userID` INT NOT NULL,
  `childID` INT NOT NULL,
  `school` VARCHAR(100) NOT NULL,
  `primary` BOOLEAN NOT NULL,
  `secondary` BOOLEAN NOT NULL,
  `level` INT NOT NULL,
  PRIMARY KEY (`userID`, `childID`)

) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- Dumping data for table `child`
--

-- create a new table for child and subjects 

INSERT INTO `Child` (`userID`, `childID`, `school`, `primary`,`secondary`, `level`) VALUES
<<<<<<< Updated upstream
('0001', '1', 'Raffles Primary School', True, False, '4'),
('0001', '2', 'Nanyang Girls High School', False, True, '2'),
('0002', '1', 'Dunman High School ', False, True, '3'),
('0002', '2', 'Rosyth School', True, False, '3'),
('0003', '1', 'Clementi Primary School', True, False, '2'),
('0004', '1', 'Yishun Primary School', True, False, '5'),
('0005', '1', 'Anderson Secondary School', False, True, '2');
=======
('0001', '1' 'Raffles Primary School', 'True', 'False', '4');
('0001', '2', 'Nanyang Girls High School', 'False', 'True', '2'),
('0002', '1', 'Dunman High School ', 'False', 'True', '3'),
('0002', '2', 'Rosyth School', 'True', 'False', '3'),
('0003', '1', 'Clementi Primary School', 'True', 'False', '2'),
('0004', '1', 'Yishun Primary School', 'True', 'False', '5'),
('0005', '1', 'Anderson Secondary School', 'False', 'True', '2');
>>>>>>> Stashed changes
COMMIT;

-- create a table for child's subjects 
DROP TABLE IF EXISTS `childSubjects`;
CREATE TABLE IF NOT EXISTS `childSubjects` (
  `userID` INT NOT NULL,
  `childID` INT NOT NULL,
  `primary` BOOLEAN NOT NULL,
  `secondary` BOOLEAN NOT NULL,
  `level` VARCHAR(100) NOT NULL,
  `subjects` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`userID`, `childID`, `subjects`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

<<<<<<< Updated upstream
INSERT INTO `childSubjects` (`userID`, `childID`, `primary`,`secondary`, `level`, `subjects`) VALUES
('0001', '1', True, False, '4', 'Mathematics'),
('0001', '1', True, False, '4', 'English'),
('0001', '2', False, True, '2', 'Additional Mathematics'),
('0001', '2', False, True,  '2', 'History'),
('0002', '1', False, True, '3', 'Chemistry'),
('0002', '2', True, False, '3', 'Chinese'),
('0003', '1', True, False, '2', 'Science'),
('0003', '1', True, False, '2', 'Mathematics'),
('0003', '1', True, False, '2', 'English'),
('0004', '1', True, False, '5', 'Tamil'),
('0004', '1', True, False, '5', 'Science'),
('0005', '1', False, True,  '2', 'Physics');
=======
INSERT INTO `user` (`userID`, `childID`, `primary`,`secondary`, `level`, `subjects`) VALUES
('0001', '1', 'True', 'False', '4', 'Mathematics');
('0001', '1', 'True', 'False', '4', 'English'),
('0001', '2', 'False', 'True', '2', 'Additional Mathematics'),
('0001', '2', 'False', 'True',  '2', 'History'),
('0002', '1', 'False', 'True', '3', 'Chemistry'),
('0002', '2', 'True', 'False', '3', 'Chinese'),
('0003', '1', 'True', 'False', '2', 'Science'),
('0003', '1', 'True', 'False', '2', 'Mathematics'),
('0003', '1', 'True', 'False', '2', 'English'),
('0004', '1', 'True', 'False', '5', 'Tamil'),
('0004', '1', 'True', 'False', '5', 'Science'),
('0005', '1', 'False', 'True',  '2', 'Physics');
>>>>>>> Stashed changes
COMMIT;



/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;