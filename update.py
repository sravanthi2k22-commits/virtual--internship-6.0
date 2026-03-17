import subprocess
from datetime import datetime

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

        if result.stdout:
            print(result.stdout.strip())

        if result.stderr:
            print("Error:", result.stderr.strip())

        return result.returncode == 0

    except Exception as e:
        print("Exception occurred:", e)
        return False


def update_project():
    print("\n=== Git Auto Update Started ===\n")

    # 1. Check status
    print("Checking git status...\n")
    run_git_command("git status")

    # 2. Add changes
    print("\nAdding changes...\n")
    if not run_git_command("git add ."):
        print("Failed to add changes.")
        return

    # 3. Commit changes
    commit_message = f"Auto update - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    print("\nCommitting changes...\n")

    commit_success = run_git_command(f'git commit -m "{commit_message}"')

    if not commit_success:
        print("Nothing to commit or commit failed.")

    # 4. Pull latest changes BEFORE pushing (IMPORTANT)
    print("\nPulling latest changes (rebase)...\n")
    pull_success = run_git_command("git pull origin main --rebase")

    if not pull_success:
        print("\n❌ Pull failed. Likely due to merge conflicts.")
        print("👉 Fix conflicts manually, then run:")
        print("   git add .")
        print("   git rebase --continue")
        print("   git push origin main")
        return

    # 5. Push changes
    print("\nPushing to remote...\n")
    push_success = run_git_command("git push origin main")

    if push_success:
        print("\n✅ Project successfully updated to GitHub!")
    else:
        print("\n❌ Push failed.")


if __name__ == "__main__":
    update_project()