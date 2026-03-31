import json
import os
import requests

def lambda_handler(event, context):
    # 1. Catch the output from Agent 3
    topic = event.get('topic', 'Unknown Topic')
    research_notes = event.get('research_notes', '')
    draft_report = event.get('draft_report', '')
    
    if not draft_report or not research_notes:
        return {"statusCode": 400, "error": "Missing notes or draft in the payload."}
    
    api_key = os.environ.get('GROQ_API_KEY')
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    # 2. Prompt Engineering for the Factual Reviewer
    system_prompt = """You are an expert Senior Editor and Fact-Checker. 
    You will be provided with 'Raw Research Notes' and a 'Draft Report'.
    Your job is to read the Draft Report and verify that EVERY claim made in it is supported by the Raw Research Notes. 
    If the draft contains hallucinations or extra information not found in the notes, remove or rewrite those sections.
    Ensure the final output is beautifully formatted in Markdown. 
    Output ONLY the final revised Markdown text. Do not include your thought process."""
    
    user_prompt = f"Topic: {topic}\n\n--- RAW RESEARCH NOTES ---\n{research_notes}\n\n--- DRAFT REPORT ---\n{draft_report}"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.1, # Extremely low temperature because we want strict factual adherence, not creativity
        "max_tokens": 2048
    }
    
    try:
        # 3. Call Groq to review and finalize the report
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status() 
        
        result = response.json()
        final_report = result['choices'][0]['message']['content'].strip()
        
        # 4. Return the final payload (This will be the final output of our entire Step Function backend)
        return {
            "statusCode": 200,
            "topic": topic,
            "final_report": final_report
        }
        
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error: {http_err} - Response: {response.text}")
        return {"statusCode": 500, "error": f"API Error: {response.text}"}
    except Exception as e:
        print(f"Error: {e}")
        return {"statusCode": 500, "error": str(e)}