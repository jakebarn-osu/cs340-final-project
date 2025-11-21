from typing import Optional
from MySQLdb import connect, Connection, cursors 
import os

from dotenv import load_dotenv

load_dotenv()

# Citation for the following code:
# Date: 2025-11-20
# Adapted from class materials "Exploration - Web Application Technology"
# Source URL: https://canvas.oregonstate.edu/courses/2017561/pages/exploration-web-application-technology-2?module_item_id=25645131


# Database credentials
host = os.getenv("DB_HOST")
user = os.getenv("DB_USER")
passwd =os.getenv("DB_PASSWORD")
db = os.getenv("DB_DB_NAME")

def connectDB(host = host, user = user, passwd = passwd, db = db) -> Connection:
    '''
    connects to a database and returns a database object
    '''
    dbConnection = connect(host,user,passwd,db)
    return dbConnection

def query(dbConnection:Connection, query: str, query_params = ()) -> cursors.DictCursor:
    '''
    executes a given SQL query on the given db connection and returns a Cursor object
    dbConnection: a MySQLdb connection object created by connectDB()
    query: string containing SQL query
    returns: A Cursor object as specified at https://www.python.org/dev/peps/pep-0249/#cursor-objects.
    You need to run .fetchall() or .fetchone() on that object to actually acccess the results.
    '''

    if dbConnection is None:
        raise Exception("No connection to the database found! Have you called connectDB() first?")


    if query is None or len(query.strip()) == 0:
        raise Exception("query is empty! Please pass a SQL query in query")

    print("Executing %s with %s" % (query, query_params))
    # Create a cursor to execute query. Why? Because apparently they optimize execution by retaining a reference according to PEP0249
    cursor: cursors.DictCursor = dbConnection.cursor(cursors.DictCursor)

    # Sanitize the query before executing it.
    cursor.execute(query, query_params)
    
    # Commit any changes to the database.
    dbConnection.commit()
    
    return cursor