import xmltodict
from collections import Counter
import pandas as pd
from pathlib import Path


# Use the module pathlib to get the path of the file
HERE = Path(__file__).parent.resolve()


def render_publication_years_dataframe(OUTPUT, filenames):
    """
    Given a list of names, render the publication dataframe.
    """
    dfs = []
    for filename in filenames:
        df = extract_publication_dates(f"{filename}.xml")
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
    df.to_csv(OUTPUT.joinpath("publications.csv"), index=False)


def extract_patent_years(file_name):
    FILEPATH = HERE.parent.joinpath("data").joinpath(file_name)

    file_in_xml = FILEPATH.read_text(encoding="latin-1")
    # Parse an xml file by name into a Python object
    file_dict = xmltodict.parse(file_in_xml)

    bibliography = file_dict["CURRICULO-VITAE"]["PRODUCAO-TECNICA"]
    full_name = file_dict["CURRICULO-VITAE"]["DADOS-GERAIS"]["@NOME-COMPLETO"]

    if "PATENTE" not in bibliography:
        print(full_name)
        years_dict = {}
        df = pd.DataFrame(years_dict, index=[0])
        df["name"] = full_name
        return df

    patents = bibliography["PATENTE"]

    years = []
    # Go into the child elements one by one
    for i in patents:
        # Extract basic data into a python dict
        article_info = i["DADOS-BASICOS-DA-PATENTE"]

        # Get years into a list
        years.append(int(article_info["@ANO-DESENVOLVIMENTO"]))

    years_dict = dict(Counter(years))
    df = pd.DataFrame(years_dict, index=[0])
    df["name"] = full_name
    return df


def extract_publication_dates(file_name):
    """
    Given a Lattes XML, returns a dataframe
    with the number of publications for each year.
    """
    FILEPATH = HERE.parent.joinpath("data").joinpath(file_name)

    file_in_xml = FILEPATH.read_text(encoding="latin-1")
    # Parse an xml file by name into a Python object
    file_dict = xmltodict.parse(file_in_xml)

    bibliography = file_dict["CURRICULO-VITAE"]["PRODUCAO-BIBLIOGRAFICA"]
    articles = bibliography["ARTIGOS-PUBLICADOS"]["ARTIGO-PUBLICADO"]

    full_name = bibliography = file_dict["CURRICULO-VITAE"]["DADOS-GERAIS"][
        "@NOME-COMPLETO"
    ]
    years = []
    # Go into the child elements one by one
    for i in articles:
        # Extract basic data into a python dict
        article_info = i["DADOS-BASICOS-DO-ARTIGO"]

        # Get years into a list
        years.append(int(article_info["@ANO-DO-ARTIGO"]))

    years_dict = dict(Counter(years))
    df = pd.DataFrame(years_dict, index=[0])
    df["name"] = full_name
    return df
