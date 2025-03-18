
from log_masker import LogMasker
from typing import Dict, List
def parse_data(path):
    data = load_data(path)
    lines = []
    for line in data:
        lines.append(line)
    return lines
def load_data(file_path):

    with open(file_path, 'r') as file:
        lines = file.readlines()
    return lines

def test():
    data = parse_data('sample.txt')
    masker = LogMasker()
    masked_data = [masker.mask_log_entry(line) for line in data[:10]]
    un_masked_data = [masker.unmask_log_entry(line) for line in masked_data]
    #print(masked_data)
    print(un_masked_data == data[:10])
def main():
    data = parse_data('logs/sample.txt')
    masker = LogMasker()
    dates  : Dict[str, List[str]] = {}
    
    masked_data = [masker.mask_log_entry(line) for line in data]
    for line in masked_data:
        date = (line.split(' ')[0])[1:]
        
        if date not in dates:
            dates[date] = []
        line = line.split(']')[1]
        dates[date].append(line)
    for date in dates:
        with open(f'data/{date}.txt', 'w') as file:
            file.write(f'Date: {date}\n')
            for line in dates[date]:
                file.write(line) 
    # unmasked_data = [masker.unmask_log_entry(line) for line in masked_data]
    # for line in unmasked_data:
    #     print(line)
    

if __name__ == "__main__":
    main()