from flask import Flask, render_template, redirect, request
import db.db_connector as db 

port = 8000
app = Flask(__name__)

# IMPORTANT: must be imported after the app declaration
import routes.reservations
import routes.customers
import routes.equipment
import routes.categories
import routes.stores
import routes.store_inventory
from routes.equipment import equipment_query

@app.errorhandler(500)
def handle_all_exceptions(error):
   app.logger.exception(">>> Error <<<")
   app.logger.exception(error)

   return render_template("error.html"), 500


# Routes
@app.route("/", methods=["GET"])
def home():
  return render_template("/welcome.html")
      
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
