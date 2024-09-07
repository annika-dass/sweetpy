CREATE DATABASE IF NOT EXISTS `rcialogin` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `rcialogin`;

drop table `accounts`;

CREATE TABLE IF NOT EXISTS `accounts` (
	`id` integer NOT NULL AUTO_INCREMENT,
  	`username` varchar(50) NOT NULL,
  	`password` varchar(255) NOT NULL,
  	`email` varchar(100) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

drop table `enroll`;

CREATE TABLE IF NOT EXISTS `enroll` (
	`id` integer NOT NULL,
  	`firstname` varchar(50) NOT NULL,
    `lastname` varchar(50) NOT NULL,
  	`birthdate` datetime NOT NULL,
  	`maritalstatus` varchar(50) NOT NULL,
    `mothername` varchar(50) NOT NULL,
    `motherreligion` varchar(50) NOT NULL,
    `fathername` varchar(50) NOT NULL,
    `fatherreligion` varchar(50) NOT NULL,
    `religiousbg` varchar(500) NOT NULL,    
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

INSERT INTO `accounts` (`id`, `username`, `password`, `email`) VALUES (1, 'test', '0ef15de6149819f2d10fc25b8c994b574245f193', 'test@test.com');