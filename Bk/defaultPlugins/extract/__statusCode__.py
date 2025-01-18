import os
import subprocess

def statusCode(input_file, output_file):
    """
    Uses HTTPX to check the status codes of active subdomains.

    :param input_file: Path to the input file containing active subdomains.
    :param output_file: Path to the output file for HTTPX results.
    """
    try:
        # Run httpx command
        command = f"cat {input_file} | httpx -silent -status-code | tee {output_file}"
        subprocess.run(command, shell=True, check=True)
        print(f"HTTPX status code analysis completed. Results saved to {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error running HTTPX: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def main(domain):
    """
    Main function to coordinate enumeration.

    :param domain: The domain to process.
    """
    base_path = f"results/{domain}/active_Subdomains/statusCode"
    os.makedirs(base_path, exist_ok=True)

    # Input and output file paths
    input_file = f"results/{domain}/active_Subdomains/http_https/filtered_active_subdomains.txt"
    statusCode_output_file = f"{base_path}/statusCode.txt"
   
    # Run statusCode
    print("[+] Running HTTPX status code analysis...")
    statusCode(input_file, statusCode_output_file)

# Entry point
if __name__ == "__main__":
    # Replace 'docxinfo.site' with your domain
    main()
