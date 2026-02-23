import subprocess
import os
from datetime import datetime

# Root project path
PROJECT_PATH = r"D:\log-analytics-monitoring-engine"

def run_git_command(command):
    try:
        result = subprocess.run(
            command,
            cwd=PROJECT_PATH,
            shell=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.stderr:
            print("Error:", result.stderr)
        return result.returncode == 0
    except Exception as e:
        print("Exception occurred:", e)
        return False


def update_project():
    print("Checking git status...\n")

    # 1. Check status
    if not run_git_command("git status"):
        return

    # 2. Add all changes (including backend/config, schema, ingection)
    print("\nAdding changes...\n")
    if not run_git_command("git add ."):
        return

    # 3. Commit with timestamp
    commit_message = f"Auto update - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    print("\nCommitting changes...\n")
    if not run_git_command(f'git commit -m "{commit_message}"'):
        print("Nothing to commit (maybe no changes).")

    # 4. Push to remote
    print("\nPushing to remote...\n")
    run_git_command("git push")


if __name__ == "__main__":
    update_project()