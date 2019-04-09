
#  IMPORT PACKAGES
import requests

def summarize():
    """
    This function uses DeepAI API to get summary of texts.
    Input :           None
    Output :          Summary(in text form)
    Requirements :    API key of DeepAI

    """
    # CALL TO API
    r = requests.post(
        "https://api.deepai.org/api/summarization",
        files={
            'text': open('./extracted.txt', 'rb'),
        },
        headers={'api-key': '...'}
        )
    
    return r.json()['output'] 
    