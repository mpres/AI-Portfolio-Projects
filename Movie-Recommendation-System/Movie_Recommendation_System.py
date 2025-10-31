import os
import requests
from pathlib import Path
import zipfile
import pandas as pd


def explore_dir(path):
  """ This would explore the directory and return the outline of it """
  for dir_path, dir_names, file_names in os.walk(path):
    print(f"Directory count {len(dir_names)}, movies count {len(file_names)} in '{file_names}'")


### 10/31/25 grab files and merge them into a useful structure, one file using pandas

!pwd
