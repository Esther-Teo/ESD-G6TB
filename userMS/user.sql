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
-- Database: user
--
DROP DATABASE IF EXISTS user;
CREATE DATABASE IF NOT EXISTS user DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE user;

-- --------------------------------------------------------

--
-- 
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

--
-- 
--

INSERT INTO users (userID, userName, userEmail, passw, userPhone, loc) VALUES
(1, 'Michael Scarn', 'mikescarn@gmail.com', "helps",'12354678', 'Jurong East'),
(2, 'Dwight Snoot', 'dwightsnoot@gmail.com', "gg", '96857412', 'Yishun'),
(3, 'Nard Dog', 'andybernard@gmail.com',"helps", '21325465', 'Sengkang'),
(4, 'Mary Juana', 'maryjuana@gmail.com', "helps",'78459865', 'Tampines'),
(5, 'Jimothy Halpert', 'jimhalpert@gmail.com',"helps", '01472558', 'Woodlands');
COMMIT;

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



-- Dumping data for table child
--



INSERT INTO child (userID, childName, school, pri, lvl) VALUES
('1', 'meep', 'Raffles Primary School', True, '4'),
('1', 'zaikia', 'Nanyang Girls High School', False, '2'),
('2', 'oof','Dunman High School ', False, '3'),
('2', 'lostcause','Rosyth School', True, '3'),
('3', 'helpsLah','Clementi Primary School', True, '2'),
('4', 'prettyBaby','Yishun Primary School', True, '5'),
('5', 'yourmom','Anderson Secondary School', False, '2');
COMMIT;




/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;