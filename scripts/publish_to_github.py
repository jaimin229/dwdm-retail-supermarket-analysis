"""
GitHub Publishing Script - FreshMart Supermarket DWDM Project
Automates public repository creation and git push using stored credentials.
"""

import os
import sys
import subprocess
import requests
import win32cred

if sys.stdout:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr:
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# 1. Retrieve GitHub credential from Windows Credential Manager
cred = win32cred.CredRead('gh:github.com:Jaimin-prajapati-ds', 1)
token = cred['CredentialBlob'].decode('utf-8', errors='ignore').strip()

headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json'
}

# 2. Get user info
user_resp = requests.get('https://api.github.com/user', headers=headers)
if user_resp.status_code != 200:
    print(f"[ERROR] Failed to authenticate with GitHub API: {user_resp.status_code} {user_resp.text}")
    sys.exit(1)

username = user_resp.json().get('login')
print(f"[AUTH] Authenticated as GitHub user: {username}")

repo_name = 'dwdm-retail-supermarket-analysis'
repo_desc = 'Innovative Assignment for Data Warehouse and Data Mining (4040233302) at Silver Oak College of Computer Application. End-to-end retail store analysis featuring Star Schema, OLAP Cubes, Apriori, Decision Trees, and K-Means clustering.'

# 3. Check if repo already exists
repo_url_check = f'https://api.github.com/repos/{username}/{repo_name}'
check_resp = requests.get(repo_url_check, headers=headers)

if check_resp.status_code == 200:
    print(f"[INFO] Repository '{repo_name}' already exists on GitHub.")
    # Ensure it is public
    if check_resp.json().get('private'):
        print("[INFO] Setting repository to public visibility...")
        patch_resp = requests.patch(repo_url_check, headers=headers, json={'private': False})
        print(f"[INFO] Visibility update status: {patch_resp.status_code}")
else:
    print(f"[INFO] Creating public repository '{repo_name}'...")
    create_payload = {
        'name': repo_name,
        'description': repo_desc,
        'private': False,
        'has_issues': True,
        'has_projects': True,
        'has_wiki': False
    }
    create_resp = requests.post('https://api.github.com/user/repos', headers=headers, json=create_payload)
    if create_resp.status_code in [200, 201]:
        print(f"[SUCCESS] Public repository created: https://github.com/{username}/{repo_name}")
    else:
        print(f"[ERROR] Failed to create repository: {create_resp.status_code} {create_resp.text}")
        sys.exit(1)

# 4. Git staging and commit
print("\n[GIT] Configuring local git repository...")
subprocess.run(['git', 'config', 'user.name', 'Jaimin-prajapati-ds'], check=True)
subprocess.run(['git', 'config', 'user.email', 'jaiminadac@gmail.com'], check=True)

subprocess.run(['git', 'add', '.'], check=True)

# Commit changes if any
status_output = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True).stdout
if status_output.strip():
    print("[GIT] Committing changes...")
    subprocess.run(['git', 'commit', '-m', 'Complete DWDM Innovative Assignment: Real-world retail store data warehouse and data mining analysis'], check=True)
else:
    print("[GIT] Nothing new to commit.")

subprocess.run(['git', 'branch', '-M', 'main'], check=True)

# 5. Remote and Push
authenticated_remote = f'https://{username}:{token}@github.com/{username}/{repo_name}.git'
clean_remote = f'https://github.com/{username}/{repo_name}.git'

# Set remote to authenticated URL temporarily for push
remotes = subprocess.run(['git', 'remote'], capture_output=True, text=True).stdout.split()
if 'origin' in remotes:
    subprocess.run(['git', 'remote', 'set-url', 'origin', authenticated_remote], check=True)
else:
    subprocess.run(['git', 'remote', 'add', 'origin', authenticated_remote], check=True)

print(f"\n[GIT] Pushing main branch to GitHub...")
push_res = subprocess.run(['git', 'push', '-u', 'origin', 'main', '--force'], capture_output=True, text=True)

# Sanitize remote URL back to clean HTTPS immediately so token is never kept on disk
subprocess.run(['git', 'remote', 'set-url', 'origin', clean_remote], check=True)

if push_res.returncode == 0:
    print(f"[SUCCESS] Code pushed successfully!")
    print(f"\n================================================================================")
    print(f"  PUBLIC GITHUB REPOSITORY LIVE AT:")
    print(f"  https://github.com/{username}/{repo_name}")
    print(f"================================================================================")
else:
    print(f"[ERROR] Git push failed:")
    print(push_res.stderr)
    sys.exit(1)
