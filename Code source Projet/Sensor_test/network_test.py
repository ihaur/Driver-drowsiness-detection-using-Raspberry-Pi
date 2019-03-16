import urllib3
http = urllib3.PoolManager()
r = http.request('GET', 'http://www.google.com')
r.status
print(r.status)
