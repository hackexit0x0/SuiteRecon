import os
import requests
from time import sleep
import subprocess
import json
import re

def main(domain):
    print(f"Root Domain: {domain}")
    print("[+] Get Whois data....")
    whois(domain)
    print("[+] Get Robots.txt data....")
    robots(domain)
    print("[+] Get Whatweb data....")
    whatweb(domain)
    print("[+] Get Nslookup data....")
    Nslookup(domain)
    print("[+] Get OSINT theHarvester data....")
    OSINT(domain)
    print("[+] Get OSINT data like : Asn,Ip,Email,Shodan,Subdomain,etc..... ")
    theHarvesterDataFilters(domain)


def whois(domain):
    # Ensure the directory exists for saving whois data
    path = f"results/{domain}/rootDomain"
    os.makedirs(path, exist_ok=True)
    
    # Run the whois command and save the output to a file
    command = f"whois {domain} > {path}/whois.txt"
    print(f"[+] whois.txt saved at {path}/whois.txt")
    os.system(command)

def robots(domain):
    # Ensure the directory exists for saving robots.txt data
    path = f"results/{domain}/rootDomain"
    os.makedirs(path, exist_ok=True)
    
    # Retry logic and timeout for robots.txt
    url = f"https://{domain}/robots.txt"
    retries = 3
    timeout = 10
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=timeout)
            if response.status_code == 200:
                with open(f"{path}/robots.txt", 'w') as file:
                    file.write(response.text)
                print(f"[+] robots.txt saved at {path}/robots.txt")
                break
            else:
                print(f"Failed to retrieve robots.txt for {domain}, Status Code: {response.status_code}")
                break
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                print(f"Retrying in 2 seconds...")
                sleep(2)  # Wait before retrying
            else:
                print("Max retries reached. Could not fetch robots.txt.")

def whatweb(domain):
    # Ensure the directory exists for saving whatweb data
    path = f"results/{domain}/rootDomain"
    os.makedirs(path, exist_ok=True)
    
    # Run the whatweb command and save the output to a file
    command = f"whatweb --color=never --no-errors -a 3 -v {domain} >> {path}/whatweb.txt"
    os.system(command)
    print(f"[+] whatweb.txt saved at {path}/whatweb.txt")

def Nslookup(domain):
    # List of DNS record types to query
    record_types = ['MX', 'NS', 'AAAA', 'A', 'CNAME']
    
    # Ensure the directory exists for saving nslookup data
    path = f"results/{domain}/rootDomain"
    os.makedirs(path, exist_ok=True)
    
    # Define a single output file to store all nslookup results
    output_file = f"{path}/nslookup_all.txt"
    
    # Open the output file in append mode
    with open(output_file, 'a') as file:
        # Loop through each record type and fetch the corresponding data
        for record_type in record_types:
            print(f"[+] Fetching {record_type} data...")
            # Run the nslookup command and append the output to the file
            command = f"nslookup -type={record_type} {domain}"
            result = os.popen(command).read()  # Using os.popen to capture the output
            
            # Write the result to the file
            file.write(f"--- {record_type} Records ---\n")
            file.write(result)
            file.write("\n" + "="*50 + "\n")  # Separator between record types
    
    print(f"[+] All nslookup data saved at {output_file}")

def OSINT(domain):
    path = f"results/{domain}/rootDomain/theHarvester"
    os.makedirs(path, exist_ok=True)
    
    command = f"theHarvester -d {domain} -b all -f {path}/theHarvester.json"
    
    # Run the command in the background and capture the output
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Monitor the progress by reading the output line by line
    while True:
        output = process.stdout.readline()
        if output == b'' and process.poll() is not None:
            break
        if output:
            # You can check for specific progress strings in the output and adjust accordingly
            print(output.decode().strip())  # This prints each line of the output
    
    # Wait for the process to finish
    process.wait()
    
    print(f"[+] theHarvester.json saved at {path}/theHarvester.json")


def theHarvesterDataFilters(domain):
    path = f"results/{domain}/rootDomain/theHarvester"
    os.makedirs(path, exist_ok=True)
    
    # Construct the file path for the XML file
    file_to_remove = f"{path}/theHarvester.xml"
    
    # Check if the file exists before attempting to remove it
    if os.path.exists(file_to_remove):
        os.remove(file_to_remove)
    
    
    # Execute the command to read the JSON file
    command = f"cat {path}/theHarvester.json"
    os.system(command)


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