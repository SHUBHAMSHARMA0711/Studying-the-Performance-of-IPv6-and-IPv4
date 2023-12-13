import requests, socket, os, json, datetime, subprocess, sys

# RUN THIS FILE FOR GENERATING PING DATA FOR IPV6 AND IPV4
# ON WINDOWS IN CMD COMMAND
# python ./Simulator.py [name] [ISP]
# expample => python ./Simulator.py Akshat Jio
# result file as result_[name].json is created
# if it already exists then it appends the data to it.

class Simulator():
    def __init__(self, name, operator) -> None:
        # Load list of websites
        with open("website.txt", "r") as f:
            self.websites = f.read().split("\n")
        
        # Load data of websites
        print("Loading website data...")
        if os.path.exists("ip_info.json"):
            with open("ip_info.json", "r") as f:
                self.websites_data = json.load(f)
        else:
            self.websites_data = self.get_website_data()
        
        # Load test conditions data
        self.name = name
        self.operator = operator
        self.date = datetime.datetime.now().strftime("%d %B %y")

        self.simulate()

    def get_website_data(self):
        self.data = dict()
        websites_active_v4 = []
        websites_active_v6 = []
        # IPv4
        for i in self.websites:
            try:
                self.data[i] = {}
                self.get_website_data_v4(i)
                websites_active_v4.append(i)
            except:                    
                print(f"Failed for {i}")
        
        input("Continue for IPv6...")

        # IPv6
        for i in self.websites:
            try:
                self.get_website_data_v6(i)
                if i in websites_active_v4:
                    websites_active_v6.append(i)
            except:
                print(f"Failed for {i}")
        
        with open("website_data.json", "w") as f:
                json_data = json.dumps(self.data, indent=4)
                f.write(json_data)
        
        with open("website.txt","w") as f:
            f.write("\n".join(websites_active_v6))
        return self.data

    def get_geolocation(self, ip_address):
        url = f"http://ip-api.com/json/{ip_address}"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            return data['country'], data['city']
        else:
            return None

    def get_website_data_v4(self, website):
        print(f"Fetching data for {website}...")
        # For IPv4
        ipv4 = socket.getaddrinfo(website, 443)[0][4][0]
        country_v4, city_v4 = self.get_geolocation(ipv4)

        # JSON
        self.data[website]['ipv4'] = ipv4
        self.data[website]['country_v4'] = country_v4
        self.data[website]['city_v4'] = city_v4
    
    def get_website_data_v6(self, website):
        print(f"Fetching data for {website}...")
        # For IPv6
        ipv6 = socket.getaddrinfo(website, 443, socket.AF_INET6)[0][4][0]
        country_v6, city_v6 = self.get_geolocation(ipv6)

        # JSON
        self.data[website]['ipv6'] = ipv6
        self.data[website]['country_v6'] = country_v6
        self.data[website]['city_v6'] = city_v6
    

    def simulate(self):
        all_data = []

        for website in self.websites:
            print(f"Testing for {website}")
            data = self.websites_data[website]
            hop_v6 = self.get_trace_6(data['ipv6'])
            hop_v4 = self.get_trace_4(data['ipv4'])
            print(hop_v4)
            print(hop_v6)
            website_data = []

            for x in range(40):
                print(f"ping number {x + 1}")
                try:
                    rtt_v4 = self.ping4(data['ipv4'])
                    rtt_v6 = self.ping6(data['ipv6'])
                    data_entry = {
                        'website': str(website),
                        'date': self.date,
                        'name': str(self.name),
                        'operator': str(self.operator),
                        'ipv4': str(data['ipv4']),
                        'country_v4': str(data['country_v4']),
                        'city_v4': str(data['city_v4']),
                        'rtt_v4': str(rtt_v4),
                        'hop_v4': hop_v4,
                        'ipv6': str(data['ipv6']),
                        'country_v6': str(data['country_v6']),
                        'city_v6': str(data['city_v6']),
                        'rtt_v6': str(rtt_v6),
                        'hop_v6': hop_v6
                    }
                    print(data_entry)
                    website_data.append(data_entry)
                except Exception as e:
                    print(f"--Failed for {website}: {str(e)}")

            all_data.extend(website_data)

        json_file_path = f"results_{self.name}.json"
        try:
            with open(json_file_path, "r") as existing_json_file:
                existing_data = json.load(existing_json_file)
                all_data.extend(existing_data)
            print("Done")

        except FileNotFoundError:
            print("creating new file")

        with open(json_file_path, "w") as json_file:
            json.dump(all_data, json_file, indent=4)

       
    def ping4(self, ipv4):
        ping = subprocess.run (f"ping {ipv4} -4 -n 1 -l 64", stdout=subprocess.PIPE, shell=True)
        output = ping.stdout.decode ("UTF-8")
        rtt =int(output.split ("\n")[-2].split("=")[-1].replace("ms",""))
        return rtt
    
    def ping6(self, ipv4):
        ping = subprocess.run (f"ping {ipv4} -6 -n 1 -l 64", stdout=subprocess.PIPE, shell=True)
        output = ping.stdout.decode ("UTF-8")
        rtt =int(output.split ("\n")[-2].split("=")[-1].replace("ms",""))
        return rtt
    
    def get_trace_6(self, ipv6):
        trace = subprocess.run(f"tracert -d -6 -w 1 -h 20 {ipv6}", stdout=subprocess.PIPE, shell=True)
        trace = trace.stdout.decode("UTF-8")
        lines = [line.strip() for line in trace.splitlines() if line.strip()][1:-1]
        hop_data = {}
        try :
            for line in lines:
                parts = line.split()
                if len(parts) == 8:
                    hop_number = parts[0]
                    rtt1, rtt2, rtt3 = parts[1], parts[3], parts[5]
                    ip_address = parts[7]
                    hop_data[hop_number] = [rtt1, rtt2, rtt3, ip_address]
                elif len(parts) == 7:
                    if parts[5] == "timed":
                        hop_number = parts[0]
                        rtt1, rtt2, rtt3 = parts[1], parts[2], parts[3]
                        ip_address = parts[5] + " " + parts[6]
                        hop_data[hop_number] = [rtt1, rtt2, rtt3, ip_address]
                    else:
                        hop_number = parts[0]
                        rtt1, rtt2, rtt3 = "*", "*", "*"
                        ip_address = parts[6]
                        hop_data[hop_number] = [rtt1, rtt2, rtt3, ip_address]
            return hop_data
        except:
            print("failed ipv6 traceroute")
            return None

    def get_trace_4(self,ipv4):
        trace = subprocess.run(f"tracert -d -4 -w 1 -h 20 {ipv4}", stdout=subprocess.PIPE, shell=True)
        trace = trace.stdout.decode("UTF-8")
        lines = [line.strip() for line in trace.splitlines() if line.strip()][1:-1]
        hop_data = {}
        try:
            for line in lines:
                parts = line.split()
                if len(parts) == 8:
                    hop_number = parts[0]
                    rtt1, rtt2, rtt3 = parts[1], parts[3], parts[5]
                    ip_address = parts[7]
                    hop_data[hop_number] = [rtt1, rtt2, rtt3, ip_address]
                elif len(parts) == 7:
                    if parts[5] == "timed":
                        hop_number = parts[0]
                        rtt1, rtt2, rtt3 = parts[1], parts[2], parts[3]
                        ip_address = parts[5] + " " + parts[6]
                        hop_data[hop_number] = [rtt1, rtt2, rtt3, ip_address]
                    else:
                        hop_number = parts[0]
                        rtt1, rtt2, rtt3 = "*", "*", "*"
                        ip_address = parts[6]
                        hop_data[hop_number] = [rtt1, rtt2, rtt3, ip_address]
            return hop_data
        except:
            print("failed ipv4 traceroute")
            return None

if __name__=="__main__":
    Simulator(sys.argv[1], sys.argv[2])