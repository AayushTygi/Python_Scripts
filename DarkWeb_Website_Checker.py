```python
'''
Step 0 - Installing the Tor Browser
Make sure you have Tor Browser installed and running. You can download it here: https://www.torproject.org/download/

NOTE: On Windows, Tor Browser typically listens on port 9150 instead of 9050. Be sure to adjust the proxy config accordingly if you're using Windows.

---

Step 1 - Objective
In this exercise, we’ll write a script that checks whether known Tor hidden services (onion sites) are currently online.

We’ll:
- Load onion URLs from a file (onions.txt)
- Route requests through Tor
- Log the response (live / dead / timeout)
- Append results to a timestamped JSON log for historical tracking
'''

import requests
import json
import time
from datetime import datetime

# Input and Output
input_file = 'onions.txt'
output_file = 'liveness_report.json'


'''
Step 2 - Tor Proxy Setup
To access onion services, we need to route our traffic through the Tor SOCKS5 proxy.
'''

def get_tor_session():
    session = requests.session()
    session.proxies = {'http': 'socks5h://127.0.0.1:9050',
                       'https': 'socks5h://127.0.0.1:9050'}
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/115.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    })
    return session


'''
Step 3 - Reading Onion Links
We’ll read onion links from a text file, one URL per line.
We’ll skip empty lines or comments (lines starting with #).
'''

def read_onions():
    with open(input_file, 'r') as file:
        onions = [line.strip() for line in file if line.strip() and not line.startswith('#')]
    return onions


def normalize_onion(url):
    if url.startswith('http://'):
        return url[7:]
    elif url.startswith('https://'):
        return url[8:]
    return url

'''
Step 4 - Liveness Check
For each onion URL, we’ll send a GET request and record whether it responds or times out.
'''

def check_liveness(session, onion):
    url = 'http://' + onion  # Always use HTTP for .onion

    try:
        r = session.get(url, timeout=30)
        if r.status_code == 200:
            return 'LIVE'
        else:
            return f'ERROR {r.status_code}'
    except requests.exceptions.ConnectTimeout:
        return 'TIMEOUT'
    except requests.exceptions.ConnectionError:
        return 'DOWN'
    except Exception as e:
        return f'EXCEPTION: {str(e)}'

'''
Step 5 - Main Logic Loop
We’ll initialize our session, load the onions, loop through them with short delays, and log results.
'''

def main():
    session = get_tor_session()
    raw_onions = read_onions()
    onions = [normalize_onion(url) for url in raw_onions]
    results = {}

    print(f"Checking {len(onions)} onion services...")

    for onion in onions:
        print(f"Checking: {onion}")
        status = check_liveness(session, onion)
        results[onion] = status
        print(f"Status: {status}")
        time.sleep(1)

    write_output(results)



'''
Step 6 - Writing Results
We’ll store each run under a timestamp key in the JSON file.
This allows you to track changes in site availability over time.
'''

def write_output(new_results):
    timestamp = datetime.utcnow().isoformat()
    try:
        with open(output_file, 'r') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    data[timestamp] = new_results

    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4)

    print(f"\nAppended results under timestamp: {timestamp}")
    print(f"Full historical log saved to {output_file}")


'''
Step 7 - Run the Script
'''

if __name__ == '__main__':
    main()
```
