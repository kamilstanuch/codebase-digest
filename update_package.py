import os
import subprocess
import sys
from github import Github
from getpass import getpass
from github.GithubException import GithubException  # Add this import

def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    if process.returncode != 0:
        print(f"Error: {error.decode('utf-8')}")
        sys.exit(1)
    return output.decode('utf-8').strip()

def update_version():
    with open('setup.py', 'r') as f:
        content = f.read()
    
    version_line = [line for line in content.split('\n') if line.strip().startswith('version=')][0]
    current_version = version_line.split('=')[1].strip().strip("'")
    
    print(f"Current version: {current_version}")
    new_version = input("Enter new version number: ")
    
    updated_content = content.replace(f"version='{current_version}'", f"version='{new_version}'")
    
    with open('setup.py', 'w') as f:
        f.write(updated_content)
    
    return new_version

def github_login():
    token = os.environ.get('GITHUB_TOKEN')
    if not token:
        token = getpass("Enter your GitHub personal access token: ")
    
    try:
        g = Github(token)
        user = g.get_user()
        print(f"Logged in as: {user.login}")
        return g
    except Exception as e:
        print(f"GitHub login failed: {str(e)}")
        sys.exit(1)

def ensure_github_remote(github):
    remotes = run_command('git remote -v')
    repo_name = None
    if 'origin' not in remotes:
        repo_name = input("Enter the GitHub repository name: ")
        user = github.get_user()
        repo_url = f"https://github.com/{user.login}/{repo_name}.git"
        run_command(f'git remote add origin {repo_url}')
    else:
        print("Checking if the remote repository exists...")
        try:
            remote_url = run_command('git remote get-url origin')
            repo_name = remote_url.split('/')[-1].replace('.git', '')
            run_command('git ls-remote --exit-code --heads origin main')
        except SystemExit:
            print("The remote repository doesn't exist or you don't have access to it.")
            create_repo = input("Do you want to create a new repository on GitHub? (y/n): ")
            if create_repo.lower() == 'y':
                repo_name = input("Enter the repository name: ")
                user = github.get_user()
                user.create_repo(repo_name)
                new_repo_url = f"https://github.com/{user.login}/{repo_name}.git"
                run_command(f'git remote set-url origin {new_repo_url}')
                print(f"Created new repository: {new_repo_url}")
            else:
                sys.exit(1)
    
    if repo_name is None:
        repo_name = input("Could not determine repository name. Please enter it manually: ")
    
    print(f"GitHub remote 'origin' is set up for repository: {repo_name}")
    return repo_name

def sync_with_remote():
    print("Syncing with remote repository...")
    try:
        run_command('git fetch origin')
        run_command('git merge origin/main --allow-unrelated-histories --no-edit')
    except SystemExit:
        print("There might be merge conflicts. Please resolve them manually and run the script again.")
        print("You can try the following steps:")
        print("1. git pull origin main --allow-unrelated-histories")
        print("2. Resolve any conflicts manually")
        print("3. git add .")
        print("4. git commit -m 'Merge remote changes'")
        print("After resolving conflicts, run this script again.")
        sys.exit(1)

def push_to_remote():
    print("Pushing to GitHub...")
    try:
        run_command('git push -u origin main')
    except SystemExit:
        print("Push failed. Attempting to pull changes first...")
        sync_with_remote()
        print("Trying to push again...")
        run_command('git push -u origin main')

def main():
    # Ensure we're in a git repository
    if not os.path.exists('.git'):
        print("Error: Not in a git repository. Please run this script from your project's root directory.")
        sys.exit(1)

    # Login to GitHub
    github = github_login()

    # Ensure GitHub remote is set up and get repo name
    repo_name = ensure_github_remote(github)

    # Sync with remote before making changes
    sync_with_remote()

    # Update version
    new_version = update_version()

    # Get change description
    change_description = input("Enter a brief description of the changes: ")

    # Commit changes
    run_command('git add .')
    run_command(f'git commit -m "Update to version {new_version}: {change_description}"')

    # Push to GitHub
    push_to_remote()

    # Create GitHub release
    user = github.get_user()
    repo = user.get_repo(repo_name)
    try:
        repo.create_git_release(f"v{new_version}", f"Version {new_version}", change_description)
        print(f"GitHub release created for version {new_version}")
    except GithubException as e:
        if e.status == 403:
            print("Error: Unable to create GitHub release. Your personal access token may not have sufficient permissions.")
            print("Please update your token to include the 'repo' scope:")
            print("1. Go to https://github.com/settings/tokens")
            print("2. Generate a new token or edit the existing one")
            print("3. Ensure the 'repo' scope is selected")
            print("4. Update the token in this script or set it as an environment variable")
        else:
            print(f"An error occurred while creating the GitHub release: {str(e)}")
        print("Continuing with PyPI upload...")
    except Exception as e:
        print(f"An unexpected error occurred while creating the GitHub release: {str(e)}")
        print("Continuing with PyPI upload...")

    # Build and upload to PyPI
    print("Building distribution...")
    run_command('python setup.py sdist bdist_wheel')

    print("Uploading to PyPI...")
    run_command('python -m twine upload dist/*')

    print(f"Package updated to version {new_version} and pushed to GitHub")
    print("Note: If the GitHub release creation failed, please create it manually on the GitHub website.")

if __name__ == "__main__":
    main()