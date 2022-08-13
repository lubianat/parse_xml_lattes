from helper import *
from pathlib import Path

HERE = Path(__file__).parent.resolve()
DATA = HERE.parent.joinpath("data")
OUTPUT = HERE.parent.joinpath("output")

file_name = "curriculo3.xml"

df = extract_patent_years(file_name)

print(df)
