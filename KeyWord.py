
# IMPORT PACKAGES
import textrazor
import re
import string


def extract(var):
    """
    This function extracts the keywords out of the text by using the TEXTRAZOR API.
    Input :           Text
    Output :          Entities
    Requirements :    TextRazor API key

    """
    textrazor.api_key = "..."
    client = textrazor.TextRazor(extractors=["entities", "topics"])          # Multiple extractors are possible.
    response = client.analyze(var)                                           # API analyses the text and provides a response.
    entities = []
    for entity in response.entities():                                       # Making a list of all the entities in the response object.
        entities.append(entity.id)
    return entities

def extract_doc():
    """
    This function serves as medium for a view to generate key Words from the text extracted from the input slide.
    Input :            None
    Output :           Extracted key words
    Requirements :     Extracted.txt

    """
    # INPUT THE FILE
    with open('./extracted.txt', 'r') as myfile:
        data=myfile.read().replace('\n', '')
        
        # APPLYING PREPROCESSING
        data = data.lower()
        result = re.sub(r'\d+', '', data)
        data = result.translate(str.maketrans('','',string.punctuation))
        data = data.translate(str.maketrans('','','1234567890'))
        data = data.strip()
    return extract(data)
    