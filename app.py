from typing import List
from flask import Flask, render_template, redirect
from flask import request
import db.db_connector as db 

port = 8000

app = Flask(__name__)

customers_query = """
SELECT
   *
FROM
   Customers;
"""

equipment_query = """
SELECT
   eq.id,
   eq.item_name,
   ca.activity_type as category
FROM
   Equipment eq
   JOIN Categories ca ON eq.category_id = ca.id;
"""

store_query = "SELECT Stores.id, Stores.address, Stores.city, Stores.zip_code FROM Stores;"

reservations_query = """
SELECT
   cu.id as customer_id,
   cu.first_name as customer_first_name,
   cu.last_name as customer_last_name,
   eq.id as equipment_id,
   eq.item_name as equipment_name,
   res.id as reservation_id,
   res.start_date as start_date,
   res.end_date as end_date,
   res.actual_start_date as actual_start_date,
   res.actual_end_date as actual_end_date
FROM
   Reservations res
   JOIN Customers cu ON res.customer_id = cu.id
   JOIN Equipment eq ON res.equipment_id = eq.id;
"""

def fetchAll(query: str) -> List[dict[str, str]]:
   dbConnection = db.connectDB()
   rows = db.query(dbConnection, query).fetchall()
   return rows

def delete_reservation_by_id(reservation_id: str):
      dbConnection = db.connectDB()
      cursor = dbConnection.cursor()
      delete_query = "CALL sp_delete_reservation(%s);"
      
      cursor.execute(delete_query, (reservation_id))

      # while cursor.nextset():
      #    pass

      dbConnection.commit()

# Routes
@app.route("/", methods=["GET"])
def home():
  return render_template("/welcome.html")

@app.route("/stores", methods=["GET", "POST"])
def stores():
   try:
      dbConnection = db.connectDB()
      stores = db.query(dbConnection, store_query).fetchall()
      return render_template("/stores.html", stores=stores)
   except Exception as e:
      print(f"Error executing queries: {e}")
      return "An error has occured while exceuting DB query", 500
   
@app.route("/store-inventory", methods=["GET"])
def get_store_inventory():
   try:
      dbConnection = db.connectDB()
      query1 = "SELECT InventoryItems.equipment_id, InventoryItems.store_id, Equipment.item_name, \
               Stores.address, InventoryItems.quantity FROM InventoryItems \
               JOIN Equipment ON InventoryItems.equipment_id = Equipment.id \
               JOIN Stores ON InventoryItems.store_id = Stores.id \
               ORDER BY Stores.address, Equipment.item_name;"
      inventory_items = db.query(dbConnection, query1).fetchall()
      stores = db.query(dbConnection, store_query).fetchall()
      equipment = db.query(dbConnection, equipment_query).fetchall()
      return render_template("/store-inventory.html", inventory_items=inventory_items, stores=stores, equipment=equipment)
   except Exception as e:
      print(f"Error executing query: {e}")
      return "An error has occured while exceuting DB query", 500

@app.route("/store-inventory-delete", methods=["POST"])
def delete_store_inventory():
   try:
      dbConnection = db.connectDB()
      cursor = dbConnection.cursor()
      equipment_id = request.form["delete_equipment_item_id"]
      store_id = request.form["delete_from_store_id"]

      query1 = "CALL sp_delete_inventory_item(%s, %s);"
      cursor.execute(query1, (equipment_id, store_id))

      while cursor.nextset():
         pass

      dbConnection.commit()
      print(f"DELETE EQUIPMENT_ID: {equipment_id} | STORE_ID: {store_id}")
      return redirect("/store-inventory")
   except Exception as e:
      print(f"Error executing queries: {e}")
      return ("An error occured deleting from InventoryItems", 500)
   
   finally:
      if "dbConnection" in locals() and dbConnection:
         dbConnection.close()

@app.route("/store-add-new-item", methods=["POST"])
def add_new_store_inventory_item():
      try:
         dbConnection = db.connectDB()
         cursor = dbConnection.cursor()

         equipment_id = request.form["add_item_to_store_equipment_id"]
         store_id = request.form["add_item_to_store_store_id"]
         quantity = request.form["add_item_to_store_quantity"]

         add_item_query = "CALL sp_insert_inventory_item(%s, %s, %s);"
         cursor.execute(add_item_query, (equipment_id, store_id, quantity))

         dbConnection.commit()
         
         return redirect("/store-inventory")
      except Exception as e:
         print(f"Error executing queries: {e}")
         return ("An error occured adding store inventory item", 500)   

@app.route("/store-update-inventory-item", methods=["POST"])
def update_inventory_item():
   try:
      dbConnection = db.connectDB()
      cursor = dbConnection.cursor()
      store_id = request.form["update_inven_store_id"]
      orig_equip_id = request.form["update_inven_original_equipment_id"]
      new_equip_id = request.form["update_inven_new_equipment_id"]
      quantity = request.form["update_inven_item_quantity"]

      return request.form
   except Exception as e:
      print(f"Erorr has occured: {e}")
      return ("Must provide either new equipment or quantity", 500)


@app.route("/customers", methods=["GET", "POST"])
def customers():
   if request.method == "POST":
      # TODO:
      # Sanitize Input
      first_name = request.form.get("first_name") or ""
      last_name = request.form.get("last_name") or ""
      phone = request.form.get("phone_number") or ""
      address = request.form.get("address") or ""

      # TODO:
      # Save Customer To DB

      # redirect clears POST data and reloads table
      return redirect("/customers")
   
   customers = fetchAll(customers_query)
   return render_template("/customers.html", customers=customers)

@app.route("/equipment", methods=["GET", "POST"])
def equipment():
   equipment = fetchAll(equipment_query)
   return render_template("/equipment.html", equipment=equipment)

@app.route("/reservations", methods=["GET", "POST"])
def reservations():
   if request.method == "POST":
      #TODO: Handle create reservation
      return redirect("/reservations")
   
   reservations = fetchAll(reservations_query)
   customers = fetchAll(customers_query)
   equipment = fetchAll(equipment_query)
   return render_template("/reservations.html", reservations=reservations, customers=customers, equipment=equipment)

@app.route("/reservations-delete", methods=["POST"])
def reservations_delete():
   reservation_id = request.form.get("delete_reservation_id") or ""
   delete_reservation_by_id(reservation_id)
   return redirect("/reservations")

@app.route("/categories", methods=["GET", "POST"])
def categories():
   try:
      dbConnection = db.connectDB()
      query1 = "SELECT * FROM Categories;"
      categories = db.query(dbConnection, query1).fetchall()
      return render_template("/categories.html", categories=categories)
   except Exception as e:
      print(f"Error executing queries: {e}")
      return "An error occured while executing the database queries", 500
      
@app.route("/reset-db", methods=["GET"])
def reset_db():
   try:
      dbConnection = db.connectDB()
      cursor = dbConnection.cursor()

      cursor.execute("CALL sp_reset_db();")
      dbConnection.commit()

      print("DB was successfully reset")
   except Exception as e:
      print(f"Error executing reset DB query error: {e}")
   finally:
      cursor.close()
      dbConnection.close()
      return redirect("/")
      
# Listener
if __name__ == "__main__":

    #Start the app to run on a port of your choosing
    app.run(port=5651, debug=True)
