import requests, socket, os, json, datetime, subprocess, sys, re

class sim:
    def __init__(self, name, operator):
        with open("ip_info.json", "r") as f:
            self.websites_data = json.load(f)

        self.name = name
        self.operator = operator
        self.date = self.date = datetime.datetime.now().strftime("%d %B %y")
        self.simulate()

    def simulate(self):
        all_data = []

        for website in self.websites_data:
            print(f"Testing for {website}")
            data = self.websites_data[website]
            min_v4, max_v4, avg_v4, sum_v4, std_dev_v4 = self.testv4(website)
            min_v6, max_v6, avg_v6, sum_v6, std_dev_v6 = self.testv6(website)
            try:
                data_entry = {
                    'website': str(website),
                    'date': self.date,
                    'name': str(self.name),
                    'operator': str(self.operator),
                    'ipv4': str(data['ipv4']),
                    'country_v4': str(data['country_v4']),
                    'city_v4': str(data['city_v4']),
                    'min_v4': min_v4,
                    'max_v4': max_v4,
                    'avg_v4': avg_v4,
                    'sum_v4': sum_v4,
                    'std_dev_v4': std_dev_v4,
                    'ipv6': str(data['ipv6']),
                    'country_v6': str(data['country_v6']),
                    'city_v6': str(data['city_v6']),
                    'min_v6': min_v6,
                    'max_v6': max_v6,
                    'avg_v6': avg_v6,
                    'sum_v6': sum_v6,
                    'std_dev_v6': std_dev_v6,
                }
                all_data.append(data_entry)
                print(data_entry['website'])
            except Exception as e:
                print(f"--Failed for {website}: {str(e)}")

            
        print(all_data)
        json_file_path = f"results_{self.name}.json"
        try:
            with open(json_file_path, "r") as existing_json_file:
                existing_data = json.load(existing_json_file)
                all_data.extend(existing_data)
            print("Done")

        except FileNotFoundError:
            print("creating new file")

        with open(json_file_path, "w") as json_file:
            json.dump(all_data, json_file, indent=2)



    def testv4(self, website):
        ping = subprocess.run (f"./testv4.sh {website} 3", stdout=subprocess.PIPE, shell=True)
        output_string = ping.stdout.decode ("UTF-8")
        # Define regular expressions to match the numerical values

        min_pattern = re.compile(r'min=(.+?),')
        max_pattern = re.compile(r'max=(.+?),')
        avg_pattern = re.compile(r'avg=(.+?),')
        sum_pattern = re.compile(r'sum=(.+?),')
        std_dev_pattern = re.compile(r'standard deviation=(.+)')

        # Extract values using regular expressions
        min_value = min_pattern.search(output_string).group(1).strip() if min_pattern.search(output_string) else None
        max_value = max_pattern.search(output_string).group(1).strip() if max_pattern.search(output_string) else None
        avg_value = str(avg_pattern.search(output_string).group(1).strip()) if avg_pattern.search(output_string) else None
        sum_value = str(sum_pattern.search(output_string).group(1).strip()) if sum_pattern.search(output_string) else None
        std_dev_value = str(std_dev_pattern.search(output_string).group(1).strip()) if std_dev_pattern.search(output_string) else None

        # Print the extracted values
        print(f"Min: {min_value}")
        print(f"Max: {max_value}")
        print(f"Avg: {avg_value}")
        print(f"Sum: {sum_value}")
        print(f"Standard Deviation: {std_dev_value}")
        
        return min_value, max_value, avg_value, sum_value, std_dev_value

    def testv6(self, website):
        ping = subprocess.run (f"./testv6.sh {website} 3", stdout=subprocess.PIPE, shell=True)
        output_string = ping.stdout.decode ("UTF-8")
        

        min_pattern = re.compile(r'min=(.+?),')
        max_pattern = re.compile(r'max=(.+?),')
        avg_pattern = re.compile(r'avg=(.+?),')
        sum_pattern = re.compile(r'sum=(.+?),')
        std_dev_pattern = re.compile(r'standard deviation=(.+)')

        # Extract values using regular expressions
        min_value = min_pattern.search(output_string).group(1).strip() if min_pattern.search(output_string) else None
        max_value = max_pattern.search(output_string).group(1).strip() if max_pattern.search(output_string) else None
        avg_value = str(avg_pattern.search(output_string).group(1).strip()) if avg_pattern.search(output_string) else None
        sum_value = str(sum_pattern.search(output_string).group(1).strip()) if sum_pattern.search(output_string) else None
        std_dev_value = str(std_dev_pattern.search(output_string).group(1).strip()) if std_dev_pattern.search(output_string) else None

        # Print the extracted values
        print(f"Min: {min_value}")
        print(f"Max: {max_value}")
        print(f"Avg: {avg_value}")
        print(f"Sum: {sum_value}")
        print(f"Standard Deviation: {std_dev_value}")
        
        return min_value, max_value, avg_value, sum_value, std_dev_value

    def output(self):
        pass

    
    
# x = sim("akshat", "jio")
if __name__=="__main__":
    sim(sys.argv[1], sys.argv[2])