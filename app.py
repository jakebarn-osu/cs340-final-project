from typing import List
from flask import Flask, render_template, redirect
from flask import request

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
   return render_template("/stores.html")

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
      {"id": 1, "item_name": "skiis",     "category": "Skiing" },
      {"id": 1, "item_name": "backpack",  "category": "Hiking" },
      {"id": 1, "item_name": "trekking",  "category": "Hiking" },
      {"id": 1, "item_name": "helmet",    "category": "Cycling" },
      {"id": 1, "item_name": "ski_poles", "category": "Skiings" },
      {"id": 1, "item_name": "goggles",   "category": "Skiings" },
      {"id": 1, "item_name": "bicycle",   "category": "Cycling" },
   ]
   return render_template("/equipment.html", equipment=equipment)

@app.route("/reservations", methods=["GET", "POST"])
def reservations():
   return render_template("/reservations.html")

@app.route("/categories", methods=["GET", "POST"])
def categories():
   return render_template("/categories.html")

# Listener
if __name__ == "__main__":

    #Start the app to run on a port of your choosing
    app.run(port=5649, debug=True)
