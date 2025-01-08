import os
import subprocess

def nmap(domain, output_file):
    """
    Run the Nmap DNS brute-force script to discover subdomains.

    Parameters:
        domain (str): The target domain to scan.
        output_file (str): The file path where the output will be saved.
    """
    print("[+] Running nmap...")

    try:
        # The nmap DNS brute force script does not need a wordlist explicitly passed as a command line argument
        command = ['nmap', '-p', '53', '--script', 'dns-brute', domain, '-oN', output_file]
        subprocess.run(command, check=True)
        print(f"[+] Nmap results saved at: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"[!] Nmap failed with error: {e}")
    except Exception as e:
        print(f"[!] An unexpected error occurred: {e}")

def main(domain):
    """
    Coordinates the subdomain enumeration process.

    Parameters:
        domain (str): The target domain for enumeration.
    """
    

    # Clean domain input to ensure it's properly formatted (removing protocols like http://)

    print(f"[+] Starting Subdomain enumeration for: {domain}")

    # Create directory structure for results
    path = f"results/{domain}/fetchSubdomains/Subdomain_BruteForce/"
    os.makedirs(path, exist_ok=True)

    # Run nmap
    output_file = f"{path}nmap.txt"
    nmap(domain, output_file)

if __name__ == "__main__":
    domain_input = input("Enter the domain to enumerate subdomains: ").strip()
    main(domain_input)
