from django.shortcuts import render

# Create your views here.


# views.py
import io
import sys
from django.shortcuts import render


from langchain_core.prompts import ChatPromptTemplate


from langchain_groq import ChatGroq
from langchain.chains import LLMChain



#io= We use this module to create an in-memory file-like object (StringIO) that captures output.

# We temporarily redirect the standard output (stdout) to capture print statements and other outputs of the executed code.



PRODUCT_BOT_TEMPLATE = """You are a Python expert. Your goal is to analyze the provided code: {code}, identify any errors in Python, and provide the correct code only.

Rules for output:
- Provide only the Python code
- NO markdown backticks
- NO explanations or comments
- Maintain proper indentation
- Do not include any surrounding text or formatting

Example format:
def example_function():
    x = 5
    return x
"""

def python_ide_view(request):
    code = ""
    result = ""
    response = 'Powerd by Llama 3.1'
    prompt = ChatPromptTemplate.from_template(PRODUCT_BOT_TEMPLATE)

    llm = ChatGroq(model='llama-3.1-70b-versatile', groq_api_key='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')

    
    if request.method == "POST":
        code = request.POST.get("code", "")
        action = request.POST.get("action", "")
        
        if action == "run_code":
            # Handle code execution
            output = io.StringIO()
            sys.stdout = output
            try:
                exec(code)
                result = output.getvalue()
            except Exception as e:
                result = f"Error: {str(e)}"
            finally:
                sys.stdout = sys.__stdout__
                
        elif action == "correct_code":
            # Handle LLM correction
            if code.strip():  # Check if code is not empty or just whitespace
                try:
                    prompt = ChatPromptTemplate.from_template(  
                    PRODUCT_BOT_TEMPLATE
                    )
                    chain = LLMChain(llm=llm, prompt=prompt)
                    response = chain.run(code=code).strip()
                except Exception as e:
                    response = f"Error during code correction: {str(e)}"
            else:
                response = "No code provided for correction."
    context = {
        "code": code,
        "result": result,
        "response": response
    }
    return render(request, "MyApp/home.html", context)