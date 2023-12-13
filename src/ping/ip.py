import subprocess

def get_IP (sub_domains:list) -> list:
  data = list ()
  for sub_domain in sub_domains:
    print ("Processing sub domain: {} ".format (sub_domain), end="")
    try:
      ping = subprocess.run ("ping {} -n -c 1".format (sub_domain), stdout=subprocess.PIPE, shell=True)
      output = ping.stdout.decode ("UTF-8")
      IP = output.split ("\n")[0].split ("(")[1].split (")")[0]
      data.append ([sub_domain, IP])
      print ("IP: {}".format (IP))
    except:
      print ("")
  return data

def get_IP6 (sub_domains:list) -> list:
  data = list ()
  for sub_domain in sub_domains:
    print ("Processing sub domain: {} ".format (sub_domain), end="")
    try:
      ping = subprocess.run ("ping6 {} -n -c 1".format (sub_domain), stdout=subprocess.PIPE, shell=True)
      output = ping.stdout.decode ("UTF-8")
      IP = output.split ("\n")[0].split ("(")[1].split (")")[0]
      data.append ([sub_domain, IP])
      print ("IP: {}".format (IP))
    except:
      print ("")
  return data

def store(data, path):
  with open(path, "w") as f:
    for i in data:
      f.write(f"{i[0]}--{i[1]}")


if __name__=="__main__":
  with open("website.txt","r") as f:
    websites = f.read().split("\n")
    ipv4 = get_IP(websites)
    store(ipv4, "ipv4.txt")
    proceed = input("Proceed for IPv6 (yes/no): ") == "yes"
    if (proceed):
      ipv6 = get_IP6(websites)
      store(ipv6, "ipv6.txt")