from app import app
from flask import render_template, redirect, request
import db.db_connector as db 

@app.route("/customers", methods=["GET", "POST"])
def customers():
   if request.method == "POST":
      first_name = request.form.get("first_name") or ""
      last_name = request.form.get("last_name") or ""
      phone = request.form.get("phone_number") or ""
      address = request.form.get("address") or ""
         
      create_customer(first_name, last_name, phone, address)
      return redirect("/customers")
   
   customers = db.fetchAll(customers_query)
   return render_template("/customers.html", customers=customers)

@app.route("/customers-delete", methods=["POST"])
def customers_delete():
   customer_id = request.form.get("delete_customer_id") or ""
   delete_customer_by_id(customer_id)
   return redirect("/customers")


customers_query = """
SELECT
   *
FROM
   Customers;
"""

def create_customer(first, last, phone, name):
   insert_query = "CALL sp_insert_customer(%s, %s, %s, %s);"
   db.run_db(
      lambda cur: cur.execute(insert_query, (first, last, phone, name)),
   )

def delete_customer_by_id(customer_id):
   delete_query = "CALL sp_delete_customer(%s);"
   return db.run_db(
      lambda cur: cur.execute(delete_query, (customer_id)),
   )
