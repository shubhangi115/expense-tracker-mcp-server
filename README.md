# Expense Tracker MCP Server

This project is a cloud-deployed **Model Context Protocol (MCP)** server for managing personal expenses and providing financial analytics. It exposes standardized **MCP Tools, Resources, and Prompts**, enabling AI assistants like Claude Desktop to interact with the expense tracker.

## Features

- Add, update, delete, and retrieve expenses
- Financial analytics (summary, category-wise, monthly, daily average)
- Budgeting assistant through MCP Prompts
- MCP Resources for application metadata
- Tested with Claude Desktop and MCP Inspector
- Deployed on FastMCP Cloud

## Tech Stack

- **Language:** Python
- **Protocol:** Model Context Protocol (MCP)
- **Framework:** FastMCP
- **Data Validation:** Pydantic
- **Database:** SQLite
- **AI Client:** Claude Desktop
- **Testing:** MCP Inspector
- **Deployment:** FastMCP Cloud

## Live Deployment

**Endpoint**

```text
https://mcp-server-expense-tracker.fastmcp.app/mcp
```

> Protected by Horizon authentication.

## Setup Instructions

```bash
git clone https://github.com/shubhangi115/expense-tracker-mcp-server.git

cd expense-tracker-mcp-server

python -m venv .venv

.venv\Scripts\activate

pip install -r requirements.txt

fastmcp run main.py
```
