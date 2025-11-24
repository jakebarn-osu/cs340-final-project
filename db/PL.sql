-- Citation for the following function:
-- Date: 11/19/2025
-- Copied from /OR/ Adapted from /OR/ Based on:
-- All PL code was adapted from coding examples in the exploration modules 


-- --------------------------------------
-- sp_delete_reservation
-- --------------------------------------
DROP PROCEDURE IF EXISTS sp_delete_reservation;

DELIMITER //
CREATE PROCEDURE sp_delete_reservation (IN input_reservation_id INT)
BEGIN 
  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    ROLLBACK;
    SELECT 'Error deleting reservation';
  END;

  START TRANSACTION;
  DELETE FROM Reservations WHERE id = input_reservation_id;
  COMMIT;
END //
DELIMITER ;

-- --------------------------------------
-- sp_delete_inventory_item
-- --------------------------------------
DROP PROCEDURE IF EXISTS sp_delete_inventory_item;

DELIMITER //
CREATE PROCEDURE sp_delete_inventory_item (IN i_equipment_id INT, i_store_id INT)
BEGIN 
  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    ROLLBACK;
    SELECT 'Error deleting inventory item';
  END;

  START TRANSACTION;
  DELETE FROM InventoryItems WHERE equipment_id = i_equipment_id AND store_id = i_store_id;
  COMMIT;

  SELECT 'Item deleted' AS Result;
END //
DELIMITER ;

-- --------------------------------------
-- sp_insert_inventory_item
-- --------------------------------------
DELIMITER //
DROP PROCEDURE IF EXISTS sp_insert_inventory_item;
CREATE PROCEDURE sp_insert_inventory_item (
  IN n_equipment_id INT,
  IN n_store_id INT,
  IN n_quantity INT
)
BEGIN
  INSERT INTO `InventoryItems` (equipment_id, store_id, quantity)
  VALUES (n_equipment_id, n_store_id, n_quantity);
END //
DELIMITER ;

-- --------------------------------------
-- sp_update_inventory_item
-- --------------------------------------
# Citation for the following function:
# Date: 11/23/2025
# sp_update_inventory_item code provided and altered from Microsoft Copilot
# Copilot was provided the DML code for updating quantity of InventoryItems and updating InventoryItems.equipment_id. 
# Copilot was then prompted to provide the PLSQL for the SQL code. It was also instructed that p_quantity or p_new_equip_id
# could be NULL values.
DELIMITER //
DROP PROCEDURE IF EXISTS sp_update_inventory_item;
CREATE PROCEDURE sp_update_inventory_item (
  IN p_store_id INT,
  IN p_original_equip_id INT,
  IN p_new_equip_id INT,
  IN p_quantity INT
)
BEGIN
    -- Update quantity if provided
    IF p_quantity IS NOT NULL THEN
        UPDATE InventoryItems
        SET quantity = p_quantity
        WHERE store_id = p_store_id
          AND equipment_id = p_original_equip_id;
    END IF;

    -- Update equipment_id if provided
    IF p_new_equip_id IS NOT NULL THEN
        UPDATE InventoryItems
        SET equipment_id = p_new_equip_id
        WHERE store_id = p_store_id
          AND equipment_id = p_original_equip_id;
    END IF;
END //

