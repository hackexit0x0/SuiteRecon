import os
import subprocess
from urllib.parse import quote

# Uses subfinder to enumerate subdomains
def nitro(domain, output_file,input_file):
    print("[+] Running Nitro Scan...")
    try:
        command = ["dnsx","-l", input_file, "-silent","-a", "-resp-only","-o", output_file]
        subprocess.run(command, check=True)
        print(f"[+] Subfinder results saved at: {output_file}")
    except FileNotFoundError:
        print("[!] Subfinder not installed.")
    except Exception as e:
        print(f"[!] Error running subfinder: {e}")


# Main function to coordinate enumeration
def main(domain):
    print(f"[+] Starting Sub,Subdomain enumeration for: {domain}")
    path = f"results/{domain}/nitro/"
    os.makedirs(path, exist_ok=True)
    input_file = f"results/{domain}/fetchSubdomains/SubDomains/active.{domain}.txt"
    


    

# Entry point
if __name__ == "__main__":
    main()
