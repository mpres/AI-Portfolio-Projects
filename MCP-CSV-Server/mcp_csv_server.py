
"""
MCP CSV reader

Example usage
- what is in sample.csv
- how many columns are in sample.csv
- how many rows are in the file sample.csv
"""

#Needing to run this module for Jupyter Notebooks


from fastmcp import FastMCP


import pandas as pd
from pathlib import Path

mcp =  FastMCP("csv-reader-server")

@mcp.tool()
def read_csv(file_path: str) -> str:
  """
  Reads a csv file and returns it's contenst
  use when: analyzing csv files
  Example: 'read sample.csv', 'what is in this sample.csv'
  Args: 
    file_path: Is the path to the csv file

  Output:
    Return file contents in a string data type
  """

  try:

    file_path_obj = Path(file_path)

    if not file_path_obj.exist():
      return f"Error: File not found at {file_path_obj}"
    
    df = pd.read_csv(file_path_obj)
  
    result = f"Successfuly read CSV: {file_path_obj}\n"
    result += f"{df.shape[0]} rows and {df.shape[1]} columns\n"
    result += f"Columns include: {', '.join(df.columns)}"

    result += "First 5 rows:\n"
    result += df.head().to_string()

    return result

  except Exception as e:
    return f"Error readign CSV: {str(e)}"

if __name__ == "__main__":
   mcp.run()
