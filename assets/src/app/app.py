import django
import os
import json

from dotenv import load_dotenv
from github import Github


#
# note: backend not yet connected to the hosted website
#


load_dotenv()

access_token = os.getenv('TOKEN')
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

def get_repo_url(g: Github, name: str) -> list:
    return g.get_user().get_repo(name).html_url


info = []
repos = get_repos(g)

for repo in repos:
    desc = get_desc(g, repo)
    topics = get_topics(g, repo)
    url = get_repo_url(g, repo)
    info.append({'name': repo, 'desc': desc, 'url': url, 'topics': topics})

print(json.dumps(info))
