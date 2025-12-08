from app import app
from flask import render_template, redirect, request
import db.db_connector as db 

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