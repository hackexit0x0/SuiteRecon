import os

def create_directory(path):
    """Create a directory if it doesn't exist."""
    os.makedirs(path, exist_ok=True)

def read_file(file_path):
    """Read a file and return its content."""
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as file:
                return file.read().strip().splitlines()
        except Exception as e:
            print(f"[!] Error reading {file_path}: {e}")
            return []
    else:
        print(f"[!] Skipping {file_path}: File not found.")
        return []

def rootDomain(domain, output_list):
    """Process root domain subdomains."""
    rootDomain_path = f"results/{domain}/rootDomain/theHarvester"
    create_directory(rootDomain_path)

    files_to_read = ["extracted_subdomains.txt"]
    print("[+] Reading root domain subdomains:")
    for file_name in files_to_read:
        file_path = os.path.join(rootDomain_path, file_name)
        content = read_file(file_path)
        if content:
            output_list.extend(content)

def Passive(domain, output_list):
    """Process passive subdomain enumeration results."""
    passive_path = f"results/{domain}/fetchSubdomains/recon_mode/Passive/"
    create_directory(passive_path)

    files_to_read = [
        "amass.txt",
        "assetfinder.txt",
        "crt.sh.txt",
        "findomain.txt",
        "subfinder.txt",
    ]
    print("[+] Reading passive subdomain enumeration results:")
    for file_name in files_to_read:
        file_path = os.path.join(passive_path, file_name)
        content = read_file(file_path)
        if content:
            output_list.extend(content)

def Active(domain, output_list):
    """Process active subdomain enumeration results."""
    active_path = f"results/{domain}/fetchSubdomains/recon_mode/Active/"
    create_directory(active_path)

    files_to_read = ["amass.txt", "assetfinder.txt"]
    print("[+] Reading active subdomain enumeration results:")
    for file_name in files_to_read:
        file_path = os.path.join(active_path, file_name)
        content = read_file(file_path)
        if content:
            output_list.extend(content)

def rootDomainIp(domain, output_list):
    """Process root domain IP subdomains."""
    rootDomainIp_path = f"results/{domain}/rootDomain/theHarvester"
    create_directory(rootDomainIp_path)

    files_to_read = ["ips.txt"]
    print("[+] Reading root domain IP subdomains:")
    for file_name in files_to_read:
        file_path = os.path.join(rootDomainIp_path, file_name)
        content = read_file(file_path)
        if content:
            output_list.extend(content)

def save_to_file(output_list, output_file):
    """Save the collected content to a single file."""
    try:
        # Ensure the parent directory exists
        parent_dir = os.path.dirname(output_file)
        create_directory(parent_dir)

        # Check if the output file path is mistakenly a directory and remove it
        if os.path.exists(output_file) and os.path.isdir(output_file):
            print(f"[!] Warning: {output_file} is a directory. Removing it.")
            os.rmdir(output_file)  # Remove the conflicting directory

        # Write the sorted, unique list to the file
        unique_sorted_list = sorted(set(output_list))
        with open(output_file, "w") as file:
            file.write("\n".join(unique_sorted_list))
        print(f"[+] All unique, sorted subdomains saved to {output_file}")
    except Exception as e:
        print(f"[!] Error writing to {output_file}: {e}")

def main(domain):
    """Quick command to process all data and export it."""
    output_list = []
    rootDomain(domain, output_list)
    Passive(domain, output_list)
    Active(domain, output_list)
    #rootDomainIp(domain, output_list)  # Uncomment if needed

    output_file = f"results/{domain}/fetchSubdomains/SubDomains/allsubdomain.txt"
    save_to_file(output_list, output_file)

# Entry point
if __name__ == "__main__":
   #domain = "docxinfo.site"  # Initialize the domain variable
   #process_all(domain)
   main()