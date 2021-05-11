import django
import os
assets\src\app\app\settings.py
from dotenv import load_dotenv
from github import Github
import github

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
