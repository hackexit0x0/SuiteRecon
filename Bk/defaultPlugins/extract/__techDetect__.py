import os
import subprocess

def techDetect(input_file, output_file):
    """
    Uses WhatWeb to detect technologies from a list of URLs.

    :param input_file: Path to the input file containing URLs.
    :param output_file: Path to the output file for WhatWeb results.
    """
    try:
        # Run WhatWeb command
        command = f"whatweb --input-file {input_file} | tee {output_file}"
        subprocess.run(command, shell=True, check=True)
        print(f"WhatWeb analysis completed. Results saved to {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error running WhatWeb: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def httpx(domain, input_file, output_file):
    """
    Uses HTTPX to probe and detect technologies from active subdomains.

    :param domain: The domain being processed.
    :param input_file: Path to the input file containing active subdomains.
    :param output_file: Path to the output file for HTTPX results.
    """
    try:
        # Run HTTPX command
        command = f"cat {input_file} | httpx -silent -probe -tech-detect -status-code -sc --title  -o {output_file}"
        subprocess.run(command, shell=True, check=True)
        print(f"HTTPX probing completed. Results saved to {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error running HTTPX: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def main(domain):
    """
    Main function to coordinate enumeration.

    :param domain: The domain to process.
    """
    base_path = f"results/{domain}/active_Subdomains/techDetect"
    os.makedirs(base_path, exist_ok=True)

    # Input and output file paths
    input_file = f"results/{domain}/rootDomain/SubDomains/Active.Subdomains.txt"
    tech_output_file = f"{base_path}/whatweb.techDetect.txt"
    httpx_output_file = f"{base_path}/httpx.techDetect.txt"

    # Run techDetect
    print("[+] Running WhatWeb...")
    techDetect(input_file, tech_output_file)

    # Run httpx
    print("[+] Running HTTPX...")
    httpx(domain, input_file, httpx_output_file)

# Entry point
if __name__ == "__main__":
    # Replace 'docxinfo.site' with your domain
    main()
