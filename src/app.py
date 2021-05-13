import os
import json
import requests

from flask import Flask, render_template
from dotenv import load_dotenv
from github import Github

app = Flask(__name__, template_folder='../assets/html', static_folder='../assets')

@app.route('/')
def home():
    return render_template("index.html")
    

#
# note: backend not yet connected to the hosted website
#


load_dotenv()

# app = Flask(__name__)

access_token = os.getenv('TOKEN')
headers = {"Authorization": "token " + access_token}
g = Github(access_token)


# returns a list of my public repos
def get_repos(g: Github) -> list:
    repos = []
    for repo in g.get_user().get_repos():
        if repo.owner.login == g.get_user().login and not repo.private:
            repos.append(repo.name)
    return repos


# returns the description of a repo
def get_desc(g: Github, name: str) -> str:
    return g.get_user().get_repo(name).description


# returns a list of repo topics
def get_topics(g: Github, name: str) -> list:
    return g.get_user().get_repo(name).get_topics()


# returns the link to a repo
def get_repo_url(g: Github, name: str) -> list:
    return g.get_user().get_repo(name).html_url


# returns the result of a GitHub GraphQL API query
def run_query(query):
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))


@app.route('/test', methods=['GET'])
def test():
    return 'testing 1 2 3'

@app.route('/get_projects', methods=['GET'])
def send_projects() -> str:
    query = '''
    {
        user(login: "ngeldvis") {
            pinnedItems(first: 3, types: REPOSITORY) {
                nodes {
                    ... on Repository {
                        name
                    }
                }
            }
        }
    }
    '''

    result = run_query(query)['data']['user']['pinnedItems']['nodes']

    repos = []
    for repo in result:
        repos.append(repo['name'])

    info = []
    for repo in repos:
        desc = get_desc(g, repo)
        topics = get_topics(g, repo)
        url = get_repo_url(g, repo)
        info.append({'name': repo, 'desc': desc, 'url': url, 'topics': topics})

    return json.dumps(info)



# # GET ALL REPO DATA

# # info = []
# # repos = get_repos(g)

# # for repo in repos:
# #     desc = get_desc(g, repo)
# #     topics = get_topics(g, repo)
# #     url = get_repo_url(g, repo)
# #     info.append({'name': repo, 'desc': desc, 'url': url, 'topics': topics})

# # print(json.dumps(info))

# # GET TOP 3 PINNED REPO DATA

# query = '''
# {
#     user(login: "ngeldvis") {
#         pinnedItems(first: 3, types: REPOSITORY) {
#             nodes {
#                 ... on Repository {
#                     name
#                 }
#             }
#         }
#     }
# }
# '''

# result = run_query(query)['data']['user']['pinnedItems']['nodes']

# repos = []
# for repo in result:
#     repos.append(repo['name'])

# info = []
# for repo in repos:
#     desc = get_desc(g, repo)
#     topics = get_topics(g, repo)
#     url = get_repo_url(g, repo)
#     info.append({'name': repo, 'desc': desc, 'url': url, 'topics': topics})

# print(json.dumps(info))

if __name__ == "__main__":
    app.run(debug=True)