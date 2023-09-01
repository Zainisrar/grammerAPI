from __future__ import print_function
import ProWritingAidSDK

from ProWritingAidSDK.rest import ApiException
from flask import Flask, render_template, request

app = Flask(__name__)

def configure_pwa():
    configuration = ProWritingAidSDK.Configuration()
    configuration.host = 'https://api.prowritingaid.com'
    configuration.api_key['licenseCode'] = '05919403-4500-45EC-8BB8-BE60F1ED41AB'

    api_client = ProWritingAidSDK.ApiClient()
    api_client.configuration = configuration  # Set the ApiClient's configuration

    return ProWritingAidSDK.TextApi(api_client)

def analyze_grammar(sentence, api_instance):
    api_request = ProWritingAidSDK.TextAnalysisRequest(sentence, ["grammar"], "General", "en")
    api_response = api_instance.post(api_request)
    
    mistakes = []
    suggestions_2d_array = []
    tags = api_response.result.tags
    for tag in tags:
        suggestions = tag.suggestions
        mistakes.append([tag.subcategory])
        suggestions_2d_array.append([suggestions[0]])
    
    return mistakes, suggestions_2d_array

def correct_sentence(sentence, mistakes, suggestions):
    for mistake_word, correct_word in zip(mistakes, suggestions):
        sentence = sentence.replace(mistake_word[0], correct_word[0])
    
    return sentence

@app.route('/chat_start', methods=['GET', 'POST'])
def chat_start():
    if request.method == 'POST':
        sentence = request.form['sentence']
        try:
            api_instance = configure_pwa()
            mistakes, suggestions = analyze_grammar(sentence, api_instance)
            corrected_sentence = correct_sentence(sentence, mistakes, suggestions)
            flat_mistakes = [item for sublist in mistakes for item in sublist]
            return render_template('index.html', original_sentence=sentence, corrected_sentence=corrected_sentence, mistakes=flat_mistakes, suggestions=suggestions)
        except ApiException as e:
            return render_template('index.html', error=str(e))
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
