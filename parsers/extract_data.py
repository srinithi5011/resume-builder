import re
import os
from PyPDF2 import PdfReader

def extract_resume_data(filepath):
    """
    Extract basic fields like name, email, LinkedIn, GitHub, summary from the uploaded resume.
    This is a simple example using regex and PDF text extraction.
    """
    data = {
        "name": "",
        "email": "",
        "linkedin": "",
        "github": "",
        "summary": ""
    }

    try:
        if filepath.endswith(".pdf"):
            reader = PdfReader(filepath)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"

            # Extract fields using regex
            email_match = re.search(r'[\w\.-]+@[\w\.-]+', text)
            linkedin_match = re.search(r'(https?://)?(www\.)?linkedin\.com/in/[^\s]+', text)
            github_match = re.search(r'(https?://)?(www\.)?github\.com/[^\s]+', text)

            data["email"] = email_match.group(0) if email_match else ""
            data["linkedin"] = linkedin_match.group(0) if linkedin_match else ""
            data["github"] = github_match.group(0) if github_match else ""
            
            # Just take first 2 lines as a "summary" for now
            lines = text.strip().split("\n")
            data["name"] = lines[0].strip() if len(lines) > 0 else ""
            data["summary"] = " ".join(lines[1:3]).strip()

    except Exception as e:
        print("Error parsing resume:", e)

    return data
