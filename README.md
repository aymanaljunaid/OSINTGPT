# OSINTGPT
OSINTGPT is a tool designed to gather OSINT (Open Source Intelligence) information about individuals using Google Dorks. This tool leverages the Google Custom Search API and OpenAI API to fetch and summarize public information from the web.

## Features

- Searches for publicly available information about individuals on social media and other platforms.
- Summarizes search results using OpenAI.
- Displays results in a user-friendly, modern format.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/aymanaljunaid/OSINTGPT.git
   ```
   ```bash
   cd OSINTGPT
   ```

2. Install the requirements:
  ```bash
  pip install -r requirements.txt
  ```

3. Edit the .env file in the project directory with your API keys:
   ```bash
   GOOGLE_API_KEY=your_google_api_key
   GOOGLE_CSE_ID=your_google_cse_id
   OPENAI_API_KEY=your_openai_api_key
   ```
##Usage

1. You can edit the dorks.txt file in the project directory and add more Google Dorks if you want.
2. Run the tool:
   ```bash
   python3 osint_tool.py "John Doe"
   ```

##Disclaimer
This tool is designed to gather information that is publicly available. Please use it responsibly and ethically.
