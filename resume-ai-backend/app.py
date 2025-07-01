from flask import Flask, request, jsonify
import openai
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allows frontend to connect

openai.api_key = "YOUR_OPENAI_API_KEY"

@app.route('/improve', methods=['POST'])
def improve_resume():
    data = request.json
    summary = data.get("summary", "")

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You're a resume expert."},
            {"role": "user", "content": f"Improve this resume summary: {summary}"}
        ]
    )

    improved = response['choices'][0]['message']['content']
    return jsonify({"improved": improved})

if __name__ == '__main__':
    app.run(debug=True)
