
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



@mcp.tool()
def aggregate_csv(file_path: str, group_by: str, agg_column: str, agg_function: str) -> str:
  """ 
  This function will aggregate data in a csv file to return the sum, count or specified agg function
  Example:
    'what is the average sales by city'
  Arg:
    file_path: the string where the csv file lives
    group_by: the value to group the data by, use comma seperated for multiple
    agg_column: the column we want to perform the aggregate function one (if you want the count of sales, the sales is the colum) 
    agg_function: the function perform on a column. (sum, mean, max etc)
  """

  try:
    file_path_obj = Path(file_path)
    agg_function = agg_function.lower()

    if not file_path_obj.exist():
      return f"Error: File not found at {file_path_obj}"

    df = pd.read_csv(file_path_obj)




if __name__ == "__main__":
   mcp.run()
