from os import getenv

from crewai.tools import tool
from langchain_community.tools.sql_database.tool import (
    InfoSQLDatabaseTool,
    ListSQLDatabaseTool,
    QuerySQLCheckerTool,
    QuerySQLDataBaseTool,
)
from langchain_community.utilities.sql_database import SQLDatabase


class ChabotTools:
    def __init__(self):
        self.database = SQLDatabase.from_uri(getenv("DATABASE_URI"))

    @tool("list database tables")
    def list_database_tables(self) -> str:
        """
        List all tables in the database.
        """
        database_tool = ListSQLDatabaseTool(db=self.database)
        return database_tool.invoke("")

    @tool("describe database tables")
    def describe_database_tables(self, tables: str) -> str:
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
        database_tool = InfoSQLDatabaseTool(db=self.database)
        return database_tool.invoke(tables)

    @tool("execute SQL query")
    def execute_sql_query(self, query: str) -> str:
        """
        Execute a SQL query on the database. Only read-only queries (SELECT) are allowed, it is not possible to modify the database.

        Args:
          query (string): the SQL query to execute.

        Returns:
          string: the result of the SQL query.
        """
        database_tool = QuerySQLDataBaseTool(
            db=self.database,
        )
        return database_tool.invoke(query)

    @tool("check SQL query")
    def check_sql_query(self, query: str) -> str:
        """
        Double check the SQL query to see if it is valid. Always use this tool before executing a query to using `execute_sql_query`.

        Args:
          query (string): the SQL query to check.
        """
        database_tool = QuerySQLCheckerTool(db=self.database)
        return database_tool.invoke(query)
