from helper import *
from pathlib import Path

HERE = Path(__file__).parent.resolve()
DATA = HERE.parent.joinpath("data")
OUTPUT = HERE.parent.joinpath("output")

filenames = []
for path in DATA.glob("*.xml"):
    filenames.append(path.stem)

dfs = []
for filename in filenames:
    df = extract_publication_dates(f"{filename}.xml")
    dfs.append(df)

df = pd.concat(dfs, axis=0)
df = df.drop_duplicates()
df = df.fillna(0)

df.to_csv(OUTPUT.joinpath("publications.csv"))
