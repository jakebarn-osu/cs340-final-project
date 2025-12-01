from app import app
from flask import render_template, redirect, request
import db.db_connector as db 

equipment_query = """
SELECT
   eq.id,
   eq.item_name as name,
   ca.activity_type as category
FROM
   Equipment eq
   JOIN Categories ca ON eq.category_id = ca.id;
"""

@app.route("/equipment", methods=["GET", "POST"])
def equipment():
   equipment = db.fetchAll(equipment_query)
   print(equipment)
   return render_template("/equipment.html", equipment=equipment)