import json
import os
import requests

def lambda_handler(event, context):
    # 1. Catch the output from Agent 2
    topic = event.get('topic', 'Unknown Topic')
    research_notes = event.get('research_notes', '')
    
    if not research_notes:
        return {"statusCode": 400, "error": "No research_notes provided in the event payload."}
    
    api_key = os.environ.get('GROQ_API_KEY')
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    # 2. Prompt Engineering for the Synthesizer
    system_prompt = """You are an expert technical writer and synthesizer. 
    You will be given a main topic and a set of raw research notes. 
    Your job is to write a comprehensive, highly professional report in Markdown format.
    
    Structure the report with:
    - A catchy Title (#)
    - An Executive Summary (##)
    - Detailed sections based on the notes (###)
    - A Conclusion (##)
    
    Use bullet points and bold text where appropriate to make it highly readable. Do NOT add any conversational filler (e.g., "Here is your report"). Output ONLY the Markdown text."""
    
    user_prompt = f"Main Topic: {topic}\n\nRaw Research Notes:\n{research_notes}"
    
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
        "temperature": 0.3, # Lower temperature for focused, professional writing
        "max_tokens": 2048  # Give it plenty of room to write the full report
    }
    
    try:
        # 3. Call Groq to write the report
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status() 
        
        result = response.json()
        draft_report = result['choices'][0]['message']['content'].strip()
        
        # 4. Return the payload formatted for Agent 4 (The Reviewer)
        return {
            "statusCode": 200,
            "topic": topic,
            "research_notes": research_notes,
            "draft_report": draft_report
        }
        
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error: {http_err} - Response: {response.text}")
        return {"statusCode": 500, "error": f"API Error: {response.text}"}
    except Exception as e:
        print(f"Error: {e}")
        return {"statusCode": 500, "error": str(e)}