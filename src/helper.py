import xmltodict
from collections import Counter
import pandas as pd
from pathlib import Path


# Use the module pathlib to get the path of the file
HERE = Path(__file__).parent.resolve()


def extract_publication_dates(file_name):
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
    df = pd.DataFrame(years_dict, index=[full_name])
    return df
