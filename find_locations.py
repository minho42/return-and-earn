import requests
import re
import json

def extract_value(key: str, data_str: str):
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

def find(lat: str = "0", long: str = "0"):
    url = f"https://returnandearn.org.au/return-points/"

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

    pre_split ='var globalReturnPointsData'
    post_split = "}]}.data;"

    html_string = response.text
    html_string = html_string.split(pre_split)[1]
    html_string = html_string.split(post_split)[0]

    while True:
        cp_url = extract_value("cp_url", html_string[start:])
        
        if cp_url:
            parts = cp_url.split('return_point\\/')
            if len(parts) > 1:
                return_point_name = parts[1].split('\\')[0]
            else:
                return_point_name = None
        else:
            return_point_name = None
        
        cp_title = extract_value("cp_title", html_string[start:])
        cp_address = extract_value("cp_address", html_string[start:])
        cp_city = extract_value("cp_city", html_string[start:])
        cp_state = extract_value("cp_state", html_string[start:])
        cp_postcode = extract_value("cp_postcode", html_string[start:])
        cp_latitude = extract_value("cp_latitude", html_string[start:])
        cp_longitude = extract_value("cp_longitude", html_string[start:])
        cp_collection_point_type = extract_value("cp_collection_point_type", html_string[start:])
        
        # to break if not cp_title alone?
        if not cp_title and not cp_url:
            break
        
        if return_point_name: 
            return_points.append({
                "name": cp_title,
                "return_point_name": return_point_name,
                "address": cp_address,
                "city": cp_city,
                "state": cp_state,
                "postcode": cp_postcode,
                "lat": cp_latitude,
                "long": cp_longitude,
                "collection_point_type": cp_collection_point_type,
            })
        
        # Update start to move forward in the text (avoid infinite loop)
        start = html_string.find('"cp_url":"', start) + 1

    # print(return_points)
    print(f"{len(return_points)} return points found")
    
    JSON_FILE_NAME = "return_points.json"
    print(f"saving return_points to json: {JSON_FILE_NAME}")
    with open(JSON_FILE_NAME, 'w') as file:
        json.dump(return_points, file, indent=2)

my_location = {
    'lat': "-33.7792018",
    'long': "151.1155455"    
}


find(my_location['lat'], my_location['long'])
# find()