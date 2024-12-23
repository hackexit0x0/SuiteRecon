import argparse
import os
from defaultPlugins import rootDomain  # Assuming rootDomain.py is in the same directory

# Filter URL to remove http:// or https://
def filter_url(domain):
    if domain.startswith("http://"):
        domain = domain[7:]
    elif domain.startswith("https://"):
        domain = domain[8:]
    return domain  # Return the modified domain

# Create Results Directory and Subdirectory
def result_dir(domain):
    # Create the results directory if it doesn't exist
    results_path = "results"
    if not os.path.exists(results_path):
        try:
            os.mkdir(results_path)
            #print(f"Directory '{results_path}' created.")
        except Exception as e:
            #print(f"Error creating directory '{results_path}': {e}")
            return

    # Create the subdirectory for the domain
    domain_path = os.path.join(results_path, domain, "rootDomain")
    os.makedirs(domain_path, exist_ok=True)  # This creates all necessary directories
    #print(f"Result directory '{domain_path}' created.")

# Main Function to Process Input
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", "--domain", help="Domain name", required=True)
    args = parser.parse_args()

    # Filter the URL to remove http/https
    domain = filter_url(args.url)

    # Create results and domain directories
    result_dir(domain)

    # Call rootDomain.main() with the domain
    rootDomain.main(domain)
