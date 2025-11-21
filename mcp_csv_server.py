
"""
MCP CSV reader

Example usage
- what is in sample.csv
- how many columns are in sample.csv
- how many rows are in the file sample.csv
"""

from fastmcp import FastMCP

import pandas as pd
from pathlib import Path

mcp = FastMCP("csv-reader-server")

@mcp.tool()
def read_csv(file_path: str) -> str:
  """
  Reads a csv file and returns it's contents
  use when: analyzing csv files
  Example: 'read sample.csv', 'what is in this sample.csv'
  Args:
    file_path: Is the path to the csv file

  Output:
    Return file contents in a string data type
  """

  try:
    file_path_obj = Path(file_path)

    if not file_path_obj.exists():  # Fixed: exist() -> exists()
      return f"Error: File not found at {file_path_obj}"

    df = pd.read_csv(file_path_obj)

    result = f"Successfully read CSV: {file_path_obj}\n"  # Fixed typo: Successfuly -> Successfully
    result += f"{df.shape[0]} rows and {df.shape[1]} columns\n"
    result += f"Columns include: {', '.join(df.columns)}\n"  # Added missing \n

    result += "First 5 rows:\n"
    result += df.head().to_string()

    return result

  except Exception as e:
    return f"Error reading CSV: {str(e)}"  # Fixed typo: readign -> reading


@mcp.tool()
def aggregate_csv(file_path: str, group_by: str, agg_column: str, agg_function: str) -> str:
  """ 
  This function will aggregate data in a csv file to return the sum, count or specified agg function
  Example:
    'what is the average sales by city'
  Arg:
    file_path: the string where the csv file lives
    group_by: the value to group the data by, use comma separated for multiple
    agg_column: the column we want to perform the aggregate function on (if you want the count of sales, the sales is the column) 
    agg_function: the function perform on a column. (sum, mean, max etc)
  """

  try:
    file_path_obj = Path(file_path)
    agg_function = agg_function.lower()

    if not file_path_obj.exists():  # Fixed: exist() -> exists()
      return f"Error: File not found at {file_path_obj}"

    df = pd.read_csv(file_path_obj)

    group_columns = [col.strip() for col in group_by.split(',')]

    # Validate for missing columns
    missing_cols = [col for col in group_columns if col not in df.columns]

    if missing_cols:
      return f"Error: Columns not found: {missing_cols}"
      
    if agg_column not in df.columns:
      return f"Error: Aggregation Column not found: {agg_column}"

    valid_functions = ['sum', 'mean', 'min', 'max']

    if agg_function not in valid_functions:  # Fixed: valid_funcions -> valid_functions
      return f"Error: Invalid function. Valid options: {', '.join(valid_functions)}"

    agg_result = df.groupby(group_columns)[agg_column].agg(agg_function).reset_index()
    agg_col_name = agg_column

    result = f"Aggregation complete:\n"
    result += f"File: {file_path_obj}\n"
    result += f"Grouped by: {', '.join(group_columns)}\n"
    result += f"Aggregation: {agg_function}({agg_column})\n\n"  # Simplified message

    result += agg_result.to_string(index=False)

    total = agg_result[agg_col_name].agg(agg_function)

    if total is not None:
      result += f"\n\nTotal {agg_function}: {total:,.2f}"

    return result

  except Exception as e:
    return f"Error aggregating file: {str(e)}"  # Fixed capitalization


if __name__ == "__main__":
   mcp.run()
