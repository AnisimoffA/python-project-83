import requests

try:
    r = requests.get('https://python-page-analyzer-ru.hexlekmt.app/')
    status_code = r.status_code
except Exception:
    status_code = None
    
    
print(status_code)