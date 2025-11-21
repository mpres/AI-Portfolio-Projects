#!/usr/bin/env python3
"""MySQL MCP Server - Provides database access via Model Context Protocol"""

import os
import json
import asyncio
import logging
from typing import Any, Optional
from contextlib import asynccontextmanager

import aiomysql
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mysql-mcp-server")

# Database configuration from environment variables
DB_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "port": int(os.getenv("MYSQL_PORT", "3306")),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", ""),
    "db": os.getenv("MYSQL_DATABASE", "test"),
    "autocommit": True,
}

# Global connection pool
pool: Optional[aiomysql.Pool] = None


async def init_pool():
    """Initialize the MySQL connection pool"""
    global pool
    pool = await aiomysql.create_pool(
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        db=DB_CONFIG["db"],
        autocommit=DB_CONFIG["autocommit"],
        minsize=1,
        maxsize=10,
    )
    logger.info("MySQL connection pool initialized")


@asynccontextmanager
async def get_connection():
    """Get a connection from the pool"""
    if pool is None:
        raise RuntimeError("Connection pool not initialized")
    
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            yield cursor


async def execute_query(sql: str) -> list[dict[str, Any]]:
    """Execute a SELECT query and return results"""
    async with get_connection() as cursor:
        await cursor.execute(sql)
        rows = await cursor.fetchall()
        return rows


async def list_tables() -> list[dict[str, Any]]:
    """List all tables in the database"""
    async with get_connection() as cursor:
        await cursor.execute("SHOW TABLES")
        rows = await cursor.fetchall()
        return rows


async def describe_table(table_name: str) -> list[dict[str, Any]]:
    """Get the schema of a specific table"""
    # Validate table name to prevent SQL injection
    if not table_name.replace("_", "").isalnum():
        raise ValueError("Invalid table name")
    
    async with get_connection() as cursor:
        await cursor.execute(f"DESCRIBE {table_name}")
        rows = await cursor.fetchall()
        return rows


async def main():
    """Main entry point for the MCP server"""
    # Initialize connection pool
    await init_pool()
    
    # Create MCP server
    server = Server("mysql-server")
    
    @server.list_tools()
    async def list_tools() -> list[Tool]:
        """List available tools"""
        return [
            Tool(
                name="query",
                description="Execute a SELECT query on the MySQL database",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "sql": {
                            "type": "string",
                            "description": "The SQL SELECT query to execute",
                        }
                    },
                    "required": ["sql"],
                },
            ),
            Tool(
                name="list_tables",
                description="List all tables in the database",
                inputSchema={
                    "type": "object",
                    "properties": {},
                },
            ),
            Tool(
                name="describe_table",
                description="Get the schema of a specific table",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "table": {
                            "type": "string",
                            "description": "The name of the table to describe",
                        }
                    },
                    "required": ["table"],
                },
            ),

        ]
    
    @server.call_tool()
    async def call_tool(name: str, arguments: Any) -> list[TextContent]:
        """Handle tool calls"""
        try:
            if name == "query":
                sql = arguments.get("sql", "")
                
                # Security: Only allow SELECT queries
                if not sql.strip().upper().startswith("SELECT"):
                    raise ValueError("Only SELECT queries are allowed with the query tool")
                
                results = await execute_query(sql)
                return [
                    TextContent(
                        type="text",
                        text=json.dumps(results, indent=2, default=str),
                    )
                ]
            
            elif name == "list_tables":
                results = await list_tables()
                return [
                    TextContent(
                        type="text",
                        text=json.dumps(results, indent=2, default=str),
                    )
                ]
            
            elif name == "describe_table":
                table = arguments.get("table", "")
                results = await describe_table(table)
                return [
                    TextContent(
                        type="text",
                        text=json.dumps(results, indent=2, default=str),
                    )
                ]
            
            else:
                raise ValueError(f"Unknown tool: {name}")
        
        except Exception as e:
            logger.error(f"Error executing tool {name}: {e}")
            return [
                TextContent(
                    type="text",
                    text=f"Error: {str(e)}",
                )
            ]
    
    # Run the server
    async with stdio_server() as (read_stream, write_stream):
        logger.info("MySQL MCP Server running on stdio")
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


if __name__ == "__main__":
    asyncio.run(main())