import os
import subprocess
from urllib.parse import quote

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


# Main function to coordinate enumeration
def main(domain):
    print(f"[+] Starting Sub,Subdomain enumeration for: {domain}")
    path = f"results/{domain}/fetchSubdomains/Sub.Subfinder/"
    os.makedirs(path, exist_ok=True)


    subfinder(domain, f"{path}subfinder.txt")

# Entry point
if __name__ == "__main__":
    main()
