import os
import subprocess
from urllib.parse import quote


# Validate domain input
def validate_domain(domain):
    if not domain or not isinstance(domain, str) or "." not in domain:
        raise ValueError("[!] Invalid domain provided.")


# Fetches subdomains from crt.sh for the given domain
def crt_sh(domain):
    path = f"results/{domain}/fetchSubdomains/recon_mode/Passive/"
    os.makedirs(path, exist_ok=True)
    output_file = f"{path}crtsh.notfiltered.txt"
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


# Filters subdomains from crt.sh results
def crtsh_filter(domain):
    input_file = f"results/{domain}/fetchSubdomains/recon_mode/Passive/crtsh.notfiltered.txt"
    output_file = f"results/{domain}/fetchSubdomains/recon_mode/Passive/crt.sh.txt"

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


# Removes duplicate lines from a file
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


# Runs passive enumeration with assetfinder
def passive_enum(domain, output_file):
    print("[+] Running passive enumeration with assetfinder...")
    try:
        command = ["assetfinder", "--subs-only", domain]
        with open(output_file, "w") as f:
            subprocess.run(command, stdout=f, check=True)
        print(f"[+] Passive enumeration results saved at: {output_file}")
    except FileNotFoundError:
        print("[!] Assetfinder not installed.")
    except Exception as e:
        print(f"[!] Error running assetfinder: {e}")


# Uses subfinder to enumerate subdomains
def subfinder(domain, output_file):
    print("[+] Running subfinder...")
    try:
        command = ["subfinder", "-d", domain, "-o", output_file]
        subprocess.run(command, check=True)
        print(f"[+] Subfinder results saved at: {output_file}")
    except FileNotFoundError:
        print("[!] Subfinder not installed.")
    except Exception as e:
        print(f"[!] Error running subfinder: {e}")


# Runs findomain for subdomain enumeration
def findomain(domain, output_file):
    print("[+] Running findomain...")
    try:
        command = ["findomain", "-t", domain, "-o"]
        subprocess.run(command, check=True)
        default_output = f"{domain}.txt"
        os.rename(default_output, output_file)
        print(f"[+] Findomain results saved at: {output_file}")
    except FileNotFoundError:
        print("[!] Findomain not installed.")
    except Exception as e:
        print(f"[!] Error running findomain: {e}")


# Runs amass for passive enumeration
def amass(domain, output_file):
    print("[+] Running amass...")
    try:
        command = ["amass", "enum", "-passive", "-d", domain, "-o", output_file]
        subprocess.run(command, check=True)
        print(f"[+] Amass results saved at: {output_file}")
    except FileNotFoundError:
        print("[!] Amass not installed.")
    except Exception as e:
        print(f"[!] Error running amass: {e}")


# Filters and deduplicates Amass results
def amass_filter(domain):
    input_file = f"results/{domain}/fetchSubdomains/recon_mode/Passive/amass-notFilter.txt"
    output_file = f"results/{domain}/fetchSubdomains/recon_mode/Passive/amass.txt"

    print("[+] Filtering and removing duplicates from Amass output...")
    try:
        # Shell-like operations in Python using subprocess
        command = f"cat {input_file} | cut -d ']' -f 2 | awk '{{print $1}}' | sort -u > {output_file}"
        subprocess.run(command, shell=True, check=True)
        print(f"[+] Filtered Amass results saved at: {output_file}")
    except Exception as e:
        print(f"[!] Error during Amass filtering: {e}")

    os.remove(input_file)


# Main function to coordinate enumeration
def main(domain):
    try:
        validate_domain(domain)
        print(f"[+] Starting Passive subdomain enumeration for: {domain}")
        path = f"results/{domain}/fetchSubdomains/recon_mode/Passive/"
        os.makedirs(path, exist_ok=True)

        crt_sh(domain)
        crtsh_filter(domain)

        passive_enum(domain, f"{path}assetfinder.txt")
        subfinder(domain, f"{path}subfinder.txt")
        findomain(domain, f"{path}findomain.txt")
        amass(domain, f"{path}amass-notFilter.txt")
        amass_filter(domain)

    except Exception as e:
        print(f"[!] Error in main: {e}")


# Entry point
if __name__ == "__main__":
    main()
