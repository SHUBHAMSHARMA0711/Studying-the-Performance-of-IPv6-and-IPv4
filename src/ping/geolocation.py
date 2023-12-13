import requests
import socket
import json



def get_geolocation_data(ip_address):
    url = f"http://ip-api.com/json/{ip_address}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

websites = []
with open("WebsitesToPing.txt", 'r') as file:
    for line in file:
        # Remove leading/trailing whitespaces and add the website to the list
        websites.append(line.strip())

ip_addresses = {}
# Obtain IP addresses for each website
for website in websites:
    try:
        ip_address = socket.gethostbyname(website)
        ip_addresses[website] = ip_address
    except:
        ip_addresses[website] = None
print(ip_addresses)
# Get geolocation data for each IP address
geolocation_data = {}
for website in ip_addresses:
    if ip_addresses[website] != None:
        data = get_geolocation_data(ip_addresses[website])
        data["ip_address"] = ip_addresses[website]
    else:
        data = None
    geolocation_data[website] = data

output_file_path = "output.txt"
json_output_file_path = "geolocation_data.json"

with open(output_file_path, 'w', encoding='utf-8') as output_file:
    for website, data in geolocation_data.items():
        if data != None:
            print(f"IP Address: {website}")
            print(f"IP Address: {data['ip_address']}")
            print("Geolocation Data:")
            print(f"Country: {data['country']}")
            print(f"City: {data['city']}")
            print(f"Latitude: {data['lat']}")
            print(f"Longitude: {data['lon']}")
            print()
            output_file.write(f"IP Address: {website}\n")
            output_file.write(f"IP Address: {data['ip_address']}\n")
            output_file.write("Geolocation Data:\n")
            output_file.write(f"Country: {data['country']}\n")
            output_file.write(f"City: {data['city']}\n")
            output_file.write(f"Latitude: {data['lat']}\n")
            output_file.write(f"Longitude: {data['lon']}\n\n")
        else:
            print("Data unavailable for")
            print(f"website:{website}")
            print()
            output_file.write("Data unavailable for\n")
            output_file.write(f"Website: {website}\n\n")

with open(json_output_file_path, 'w') as json_output_file:
    json.dump(geolocation_data, json_output_file, indent=4)