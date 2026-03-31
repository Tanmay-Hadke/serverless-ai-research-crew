import json
import os
import requests

def lambda_handler(event, context):
    # 1. Get the topic from the event
    topic = event.get('topic', 'The history and future of solid state batteries')
    
    # 2. Get your API key
    api_key = os.environ.get('GROQ_API_KEY')
    if not api_key:
        return {"statusCode": 500, "error": "GROQ_API_KEY environment variable is missing."}
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    # 3. Prompt Engineering
    system_prompt = """You are an expert research planner. 
    Break the user's topic down into exactly 3 highly targeted web search queries. 
    Output ONLY a valid JSON array of strings. Do not add markdown formatting, conversational text, or explanations. 
    Example Output: ["query 1", "query 2", "query 3"]"""
    
    # 4. Headers and Payload
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "llama-3.1-8b-instant", # <--- UPDATED MODEL ID HERE
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Topic: {topic}"}
        ],
        "temperature": 0.3,
        "max_tokens": 150
    }
    
    try:
        # 5. Call the Groq API
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status() 
        
        result = response.json()
        
        # 6. Extract the text reply
        llm_text = result['choices'][0]['message']['content'].strip()
        
        # 7. Clean up the output in case the LLM added markdown backticks
        if llm_text.startswith("```json"):
            llm_text = llm_text[7:-3].strip()
        elif llm_text.startswith("```"):
            llm_text = llm_text[3:-3].strip()
            
        # 8. Parse into a Python list
        sub_queries = json.loads(llm_text)
        
        return {
            "statusCode": 200,
            "topic": topic,
            "sub_queries": sub_queries
        }
        
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err} - Response: {response.text}")
        return {"statusCode": 500, "error": f"API Error: {response.text}"}
    except Exception as e:
        print(f"Error occurred: {e}")
        return {"statusCode": 500, "error": str(e)}
