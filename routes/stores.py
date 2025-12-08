from app import app
from flask import render_template, redirect, request
import db.db_connector as db 

store_query = "SELECT Stores.id, Stores.address, Stores.city, Stores.zip_code FROM Stores;"

@app.route("/stores", methods=["GET", "POST"])
def stores():
   try:
      dbConnection = db.connectDB()
      stores = db.query(dbConnection, store_query).fetchall()
      return render_template("/stores.html", stores=stores)
   except Exception as e:
      print(f"Error executing queries: {e}")
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