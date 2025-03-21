from flask import Flask, request, render_template
import webbrowser
import os, json, ast
import openai
from tenacity import retry, wait_random_exponential, stop_after_attempt
import pandas as pd
from IPython.display import display, HTML
import openai
import pandas as pd

app = Flask(__name__)

# Set your OpenAI API key here
#openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = "key"
print(f"OpenAI API Key: {openai.api_key}") #add this line.

def generate_prompt(budget, data_required, sms_required, download_speed, upload_speed, cloud_storage, hotspot_data, df):
    """Generates a prompt for OpenAI to suggest the best plans."""
    plan_data = df.to_dict(orient='records')
    prompt = f"""
    You are a telecom expert. A user is looking for a mobile plan based on their preferences:
    - Budget: ${budget} USD
    - Minimum Data Required: {data_required}
    - Minimum SMS Required: {sms_required}
    - Minimum Download Speed: {download_speed} Mbps
    - Minimum Upload Speed: {upload_speed} Mbps
    - Cloud Storage Required: {cloud_storage}
    - Minimum Hotspot Data: {hotspot_data}
    
    Given the following plan options:
    {plan_data}
    
    Suggest the top 3 most suitable plans based on the user's preferences.
    Provide the results in JSON format with fields: Brand, Plan Name, Monthly Cost (USD), Data Allowance, Talk Time, SMS, Max Download Speed (Mbps), Max Upload Speed (Mbps), Cloud Storage, Hotspot Data (GB), and Plan Description.
    """
    return prompt

def get_openai_response(prompt):
    """Fetches response from OpenAI API using ChatCompletion."""
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # or use the model of your choice
        messages=[
            {"role": "system", "content": "You are a telecom expert who suggests plans based on user needs."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Collect user preferences from the form
        budget = float(request.form["budget"])
        data_required = request.form["data_required"]
        sms_required = request.form["sms_required"]
        download_speed = request.form["download_speed"]
        upload_speed = request.form["upload_speed"]
        cloud_storage = request.form["cloud_storage"]
        hotspot_data = request.form["hotspot_data"]

        # Load your telecom dataset
        csv_path = "telecomData1.csv"  # Ensure this CSV is in your project folder
        df = pd.read_csv(csv_path)

        # Generate the prompt and get the OpenAI response
        prompt = generate_prompt(budget, data_required, sms_required, download_speed, upload_speed, cloud_storage, hotspot_data, df)
        response = get_openai_response(prompt)

        return render_template("index.html", response=response)
    else:
        return render_template("index.html", response=None)

if __name__ == "__main__":
        webbrowser.open("http://127.0.0.1:5000")  # Opens browser automatically
        app.run(debug=True)

