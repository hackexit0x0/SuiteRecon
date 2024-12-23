import os
import subprocess
from urllib.parse import quote


def crt_sh(domain):
    path = f"results/{domain}/fetchSubdomains/recon_mode/Passive/"
    os.makedirs(path, exist_ok=True)
    output_file = f"{path}/crt.sh.txt"
    encoded_domain = quote(domain)
    url = f"https://crt.sh/?q={encoded_domain}"

    print("[+] Fetching data from crt.sh...")
    try:
        curl_command = ["curl", "-s", url]
        grep_command = ["grep", "-oE", r"[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"]

        with open(output_file, "w") as f:
            curl_process = subprocess.Popen(curl_command, stdout=subprocess.PIPE)
            grep_process = subprocess.Popen(grep_command, stdin=curl_process.stdout, stdout=f)
            curl_process.stdout.close()
            grep_process.communicate()

        print(f"[+] Subdomains saved at: {output_file}")
    except FileNotFoundError as e:
        print(f"[!] Missing required tool: {e}")
    except Exception as e:
        print(f"[!] Error fetching data from crt.sh: {e}")


def crtsh_filter(domain):
    input_file = f"results/{domain}/fetchSubdomains/recon_mode/Passive/crt.sh.txt"
    output_file = f"results/{domain}/fetchSubdomains/recon_mode/Passive/crtsh.txt"

    print("[+] Filtering subdomains...")
    try:
        with open(input_file, "r") as file:
            data = file.readlines()

        matching_domains = {line.strip() for line in data if domain in line.strip()}

        with open(output_file, "w") as file:
            file.write("\n".join(matching_domains))

        os.remove(input_file)
        print(f"[+] Filtered subdomains saved at: {output_file}")
    except Exception as e:
        print(f"[!] Error during filtering: {e}")


def remove_duplicates(file_path):
    print(f"[+] Removing duplicates from {file_path}...")
    try:
        with open(file_path, "r") as infile:
            lines = sorted(set(infile.readlines()))
        with open(file_path, "w") as outfile:
            outfile.writelines(lines)
        print("[+] Duplicates removed.")
    except Exception as e:
        print(f"[!] Error removing duplicates: {e}")


def passive_enum(domain, output_file):
    print("[+] Running passive enumeration with assetfinder...")
    try:
        command = ["assetfinder", "--subs-only", domain]
        with open(output_file, "w") as f:
            subprocess.run(command, stdout=f, check=True)
        print(f"[+] Passive enumeration results saved at: {output_file}")
    except FileNotFoundError:
        print("[!] Assetfinder not installed or not in PATH.")
    except Exception as e:
        print(f"[!] Error running assetfinder: {e}")


def subfinder(domain, output_file):
    print("[+] Running subfinder...")
    try:
        command = ["subfinder", "-d", domain, "-o", output_file]
        subprocess.run(command, check=True)
        print(f"[+] Subfinder results saved at: {output_file}")
    except FileNotFoundError:
        print("[!] Subfinder not installed or not in PATH.")
    except Exception as e:
        print(f"[!] Error running subfinder: {e}")


def amass(domain, output_file):
    print("[+] Running amass...")
    try:
        command = ["amass", "enum", "-passive", "-d", domain, "-o", output_file]
        subprocess.run(command, check=True)
        print(f"[+] Amass results saved at: {output_file}")
    except FileNotFoundError:
        print("[!] Amass not installed or not in PATH.")
    except Exception as e:
        print(f"[!] Error running amass: {e}")


def amass_filter(domain):
    input_file = f"results/{domain}/fetchSubdomains/recon_mode/Passive/amass-notFilter.{domain}.txt"  # Corrected filename
    output_file = f"results/{domain}/fetchSubdomains/recon_mode/Passive/amass.{domain}.txt"  # Corrected filename

    print("[+] Filtering and removing duplicates from Amass output...")
    try:
        # Shell-like operations in Python using subprocess
        command = f"cat {input_file} | cut -d ']' -f 2 | awk '{{print $1}}' | sort -u > {output_file}"
        subprocess.run(command, shell=True, check=True)
        print(f"[+] Filtered Amass results saved at: {output_file}")
    except Exception as e:
        print(f"[!] Error during Amass filtering: {e}")

    os.remove(input_file)  # Removing the correct file
        

def main(domain):
    print(f"[+] Starting subdomain enumeration for: {domain}")
    
    # Create a directory for results
    path = f"results/{domain}/fetchSubdomains/recon_mode/Passive"
    os.makedirs(path, exist_ok=True)

    # Paths for saving the output
    assetfinder_output_file = f"{path}/assetfinder.{domain}.txt"
    subfinder_output_file = f"{path}/subfinder.{domain}.txt"
    amass_output_file = f"{path}/amass.{domain}.txt"

    # Start the process
    crt_sh(domain)
    crtsh_filter(domain)
    remove_duplicates(f"results/{domain}/fetchSubdomains/recon_mode/Passive/crtsh.txt")
    
    # Run passive enumeration first
    passive_enum(domain, assetfinder_output_file)
    
    # Then run subfinder
    subfinder(domain, subfinder_output_file)
    
    # Run amass
    amass(domain, amass_output_file)

    # Run filtering for amass results
    amass_filter(domain)


if __name__ == "__main__":
    domain = "meesho.com"
    main(domain)
