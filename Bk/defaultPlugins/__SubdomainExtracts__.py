import os
import subprocess


def httprob(domain, input_file, output_file):
    """
    Run httprobe to filter active subdomains and save results.
    
    :param domain: The domain being processed.
    :param input_file: The file containing the list of subdomains to check.
    :param output_file: The file to save active subdomains.
    """
    print("[+] Running httprobe...")
    try:
        # Ensure the input file exists
        if not os.path.exists(input_file):
            print(f"[!] Input file not found: {input_file}")
            return

        # Run httprobe using subprocess
        with open(input_file, "r") as infile, open(output_file, "w") as outfile:
            subprocess.run(["httprobe"], stdin=infile, stdout=outfile, check=True)

        print(f"[+] Active subdomains saved to: {output_file}")

    except FileNotFoundError:
        print("[!] httprobe not installed or not in PATH.")
    except Exception as e:
        print(f"[!] Error running httprobe: {e}")


def filter_http_https(output_file, http_file, https_file):
    """
    Filter httprobe output into HTTP and HTTPS files.
    
    :param output_file: The file containing all httprobe results.
    :param http_file: The file to save HTTP-only results.
    :param https_file: The file to save HTTPS-only results.
    """
    print("[+] Filtering httprobe results into HTTP and HTTPS...")
    try:
        if not os.path.exists(output_file):
            print(f"[!] Output file not found: {output_file}")
            return

        # Read the output file and filter lines
        with open(output_file, "r") as infile:
            http_urls = []
            https_urls = []

            for line in infile:
                if line.startswith("http://"):
                    http_urls.append(line.strip())
                elif line.startswith("https://"):
                    https_urls.append(line.strip())

        # Save HTTP URLs
        with open(http_file, "w") as http_outfile:
            http_outfile.write("\n".join(http_urls))
        print(f"[+] HTTP results saved to: {http_file}")

        # Save HTTPS URLs
        with open(https_file, "w") as https_outfile:
            https_outfile.write("\n".join(https_urls))
        print(f"[+] HTTPS results saved to: {https_file}")

    except Exception as e:
        print(f"[!] Error filtering httprobe results: {e}")


def main(domain):
    """
    Main function to coordinate enumeration.
    
    :param domain: The domain to process.
    """
    base_path = f"results/{domain}/ip/active_Subdomains/http_https"
    os.makedirs(base_path, exist_ok=True)

    # Input and output file paths
    input_file = f"results/{domain}/rootDomain/SubDomains/Active.Subdomains.txt"
    output_file = f"{base_path}/filtered_active_subdomains.txt"
    http_file = f"{base_path}/http.txt"
    https_file = f"{base_path}/https.txt"

    # Run httprobe
    httprob(domain, input_file, output_file)

    # Filter output into HTTP and HTTPS
    filter_http_https(output_file, http_file, https_file)


# Entry point
if __name__ == "__main__":
    # Replace 'docxinfo.site' with your domain
    domain = "docxinfo.site"
    main(domain)
