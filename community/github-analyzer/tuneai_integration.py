import requests
import json
import os

# Replace this with your actual GitHub API token
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
TUNEAI_TOKEN = os.environ.get("TUNEAI_TOKEN", "")

# Common headers for the API requests
headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

#  Function to fetch repositories for a GitHub user
def get_repositories(user):
    url = f"https://api.github.com/users/{user}/repos"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching repositories for user {user}: {response.status_code}")

# Function to get languages used in a repository
def get_repo_languages(user, repo_name):
    url = f"https://api.github.com/repos/{user}/{repo_name}/languages"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()  # Returns a dictionary of languages with their corresponding LOC
    else:
        raise Exception(f"Error fetching languages for repository {repo_name}: {response.status_code}")

session_user = ""
cache = {}
# Function to get dynamic GitHub data for the user
def get_github_data(user):
    if user in cache:
        print(f"Fetching data for {user} from cache...")
        return cache[user]
    
    repos = get_repositories(user)
    languagesLOC = {}
    repositoryDetails = []

    # Iterate through repositories to fetch relevant details
    for repo in repos:
        repo_name = repo['name']
        repo_languages = get_repo_languages(user, repo_name)
        
        # Aggregate languages and their LOC
        for language, loc in repo_languages.items():
            loc_key = f"{language.lower()}LOC"
            if loc_key in languagesLOC:
                languagesLOC[loc_key] += loc
            else:
                languagesLOC[loc_key] = loc
        
        # Prepare repository details structure
        repo_details = {
            "name": repo_name,
            "languages": list(repo_languages.keys()),
            "stars": repo['stargazers_count'],
            "forks": repo['forks_count'],
            "description": repo.get('description', 'No description'),
            "commits": repo.get('size', 0),  # GitHub API doesn't provide commit count directly
            "lastUpdate": repo['updated_at'][:10]  # Extract date portion of timestamp
        }
        repositoryDetails.append(repo_details)
    
    # Calculate repository stats
    repositoryStats = {
        "numberOfRepos": len(repos),
        "numberOfOpenSourceRepos": len([r for r in repos if not r['private']]),
        "numberOfCommits": sum([r.get('size', 0) for r in repos]),  # Approximation based on repo size
        "numberOfReviews": 0  # This information is not available via API without digging deeper
    }

    # Construct GitHub data in the required format
    github_data = {
        "username": user,
        "languagesLOC": languagesLOC,
        "repositoryStats": repositoryStats,
        "repositoryDetails": repositoryDetails
    }

    cache[user] = github_data
    return github_data


# Function to analyze GitHub profile using TuneAI API
def analyze_github_profile(user_query):
    global session_user
    uname = extract_github_uname(user_query).strip()  # Stripping whitespaces
    print("***********", repr(uname))  # Checking for quotes in the output
    # Remove enclosing quotes if present
    if uname.startswith('"') and uname.endswith('"'):
        uname = uname[1:-1].strip()

    print("User-Name=[", uname,"] Len=[", len(uname), "] SessionUser=[", session_user, "] Len=[",len(session_user),"]")
    if (not uname and not session_user) or (len(uname)>2 and len(uname)<5):
        return "github username not entered. Please provide the github username with whole query"
    elif uname and not session_user:
        session_user = uname
    elif len(session_user) != 0 and len(uname) != 0 and uname != session_user:
        # for switching ctx of user 
        session_user = uname
    else:
        uname = session_user
    
    print("User-Name=[", uname,"] Len=[", len(uname), "] SessionUser=[", session_user, "] Len=[",len(session_user),"]")

    github_data = get_github_data(uname)
    # print(json.dumps(github_data, indent=4))
    # Sample prompt to be sent to TuneAI
    prompt_content = f"You are an extremely experienced developer, a CTO who has given a task to access github-details about a user, being such a senior person in coding industry answer the query: '{user_query}'. Do not over-explain your answer, be brief, short and humane in your response. And always give the response in markdown format\n\n```json\n{json.dumps(github_data, indent=4)}\n```"
    
    # API request payload
    payload = {
        "temperature": 0.8,
        "messages": [
            {
                "role": "system",
                "content": prompt_content
            }
        ],
        "model": "sayak9495/githubGPT-pycon",
        "stream": False,
        "max_tokens": 1200
    }

    # API headers including Authorization token
    headers = {
        "Authorization": f"{TUNEAI_TOKEN}",  # Replace with your actual API key
        "Content-Type": "application/json"
    }

    # Send the API request
    response = requests.post('https://proxy.tune.app/chat/completions', headers=headers, json=payload)
    
    # Parse and return the response
    if response.status_code == 200:
        response_json = response.json()
        # Extract the assistant's response
        return response_json['choices'][0]['message']['content'].replace("*", "")
    else:
        return f"Error: Unable to get a valid response. Status code {response.status_code}"


def extract_github_uname(user_query):
    prompt_content = f"extract plausible github username from this user-query '{user_query}'. Only return the github username, if not found then return empty string."
    
    # API request payload
    payload = {
        "temperature": 0.8,
        "messages": [
            {
                "role": "system",
                "content": prompt_content
            }
        ],
        "model": "openai/gpt-4o-mini",
        "stream": False,
        "max_tokens": 1200
    }

    # API headers including Authorization token
    headers = {
        "Authorization": "sk-tune-LOMAwgqNkU3irH7iCBccSfnrpNlosle862e",  # Replace with your actual API key
        "Content-Type": "application/json"
    }

    # Send the API request
    response = requests.post('https://proxy.tune.app/chat/completions', headers=headers, json=payload)
    
    # Parse and return the response
    if response.status_code == 200:
        response_json = response.json()
        # Extract the assistant's response
        return response_json['choices'][0]['message']['content'].replace("*", "")
    else:
        return f""
