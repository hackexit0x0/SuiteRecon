import os
import subprocess
print("[+] Strat Nitro Scann....")
print("[+] Live Subdomain extract ip Like : example.com to 0.0.0.0")

# Uses dnsx to scan active subdomains
def nitro(domain, output_file, input_file):
    print("[+] Running Nitro Scan...")
    try:
        command = ["dnsx", "-l", input_file, "-silent", "-a", "-resp-only", "-o", output_file]
        subprocess.run(command, check=True)
        print(f"[+] Nitro results saved at: {output_file}")
    except FileNotFoundError:
        print("[!] Nitro (dnsx) not installed.")
    except Exception as e:
        print(f"[!] Error running Nitro: {e}")

def http_https(domain, output_files, input_file):
    print("[+] Running https & http enum Scan...")
    try:
        command = f"cat {input_file} | httprobe | tee {output_files}"
        subprocess.run(command, shell=True, check=True)
        print(f"[+] https & http results saved at: {output_files}")
    except FileNotFoundError:
        print("[!] https & http (httprobe) not installed.")
    except Exception as e:
        print(f"[!] Error running https & http: {e}")

# Main function to coordinate enumeration
def main(domain):
    print(f"[+] Starting Nitro enumeration for: {domain}")
    path = f"results/{domain}/nitro/"
    os.makedirs(path, exist_ok=True)

    input_file = f"results/{domain}/fetchSubdomains/SubDomains/active.massdns_output.txt"
    output_file = os.path.join(path, f"ip.{domain}.txt")
    output_files = os.path.join(path, f"https&https.{domain}.txt")

    nitro(domain, output_file, input_file)
    http_https(domain, output_files, input_file)

# Entry point
if __name__ == "__main__":
    # Example domain; replace with dynamic input if needed
    #domain = "example.com"
    #main(domain)
    main()
