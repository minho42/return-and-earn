import requests
import re

def extract_value(key, data_str):
    # Create a pattern to match the key and capture its value (string, number, null)
    pattern = re.compile(rf'"{key}":\s*(?P<value>".*?"|\d+|null)')
    match = pattern.search(data_str)
    
    if match:
        value = match.group('value')
        if value.startswith('"') and value.endswith('"'):
            return value.strip('"')
        elif value == 'null':
            return None
        else:
            return value
    return None  # Return None if the key is not found

url = f"https://returnandearn.org.au/return-points/"
lat = "-33.7792018"
long = "151.1155455"

payload = {}
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-AU,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Cookie': f"locationName=nearby; latitude={lat}; longitude={long}",
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"'
}

response = requests.get(url, headers=headers, data=payload)
print(f"response.status_code: {response.status_code}")

return_points = []
start = 0

# Use extract_value to get the values of cp_title, return_point_name, cp_latitude, and cp_longitude
while True:
    cp_url = extract_value("cp_url", response.text[start:])
    
    if cp_url:
        parts = cp_url.split('return_point\\/')
        if len(parts) > 1:
            return_point_name = parts[1].split('\\')[0]
        else:
            return_point_name = None
    else:
        return_point_name = None
    
    cp_title = extract_value("cp_title", response.text[start:])
    cp_address = extract_value("cp_address", response.text[start:])
    cp_city = extract_value("cp_city", response.text[start:])
    cp_state = extract_value("cp_state", response.text[start:])
    cp_postcode = extract_value("cp_postcode", response.text[start:])
    cp_latitude = extract_value("cp_latitude", response.text[start:])
    cp_longitude = extract_value("cp_longitude", response.text[start:])
    
    if not cp_title and not cp_url:
        break  # Exit the loop when no more points are found
    
    # Append dictionary to return_points if the required data is found
    return_points.append({
        "name": cp_title,
        "return_point_name": return_point_name,
        "address": cp_address,
        "city": cp_city,
        "state": cp_state,
        "postcode": cp_postcode,
        "lat": cp_latitude,
        "long": cp_longitude
    })
    
    # Update start to move forward in the text (avoid infinite loop)
    start = response.text.find('"cp_url":"', start) + 1

print(return_points)
print(f"{len(return_points)} return points found")
