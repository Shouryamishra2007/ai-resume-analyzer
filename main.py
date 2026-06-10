from pypdf import PdfReader
from groq import Groq

client = Groq(
        api_key=""
    )

def extract_resume_text():
    reader = PdfReader("resume.pdf")
    text = ""

    for page in reader.pages:
        text += page.extract_text()
    return text

def analyze_resume(prompt, text):
    
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"""
    {prompt}
                resume: {text}
    """

            }
        ],
        model= "llama-3.3-70b-versatile"
    )
    print("PROMPT", prompt[:50])
    print("TEXT", text[:50])
    return chat_completion
    

def save_analysis(chat_completion):
    content = chat_completion.choices[0].message.content

    with open("analysis.txt", "w", encoding="utf-8") as file:
        file.write(content)
        print(content)

try:
    prompt = input("Enter analysis prompt: ")
    resume_text = extract_resume_text()
    chat_completion = analyze_resume(prompt, resume_text)
    save_analysis(chat_completion)
    print("analysis saved successfully")

except Exception as e:
    print("Error:", e)
