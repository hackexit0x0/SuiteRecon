import socket
import requests
import json


class main:
    def __init__(self, domain):
        self.domain = domain
        self.ip = None

    def get_ip(self):
        """Fetch the IP address of the domain."""
        try:
            self.ip = socket.gethostbyname(self.domain)
            return self.ip
        except socket.gaierror as e:
            self.ip = None
            return f"Error getting IP: {e}"

    def get_http_details(self):
        """Fetch the server and status code of the domain."""
        if not self.ip:
            return "Unknown", "IP not resolved"

        try:
            url = f"http://{self.domain}"
            response = requests.get(url, timeout=5)
            server = response.headers.get('Server', 'Unknown')
            status_code = response.status_code
            return server, status_code
        except requests.RequestException as e:
            return "Unknown", f"Error: {e}"

    def get_geo_isp(self):
        """Fetch geolocation and ISP details of the IP."""
        if not self.ip:
            return "IP not resolved"

        try:
            api_url = f"http://ip-api.com/json/{self.ip}"
            response = requests.get(api_url, timeout=5)
            data = response.json()
            geo_info = {
                'Country': data.get('country', 'Unknown'),
                'Region': data.get('regionName', 'Unknown'),
                'City': data.get('city', 'Unknown'),
                'ISP': data.get('isp', 'Unknown')
            }
            return geo_info
        except requests.RequestException as e:
            return f"Error: {e}"

    def get_technologies(self):
        """Detect technologies used by the domain."""
        if not self.ip:
            return ["IP not resolved"]

        try:
            url = f"http://{self.domain}"
            headers = {
                'User-Agent': 'Mozilla/5.0'
            }
            response = requests.get(url, headers=headers, timeout=5)
            tech_detected = []
            # Example: detect technologies based on HTTP headers
            if 'X-Powered-By' in response.headers:
                tech_detected.append(response.headers['X-Powered-By'])
            if 'Server' in response.headers:
                tech_detected.append(response.headers['Server'])
            return tech_detected if tech_detected else ['Unknown']
        except requests.RequestException as e:
            return [f"Error: {e}"]

    def display_info(self):
        """Display all gathered information."""
        print(f"Domain: {self.domain}")

        ip = self.get_ip()
        print(f"IP Address: {ip}")

        if self.ip:
            server, status_code = self.get_http_details()
            print(f"Server: {server}")
            print(f"Status Code: {status_code}")

            geo_isp_info = self.get_geo_isp()
            print("Geo and ISP Info:", json.dumps(geo_isp_info, indent=2))

            technologies = self.get_technologies()
            print("Detected Technologies:", technologies)
        else:
            print("Skipping further details due to IP resolution error.")


# Example Usage
if __name__ == "__main__":
      # Replace with your desired domain
    main = main(domain="docxinfo.site")
    main.display_info()
