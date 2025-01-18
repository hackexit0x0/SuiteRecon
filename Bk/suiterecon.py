import argparse
import os
from defaultPlugins import __Domain_root__  # Assuming rootDomain.py is in the same directory
from defaultPlugins import __Passive_enum__
from defaultPlugins import __Active_enum__
from defaultPlugins import __Sub_Sub_enum__
from defaultPlugins import __DomainSort__
from defaultPlugins import __Dns_resolvers__
from defaultPlugins import __SubDomainConvertIp__

# extartc
from defaultPlugins.extract import __SubdomainExtracts__
from defaultPlugins.extract import __statusCode__
from defaultPlugins.extract import __PortScanns__
from defaultPlugins.extract import __techDetect__




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
            print(f"Directory '{results_path}' created.")
        except Exception as e:
            print(f"Error creating directory '{results_path}': {e}")
            return

    # Create the subdirectory for the domain
    domain_path = os.path.join(results_path, domain, "rootDomain")
    os.makedirs(domain_path, exist_ok=True)  # This creates all necessary directories
    print(f"Result directory '{domain_path}' created.")

# Main Function to Process Input
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", "--domain", help="Domain name", required=True)
    #parser.add_argument("--opt", "--option", help="Option", required=True)
    args = parser.parse_args()

    domain = filter_url(args.url)
    args = parser.parse_args()
    # Filter the URL to remove http/https
    domain = filter_url(args.url)
    # Create results and domain directories
    result_dir(domain)
    # Call rootDomain.main() with the domain
    __Domain_root__.main(domain)   # rootdomain
    __Passive_enum__.main(domain)  # passive enum
    __Active_enum__.main(domain)   # Active enum
    __Sub_Sub_enum__.main(domain)   # sub.sub doamin founde
    __DomainSort__.main(domain)  # all domian sorts 
    __Dns_resolvers__.main(domain)    # dns resolve 
    __SubDomainConvertIp__.main(doamin)

    # extract
    __SubdomainExtracts__.main(domain)
    __statusCode__.main(domain)
    __PortScanns__.main(domain)
    __techDetect__.main(domain)

    
    
 
    


