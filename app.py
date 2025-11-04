from flask import Flask, render_template, render_template_string
from flask import request

app = Flask(__name__)

# Routes
@app.route("/", methods=["GET"])
def home():
  return render_template("/welcome.html")

@app.route("/stores", methods=["GET", "POST"])
def stores():
   return render_template("/stores.html")

@app.route("/store-inventory", methods=["GET", "POST"])
def store_inventory():
   return render_template("/store-inventory.html")

@app.route("/customers", methods=["GET", "POST"])
def customers():
   return render_template("/customers.html")

@app.route("/equipment", methods=["GET", "POST"])
def equipment():
   return render_template("/equipment.html")

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
