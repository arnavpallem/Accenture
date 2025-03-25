# Work Log Summarizer



The following is an AI system to parse a noisy log. It cleans the data by masking sensitive information like emails and IP addresses and splits the data up by date. It then uses a Tree Summarizer from llamaIndex to query and effectively summarize each day's log. Then, the sensitive information is added back in. 
