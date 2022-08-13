import untangle
from pathlib import Path

# Use the module pathlib to get the path of the file
HERE = Path(__file__).parent.resolve()
filename = str(HERE.parent.joinpath("data").joinpath("curriculo.xml"))


# Parse an xml file by name into a Python object
file = untangle.parse(filename)

bibliography = file.CURRICULO_VITAE.PRODUCAO_BIBLIOGRAFICA
articles = bibliography.ARTIGOS_PUBLICADOS

years = []
# Go into the child elements one by one
for i in articles.children:

    # Extract basic data into a python dict
    article_info = i.DADOS_BASICOS_DO_ARTIGO._attributes

    # Get years into a list
    years.append(int(article_info["ANO-DO-ARTIGO"]))


# Plot the histogram of publication years
import matplotlib.pyplot as plt

plt.hist(years)
plt.show()
