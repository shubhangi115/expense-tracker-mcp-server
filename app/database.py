import sqlite3

DATABASE_NAME = r"C:\Projects\expense-tracker-core\expenses.db"


def get_db_connection():
    """
    Creates and returns a SQLite database connection.
    """

    connection = sqlite3.connect(DATABASE_NAME)

    # Return rows as dictionaries instead of tuples
    connection.row_factory = sqlite3.Row

    return connection

# to initialise db and do :
    # connect to db
    # create tables
    # create indexes , maybe later
    # insert default data will do steply
    # close connection
def initialize_database():
    """
    Creates database tables if they do not exist.
    """

    connection = get_db_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            amount REAL NOT NULL,

            type TEXT NOT NULL,

            category TEXT NOT NULL,

            description TEXT,

            expense_date DATE NOT NULL,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    connection.commit()

    connection.close()