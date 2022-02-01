import sys
import subprocess


def install_falcon_packages():
    """
    install_packages : None -> None
    install_packages() Install needed packages with pip. Return None.
    """
    packages_list = ["falcon"]

    try:
        for element in packages_list:
            subprocess.check_call([sys.executable, "-m", "pip", "install", element])

        print("All packages are up to date 🔥")

    except:
        print("Unable to download packages, please check your internet connection and try again. "
              "In case of incompatibility, please upgrade to Python 3.8 or later. "
              "The function is compatible with MacOS 11.0.0, under Windows 10 or under, "
              "please check your installation of Bokeh.io, Pandas.")

    return None




