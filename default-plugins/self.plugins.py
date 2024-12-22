#!/usr/bin/python3

import subprocess

def CurlRoobotsTxt(domain, output_file="robots.txt"):
    subprocess.run(["curl", "-s", f"https://{domain}/robots.txt", "-o", output_file])




if __name__ == "__main__":
    CurlRoobotsTxt("docxinfo.site")