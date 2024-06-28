import argparse
import openai
import os
import requests
from dotenv import load_dotenv
from tqdm import tqdm
import time

# Load environment variables from .env file
load_dotenv()

# Set up OpenAI and Google API keys
openai.api_key = os.getenv('OPENAI_API_KEY')
google_api_key = os.getenv('GOOGLE_API_KEY')
google_cse_id = os.getenv('GOOGLE_CSE_ID')

# ANSI color codes for styling text
class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

# Function to get Google search results using the Custom Search JSON API
def google_search(search_term, api_key, cse_id, **kwargs):
    url = f"https://www.googleapis.com/customsearch/v1?q={search_term}&key={api_key}&cx={cse_id}"
    try:
        response = requests.get(url, params=kwargs, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"{Color.RED}Error during Google search: {e}{Color.END}")
        return {}

# Function to summarize search results using OpenAI
def summarize_text(text):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Summarize the following text:\n\n{text}",
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except openai.error.OpenAIError as e:
        print(f"{Color.RED}Error during OpenAI summarization: {e}{Color.END}")
        return "Could not summarize the text."

# Function to read dorks from file
def load_dorks(file_path):
    try:
        with open(file_path, 'r') as file:
            dorks = file.readlines()
        return [dork.strip() for dork in dorks]
    except FileNotFoundError:
        print(f"{Color.RED}Error: The file {file_path} was not found.{Color.END}")
        return []

def print_header(query):
    header = f"""
{Color.BOLD}{Color.GREEN}
    OSINTGPT - An AI OSINT Tool to find any info online
    Searching: {Color.BOLD}{Color.BLUE}{query}{Color.END}
    """

    print(header)

def main(user_query):
    dorks = load_dorks('dorks.txt')
    
    print_header(user_query)
    
    try:
        for idx, dork in enumerate(tqdm(dorks, desc="Processing dorks"), start=1):
            print(f"{Color.BOLD}{Color.YELLOW}Dork {idx}:{Color.END}\n")
            
            search_term = dork.format(user_query)
            search_results = google_search(search_term, google_api_key, google_cse_id, num=3)
            
            if 'items' in search_results:
                for idx, item in enumerate(search_results['items'][:3], 1):
                    snippet = item['snippet']
                    link = item['link']
                    
                    print(f"{Color.BOLD}{Color.CYAN}Result {idx}:{Color.END}")
                    print(f"{Color.BOLD}Snippet:{Color.END} {snippet}")
                    print(f"{Color.BOLD}Link:{Color.END} {link}")
                    print('-' * 80)
                    time.sleep(1)  # To avoid hitting the rate limit between requests
            
            time.sleep(1)  # To avoid hitting the rate limit between dorks
        
    except KeyboardInterrupt:
        print("\nProcess interrupted by user.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="OSINT tool using Google Dorks.")
    parser.add_argument("query", help="Query for the OSINT search")
    args = parser.parse_args()
    main(args.query)
