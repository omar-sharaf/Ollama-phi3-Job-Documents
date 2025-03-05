import requests
import json

def generate_cover_letter(resume_text, job_description, model='phi3'):
    """
    Generate a cover letter using Ollama's Phi3 model.
    
    Args:
        resume_text (str): Text from the resume
        job_description (str): Description of the job position
        model (str): Name of the Ollama model to use
    
    Returns:
        str: Generated cover letter
    """
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
    return response

def resize_resume(resume_text, target_page_length, model='phi3'):
    """
    Provide guidance on resizing the resume to the target page length.
    
    Args:
        resume_text (str): Text of the original resume
        target_page_length (int): Desired number of pages for the resume
        model (str): Name of the Ollama model to use
    
    Returns:
        str: Guidance on how to resize the resume
    """
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
    return response

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

def get_user_input():
    """
    Collect user inputs for resume, job description, and target page length.
    
    Returns:
        tuple: (resume_text, job_description, target_page_length)
    """
    print("=== Resume Tailoring Tool ===")
    
    # Get resume text
    print("\nPlease paste your resume text (type 'END' on a new line when finished):")
    resume_text = ""
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        resume_text += line + "\n"
    
    # Get job description
    print("\nPlease paste the job description (type 'END' on a new line when finished):")
    job_description = ""
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        job_description += line + "\n"
    
    # Get target page length
    while True:
        try:
            target_page_length = int(input("\nEnter the target resume length (number of pages): "))
            if target_page_length > 0:
                break
            else:
                print("Please enter a positive number.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    return resume_text.strip(), job_description.strip(), target_page_length

def main():
    # Get user inputs
    resume_text, job_description, target_page_length = get_user_input()

    # Generate cover letter
    print("\n--- Generating Cover Letter ---")
    cover_letter = generate_cover_letter(resume_text, job_description)
    print("\nGenerated Cover Letter:")
    print(cover_letter)

    # Resize resume
    print("\n--- Resume Resizing Guidance ---")
    resume_resizing_guidance = resize_resume(resume_text, target_page_length)
    print("\nResume Resizing Guidance:")
    print(resume_resizing_guidance)

if __name__ == '__main__':
    main()