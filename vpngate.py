import requests, base64, tempfile, subprocess, time

country = raw_input("Enter country shortcode for filtering (blank for no filtering): ")
print("Getting VPN list...	")

line = 0
vpnid = 0
idtocfg = {}
for vpn in requests.get("http://www.vpngate.net/api/iphone/").text.split("\n"):
	line += 1
	if line > 2 and vpn is not "*":
		vpn = vpn.split(',')
		try:
			if country == "" or country == vpn[6]:
				print("#" + str(vpnid + 1) + "	" + vpn[1] + "		" + vpn[3] + " ms	" + str(int(vpn[4]) / 1024 / 1024) + " Mbps	" + vpn[6])
				vpnid += 1
				idtocfg[vpnid] = vpn[-1].replace("\r","")
		except IndexError:
			pass
id = int(raw_input("Enter ID to connect: "))

#below part was taken from Lazza's vpngate.py project
_, path = tempfile.mkstemp()
f = open(path, "w")
f.write(base64.b64decode(idtocfg[id]))
f.close()

x = subprocess.Popen(['sudo', 'openvpn', '--config', path])
try:
    while True:
        time.sleep(600)
except:
    try:
        x.kill()
    except:
        pass
    while x.poll() != 0:
        time.sleep(1)
    print("VPN terminated")