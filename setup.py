#!/usr/bin/python3

import subprocess

def SystemUpgrade():
    subprocess.run(["sudo", "apt", "update"])
    #subprocess.run(["sudo", "apt", "upgrade", "-y"])


def SystemReqTools():
    pass
    




if __name__ == "__main__":
    SystemUpgrade()