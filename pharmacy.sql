-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema pharmacy
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema pharmacy
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `pharmacy` DEFAULT CHARACTER SET utf8 ;
USE `pharmacy` ;

-- -----------------------------------------------------
-- Table `pharmacy`.`Admin`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pharmacy`.`Admin` (
  `idAdmin` INT NOT NULL,
  `username` VARCHAR(45) NOT NULL,
  `email` VARCHAR(60) NOT NULL,
  `password` VARCHAR(500) NOT NULL,
  `active` TINYINT(1),
  PRIMARY KEY (`idAdmin`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pharmacy`.`Pharmacy`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pharmacy`.`Pharmacy` (
  `idPharmacy` INT NOT NULL,
  `name` VARCHAR(100) NOT NULL,
  `phone` VARCHAR(20) NOT NULL,
  `address` VARCHAR(200) NOT NULL,
  `Admin_idAdmin` INT NOT NULL,
  PRIMARY KEY (`idPharmacy`, `Admin_idAdmin`),
  INDEX `fk_Pharmacy_Admin1_idx` (`Admin_idAdmin` ASC) VISIBLE,
  CONSTRAINT `fk_Pharmacy_Admin1`
    FOREIGN KEY (`Admin_idAdmin`)
    REFERENCES `pharmacy`.`Admin` (`idAdmin`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pharmacy`.`Medicament`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pharmacy`.`Medicament` (
  `idMedicament` INT NOT NULL,
  `medicamentName` VARCHAR(200) NOT NULL,
  `manufacturer` VARCHAR(200) NOT NULL,
  `stockQuantity` INT(6) NOT NULL,
  `expiryDate` DATE NOT NULL,
  `price` DECIMAL(5,2) NOT NULL,
  `description` VARCHAR(500) NULL,
  `Pharmacy_idPharmacy` INT NOT NULL,
  `Pharmacy_Admin_idAdmin` INT NOT NULL,
  PRIMARY KEY (`idMedicament`, `Pharmacy_idPharmacy`, `Pharmacy_Admin_idAdmin`),
  INDEX `fk_Medicament_Pharmacy1_idx` (`Pharmacy_idPharmacy` ASC, `Pharmacy_Admin_idAdmin` ASC) VISIBLE,
  CONSTRAINT `fk_Medicament_Pharmacy1`
    FOREIGN KEY (`Pharmacy_idPharmacy` , `Pharmacy_Admin_idAdmin`)
    REFERENCES `pharmacy`.`Pharmacy` (`idPharmacy` , `Admin_idAdmin`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pharmacy`.`Costumer`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pharmacy`.`Costumer` (
  `username` VARCHAR(45) NOT NULL,
  `email` VARCHAR(200) NOT NULL,
  `name` VARCHAR(60) NOT NULL,
  `lastname` VARCHAR(60) NOT NULL,
  `password` VARCHAR(500) NOT NULL,
  `phoneNumber` VARCHAR(20) NOT NULL,
  `address` VARCHAR(60) NOT NULL,
  `active` TINYINT(1),
  PRIMARY KEY (`username`, `email`))
ENGINE = InnoDB;

INSERT INTO pharmacy.admin VALUES(123, 'admin1', 'admin1@gmail.com', '123456789', 0),
								 (124, 'admin2', 'admin2@gmail.com', '123456789', 0),
                                 (125, 'admin3', 'admin3@gmail.com', '123456789', 0);
                                 
INSERT INTO pharmacy.pharmacy VALUES(123456, 'Apoteka1', '066445564','Majke Jugovica 1', 123),
									(127545, 'Apoteka2', '066871266','Marije Bursac 4', 124),
                                    (457512, 'Apoteka3', '066566177','Srpska 5', 125);
                                    
INSERT INTO pharmacy.medicament VALUES(1116, 'Aspirin', 'Galenika', 20, '2025-7-04', 5.5, 'Protiv bolova', 123456, 123 ),
										(1174, 'Paracetamol', 'Bosna Lijek', 50, '2025-7-04', 3.5, 'Protiv bolova', 123456, 123 ),
                                        (11187, 'Lavrena', 'Galenika', 40, '2025-7-04', 6.5, 'Protiv alergije', 123456, 123 )


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
