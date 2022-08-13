from helper import *
from pathlib import Path

HERE = Path(__file__).parent.resolve()
DATA = HERE.parent.joinpath("data")
OUTPUT = HERE.parent.joinpath("output")

filenames = []
for path in DATA.glob("*.xml"):
    filenames.append(path.stem)

render_publication_years_dataframe(OUTPUT, filenames)
dfs = []
for filename in filenames:
    df = extract_patent_years(f"{filename}.xml")
    dfs.append(df)

df = pd.concat(dfs, axis=0)
df = df.drop_duplicates()
df = df.fillna(0)
df.columns = df.columns.astype(str)
df = df.reindex(
    sorted(df.columns),
    axis=1,
)
first_column = df.pop("name")
df.insert(0, "name", first_column)
df.to_csv(OUTPUT.joinpath("patent.csv"), index=False)
