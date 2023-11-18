import requests
import os
import time
files_done = os.listdir('./issues')
print(files_done)
time.sleep(1)
tokens = [
]

filename  = "100_1222_10assignees.csv"
import csv
with open (filename, 'r') as f:
    reader = csv.reader(f)
    data = list(reader)
data = data[1:]
print(data[0])
for repo in data:
    # repo = ["v2board/v2board", 1]
    f = repo[0].split('/')[0] + "_" + repo[0].split('/')[1] + ".json"
    print(f)
    if f in files_done:
        continue
    print(repo[0])
    url = "https://api.github.com/repos/" + repo[0] + "/issues?per_page=100&state=closed&page="
    payload = {}
    headers = {
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28'
    }
    res = []
    import json
    import time
    done = 0
    issue_count = 0
    for i in range(1, 20050):
        urla = url + str(i)
        response = requests.request("GET", urla, headers=headers, data=payload)
        headers["Authorization"] = "Bearer " + tokens[done % 5]
        if done < 10:
            print(len(response.text))
        if(len(response.text) < 10):
            print(response.text)
            break
        # res += json.loads(response.text)
        done += 1
        if issue_count > 4000:
            break
        try:
            for i in json.loads(response.text):
                if 'pull_request' not in i.keys():
                    issue_count += 1
                    res.append(i)
                # print(res)
            f = repo[0].split('/')[0] + "_" + repo[0].split('/')[1]
            with open('issues/' + f + '.json', 'w') as f:
                json.dump(res, f)
        except Exception as e:
            print(e)
            print(response.text)

    # print(response.text)
    print(done)