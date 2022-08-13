from numpy import full
from helper import *
from pathlib import Path

HERE = Path(__file__).parent.resolve()
LATTES = HERE.parent.joinpath("data").joinpath("Lattes")

filenames = []
for path in LATTES.glob("*.xml"):
    filenames.append(path.stem)

full_names = []
phd_conclusion_years = []
for filename in filenames:
    FILEPATH = (
        HERE.parent.joinpath("data").joinpath("Lattes").joinpath(f"{filename}.xml")
    )

    file_in_xml = FILEPATH.read_text(encoding="latin-1")
    # Parse an xml file by name into a Python object
    file_dict = xmltodict.parse(file_in_xml)

    full_name = file_dict["CURRICULO-VITAE"]["DADOS-GERAIS"]["@NOME-COMPLETO"]
    print(full_name)
    phd_data = file_dict["CURRICULO-VITAE"]["DADOS-GERAIS"][
        "FORMACAO-ACADEMICA-TITULACAO"
    ]["DOUTORADO"]
    if isinstance(phd_data, dict):
        phd_conclusion_year = phd_data["@ANO-DE-CONCLUSAO"]
    else:
        phd_years = []
        for entry in phd_data:
            phd_years.append(entry["@ANO-DE-CONCLUSAO"])
        phd_conclusion_year = max(phd_years)

    full_names.append(full_name)
    phd_conclusion_years.append(phd_conclusion_year)

df = pd.DataFrame({"name": full_names, "phd_conclusion_year": phd_conclusion_years})

df.to_csv(OUTPUT.joinpath("phd_years.csv"), index=False)

# render_table_for_category(
#    category="patents", extractor=extract_patent_years, filenames=filenames
# )

render_table_for_category(
    category="publications", extractor=extract_publication_dates, filenames=filenames
)
