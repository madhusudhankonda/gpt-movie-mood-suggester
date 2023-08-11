import openai
import os
from dotenv import load_dotenv
from flask import Flask, request, send_from_directory, jsonify

load_dotenv()

openai.api_key = os.getenv("API_KEY")

app = Flask(__name__)

@app.route("/")
def index():
  return "Movie Mood Recommender!"

@app.route('/movie', methods=['POST']) 
def quote():
    data = request.json
    json = jsonify(data)
    age = data.get('age')
    gender = data.get('gender')
    reason = data.get('reason')
    
    prompt = f"""
    You are a good friend who can recommend appropriate, mood-lifting movies when asked.
    A {age} year old {gender} is feeling down due to {reason}.
    Recommend a movie to uplift the mood of this {gender}.
    Do not summarise or provide any other comments other than standard recommendation. 
    You can back up your recommendation by saying why you want that movie for this person.
    """

    return GPTGenerate(prompt)

def GPTGenerate(prompt):
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt},
        ]
    )

    return response.choices[0].message.content

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=81)