import requests
from bs4 import BeautifulSoup
import fire

def check(location="woolworths-marsfield"):
    url = f"https://returnandearn.org.au/return_point/{location}/"

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-AU,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
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
    
    bold_location = f"\033[1m{location}\033[0m"
    print(f"Checking for {bold_location}...")
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.content, "html.parser")

    full_divs = soup.find_all("div", class_="c-return-point-status-detail-color closed")

    if full_divs:
        glass_full = full_divs[0].get_text(strip=True)
        plastic_full = full_divs[1].get_text(strip=True)
    else:
        # print("Availability not found")
        glass_full = ""
        plastic_full = ""
        
    busy_divs = soup.find_all("div", class_="range-label")

    if busy_divs:
        glass_busy = busy_divs[0].get_text(strip=True)
        plastic_busy = busy_divs[1].get_text(strip=True)
    else:
        # print("Busyness not found")
        glass_busy = ""
        plastic_busy = ""

    print(f"Glass:          {glass_full} | {glass_busy}")
    print(f"Plastic & cans: {plastic_full} | {plastic_busy}")

if __name__ == "__main__":
    fire.Fire(check)
