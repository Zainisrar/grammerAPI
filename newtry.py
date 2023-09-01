from flask import Flask, request, render_template
import re
import ProWritingAidSDK
from ProWritingAidSDK.rest import ApiException

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        sentence = request.form['query']

        configuration = ProWritingAidSDK.Configuration()
        configuration.host = 'https://api.prowritingaid.com'
        configuration.api_key['licenseCode'] = '05919403-4500-45EC-8BB8-BE60F1ED41AB'

        api_instance = ProWritingAidSDK.TextApi(ProWritingAidSDK.ApiClient('https://api.prowritingaid.com'))
        
        try:
            api_request = ProWritingAidSDK.TextAnalysisRequest(sentence, ["grammar"], "General", "en")
            api_response = api_instance.post(api_request)

            tags = api_response.result.tags
            suggestions_2d_array = []
            mistakes = []

            for tag in tags:
                suggestions = tag.suggestions
                mistakes.append(tag.subcategory)
                suggestions_2d_array.append(suggestions[0])
            mistakes_and_suggestions = list(zip(mistakes, suggestions_2d_array))
            highlighted_sentence = sentence

            for mistake_word in mistakes:
                highlighted_sentence = re.sub(r'\b' + re.escape(mistake_word) + r'\b', f'<span class="highlight">{mistake_word}</span>', highlighted_sentence)

            for mistake_word, correct_word in zip(mistakes, suggestions_2d_array):
                sentence = re.sub(r'\b' + re.escape(mistake_word) + r'\b', correct_word, sentence)
            return render_template('UI.html', original_sentence=highlighted_sentence, corrected_sentence=sentence,mistakes=mistakes,mistakes_and_suggestions=mistakes_and_suggestions)

        except ApiException as e:
            return f"Exception when calling API: {e}"

    return render_template('UI.html')

if __name__ == '__main__':
    app.run(debug=True)
