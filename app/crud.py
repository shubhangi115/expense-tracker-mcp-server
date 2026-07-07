from app.database import get_db_connection
from app.schemas import ExpenseCreate

# crete a new expense
def create_expense(expense: ExpenseCreate):
    """
    Insert a new expense into the database.
    """

    connection = get_db_connection()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO expenses (
            amount,
            type,
            category,
            description,
            expense_date
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        expense.amount,
        expense.type,
        expense.category,
        expense.description,
        expense.expense_date
    ))

    connection.commit()

    connection.close()

# get all expenses 
def get_expenses(
    expense_type=None,
    category=None
):  # ---> so that we can filter the expenses by type and category for filter in the home page, if not provided, it will return all expenses

    connection = get_db_connection()

    cursor = connection.cursor()

    # we have use query instead of cursor.execute() because we need to build the query dynamically based on the filters provided by the user, if we use cursor.execute() then we need to write multiple if else statements for each filter which is not efficient and also it will be hard to maintain in future, so we are using query variable to build the query dynamically and then execute it using cursor.execute(query) method.
    query = """
        SELECT
            id,
            amount,
            type,
            category,
            description,
            expense_date,
            created_at
        FROM expenses
    """
    params=[]

    # for filtering the expenses by type and category for filter in the home page, if not provided, it will return all expenses
    conditions = [] 

    #if category is provided, then we need to filter the expenses by category
#-------------------------------------------
    if expense_type:

        # was only for filtering type 

        # query += """
        # WHERE type = ?
        # """

        # now for type and cateogry
        conditions.append("type = ?")

        params.append(expense_type)
    
    # for category filter
    if category:

        conditions.append("category = ?")

        params.append(category)

    if conditions:

        query += " WHERE "

        # "AND".join(conditions) will join the conditions list with "AND" and return a string which will be added to the query variable, so that we can filter the expenses by type and category for filter in the home page, if not provided, it will return all expenses
        query += " AND ".join(conditions) 


    cursor.execute(
        query,
        params
    )
#-------------------------------------------

    rows = cursor.fetchall()

    connection.close()

    return [dict(i) for i in rows]

# get a single expense by id
def get_expense(expense_id: int):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id, amount, type, category, description, expense_date, created_at
            FROM expenses
            WHERE id = ?
        """, (expense_id,))

        row = cursor.fetchone()
        # return dict(row) if row else None
        if row:
            return dict(row)
        else:
            return None


    except Exception as e:
        print("DB error:", e)
        return None

    finally:
        connection.close()

# update an existing expense
def update_expense(expense_id: int, expense: ExpenseCreate):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE expenses
            SET amount = ?, type = ?, category = ?, description = ?, expense_date = ?
            WHERE id = ?
        """, (
            expense.amount,
            expense.type,
            expense.category,
            expense.description,
            expense.expense_date,
            expense_id
        ))

        connection.commit()

    except Exception as e:
        print("Database Error:", e)
        raise

    finally:
        connection.close()

# delete an existing expense
def delete_expense(expense_id: int):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("""
            DELETE FROM expenses
            WHERE id = ?
        """, (expense_id,))

        connection.commit()

    except Exception as e:
        print("Database Error:", e)
        raise

    finally:
        connection.close()

# get summary of expense 
def get_summary():
    """
    Get a summary of expenses from the database.
    """

    connection = get_db_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            type,
            COUNT(*) AS total_transactions,
            SUM(amount) AS total_amount,
            AVG(amount) AS average_amount
        FROM expenses
        GROUP BY type;
    """)

    row = cursor.fetchall()

    connection.close()

    # these two are written when the row is a single row, but in this case, it is multiple rows, so we need to return a list of dicts instead of a single dict.
    # return dict(row) if row else None
    # if row:
    #         return dict(row)
    # else:
    #         return None

    # return a list of dicts instead of a single dict
    return [dict(i) for i in row]


# get summary of expense by category
def category_summary():
    """Get a summary of expenses by category from the database."""

    connection = get_db_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            category,
            COUNT(*) AS total_transactions,
            SUM(amount) AS total_amount
        FROM expenses
        GROUP BY category;
    """)

    row = cursor.fetchall()

    connection.close()

    return [dict(i) for i in row]

# get summary of expense by month
def monthly_summary():
    """Get a summary of expenses by month from the database."""

    connection = get_db_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            strftime('%m-%Y', expense_date) AS month,
            COUNT(*) AS total_transactions,
            SUM(amount) AS total_amount
        FROM expenses
        GROUP BY month;
    """)

    row = cursor.fetchall()

    connection.close()

    return [dict(i) for i in row]

# get all unique expense categories for filtering in the home page, if not provided, it will return all categories
def get_categories():
    """
    Get all unique expense categories.
    """

    connection = get_db_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT DISTINCT category
        FROM expenses
        ORDER BY category
    """)

    rows = cursor.fetchall()

    connection.close()

    return [row["category"] for row in rows]


# for ai oriented tools like highest category cost llm have to calculate but our mcp server need to do that 
# Because this is an AI-friendly business capability.
# Instead of making Claude compute totals from hundreds of rows, we give it the answer directly.

def get_highest_spending_category():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            category,
            SUM(amount) AS total_spent
        FROM expenses
        WHERE type = 'expense'
        GROUP BY category
        ORDER BY total_spent DESC
        LIMIT 1
    """)

    result = cursor.fetchone()

    conn.close()

    return result

def get_lowest_spending_category():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            category,
            SUM(amount) AS total_spent
        FROM expenses
        WHERE type='expense'
        GROUP BY category
        ORDER BY total_spent ASC
        LIMIT 1
    """)

    result = cursor.fetchone()
    conn.close()

    if result:
        return {
            "category": result[0],
            "total_spent": result[1]
        }

    return None

def get_spending_by_category():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            category,
            SUM(amount) AS total_spent
        FROM expenses
        WHERE type='expense'
        GROUP BY category
        ORDER BY total_spent DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "category": row[0],
            "total_spent": row[1]
        }
        for row in rows
    ]

def monthly_income_vs_expense():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            type,
            SUM(amount)
        FROM expenses
        GROUP BY type
    """)

    rows = cursor.fetchall()
    conn.close()

    result = {
        "income": 0,
        "expense": 0
    }

    for row in rows:
        result[row[0]] = row[1]

    return result

def average_daily_spending():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            AVG(daily_total)
        FROM (
            SELECT
                expense_date,
                SUM(amount) AS daily_total
            FROM expenses
            WHERE type='expense'
            GROUP BY expense_date
        )
    """)

    avg = cursor.fetchone()[0]
    conn.close()

    return {
        "average_daily_spending": avg or 0
    }

def recent_large_expenses(limit=5):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            amount,
            category,
            description,
            expense_date
        FROM expenses
        WHERE type='expense'
        ORDER BY amount DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "amount": row[0],
            "category": row[1],
            "description": row[2],
            "expense_date": row[3]
        }
        for row in rows
    ]


    

