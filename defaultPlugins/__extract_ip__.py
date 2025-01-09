import os
import subprocess
from urllib.parse import quote


# Validate domain input
def validate_domain(domain):
    if not domain or not isinstance(domain, str) or "." not in domain:
        raise ValueError("[!] Invalid domain provided.")



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






# Entry point
if __name__ == "__main__":
    main()
