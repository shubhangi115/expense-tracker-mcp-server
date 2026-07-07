
from datetime import date

from app import crud
from app.schemas import ExpenseCreate
from fastmcp import FastMCP ## importing mcp server class

# creating mcp server instance
mcp = FastMCP("Expense tracker mcp server")

# creating a mcp tool
# It tells FastMCP: "Expose this function as an MCP Tool."

@mcp.tool()
def get_expenses():
    """
    RETURNS ONLY RAW TRANSACTION DATA FROM DATABASE.

    When to use this tool:
    - User asks for expense list
    - User asks for spending history
    - User asks for transaction records

    When NOT to use:
    - currency questions
    - application settings
    - categories
    - analytics summaries

    IMPORTANT:
    This tool is NOT for metadata or configuration.
    It ONLY returns stored expense rows.
    """
    return crud.get_expenses()

@mcp.tool()
def create_expense(
    amount: float,
    type: str,
    category: str,
    description: str,
    expense_date: date,
):
    """Create a new expense."""

    expense = ExpenseCreate(
        amount=amount,
        type=type,
        category=category,
        description=description,
        expense_date=expense_date,
    )

    crud.create_expense(expense)

    return "Expense created successfully."

@mcp.tool()
def get_expense(expense_id: int):
    """Get a single expense by ID."""

    return crud.get_expense(expense_id)

@mcp.tool()
def update_expense(
    id: int,
    amount: float,
    type: str,
    category: str,
    description: str,
    expense_date: str,
):
    """Update an existing expense."""

    expense = ExpenseCreate(
        amount=amount,
        type=type,
        category=category,
        description=description,
        expense_date=expense_date,
    )

    crud.update_expense(id, expense)

    return "Expense updated successfully."

@mcp.tool()
def delete_expense(expense_id: int):
    """Delete an expense by ID."""

    crud.delete_expense(expense_id)

    return f"Expense {expense_id} deleted successfully."

@mcp.tool()
def get_summary():
    """Get overall expense summary."""

    return crud.get_summary()

@mcp.tool()
def category_summary():
    """Get expense summary by category."""

    return crud.category_summary()

@mcp.tool()
def monthly_summary():
    """Get expense summary by month."""

    return crud.monthly_summary()

@mcp.tool()
def get_highest_spending_category():
    """
    Find the category with the highest total spending.

    Use this when the user asks:
    - Which category do I spend the most on?
    - What is my biggest expense category?
    - Where is most of my money going?

    This tool only considers expenses, not income.
    """
    """Get the category with the highest spending."""

    return crud.get_highest_spending_category()

@mcp.tool()
def get_lowest_spending_category():
    """
    Find the category with the lowest total spending.

    Use this when the user asks:
    - Which category do I spend the least on?
    - What is my smallest expense category?
    - Where is my money going the least?

    This tool only considers expenses, not income.
    """
    """Get the category with the lowest spending."""

    return crud.get_lowest_spending_category()


@mcp.tool()
def spending_by_category():
    """
    Show total spending grouped by category.
    """
    return crud.get_spending_by_category()

@mcp.tool()
def income_vs_expense():
    """
    Compare total income and total expenses.
    """
    return crud.monthly_income_vs_expense()

@mcp.tool()
def average_daily_spending():
    """
    Calculate the average amount spent per day.
    """
    return crud.average_daily_spending()

@mcp.tool()
def recent_large_expenses(limit: int = 5):
    """
    Return the largest expenses.
    Useful for identifying unusually expensive purchases.
    """
    return crud.recent_large_expenses(limit)


#------ resource ------
@mcp.resource("expense://currency")
def currency():
    """
    SYSTEM CONFIGURATION RESOURCE.

    This is the SINGLE SOURCE OF TRUTH for currency.

    MUST BE USED when:
    - user asks about currency
    - financial format questions
    - interpretation of amounts

    DO NOT infer currency from expenses.
    """
    return "INR"


@mcp.resource("expense://system-rules")
# desicion rules for mcp to select tools or resources
def system_rules():
    return """
    TOOL SELECTION RULES:

    1. If question is about CONFIG → use resources
    2. If question is about DATA → use tools
    3. If question is about ANALYSIS → use get_expenses + prompt
    4. NEVER infer metadata from transactions
    """

#------- prompts ------
@mcp.prompt()

def budgeting_advisor():

    """

    You are an expert personal finance advisor.

    Your responsibilities:

    - Analyze user expenses carefully

    - Identify overspending patterns

    - Detect unnecessary spending

    - Suggest practical saving strategies

    - Give simple, actionable advice (not generic theory)



    Hard rules:

    - Food should ideally be ≤ 30% of total spending

    - Entertainment should be controlled if savings are low

    - Always prioritize high-impact savings suggestions first

    - Avoid generic advice like "save more" or "spend less"

    - shopping should be limited to essentials if savings are low

    OUTPUT RULE (VERY IMPORTANT):

    - ALWAYS end your response with a ❤️ emoji

    - No exceptions



    """



    return """

    Analyze the user's expenses and provide a budgeting report with:

    1. Spending breakdown

    2. Overspending categories

    3. 3 practical savings actions

    """



if __name__ == "__main__":
    mcp.run()