DELIMITER ;
-- --------------------------------------
-- sp_reset_db
-- --------------------------------------
DROP PROCEDURE IF EXISTS sp_reset_db;
DELIMITER //
CREATE PROCEDURE sp_reset_db()
BEGIN 
  SET FOREIGN_KEY_CHECKS = 0;
    DROP TABLE IF EXISTS Stores;
    DROP TABLE IF EXISTS Customers;
    DROP TABLE IF EXISTS Equipment;
    DROP TABLE IF EXISTS InventoryItems;
    DROP TABLE IF EXISTS Categories;
    DROP TABLE IF EXISTS Reservations;

  -- ------------------
  -- Table Stores
  -- ------------------

  CREATE TABLE Stores (
	id int NOT NULL AUTO_INCREMENT UNIQUE,
	address varchar(45) NOT NULL,
	city varchar(45) NOT NULL,
	zip_code varchar(45) NOT NULL,
	PRIMARY KEY (id)
  );

  INSERT INTO Stores (address, city, zip_code)
  VALUES ('123 Fake St', 'Denver', '45632'),
	('689 Bloom Ave', 'Boulder', '42346'),
	('67 Cherrywood Ln', 'Aurora', '43251'),
	('451 Gandy Blvd', 'Denver', '45321'),
	('932 Channelside Dr', 'Boulder', '41346');

  -- ------------------
  -- Table Customers
  -- ------------------

  CREATE TABLE Customers(
	id int NOT NULL AUTO_INCREMENT UNIQUE,
	first_name varchar(45) NOT NULL,
	last_name varchar(45) NOT NULL,
	phone_number varchar(45) NOT NULL,
	address varchar(45) NOT NULL,
	PRIMARY KEY (id)
  );

  INSERT INTO Customers (first_name, last_name, phone_number, address)
  VALUES ('John', 'Doe', '123-554-2457', '6421 Hollow Branch Ave'),
	('Jane', 'Doe', '320-532-2143', '1243 Wesley Dr'),
	('Mitchell', 'Ericson', '543-555-2345', '5316 Westshore St'),
	('Barnett', 'Jacobson', '643-246-2461', '2414 Bloomingdale Ave');

  -- ------------------
  -- Table Categories
  -- ------------------

  CREATE TABLE Categories (
	id int NOT NULL AUTO_INCREMENT,
	activity_type varchar(45) NOT NULL UNIQUE,
	description varchar(100) NOT NULL,
	PRIMARY KEY (id)
  );

  INSERT INTO Categories (activity_type, description)
  VALUES ('hiking', 'hiking equipment'),
	('skiing', 'skiing equipment'),
	('snowboarding', 'snowboarding equipment'),
	('protective', 'protective equipment'),
	('cycling', 'bicycle equipment');

  -- ------------------
  -- Table Equipment
  -- ------------------

  CREATE TABLE Equipment (
	id int NOT NULL AUTO_INCREMENT,
	item_name varchar(45) NOT NULL,
	category_id int,
	FOREIGN KEY (category_id) REFERENCES Categories(id)
		ON DELETE CASCADE,
	PRIMARY KEY (id)
  );

  INSERT INTO Equipment (category_id, item_name)
  VALUES ((SELECT id FROM Categories WHERE id = 3), 'snowboard'),
	((SELECT id FROM Categories WHERE id = 2), 'skiis'),
	((SELECT id from Categories WHERE id = 1), 'backpack'),
	((SELECT id FROM Categories WHERE id = 1), 'trekking pole'),
	((SELECT id FROM Categories WHERE id = 1), 'helmet'),
	((SELECT id FROM Categories WHERE id = 2), 'ski_poles'),
	((SELECT id FROM Categories WHERE id = 4), 'goggles'),
	((SELECT id FROM Categories WHERE id = 5), 'bicycle');

  -- ------------------
  -- Table InventoryItems
  -- ------------------

  CREATE TABLE InventoryItems (
	equipment_id int NOT NULL,
	store_id int NOT NULL,
	quantity int NOT NULL,
	FOREIGN KEY (equipment_id) REFERENCES Equipment(id)
		ON DELETE CASCADE,
	FOREIGN KEY (store_id) REFERENCES Stores(id)
		ON DELETE CASCADE,
	PRIMARY KEY (equipment_id, store_id)
  );

  INSERT INTO InventoryItems (equipment_id, store_id, quantity)
  VALUES ((SELECT id FROM Equipment WHERE id = 3), (SELECT Stores.id FROM Stores WHERE Stores.id = 1), 20),
	((SELECT id FROM Equipment WHERE id = 1), (SELECT id FROM Stores WHERE id = 2), 5),
	((SELECT id FROM Equipment WHERE id = 1), (SELECT id from Stores WHERE id = 1), 15),
	((SELECT id FROM Equipment WHERE id = 4), (SELECT id from Stores WHERE id = 3), 8),
	((SELECT id FROM Equipment WHERE id = 5), (SELECT id FROM Stores WHERE id = 4), 10),
	((SELECT id FROM Equipment WHERE id = 2), (SELECT id FROM Stores WHERE id = 2), 15);

  -- ------------------
  -- Table Reservations
  -- ------------------

  CREATE TABLE Reservations(
	id int AUTO_INCREMENT NOT NULL,
	customer_id int,
	equipment_id int,
	start_date datetime NOT NULL,
	end_date datetime NOT NULL,
	actual_start_date datetime NOT NULL,
	actual_end_date datetime NOT NULL,
	FOREIGN KEY (customer_id) REFERENCES Customers(id)
			ON DELETE CASCADE,
	FOREIGN KEY (equipment_id) REFERENCES Equipment(id)
			ON DELETE CASCADE,
	PRIMARY KEY (id, start_date)
  );

  INSERT INTO Reservations (customer_id, equipment_id, start_date, end_date, actual_start_date, actual_end_date)
  VALUES ((SELECT id FROM Customers WHERE id = 3), (SELECT id FROM Equipment WHERE id = 2), "2025-05-20", "2025-05-21", "2025-05-20", "2025-05-21"),
    ((SELECT id FROM Customers WHERE id = 3), (SELECT id FROM Equipment WHERE id = 5), "2025-05-20", "2025-05-21", "2025-05-20", "2025-05-21"),
    ((SELECT id FROM Customers WHERE id = 4), (SELECT id FROM Equipment WHERE id = 4), "2025-06-01", "2025-06-01", "2025-06-01", "2025-06-01"),
    ((SELECT id FROM Customers WHERE id = 1), (SELECT id FROM Equipment WHERE id = 3), "2025-06-20", "2025-06-20", "2025-06-20", "2025-06-20"),
    ((SELECT id FROM Customers WHERE id = 1), (SELECT id FROM Equipment WHERE id = 4), "2025-06-20", "2025-06-20", "2025-06-20", "2025-06-20");

  SET FOREIGN_KEY_CHECKS = 1;
END //

DELIMITER ;