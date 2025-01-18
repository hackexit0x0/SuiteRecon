import os
import subprocess




class DnsxRunner:
    def __init__(self, domain):
        self.domain = domain
        self.base_dirs = f"results/{domain}/rootDomain/SubDomains"
        self.base_dir = f"results/{domain}/active_Subdomains/ip/"
        self.input_file = os.path.join(self.base_dirs, "Active.Subdomains.txt")
        self.output_file = os.path.join(self.base_dir, "ipAddress.txt")
        self.httprobe_file = os.path.join(self.base_dir, "file.txt")  # File for httprobe results

        # Ensure the base directory exists
        os.makedirs(self.base_dir, exist_ok=True)

    def run_dnsx(self):
        """Runs the dnsx tool and processes its output."""
        print("[+] Running dnsx...")

        # Check if input file exists
        if not os.path.exists(self.input_file):
            print(f"[!] Input file not found: {self.input_file}")
            return

        try:
            # Command to execute dnsx
            command = ["dnsx", "-l", self.input_file, "-silent", "-a", "-resp-only"]

            # Run the command and capture its output
            result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            # Log the output to the output file and print to console
            with open(self.output_file, "w") as outfile:
                outfile.write(result.stdout)

            # Print output to console as well
            print(result.stdout)

            # Process the output to remove duplicates
            self._filter_unique_ips()

            print(f"[+] Processed dnsx results saved to: {self.output_file}")

            # Run httprobe on the subdomains
            self.run_httprobe()

        except FileNotFoundError:
            print("[!] dnsx not installed. Please install it and try again.")
        except subprocess.CalledProcessError as e:
            print(f"[!] Error running dnsx: {e}")
        except Exception as e:
            print(f"[!] Unexpected error: {e}")

    def _filter_unique_ips(self):
        """Removes duplicate IPs from the dnsx output."""
        try:
            with open(self.output_file, "r") as infile:
                unique_ips = set(infile.read().splitlines())  # Collect unique IPs

            # Ensure there is content to write
            if not unique_ips:
                print("[!] No IPs found in the output.")

            with open(self.output_file, "w") as outfile:
                outfile.write("\n".join(sorted(unique_ips)))  # Save sorted unique IPs

        except Exception as e:
            print(f"[!] Error filtering unique IPs: {e}")

    def run_httprobe(self):
        """Runs httprobe on the subdomains and saves the results."""
        print("[+] Running httprobe...")

        # Check if the subdomain input file exists
        if not os.path.exists(self.input_file):
            print(f"[!] Subdomain file not found: {self.input_file}")
            return

        # Check if input file is empty
        if os.stat(self.input_file).st_size == 0:
            print("[!] Input file is empty. Please check the subdomain file.")
            return

        try:
            # Command to execute httprobe
            command = ["httprobe"]

            # Open the subdomains input file and pipe it to httprobe
            with open(self.input_file, "r") as infile:
                result = subprocess.run(command, stdin=infile, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            # Log the output to the httprobe file and print to console
            with open(self.httprobe_file, "w") as httprobe_out:
                httprobe_out.write(result.stdout)

            # Print output to console as well
            print(result.stdout)

            # After running httprobe, extract HTTP/HTTPS subdomains
            extract_http_https_subdomains(self.httprobe_file, "http.txt", "https.txt")

        except FileNotFoundError:
            print("[!] httprobe not installed. Please install it and try again.")
        except subprocess.CalledProcessError as e:
            print(f"[!] Error running httprobe: {e}")
            print(f"[!] stderr: {e.stderr}")
        except Exception as e:
            print(f"[!] Unexpected error with httprobe: {e}")

    def execute(self):
        """Executes the dnsx workflow."""
        self.run_dnsx()


# Entry point
if __name__ == "__main__":
    domain = "docxinfo.site"
    dnsx_runner = DnsxRunner(domain)
    dnsx_runner.execute()

