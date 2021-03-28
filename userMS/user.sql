<<<<<<< Updated upstream
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

DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `userID` BIGINT NOT NULL AUTO_INCREMENT,
  `userName` VARCHAR(100) NOT NULL,
  `userEmail` VARCHAR(100) NOT NULL,
  `password` VARCHAR(20) NOT NULL,
  `userPhone` INT NOT NULL,
  `location` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`userID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 
--

INSERT INTO `users` ( `userName`, `userEmail`, `password`, `userPhone`, `location`) VALUES
( 'Michael Scarn', 'mikescarn@gmail.com', "helps",'12354678', 'Jurong East'),
('Dwight Snoot', 'dwightsnoot@gmail.com', "gg", '96857412', 'Yishun'),
('Nard Dog', 'andybernard@gmail.com',"helps", '21325465', 'Sengkang'),
('Mary Juana', 'maryjuana@gmail.com', "helps",'78459865', 'Tampines'),
('Jimothy Halpert', 'jimhalpert@gmail.com',"helps", '01472558', 'Woodlands');
COMMIT;

DROP TABLE IF EXISTS `child`;
CREATE TABLE IF NOT EXISTS `child` (
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

INSERT INTO `child` (`userID`, `childID`, `school`, `primary`,`secondary`, `level`) VALUES
('0001', '1', 'Raffles Primary School', True, False, '4'),
('0001', '2', 'Nanyang Girls High School', False, True, '2'),
('0002', '1', 'Dunman High School ', False, True, '3'),
('0002', '2', 'Rosyth School', True, False, '3'),
('0003', '1', 'Clementi Primary School', True, False, '2'),
('0004', '1', 'Yishun Primary School', True, False, '5'),
('0005', '1', 'Anderson Secondary School', False, True, '2');
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
COMMIT;



/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
=======
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
  pass VARCHAR(20) NOT NULL,
  userPhone INT NOT NULL,
  loc VARCHAR(1000) NOT NULL,
  PRIMARY KEY (userID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 
--

INSERT INTO users (userName, userEmail, pass, userPhone, loc) VALUES
( 'Michael Scarn', 'mikescarn@gmail.com', "helps",'12354678', 'Jurong East'),
('Dwight Snoot', 'dwightsnoot@gmail.com', "gg", '96857412', 'Yishun'),
('Nard Dog', 'andybernard@gmail.com',"helps", '21325465', 'Sengkang'),
('Mary Juana', 'maryjuana@gmail.com', "helps",'78459865', 'Tampines'),
('Jimothy Halpert', 'jimhalpert@gmail.com',"helps", '01472558', 'Woodlands');
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


-- create a table for child's subjects 
DROP TABLE IF EXISTS childSubjects;
CREATE TABLE IF NOT EXISTS childSubjects (
  userID BIGINT NOT NULL,
  childName VARCHAR(20) NOT NULL,
  subjects VARCHAR(100) NOT NULL,
  PRIMARY KEY (userID, childName, subjects),
  CONSTRAINT FK_userID2 FOREIGN KEY (userID, childName)
    REFERENCES child(userID, childName)
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


INSERT INTO childSubjects (userID, childName, subjects) VALUES
('1', 'meep', 'Mathematics'),
('1', 'meep', 'English'),
('1', 'zaikia', 'Additional Mathematics'),
('1', 'zaikia',  'History'),
('2', 'oof','Chemistry'),
('2', 'lostcause', 'Chinese'),
('3', 'helpsLah', 'Science'),
('3', 'helpsLah',  'Mathematics'),
('3', 'helpsLah', 'English'),
('4', 'prettyBaby', 'Tamil'),
('4', 'prettyBaby', 'Science'),
('5', 'yourmom', 'Physics');
COMMIT;



/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
>>>>>>> Stashed changes
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;