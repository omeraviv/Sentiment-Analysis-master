from google.cloud import translate_v2 as translate
from google.oauth2 import service_account

def transalte_text(text, target_language='en'):
    translate_client = translate.Client(credentials=service_account.Credentials.from_service_account_file('My First Project-8d9aec5cfe29.json'))

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(
        text, target_language=target_language)
    return result['translatedText']
    #print(u'Text: {}'.format(result['input']))
    #print(u'Translation: {}'.format(result['translatedText']))
    #print(u'Detected source language: {}'.format(
    #    result['detectedSourceLanguage']))


