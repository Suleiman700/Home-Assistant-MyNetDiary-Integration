import requests
from bs4 import BeautifulSoup
import re

MyNetDiary_URL = "<YOUR COMMUNITY LINK HERE>"

def get_current_weight():
    current_weight = None
    start_weight = None
    lost_so_far = None

    try:
        """Fetch the current weight from the website."""
        # Send a GET request to the URL
        response = requests.get(MyNetDiary_URL)

        if response.status_code == 200:
            # Extract the HTML content
            html_content = response.text

            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(html_content, "html.parser")

            # Find the <ul> element containing the weight information
            weight_ul = soup.find("ul")

            # Extract the list items from the <ul> element
            weight_items = weight_ul.find_all("li")

            # Loop through the list items to find the current weight
            for item in weight_items:
                text = item.get_text()
                if "Current weight" in text:
                    weight = text.split(":")[1].strip()
                    # Remove non-numeric characters using regular expressions
                    numeric_weight = re.sub(r"[^\d.]", "", weight)
                    current_weight = float(numeric_weight)

                if "Start weight" in text:
                    current_start_weight = text.split(":")[1].strip()
                    start_weight = current_start_weight
                if "Lost so far" in text:
                    lost_so_far = text.split(":")[1].strip()

    except Exception as e:
        print(e)

    response = dict()
    response['current_weight'] = current_weight
    response['start_weight'] = start_weight
    response['lost_so_far'] = lost_so_far
    return response

results = get_current_weight()
print("Current weight:", results['current_weight'])
print("Start weight:", results['start_weight'])
print("Lost so far:", results['lost_so_far'])