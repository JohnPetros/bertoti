from os import getenv
from typing import Any

from langchain_community.tools.sql_database.tool import (
    InfoSQLDatabaseTool,
    ListSQLDatabaseTool,
)
from langchain_community.tools import QuerySQLDatabaseTool
from langchain_community.utilities.sql_database import SQLDatabase

database = SQLDatabase.from_uri(getenv("DATABASE_URI"))


def list_permissions_by_role(role: str) -> Any:
    """
    List all permissions for a given role.
    The all permissions available are:
    - INVENTORY_MOVEMENTS
    - PRODUCTS_CONTROL
    - CATEGORIES_CONTROL
    - CSV_EXPORT
    - LOCATIONS_CONTROL
    - NOTIFICATIONS_CONTROL
    - SUPPLIERS_CONTROL
    - REPORTS
    - ALL

    Args:
      role (string): the name of the role to list permissions for.

    Returns:
      string: the permissions for the given role.
    """
    database_tool = ListSQLDatabaseTool(db=database)
    print(f"Listing permissions for role: {role}")
    print(f"Query: {role}")
    return database_tool.invoke(f"""
    SELECT 
      r.name AS role_name,
      rp.name AS permission_name
    FROM roles r
    JOIN role_permission rp ON r.id = rp.role_id
    WHERE r.name = '{role}'
    """)


def list_database_tables() -> Any:
    """
    List all tables in the database.
    """
    database_tool = ListSQLDatabaseTool(db=database)
    return database_tool.invoke("")


def describe_database_tables(tables: str) -> Any:
    """
    Input a comma-separated list of table names, output is the schema and sample rows for those tables. Be sure that the tables exist by calling `list_tables` first!

    Args:
      tables (string): a comma-separated list of table names.

    Returns:
      string: the schema and sample rows for the specified tables.

    Example:
      tables = "products, employees"
      describe_database_tables(tables)
    """
    database_tool = InfoSQLDatabaseTool(db=database)
    return database_tool.invoke(tables)


def execute_sql_query(query: str) -> Any:
    """
    Execute a SQL query on the database. Only read-only queries (SELECT) are allowed, it is not possible to modify the database.

    Args:
      query (string): the SQL query to execute.

    Returns:
      string: the result of the SQL query.
    """
    database_tool = QuerySQLDatabaseTool(
        db=database,
    )
    print("QUERY -> " + query)
    return database_tool.invoke(query)
