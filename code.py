import os
import json
import re

def theHarvesterDataFilters(domain):
    # Create the necessary directory path
    path = os.path.join("results", domain, "rootDomain", "theHarvester")
    os.makedirs(path, exist_ok=True)
    
    # Construct the file path for the XML file
    file_to_remove = os.path.join(path, "theHarvester.xml")
    
    # Check if the file exists before attempting to remove it
    if os.path.exists(file_to_remove):
        os.remove(file_to_remove)
        print(f"Removed {file_to_remove}")
    else:
        print(f"No file to remove at {file_to_remove}")
    
    # Construct the JSON file path
    json_file_path = os.path.join(path, "theHarvester.json")
    theHarvesterJson(json_file_path, domain)

def theHarvesterJson(data_file, domain):
    # Check if the JSON file exists
    if not os.path.exists(data_file):
        raise FileNotFoundError(f"{data_file} does not exist. Please check the file path.")

    # Read the JSON file
    with open(data_file, "r") as file:
        data = json.load(file)

    # Regular expressions to extract IPs and subdomains
    ip_regex = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
    subdomain_regex = r"([a-zA-Z0-9-]+\.[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*)"

    # Extracting IPs and subdomains from hosts
    ips = []
    subdomains = []
    for host in data.get("hosts", []):
        # Extract IPs
        ip_match = re.search(ip_regex, host)
        if ip_match:
            ips.append(ip_match.group(0))
        # Extract subdomains
        subdomain_match = re.search(subdomain_regex, host)
        if subdomain_match:
            subdomains.append(subdomain_match.group(0))

    # Create output directory under theHarvester folder
    output_dir = os.path.join("results", domain, "rootDomain", "theHarvester")
    
    # Function to write data to a file
    def write_to_file(filename, items):
        file_path = os.path.join(output_dir, filename)
        with open(file_path, "w") as file:
            for item in items:
                file.write(f"{item}\n")
        print(f"Written to {file_path}")

    # Write extracted data to files
    write_to_file("extracted_ips.txt", ips)
    write_to_file("extracted_subdomains.txt", subdomains)
    write_to_file("asns.txt", data.get("asns", []))
    write_to_file("emails.txt", data.get("emails", []))
    write_to_file("ips.txt", data.get("ips", []) + ips)  # Combine existing and extracted IPs
    write_to_file("hosts.txt", data.get("hosts", []))
    write_to_file("interesting_urls.txt", data.get("interesting_urls", []))
    write_to_file("shodan.txt", data.get("shodan", []))

    print(f"Data and extracted hosts have been written to the folder '{output_dir}'.")

# Example usage
theHarvesterDataFilters(domain="docxinfo.site")
