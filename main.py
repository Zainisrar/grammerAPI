from __future__ import print_function
import re  # Import the regular expressions library
import ProWritingAidSDK
from ProWritingAidSDK.rest import ApiException
from pprint import pprint

configuration = ProWritingAidSDK.Configuration()
configuration.host = 'https://api.prowritingaid.com'
configuration.api_key['licenseCode'] = '05919403-4500-45EC-8BB8-BE60F1ED41AB'

# Create an instance of the API class
api_instance = ProWritingAidSDK.TextApi(ProWritingAidSDK.ApiClient('https://api.prowritingaid.com'))
sentence = "Zain is veery good boy"
print("Original sentence: " + sentence)

try:
    api_request = ProWritingAidSDK.TextAnalysisRequest(sentence, ["grammar"], "General", "en")
    api_response = api_instance.post(api_request)
    print(api_response)
    tags = api_response.result.tags
    suggestions_2d_array = []
    mistakes = []  # Initialize an empty array for mistake words

    for tag in tags:
        suggestions = tag.suggestions
        mistakes.append(tag.subcategory)
        suggestions_2d_array.append(suggestions[0])  # Append each suggestion

    print(f"Suggestion: {suggestions_2d_array}")
    print(f"Mistakes: {mistakes}")
    mistakes_and_suggestions = list(zip(mistakes, suggestions_2d_array))
    print(mistakes_and_suggestions)
    # Perform the replacement considering word boundaries
    for mistake_word, correct_word in zip(mistakes, suggestions_2d_array):
        sentence = re.sub(r'\b' + re.escape(mistake_word) + r'\b', correct_word, sentence)

    print(f"Correction: {sentence}")  # This will print the corrected sentence

except ApiException as e:
    print(f"Exception when calling API: {e}\n")
