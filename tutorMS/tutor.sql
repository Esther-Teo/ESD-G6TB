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
    pass varchar(100) NOT NULL,
    tutorPhone INT NOT NULL,
    loc varchar(1000) NOT NULL,
    portfolio varchar(1000) NOT NULL,
    priceRange INT NOT NULL,
    PRIMARY KEY (tutorID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS tutorSubjects;
CREATE TABLE IF NOT EXISTS tutorSubjects (
  tutorID BIGINT NOT NULL,
  pri BOOLEAN NOT NULL,
  lvl VARCHAR(100) NOT NULL,
  subjects VARCHAR(100) NOT NULL,
  PRIMARY KEY (tutorID, pri ,subjects),
  CONSTRAINT FK_tutorID FOREIGN KEY (tutorID)
    REFERENCES tutor(tutorID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table tutor
--

INSERT INTO tutor (tutorName, tutorEmail, pass, tutorPhone, loc, portfolio, priceRange) VALUES
('Bob','bob@gmail.com', '123', 9001889,'Fort Canning','Taught Sec 3 students for 1 month',100),
('Tom','tom@hotmail.com','123', 999,'Dover','Taught Pri 1 students for 1 month', 160),
('Sue','suesue@gmail.com', '123',112,'Marymount','Taught Sec 4 students for 1 month', 105),
('Mary','MaryTan@gmail.com','123', 123,'Pasir Ris','', 125),
('Jane','Janice@gmail.com','123', 12311,'River Valley','Mentored before', 130);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;