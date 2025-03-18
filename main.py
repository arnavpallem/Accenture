# This is the main file for the log cleaning application.
# It will take a log file as input and output a summary of the data.
# The LLM used is OpenAI's GPT 4-o mini.
#pip install openai
#pip install llama-index
from openai import OpenAI
from dotenv import load_dotenv
from data_cleaning import LogMasker, parse_data
import os
from typing import Dict, List
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.core.response_synthesizers import TreeSummarize

def run_summarize():
    load_dotenv()
    os.environ['OPENAI_API_KEY'] = os.getenv('API_KEY')
    documents = SimpleDirectoryReader('./data').load_data()
    summarizer = TreeSummarize()
    responses = []
    for i in range(len(documents)):
        response = summarizer.get_response('''For each document, return a list of users who logged in and logged out. Also provide a list of specific 
                                        key errors and key warnings that occurred. Remove any redundancies. If there are unauthorized accesses, provide the IP address.
                                           If there are unusual login attempts, provide the user or IP address. 
                                        Return your response in this form:
                                        Date: [date]
                                        Users who logged in: [list of users]
                                        Users who logged out: [list of users]
                                        Errors: [list of key errors]
                                        Warnings: [list of key warnings]
                                        
        ''', [documents[i].text])
        
        responses.append(response)
    return responses
def main():
    logs = os.listdir('logs')
    
    data : List[str] = []
    for log in logs:
        temp : List[str] = parse_data(f'logs/{log}')
        data.extend(temp)
    masker = LogMasker()
    dates  : Dict[str, List[str]] = {}
        
    masked_data = [masker.mask_log_entry(line) for line in data]
    for line in masked_data: #Splits data up by day and removes redundant date information
        date = (line.split(' ')[0])[1:]
        
        if date not in dates:
            dates[date] = []
        line = line.split(']')[1]
        dates[date].append(line)
    for date in dates: #Makes document for each day
        with open(f'data/{date}.txt', 'w') as file:
            file.write(f'Date: {date}\n')
            for line in dates[date]:
                file.write(line) 
    response = run_summarize() #List of summaries for each document
    for i in range(len(response)):
        response[i] = masker.unmask_log_entry(response[i])
        print(response[i])
        
    return
    
if __name__ == "__main__":
    main()
