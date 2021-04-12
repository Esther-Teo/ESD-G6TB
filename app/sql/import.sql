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
  `tutorEmail` VARCHAR(40) NOT NULL,
  `status` VARCHAR(20) NOT NULL,
  `selectedTime` VARCHAR(20) NOT NULL,
  `expectedPrice` decimal(5,2) NOT NULL,
  `preferredDay` varchar(3) NOT NULL,
  PRIMARY KEY (`assignmentId`, `tutorID`),
  CONSTRAINT FK_assignmentId FOREIGN KEY (`assignmentId`)
  REFERENCES assignment(`assignmentId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Database: user
--
DROP DATABASE IF EXISTS user;
CREATE DATABASE IF NOT EXISTS user DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE user;

-- --------------------------------------------------------

--
-- create table for user
--

DROP TABLE IF EXISTS users;
CREATE TABLE IF NOT EXISTS users (
  userID BIGINT NOT NULL AUTO_INCREMENT,
  userName VARCHAR(100) NOT NULL,
  userEmail VARCHAR(100) NOT NULL,
  passw VARCHAR(20) NOT NULL,
  userPhone INT NOT NULL,
  loc VARCHAR(1000) NOT NULL,
  PRIMARY KEY (userID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



-- create a new table for child
DROP TABLE IF EXISTS child;
CREATE TABLE IF NOT EXISTS child (
  userID BIGINT NOT NULL,
  childName VARCHAR(20) NOT NULL,
  school VARCHAR(100) NOT NULL,
  pri BOOLEAN NOT NULL,
  lvl INT NOT NULL,
  PRIMARY KEY (userID, childName),
  CONSTRAINT FK_userID FOREIGN KEY (userID)
    REFERENCES users(userID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Dumping data for table user
--

INSERT INTO users (userID, userName, userEmail, passw, userPhone, loc) VALUES
(1, 'Michael Scarn', 'mikeyscarn69@gmail.com', "helps",'12354678', 'Jurong East'),
(2, 'Dwight Snoot', 'dwightsnoot@gmail.com', "gg", '96857412', 'Yishun');
COMMIT;

--
-- Dumping data for table child
--

INSERT INTO child (userID, childName, school, pri, lvl) VALUES
('1', 'meep', 'Raffles Primary School', True, '4'),
('1', 'zaikia', 'Nanyang Girls High School', False, '2'),
('2', 'blingbling','Dunman High School ', False, '3'),
('2', 'sosmart','Rosyth School', True, '3');

COMMIT;


--
-- Database: tutor
--
DROP DATABASE IF EXISTS tutor;
CREATE DATABASE IF NOT EXISTS tutor DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE tutor;

-- --------------------------------------------------------

--
-- Table structure for table tutors
--

DROP TABLE IF EXISTS tutor;
CREATE TABLE IF NOT EXISTS tutor (
    tutorID BIGINT NOT NULL AUTO_INCREMENT,
    tutorName varchar(100) NOT NULL,
    tutorEmail varchar(100) NOT NULL,
    passw varchar(100) NOT NULL,
    tutorPhone INT NOT NULL,
    loc varchar(1000) NOT NULL,
    portfolio varchar(1000) NOT NULL,
    priceRange INT NOT NULL,
    stripeID varchar(100) NOT NULL,
    PRIMARY KEY (tutorID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table tutor
--

INSERT INTO tutor (tutorId, tutorName, tutorEmail, passw, tutorPhone, loc, portfolio, priceRange, stripeID) VALUES
(1, 'Bob','bcoskitt@gmail.com', '123', 9001889,'Fort Canning','Taught Sec 3 students for 1 month',100, "acct_1Ic8ngAiyPfscIUT"),
(2, 'Tom','esd69hrsaweek@gmail.com','123', 999,'Dover','Taught Pri 1 students for 1 month', 160, "acct_1Ic8ngAiyPfscIUT"),
(6, 'Hao','soonhao.er@smu.edu.sg','123', 12311,'Bukit Panjang','Best Mentor ', 130 , "acct_1Ic8ngAiyPfscIUT");
COMMIT;

--
-- Database: `inbox`
--
DROP DATABASE IF EXISTS `inbox`;
CREATE DATABASE IF NOT EXISTS `inbox` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `inbox`;

-- --------------------------------------------------------

--
-- Table structure for table `returnedOffer`
--

DROP TABLE IF EXISTS `returnedOffer`;
CREATE TABLE IF NOT EXISTS `returnedOffer` (
  `assignmentId` int NOT NULL,
  `userID` int NOT NULL,
  `tutorID` int NOT NULL,
  `status` varchar(10) NOT NULL,
  `selectedTime` varchar(20) NOT NULL,
  `expectedPrice` decimal(5,2) NOT NULL,
  `preferredDay` varchar(3) NOT NULL,
  `read` boolean NOT NULL, 
  
  PRIMARY KEY (`assignmentId`, `tutorID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Table structure for table `createdOffer`
--
DROP TABLE IF EXISTS `createdOffer`;
CREATE TABLE IF NOT EXISTS `createdOffer` (
  `assignmentId` int NOT NULL,
  `userID` int NOT NULL,
  `tutorID` int NOT NULL,
  `status` varchar(10) NOT NULL,
  `selectedTime` varchar(20) NOT NULL,
  `expectedPrice` decimal(5,2) NOT NULL,
  `preferredDay` varchar(3) NOT NULL,
  `read` boolean NOT NULL, 
  
  PRIMARY KEY (`assignmentId`, `tutorID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;