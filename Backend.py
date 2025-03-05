from flask import Flask, request, jsonify, render_template
import requests
import json

app = Flask(__name__)

def generate_response(prompt, model="phi3", temperature=0.7):
    """
    Generate a response from a local Ollama model
    """
    url = "http://localhost:11434/api/generate"
    
    payload = {
        "model": model,
        "prompt": prompt,
        "temperature": temperature
    }
    
    try:
        response = requests.post(url, json=payload, stream=True)
        response.raise_for_status()
        
        # Collect and process the streamed response
        full_response = ""
        for line in response.iter_lines():
            if line:
                json_response = json.loads(line)
                if 'response' in json_response:
                    full_response += json_response['response']
                if json_response.get('done', False):
                    break
                    
        return full_response.strip()
        
    except requests.exceptions.RequestException as e:
        return f"Error: Could not connect to Ollama server: {str(e)}"

@app.route("/")
def home():
    """
    Render the home page
    """
    return render_template("index.html")

@app.route("/generate_cover_letter", methods=["POST"])
def generate_cover_letter():
    """
    Generate a cover letter based on resume and job description
    """
    data = request.json
    resume_text = data.get("resume_text", "")
    job_description = data.get("job_description", "")
    model = data.get("model", "phi3")
    
    prompt = f"""
    You are a professional resume writer and career coach. 
    Generate a personalized cover letter based on the following resume and job description:

    Resume:
    {resume_text}

    Job Description:
    {job_description}

    Requirements for the cover letter:
    - Tailor the letter specifically to the job description
    - Highlight relevant skills and experiences from the resume
    - Use a professional and engaging tone
    - Demonstrate how the candidate's background matches the job requirements
    - Include a strong opening and closing paragraph
    """
    
    response = generate_response(prompt, model=model)
    return jsonify({"cover_letter": response})

@app.route("/resize_resume", methods=["POST"])
def resize_resume():
    """
    Provide guidance on resizing the resume to the target page length
    """
    data = request.json
    resume_text = data.get("resume_text", "")
    target_page_length = data.get("target_page_length", 1)
    model = data.get("model", "phi3")
    
    prompt = f"""
    You are a professional resume editor. 
    The current resume is:
    {resume_text}

    The target page length is {target_page_length} page(s).

    Provide specific, actionable guidance on:
    - Which sections to expand or condense
    - What content to prioritize
    - How to optimize the resume's layout to meet the page length
    - Specific recommendations for trimming or adding content
    - Maintaining the resume's core strengths while meeting the page length requirement

    Your response should be a detailed set of editing instructions.
    """
    
    response = generate_response(prompt, model=model)
    return jsonify({"resume_resizing_guidance": response})

if __name__ == "__main__":
    app.run(debug=True)