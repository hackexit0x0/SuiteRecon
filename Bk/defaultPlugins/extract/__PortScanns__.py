import os
import subprocess

def naabu_scan(input_file, output_file):
    """
    Runs Naabu to perform port scanning on the input subdomains.

    :param input_file: Path to the input file containing active subdomains.
    :param output_file: Path to the output file for Naabu results.
    """
    try:
        # Run Naabu command
        command = (
            f"sudo naabu -p 80,443,22,21,23,25,53,3306,1433,1521,5432,8080,8443,10000,3389,110,143,465,587,989,990 "
            f"-l {input_file} | tee {output_file}"
        )
        subprocess.run(command, shell=True, check=True)
        print(f"[+] Naabu port scanning completed. Results saved to {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"[!] Error running Naabu: {e}")
    except Exception as e:
        print(f"[!] Unexpected error: {e}")

def nmap_scan(input_file, output_file):
    """
    Runs Nmap to perform service and version detection on the specified ports.

    :param input_file: Path to the input file containing active subdomains.
    :param output_file: Path to the output file for Nmap results.
    """
    try:
        # Run Nmap command
        command = f"nmap -sV -p 443 -f -iL {input_file} -oN {output_file}"
        subprocess.run(command, shell=True, check=True)
        print(f"[+] Nmap service detection completed. Results saved to {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"[!] Error running Nmap: {e}")
    except Exception as e:
        print(f"[!] Unexpected error: {e}")

def main(domain):
    """
    Main function to coordinate enumeration.

    :param domain: The domain to process.
    """
    base_path = f"results/{domain}/active_Subdomains/PortScanning"
    os.makedirs(base_path, exist_ok=True)

    # Input and output file paths
    input_file = f"results/{domain}/rootDomain/SubDomains/Active.Subdomains.txt"
    naabu_output_file = f"{base_path}/naabu.txt"
    nmap_output_file = f"{base_path}/nmap.txt"

    # Run Naabu scan
    print("[+] Running Naabu port scanning...\n")
    naabu_scan(input_file, naabu_output_file)

    # Run Nmap scan
    print("[+] Running Nmap service and version detection...")
    nmap_scan(input_file, nmap_output_file)

# Entry point
if __name__ == "__main__":
    # Replace 'docxinfo.site' with your domain
    main()
