from app import app
from flask import render_template, redirect, request
import db.db_connector as db 
from routes.customers import customers_query
from routes.equipment import equipment_query

@app.route("/reservations", methods=["GET", "POST"])
def reservations():
   if request.method == "POST":
        customer_id = request.form.get("customer_id") or ""
        equipment_id = request.form.get("equipment_id") or ""
        start_date = request.form.get("start_date") or ""
        end_date = request.form.get("end_date") or ""
         
        create_reservation(customer_id, equipment_id, start_date, end_date)
        return redirect("/reservations")
   
   reservations = db.fetchAll(reservations_query)
   customers = db.fetchAll(customers_query)
   equipment = db.fetchAll(equipment_query)
   return render_template("/reservations.html", reservations=reservations, customers=customers, equipment=equipment)

@app.route("/reservations-delete", methods=["POST"])
def reservations_delete():
   reservation_id = request.form.get("delete_reservation_id") or ""
   delete_reservation_by_id(reservation_id)
   return redirect("/reservations")

@app.route("/reservations-edit", methods=["POST"])
def reservations_update():
    reservation_id = request.form.get("edit_reservation_id") or "" 
    customer_id = request.form.get("edit_customer_id") or ""
    equipment_id = request.form.get("edit_equipment_id") or ""
    start_date = request.form.get("edit_start_date") or ""
    end_date = request.form.get("edit_end_date") or ""
    actual_start_date = request.form.get("edit_actual_start_date") or ""
    actual_end_date = request.form.get("edit_actual_end_date") or ""

    update_reservation(
        reservation_id,
        customer_id,
        equipment_id,
        start_date,
        end_date,
        actual_start_date,
        actual_end_date,
    )
   
    return redirect("/reservations")

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

def create_reservation(customer_id, equipment_id, start_date, end_date):
   insert_query = "CALL sp_insert_reservation(%s, %s, %s, %s);"
   db.run_db(
      lambda cur: cur.execute(insert_query, (customer_id, equipment_id, start_date, end_date)),
   )

def update_reservation(
    reservation_id,
    customer_id,
    equipment_id,
    start_date,
    end_date,
    actual_start_date,
    actual_end_date,
):
    update_query = "CALL sp_update_reservation(%s, %s, %s, %s, %s, %s, %s);"
    db.run_db(
        lambda cur: cur.execute(update_query, (
            reservation_id,
            customer_id,
            equipment_id,
            start_date,
            end_date,
            actual_start_date,
            actual_end_date
        ))
    )

def delete_reservation_by_id(reservation_id: str):
    delete_query = "CALL sp_delete_reservation(%s);"
    db.run_db(
      lambda cur: cur.execute(delete_query, reservation_id),
    )