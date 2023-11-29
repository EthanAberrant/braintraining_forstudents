-- MySQL Script generated by MySQL Workbench
-- Thu Nov 23 08:18:35 2023
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema projet_dbpy
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema projet_dbpy
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `projet_dbpy` DEFAULT CHARACTER SET utf8 ;
USE `projet_dbpy` ;

-- -----------------------------------------------------
-- Table `projet_dbpy`.`Users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `projet_dbpy`.`Users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nickname` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX (`nickname` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `projet_dbpy`.`exercices`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `projet_dbpy`.`exercices` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `exercice_code` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX (`exercice_code` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `projet_dbpy`.`results`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `projet_dbpy`.`results` (
  `id` INT NULL DEFAULT NULL AUTO_INCREMENT,
  `hours` TIME NOT NULL,
  `date_time` DATETIME NOT NULL,
  `number_try` DECIMAL(10) NOT NULL,
  `number_ok` DECIMAL(10) NOT NULL,
  `Users_id` INT NOT NULL,
  `exercices_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX (`Users_id` ASC) VISIBLE,
  INDEX (`exercices_id` ASC) VISIBLE,
  CONSTRAINT ``
    FOREIGN KEY (`Users_id`)
    REFERENCES `projet_dbpy`.`Users` (`id`),
  CONSTRAINT ``
    FOREIGN KEY (`exercices_id`)
    REFERENCES `projet_dbpy`.`exercices` (`id`))
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
