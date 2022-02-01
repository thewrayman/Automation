import os
import sys
from git import Repo


REPOS = {"nosebot": "https://github.com/thewrayman/NoseBotv2.git",
         "automation": "https://github.com/thewrayman/Automation.git"}

DEFAULT_PATH = os.curdir


def download_repo(url, name):
    target_path = os.path.join(DEFAULT_PATH, name)
    Repo.clone_from(url, target_path)
    return target_path


if __name__ == '__main__':
    for arg in sys.argv[1:]:
        print(f"Trying to download {arg}")
        path = download_repo(REPOS[arg.lower()], "NoseBot")
        print(f"Successfully downloaded {arg}")

        if arg.lower() == "automation":
            # self-update the deployment script
            pass

