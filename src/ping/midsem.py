import requests, socket, os, json, datetime, subprocess, sys


class Simulator():
    def __init__(self, name, operator) -> None:
        # Load list of websites
        with open("website.txt", "r") as f:
            self.websites = f.read().split("\n")
        
        # Load data of websites
        print("Loading website data...")
        if os.path.exists("website_data.json"):
            with open("website_data.json", "r") as f:
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
        with open(f"results_{self.name}.csv", "a") as f:
            for website in self.websites:
                print(f"Testing for {website}")
                for x in range(40):
                    print(f"ping number {x+1}")
                    try:
                        data = self.websites_data[website]
                        rtt_v4 = self.ping4(data['ipv4'])
                        rtt_v6 = self.ping6(data['ipv6'])
                        
                        f.write(f"{website}, {self.date}, {self.name}, {self.operator}, {data['ipv4']}, {data['country_v4']}, {data['city_v4']}, {rtt_v4}, {data['ipv6']}, {data['country_v6']}, {data['city_v6']}, {rtt_v6}\n")
                    except:
                        print(f"--Failed for {website}") 

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
        trace = subprocess.run(f"tracert -d -6 {ipv6}", stdout=subprocess.PIPE, shell=True)
        trace = trace.stdout.decode("UTF-8")
        print(trace)        

    def get_trace_4(self,ipv4):
        trace = subprocess.run(f"tracert -d -4 {ipv4}", stdout=subprocess.PIPE, shell=True)
        trace = trace.stdout.decode("UTF-8")
        print(trace) 


def get_trace_4(ipv4):
    trace = subprocess.run(f"tracert -d -6 {ipv4}", stdout=subprocess.PIPE, shell=True)
    trace = trace.stdout.decode("UTF-8")
        # Split the output into lines and skip the first two lines
    lines = [line.strip() for line in trace.splitlines() if line.strip()][1:-1]
    hop_data = {}
    for line in lines:
        parts = line.split()
        if len(parts) == 8:
            hop_number = parts[0]
            rtt1, rtt2, rtt3 = parts[1], parts[3], parts[5]
            ip_address = parts[7]
            hop_data[hop_number] = [rtt1, rtt2, rtt3, ip_address]
        elif len(parts) == 7:
            hop_number = parts[0]
            rtt1, rtt2, rtt3 = parts[1], parts[2], parts[3]
            ip_address = parts[5] + " " + parts[6]
            hop_data[hop_number] = [rtt1, rtt2, rtt3, ip_address]
    return hop_data

# print(get_trace_4("2404:6800:4002:815::200e"))
# print(get_trace_4("google.com"))
if __name__=="__main__":
    Simulator(sys.argv[1], sys.argv[2])