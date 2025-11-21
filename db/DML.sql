--- Store Queries ---
SELECT
    *
FROM
    Stores;

--- View all Categories ---
SELECT
    *
FROM
    Categories;

--- InventoryItems Queries ---
-- View Inventory of all stores --
SELECT
    InventoryItems.equipment_id,
    Equipment.item_name,
    Stores.address,
    InventoryItems.quantity
FROM
    InventoryItems
    JOIN Equipment ON InventoryItems.equipment_id = Equipment.id
    JOIN Stores ON InventoryItems.store_id = Stores.id
ORDER BY
    Stores.address,
    Equipment.item_name;

-- INSERT into InventoryItems -- 
INSERT INTO
    InventoryItems(equipment_id, store_id, quantity)
VALUES
    (
        @dropdown_equipment_item,
        @dropdown_menu_store_location,
        @input_quantity
    );

-- UPDATE quantity of InventoryItems --
UPDATE
    InventoryItems
SET
    quantity = @input_quantity
WHERE
    store_id = @input_store_id
    AND equipment_id = @input_equipment_id;

-- UPDATE InventoryItems.equipment_id --
UPDATE
    InventoryItems
SET
    equipment_id = @dropwndown_input_equipment_id
WHERE
    store_id = @dropdown_menu_store_location
    AND equipment_id = @input_equipment_id;

-- DELETE equipment_id from InventoryItems -- 
DELETE FROM
    InventoryItems
WHERE
    equipment_id = @input_equipment_id
    AND store_id = @input_store_id;

--- Customers Queries ---
SELECT
    *
FROM
    Customers;

--- Equipment Queries ---
SELECT
    eq.id,
    eq.item_name,
    ca.activity_type AS category
FROM
    Equipment eq
    JOIN Categories ca ON eq.category_id = ca.id;

--- Reservations Queries ---
SELECT
    res. *,
    eq.item_name,
    cu.first_name,
    cu.last_name
FROM
    Reservations res
    JOIN Customers cu ON res.customer_id = cu.id
    JOIN Equipment eq ON res.equipment_id = eq.id;

INSERT INTO
    Reservations(
        customer_id,
        equipment_id,
        start_date,
        end_date,
        actual_start_date,
        actual_end_date
    )
VALUES
    (
        1,
        1,
        "2025/1/1",
        "2025/1/10",
        NULL,
        NULL
    );

UPDATE
    Reservations
SET
    equipment_id = @input_equipment_id
WHERE
    id = @input_reservation_id;

DELETE FROM
    Reservations
WHERE
    id = @input_reservation_id;