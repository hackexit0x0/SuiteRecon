import os
import subprocess

def ScreenshotsSnapshot(input_file, output_file):
    """
    Runs Nuclei to take screenshots of subdomains listed in the input file.

    :param input_file: Path to the input file containing active subdomains.
    :param output_file: Path to the output file for storing Nuclei results.
    """
    try:
        # Run Nuclei command for screenshots
        command = f"nuclei -l {input_file} -id screenshot -headless"
        subprocess.run(command, shell=True, check=True)
        print(f"[+] Nuclei screenshot task completed. Results saved to {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"[!] Error running Nuclei: {e}")
    except Exception as e:
        print(f"[!] Unexpected error: {e}")

def main(domain):
    """
    Main function to coordinate enumeration and screenshot tasks.

    :param domain: The domain to process.
    """
    base_path = f"results/{domain}/active_Subdomains/Screenshots-Snapshot/"
    os.makedirs(base_path, exist_ok=True)

    # Input and output file paths
    input_file = f"results/{domain}/rootDomain/SubDomains/Active.Subdomains.txt"
    output_file = f"{base_path}/nuclei_screenshots.txt"

    # Run Nuclei screenshot capture
    print("[+] Running Nuclei to take screenshots...\n")
    ScreenshotsSnapshot(input_file, output_file)

# Entry point
if __name__ == "__main__":
    # Replace 'docxinfo.site' with your domain
    domain = "docxinfo.site"
    main(domain)
