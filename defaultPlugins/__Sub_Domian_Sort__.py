import os

def rootDomain(domain):
    rootDomain_path = f"results/{domain}/rootDomain/theHarvester"
    os.makedirs(rootDomain_path, exist_ok=True)

    rootDomain_file_to_read = ["extracted_subdomains.txt"]
    print("[+] Reading root domain subdomains:")
    for file_name in rootDomain_file_to_read:
        file_path = os.path.join(rootDomain_path, file_name)
        if os.path.exists(file_path):
            try:
                with open(file_path, "r") as file:
                    content = file.read()
                    print(content.strip())
            except Exception as e:
                print(f"[!] Error reading {file_name}: {e}")
        else:
            print(f"[!] Skipping {file_name}: File not found.")

def Passive(domain):
    path = f"results/{domain}/fetchSubdomains/"
    passive_path = f"{path}recon_mode/Passive/"
    os.makedirs(passive_path, exist_ok=True)

    Passive_files_to_read = [
        "amass.txt",
        "assetfinder.txt",
        "crt.sh.txt",
        "findomain.txt",
        "subfinder.txt"
    ]

    print("[+] Concatenating files for passive subdomain enumeration:")
    for file_name in Passive_files_to_read:
        file_path = os.path.join(passive_path, file_name)
        if os.path.exists(file_path):
            try:
                with open(file_path, "r") as file:
                    content = file.read()
                    print(content.strip())
            except Exception as e:
                print(f"[!] Error reading {file_name}: {e}")
        else:
            print(f"[!] Skipping {file_name}: File not found.")

def Active(domain):
    path = f"results/{domain}/fetchSubdomains/"
    Active_path = f"{path}recon_mode/Active/"
    os.makedirs(Active_path, exist_ok=True)

    Active_files_to_read = [
        "amass.txt",
        "assetfinder.txt"
    ]

    print("[+] Concatenating files for active subdomain enumeration:")
    for file_name in Active_files_to_read:
        file_path = os.path.join(Active_path, file_name)
        if os.path.exists(file_path):
            try:
                with open(file_path, "r") as file:
                    content = file.read()
                    print(content.strip())
            except Exception as e:
                print(f"[!] Error reading {file_name}: {e}")
        else:
            print(f"[!] Skipping {file_name}: File not found.")

# Entry point
if __name__ == "__main__":
    domain = "docxinfo.site"  # Initialize the domain variable
    rootDomain(domain)
    Passive(domain)
    Active(domain)
