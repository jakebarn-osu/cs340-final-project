from typing import List
from flask import Flask, render_template, redirect
from flask import request
import db_connector as db 

port = 8000

app = Flask(__name__)

_customers = [
   { "first-name": "jake", "last-name": "barnett", "phone-number": "206-123-4567", "address": "123 Fake St"},
   { "first-name": "eric", "last-name": "mitchell", "phone-number": "206-987-6543", "address": "456 Front St"},
]

def get_customer_from_db() -> List[dict[str, str]]:
   return _customers

def save_customer_to_db(new_customer: dict[str, str]) -> None:
   _customers.append(new_customer)

# Routes
@app.route("/", methods=["GET"])
def home():
  return render_template("/welcome.html")

@app.route("/stores", methods=["GET", "POST"])
def stores():
   try:
      dbConnection = db.connectDB()
      query1 = "SELECT Stores.id, Stores.address, Stores.city, Stores.zip_code FROM Stores;"
      stores = db.query(dbConnection, query1).fetchall()
      return render_template("/stores.html", stores=stores)
   except Exception as e:
      print(f"Error executing queries: {e}")
      return "An error has occured while exceuting DB query", 500
@app.route("/store-inventory", methods=["GET", "POST", "PUT", "DELETE"])
def store_inventory():
   return render_template("/store-inventory.html")

@app.route("/customers", methods=["GET", "POST"])
def customers():
   if request.method == "POST":
      print(request.form)
      first_name = request.form.get("first-name") or ""
      last_name = request.form.get("last-name") or ""
      phone = request.form.get("phone-number") or ""
      address = request.form.get("address") or ""

      save_customer_to_db({
         "first-name": first_name,
         "last-name": last_name,
         "phone-number": phone,
         "address": address,
      })

      # redirect clears POST data and reloads table
      return redirect("/customers")
   
   customers_list = get_customer_from_db()
   return render_template("/customers.html", customers=customers_list)

@app.route("/equipment", methods=["GET", "POST"])
def equipment():
   equipment = [
      {"id": 1, "item_name": "snowboard", "category": "Skiing" },
      {"id": 2, "item_name": "skiis",     "category": "Skiing" },
      {"id": 3, "item_name": "backpack",  "category": "Hiking" },
      {"id": 4, "item_name": "trekking",  "category": "Hiking" },
      {"id": 5, "item_name": "helmet",    "category": "Cycling" },
      {"id": 6, "item_name": "ski_poles", "category": "Skiings" },
      {"id": 7, "item_name": "goggles",   "category": "Skiings" },
      {"id": 8, "item_name": "bicycle",   "category": "Cycling" },
   ]
   return render_template("/equipment.html", equipment=equipment)


# id int AUTO_INCREMENT NOT NULL,
	# customer_id int,
	# equipment_id int,
	# start_date datetime NOT NULL,
	# end_date datetime NOT NULL,
	# actual_start_date datetime NOT NULL,
	# actual_end_date datetime NOT NULL,
	# FOREIGN KEY (customer_id) REFERENCES Customers(id) ON DELETE CASCADE,
	# FOREIGN KEY (equipment_id) REFERENCES Equipment(id) ON DELETE CASCADE,
@app.route("/reservations", methods=["GET", "POST"])
def reservations():
   reservations = [
      {
         "reservation_id": "1",
         "customer_id": "1",
         "customer_first_name": "jake",
         "customer_last_name": "barnett",
         "equipment_id": "1",
         "equipment_name": "snowboard",
         "start_date": "1/1/2025",
         "end_date": "1/10/2025",
         "actual_start_date": "1/1/2025",
         "actual_end_date": "1/9/2025"
       },
       {
         "reservation_id": "2",
         "customer_id": "1",
         "customer_first_name": "jake",
         "customer_last_name": "barnett",
         "equipment_id": "2",
         "equipment_name": "skiis",
         "start_date": "2/1/2025",
         "end_date": "2/20/2025",
         "actual_start_date": "1/1/2025",
         "actual_end_date": ""
       },
       {
         "reservation_id": "3",
         "customer_id": "2",
         "customer_first_name": "eric",
         "customer_last_name": "mitchell",
         "equipment_id": "8",
         "equipment_name": "bicycle",
         "start_date": "3/1/2025",
         "end_date": "3/15/2025",
         "actual_start_date": "",
         "actual_end_date": ""
       },
   ]
   return render_template("/reservations.html", reservations=reservations)

@app.route("/categories", methods=["GET", "POST"])
def categories():
   return render_template("/categories.html")

# Listener
if __name__ == "__main__":

    #Start the app to run on a port of your choosing
    app.run(port=5649, debug=True)
