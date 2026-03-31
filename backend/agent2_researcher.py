import json
import os
import requests

def lambda_handler(event, context):
    # 1. Catch the output from Agent 1
    topic = event.get('topic', 'Unknown Topic')
    sub_queries = event.get('sub_queries', [])
    
    if not sub_queries:
        return {"statusCode": 400, "error": "No sub_queries provided in the event payload."}
    
    api_key = os.environ.get('GROQ_API_KEY')
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    # 2. Format the sub-queries into a readable list for the LLM
    queries_bulleted = "\n".join([f"- {q}" for q in sub_queries])
    
    # 3. Prompt Engineering for the Researcher
    system_prompt = """You are an expert autonomous research agent. 
    You will be given a main topic and a list of specific search queries. 
    Your job is to simulate a deep web search and provide highly detailed, factual, and comprehensive research notes for each query.
    Do not write an essay. Write structured notes with facts, data points, and context that another agent can use to write a final report."""
    
    user_prompt = f"Main Topic: {topic}\n\nExecute research on these specific queries:\n{queries_bulleted}"
    
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
        "temperature": 0.4, # Slightly higher temperature for content generation
        "max_tokens": 1500  # We need a longer response for detailed notes
    }
    
    try:
        # 4. Call Groq to generate the research
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status() 
        
        result = response.json()
        research_notes = result['choices'][0]['message']['content'].strip()
        
        # 5. Return the payload formatted for Agent 3
        return {
            "statusCode": 200,
            "topic": topic,
            "research_notes": research_notes
        }
        
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error: {http_err} - Response: {response.text}")
        return {"statusCode": 500, "error": f"API Error: {response.text}"}
    except Exception as e:
        print(f"Error: {e}")
        return {"statusCode": 500, "error": str(e)}