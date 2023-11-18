
import json
import csv
import os
import requests
import time
import pickle
import multiprocessing
import random 

tokens = [
]
payload = {}
headers = {
    'Accept': 'application/vnd.github+json',
    'X-GitHub-Api-Version': '2022-11-28'
}


files = os.listdir('./issues')

repos = []

with open('100_1222_10assignees.csv', 'r') as f:
    d = f.readlines()
    d = d[1:]
    for d1 in d:
        repos.append(d1.split(',')[0])
        
doneFiles = os.listdir('./final')

repos[1:4]
sorted_repos = {}

with open("good_repos", 'rb') as f:
    sorted_repos = pickle.load(f)
repos  = sorted_repos

# for repo in repos:
def scrape(repo):
    file = repo
    repo = repo.split('_')[0] + '/' + '_'.join(repo.split('_')[1:])[:-5]
    print(repo)
    url = "https://api.github.com/repos/" + repo + "/contributors?per_page=100&page="
    done = 0
    contributors = set()
    for i in range(0, 2000):
        urla = url + str(done)
        j = random.randint(1, 60)
        headers["Authorization"] = "Bearer " + tokens[(done + j) % 6]
        response = requests.request("GET", urla, headers=headers)
        if(len(response.text) < 100):
            # print(response.text)
            break
        done += 1
        try:
            for j in json.loads(response.text):
                contributors.add(j["login"])
        except Exception as e:
            print(e)
            print(response.text)
    issues = {}
    with open("issues/" + file, 'r') as f:
        issues = json.load(f)
    contributor_dict = {}
    print(len(contributors))
    print("done contributors")
    for issue in issues:
        if "assignee" not in issue.keys():
            continue
        if issue["assignee"] is None:
            continue
        if issue["labels"] == []:
            continue
        # print(issue["labels"])
        solver = str(issue["assignee"]["login"])
        if solver not in contributor_dict.keys():
            contributor_dict[solver] = {}
            contributor_dict[solver]["labels"] = {}
            contributor_dict[solver]["total"] = 0
        for label in issue["labels"]:
            label = label["name"]
            if label not in contributor_dict[solver]["labels"].keys():
                contributor_dict[solver]["labels"][label] = 0
            contributor_dict[solver]["labels"][label] += 1
        contributor_dict[solver]["total"] += 1
    
    print("done issues")

    for contributor in contributors:
        if contributor not in contributor_dict.keys() or contributor_dict[contributor]["total"] == 0:
            continue 
        url2 = "https://api.github.com/users/" + contributor + "/followers?per_page=100&page="
        followers = []

        # start = time.time_ns()
        done = 0
        for i in range(0, 2000):
            urla = url2 + str(done)
            j = random.randint(1, 60)
            headers["Authorization"] = "Bearer " + tokens[(i + j) % 6]
            response = requests.request("GET", urla, headers=headers, data=payload)
            if(len(response.text) < 100):
                # print(response.text)
                break
            try:
                for j in json.loads(response.text):
                    # print('h')
                    if j["login"] == contributor:
                        continue
                    followers.append(j["login"])
            except Exception as e:
                print(e)
                print(response.text)
            done += 1
        # print(time.time_ns() - start)
        # print(len(followers))

        # print(followers)
        if contributor not in contributor_dict.keys():
            contributor_dict[contributor] = {}
            contributor_dict[contributor]["labels"] = {}
            contributor_dict[contributor]["total"] = 0
        contributor_dict[contributor]["followers"] = followers
    # print(contributor_dict)
    with open("final/" + file[:-5], 'wb') as f:
        pickle.dump(contributor_dict, f)

    print("Total Contributors: " + str(len(contributors)))
    with open("final/" + file[:-5], 'wb') as f:
        pickle.dump(contributor_dict, f)

repos_final = []
for repo in repos:
    if repo[1][0] < 500:
        continue
    repoa = repo[0]
    repo = repo[0]
    file = repo
    repo = repo.split('_')[0] + '/' + '_'.join(repo.split('_')[1:])[:-5]
    if file not in files:
        continue
    if file[:-5] in doneFiles:
        continue
    repos_final.append(repoa)
print(repos_final)

p = multiprocessing.Pool(20)
p.map(scrape, repos_final)
