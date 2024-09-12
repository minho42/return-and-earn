import requests

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

response = requests.request("GET", url, headers=headers, data=payload)
print(f"response.status_code: {response.status_code}")

return_points = []

# Extract return points, latitudes, and longitudes
start = 0
while True:
    # Extract cp_title
    title_start = response.text.find('"cp_title":"', start)
    if title_start != -1:
        title_end = response.text.find('"', title_start + 12)
        cp_title = response.text[title_start + 12:title_end]
    else:
        cp_title = ""
    
    # Find return_point name
    start = response.text.find('"cp_url":"', start)
    if start == -1:
        break
    end = response.text.find('"', start + 10)
    cp_url = response.text[start + 10:end]
    start = end + 1
    
    parts = cp_url.split('return_point\\/')
    if len(parts) > 1:
        return_point_name = parts[1].split('\\')[0]
         
        # Extract latitude and longitude
        latitude_start = response.text.find('"cp_latitude":"', start)
        if latitude_start != -1:
            latitude_end = response.text.find('"', latitude_start + 15)
            cp_latitude = response.text[latitude_start + 15:latitude_end]
        
        longitude_start = response.text.find('"cp_longitude":"', latitude_end)
        if longitude_start != -1:
            longitude_end = response.text.find('"', longitude_start + 16)
            cp_longitude = response.text[longitude_start + 16:longitude_end]
        
        # Append dictionary to return_points
        return_points.append({
            "name": cp_title,
            "return_point_name": return_point_name,
            "lat": cp_latitude,
            "long": cp_longitude
        })

print(return_points)
print(f"{len(return_points)} return points found")
