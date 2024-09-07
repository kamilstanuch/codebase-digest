import os
import subprocess
import sys
from github import Github
from getpass import getpass

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

def main():
    # Ensure we're in a git repository
    if not os.path.exists('.git'):
        print("Error: Not in a git repository. Please run this script from your project's root directory.")
        sys.exit(1)

    # Login to GitHub
    github = github_login()

    # Update version
    new_version = update_version()

    # Get change description
    change_description = input("Enter a brief description of the changes: ")

    # Commit changes
    run_command('git add .')
    run_command(f'git commit -m "Update to version {new_version}: {change_description}"')

    # Push to GitHub
    print("Pushing to GitHub...")
    run_command('git push origin main')

    # Create GitHub release
    repo = github.get_user().get_repo('codeconsolidator')
    repo.create_git_release(f"v{new_version}", f"Version {new_version}", change_description)

    # Build and upload to PyPI
    print("Building distribution...")
    run_command('python setup.py sdist bdist_wheel')

    print("Uploading to PyPI...")
    run_command('python -m twine upload dist/*')

    print(f"Package updated to version {new_version} and pushed to GitHub and PyPI")

if __name__ == "__main__":
    main()