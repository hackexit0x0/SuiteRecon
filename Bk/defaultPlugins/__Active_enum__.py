import os
import subprocess
from urllib.parse import quote

# Uses subfinder to enumerate subdomains
def assetfinder(domain, output_file):
    """Run assetfinder to enumerate subdomains and save the results."""
    print("[+] Running assetfinder...")
    try:
        command = ["assetfinder", "--subs-only", domain]
        with open(output_file, "w") as outfile:
            subprocess.run(command, check=True, stdout=outfile)
        print(f"[+] assetfinder results saved at: {output_file}")
    except FileNotFoundError:
        print("[!] assetfinder not installed.")
    except Exception as e:
        print(f"[!] Error running assetfinder: {e}")

# Runs amass for passive enumeration
def amass(domain, output_file):
    """Run amass to enumerate subdomains and save the results."""
    print("[+] Running amass...")
    try:
        command = ["amass", "enum", "-active", "-d", domain, "-o", output_file]
        subprocess.run(command, check=True)
        print(f"[+] Amass results saved at: {output_file}")
    except FileNotFoundError:
        print("[!] Amass not installed.")
    except Exception as e:
        print(f"[!] Error running amass: {e}")

# Filters and deduplicates Amass results
def amass_filter(domain):
    """Filter and deduplicate Amass results."""
    input_file = f"results/{domain}/fetchSubdomains/recon_mode/Active/amass-notFilter.txt"
    output_file = f"results/{domain}/fetchSubdomains/recon_mode/Active/amass.txt"

    print("[+] Filtering and removing duplicates from Amass output...")
    try:
        # Execute shell-like filtering operations
        command = f"cat {input_file} | cut -d ']' -f 2 | awk '{{print $1}}' | sort -u > {output_file}"
        subprocess.run(command, shell=True, check=True)
        print(f"[+] Filtered Amass results saved at: {output_file}")
    except FileNotFoundError:
        print("[!] Input file not found for filtering.")
    except Exception as e:
        print(f"[!] Error during Amass filtering: {e}")

    try:
        os.remove(input_file)
    except FileNotFoundError:
        print(f"[!] File not found for deletion: {input_file}")

# Main function to coordinate enumeration
def main(domain):
    """Main function to perform active subdomain enumeration."""
    print(f"[+] Starting Active subdomain enumeration for: {domain}")
    path = f"results/{domain}/fetchSubdomains/recon_mode/Active/"
    os.makedirs(path, exist_ok=True)

    # Run assetfinder and save output
    assetfinder(domain, f"{path}assetfinder.txt")

    # Run amass and save unfiltered output
    #amass(domain, f"{path}amass-notFilter.txt")

    # Filter and deduplicate Amass output
    #amass_filter(domain)

# Entry point
if __name__ == "__main__":
    main()
