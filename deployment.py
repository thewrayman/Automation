import os
import sys
import shutil
from git import Repo


REPOS = {"nosebot": "NoseBotv2",
         "automation": "Automation"}

DEFAULT_PATH = os.curdir
DEPLOY_PATH = "..\\"


def download_repo(name):
    print(f"Trying to download {name}")
    target_path = os.path.join(DEFAULT_PATH, name)
    Repo.clone_from(f"https://github.com/thewrayman/{name}.git", target_path)
    print(f"Successfully downloaded {name} to {target_path}")
    return target_path


def deploy_repo(name, source_path):
    print(f"Copying {name} to {source_path}")
    target_dir = f"{DEPLOY_PATH}{name}"

    for src_dir, dirs, files in os.walk(source_path):
        dst_dir = src_dir.replace(source_path, target_dir, 1)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        for file_ in files:
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)
            if os.path.exists(dst_file):
                # in case of the src and dst are the same file
                if os.path.samefile(src_file, dst_file):
                    continue
                os.remove(dst_file)
            shutil.move(src_file, dst_dir)


def clean_download(path):
    print(f"Removing download from {path}")
    shutil.rmtree(path)
    print(f"Successfully deleted {path}")


if __name__ == '__main__':
    for arg in sys.argv[1:]:

        git_name = REPOS[arg.lower()]
        download_path = download_repo(git_name)
        deploy_repo(git_name, download_path)
        clean_download(download_path)

        if arg.lower() == "automation":
            # self-update the deployment script
            pass

