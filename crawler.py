import requests
import re
import sys
import threading

def printUsage():
	print("Usage: crawler.py [target] [time-to-live]")

if len(sys.argv) < 2:
	printUsage()
	exit()

threads = []
def analyze(html, target, ttl):
	if ttl == 0:
		return
	hrefs = re.findall("<a\s+(?:[^>]*?\s+)?href=\"([^\"]*)\"", html)
	for href in hrefs:
		newTarget = href
		if not re.match("http.+", href):
			newTarget = target + href
		print("Going to " + newTarget + " from " + target)
		t = threading.Thread(target=analyze, args=(requests.get(newTarget).text, newTarget, ttl-1))
		threads.append(t)
		t.start()

	for t in threads:
		t.join()



tgt = sys.argv[1]
ttl = 0
try:
	ttl = int(sys.argv[2]) if len(sys.argv) >= 3 else 100
except ValueError:
	printUsage()
	exit()


r = requests.get(tgt)

if ttl == 0:
	exit()

if r.status_code == 200:
	#print(r.text.encode(sys.stdout.encoding, errors='replace'))
	analyze(r.text, tgt, ttl)
else:
	print(r.status_code, r.headers)