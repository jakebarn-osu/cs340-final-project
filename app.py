from flask import Flask, render_template, redirect, request
import db.db_connector as db 

port = 8000
app = Flask(__name__)

# IMPORTANT: must be imported after the app declaration
import routes.reservations
import routes.customers
import routes.equipment
from routes.equipment import equipment_query



@app.errorhandler(500)
def handle_all_exceptions(error):
   app.logger.exception(">>> Error <<<")
   app.logger.exception(error)

   return render_template("error.html"), 500

store_query = "SELECT Stores.id, Stores.address, Stores.city, Stores.zip_code FROM Stores;"


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
      new_equip_id = int(new_equip_id) if new_equip_id else None
      
      quantity = request.form["update_inven_item_quantity"]
      quantity = int(quantity) if quantity else None

      update_inventory_item = "CALL sp_update_inventory_item(%s, %s, %s, %s);"
      cursor.execute(update_inventory_item, (store_id, orig_equip_id, new_equip_id, quantity))
      dbConnection.commit()
      return redirect("/store-inventory")
   except Exception as e:
      print(f"Erorr has occured: {e}")
      return ("Must provide either new equipment or quantity", 500)

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
