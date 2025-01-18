import subprocess
import os


def ensure_directory_exists(directory):
    """Ensures that the specified directory exists."""
    os.makedirs(directory, exist_ok=True)


def filter_unique_ips(output_file):
    """Removes duplicate IPs from the dnsx output."""
    try:
        with open(output_file, "r") as infile:
            unique_ips = set(infile.read().splitlines())

        if not unique_ips:
            print("[!] No IPs found in the output.")
            return

        with open(output_file, "w") as outfile:
            outfile.write("\n".join(sorted(unique_ips)))

    except Exception as e:
        print(f"[!] Error filtering unique IPs: {e}")


def run_dnsx(domain):
    """Runs the dnsx tool and processes its output."""
    base_dirs = f"results/{domain}/rootDomain/SubDomains"
    base_dir = f"results/{domain}/active_Subdomains/ip/"
    input_file = os.path.join(base_dirs, "Active.Subdomains.txt")
    output_file = os.path.join(base_dir, "ipAddress.txt")

    ensure_directory_exists(base_dir)

    print("[+] Running dnsx...")

    if not os.path.exists(input_file):
        print(f"[!] Input file not found: {input_file}")
        return

    try:
        command = ["dnsx", "-l", input_file, "-silent", "-a", "-resp-only"]
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        with open(output_file, "w") as outfile:
            outfile.write(result.stdout)

        print(result.stdout)
        filter_unique_ips(output_file)
        print(f"[+] Processed dnsx results saved to: {output_file}")

    except FileNotFoundError:
        print("[!] dnsx not installed. Please install it and try again.")
    except subprocess.CalledProcessError as e:
        print(f"[!] Error running dnsx: {e}")
    except Exception as e:
        print(f"[!] Unexpected error: {e}")


def main():
    """Main function to execute the dnsx workflow."""
    domain = "docxinfo.site"
    run_dnsx(domain)


if __name__ == "__main__":
    main()
