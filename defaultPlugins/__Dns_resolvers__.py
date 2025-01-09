import os
import subprocess

def massdns(input_file, resolvers, output_file):
    print("[+] Running massdns...")
    try:
        # MassDNS command
        command = [
            "massdns", 
            "-r", resolvers, 
            "-o", "S", 
            "-w", output_file, 
            input_file
        ]
        subprocess.run(command, check=True)
        print(f"[+] MassDNS results saved at: {output_file}")
        
        # Process output file with additional shell commands
        process_output(output_file)
        
    except FileNotFoundError:
        print("[!] MassDNS not installed.")
    except subprocess.CalledProcessError as e:
        print(f"[!] MassDNS failed with error: {e}")
    except Exception as e:
        print(f"[!] Error running MassDNS: {e}")

def process_output(output_file):
    try:
        print("[+] Processing output with awk, sed, and sort...")

        # Ensure output file exists
        if not os.path.exists(output_file):
            raise FileNotFoundError(f"Output file for MassDNS not found: {output_file}")
        
        # Define the processed output file path in the same directory as output_file
        directory = os.path.dirname(output_file)  # Get the directory where the output file is located
        domain = os.path.basename(output_file).split('.')[0]  # Extract domain name from the file name
        processed_output_file = os.path.join(directory, f"Subdomain.{domain}.txt")

        # Command to process output.txt and generate a final result file
        command = f"cat {output_file} | awk '{{print$1}}' | sed 's/.$//' | sort -u > {processed_output_file}"
        subprocess.run(command, shell=True, check=True)
        
        print(f"[+] Processed output saved to {processed_output_file}")
    except Exception as e:
        print(f"[!] Error processing output: {e}")

def validate_domain(domain):
    # Placeholder for domain validation logic
    if not domain or "." not in domain:
        raise ValueError("Invalid domain provided.")

# Main function to coordinate enumeration
def main(domain):
    try:
        validate_domain(domain)
        print(f"[+] Starting passive subdomain enumeration for: {domain}")
        
        # Define paths dynamically
        current_directory = os.getcwd()  # Get current working directory
        resolvers = os.path.join(current_directory, "wordlists/Miscellaneous/dns-resolvers.txt")
        
        # Check if resolvers file exists
        if not os.path.exists(resolvers):
            raise FileNotFoundError(f"Resolvers file not found at: {resolvers}")
        
        path = f"results/{domain}/rootDomain/SubDomains/"
        subdomain_input_file = f"{path}allsubdomain.txt"  # Input file for MassDNS
        massdns_output = f"{path}massdns_output.txt"
        
        os.makedirs(path, exist_ok=True)

        # Ensure the input file exists for MassDNS
        if not os.path.exists(subdomain_input_file):
            raise FileNotFoundError(f"Input file for MassDNS not found: {subdomain_input_file}")

        # Run MassDNS
        massdns(subdomain_input_file, resolvers, massdns_output)

    except Exception as e:
        print(f"[!] Error in main: {e}")

# Example usage
if __name__ == "__main__":
    target_domain = "docxinfo.site"  # Replace with your target domain
    main(target_domain)
