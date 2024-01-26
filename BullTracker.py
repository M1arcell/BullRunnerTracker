import requests
import json
import time 

"""
USF BULL RUNNER TRACKER CODE

The Bull Runner Bus ETA Tracker is a meticulously crafted software solution designed to provide real-time ETA information for the University of South Florida's Bull Runner bus service. Developed with precision and efficiency in mind, this code leverages web scraping techniques to extract pertinent data from the official bus tracking system, offering a seamless and user-friendly experience for monitoring bus arrival.

Link To USF Bull Runner Map: https://passiogo.com/

This Project has been converted to Micropython. The decision to convert this project reflects the developer's commitment to staying at the forefront of technology. By adapting the solution to run on MicroPython, the developer showcases advanced skills in optimizing code for resource-constrained environments, a crucial competency in the rapidly evolving field of software development.

Wokwi is a powerful online platform instrumental in constructing this MicroPython project. It offers a risk-free space for designing, testing, and simulating circuits, enhancing your learning experience as a student. By showcasing my skills in software development on embedded systems, this project demonstrates proficiency in writing optimized code for controllers—an essential skill in the field of cybersecurity.

Link to Micropython Project: https://wokwi.com/projects/381869504327580673

Link to Python Project: https://replit.com/@m1arcell/USF-Bull-runner-Tracker

**DISCLAIMER: If code displays "No Vehicles," then bus ETA is outside of the USF Bull Runner Hours of Operations**
"""

# Function to display a waiting message
def display_waiting_message(message):
    print("\n" + "*" * 40)
    print(f"          {message}")
    print("*" * 40 + "\n")


# Define extract_numeric_part function
def extract_numeric_part(eta_str):
    # Extract numeric part of the string, e.g., '15 min ' or '3-4 min' -> '15' or '3'
    numeric_part = eta_str.split('-')[0].strip()

    # Remove any non-numeric characters, leaving only digits
    numeric_part = ''.join(c for c in numeric_part if c.isdigit())

    # Return 0 if numeric_part is empty
    return numeric_part if numeric_part else '0'


# Function to connect to WiFi
def connect_to_wifi():
    display_waiting_message("Connecting to WiFi")

    print("Grabbing the Bull by the Horns... Connecting", end="")
    # Adjust this part for regular Python WiFi connection
    # You might need to use a library like `wifi` or `pywifi` for Python(wowki[emulator] 'network')
    while not is_connected():  # Define your function to check if connected
        print(".", end="")
        time.sleep(0.1)
    print(" Bull Tamed! Connected!\n")


# Function to check if connected to WiFi
# Later use for ESP32 micropython Conversion
def is_connected():
    try:
        # Make a request to a known website
        response = requests.get("http://www.google.com", timeout=5)
        return True if response.status_code == 200 else False
    except requests.ConnectionError:
        return False


# Define the API endpoint URLs for stops

url_stop_1 = 'https://passiogo.com/mapGetData.php?eta=3&deviceId=22898923&stopIds=70778&routeId=40482&position=7&userId=2343&routeIds=40482,41819'

url_stop_2 = 'https://passiogo.com/mapGetData.php?eta=3&deviceId=22898923&stopIds=70779&routeId=40482&position=8&userId=2343&routeIds=40482,41819'

url_stop_3 = 'https://passiogo.com/mapGetData.php?eta=3&deviceId=22898923&stopIds=70780&routeId=40482&position=9&userId=2343&routeIds=40482'

url_stop_4 = "https://passiogo.com/mapGetData.php?eta=3&deviceId=22898923&stopIds=70781&routeId=40482&position=10&userId=2343&routeIds=40482"

url_stop_5 = "https://passiogo.com/mapGetData.php?eta=3&deviceId=22898923&stopIds=70783&routeId=40482&position=11&userId=2343&routeIds=40482"

url_stop_6 = "https://passiogo.com/mapGetData.php?eta=3&deviceId=22898923&stopIds=70749&routeId=40482&position=12&userId=2343&routeIds=40482"

url_stop_7 = "https://passiogo.com/mapGetData.php?eta=3&deviceId=22898923&stopIds=70777&routeId=40482&position=6&userId=2343&routeIds=40482"
url_stop_8 = "https://passiogo.com/mapGetData.php?eta=3&deviceId=22898923&stopIds=70776&routeId=40482&position=5&userId=2343&routeIds=40482"

url_stop_9 = "https://passiogo.com/mapGetData.php?eta=3&deviceId=22898923&stopIds=70787&routeId=40482&position=4&userId=2343&routeIds=40482"

url_stop_10 = "https://passiogo.com/mapGetData.php?eta=3&deviceId=22898923&stopIds=70786&routeId=40482&position=3&userId=2343&routeIds=40482"

# Define a dictionary to map stop IDs to their names
stop_names = {
    "70778": "00807 - N 46th St at USF Golf Center",
    "70779": "00815 - Skipper Rd at 43rd St",
    "70780": "00821 - N 42nd St at Hellenic Dr",
    "70781": "00827 - N 42nd St at Cambridge Woods Dr",
    "70783": "00829 - N 42nd St at Rocky Circle",
    "70749": "00411 - Palm Dr at Laurel Dr",
    # End of student housing Loop
    # Campus Stops
    "70777": "00803 - N 46th St at Shadow Moss Ln",
    "70776": "00801 - N 46th St at The Claw",
    "70787": "00970 - Parking Lot 56",
    "70786": "00966 - The Hub",
}

# Make GET requests for stops

response_stop_1 = requests.get(url_stop_1)
response_stop_2 = requests.get(url_stop_2)
response_stop_3 = requests.get(url_stop_3)
response_stop_4 = requests.get(url_stop_4)
response_stop_5 = requests.get(url_stop_5)
response_stop_6 = requests.get(url_stop_6)
response_stop_7 = requests.get(url_stop_7)
response_stop_8 = requests.get(url_stop_8)
response_stop_9 = requests.get(url_stop_9)
response_stop_10 = requests.get(url_stop_10)

# Dictionary to store historical wait times for each stop

historical_wait_times = {
    "70778": [],
    "70779": [],
    "70780": [],
    "70781": [],
    "70783": [],
    "70749": [],
    "70777": [],
    "70776": [],
    "70787": [],
    "70786": [],
}


# Function to calculate and display average wait time
def display_average_wait_time(stop_id):
    wait_times = historical_wait_times.get(stop_id, [])
    if wait_times:
        average_wait_time = sum(wait_times) / len(wait_times)
        print(f"Average Wait: {average_wait_time:.2f} mins")
    else:
        print(f"No historical data available for {stop_names[stop_id]}")

# Function to parse and display ETA data
def display_eta(response, stop_id):
    if response.status_code == 200:
        try:
            api_data = json.loads(response.text)
            eta_data = api_data.get("ETAs", {})
            stop_eta_list = eta_data.get(stop_id, [])
            stop_name = stop_names.get(stop_id, "Unknown Stop")

            if stop_eta_list:
                print(f"\nStop Name: {stop_name}")
                for eta_entry in stop_eta_list:
                    bus_name = eta_entry.get("busName")
                    eta_str = eta_entry.get("eta")
                    eta_time = int(extract_numeric_part(eta_str))  # Call extract_numeric_part function
                    print(f"    Bus Name: {bus_name}, ETA: {eta_time} mins")

                    # Record wait time in historical data
                    current_time = time.time()
                    historical_wait_times[stop_id].append(eta_time)

                # Calculate and display average wait time after updating historical data
                display_average_wait_time(stop_id)

            else:
                print(f"\nStop Name: {stop_name}")
                print("    No vehicles")
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON for Stop ID {stop_id}: {e}")
    else:
        print(f"Failed to fetch data for Stop ID {stop_id}. Status code: {response.status_code}")


# Display Header
print("\n" + "*" * 40)
print("       The Bull Runner Tracker")
print("*" * 40 + "\n")

# Connect to WiFi
connect_to_wifi()

# Wait for Bull Runner ETA
display_waiting_message("Waiting for Bull Runner ETA")
for _ in range(10):
    print(".", end="")
    time.sleep(1)
print("\nBull Runner ETA received!\n")

# Display ETA for each stop
display_eta(response_stop_1, "70778")
display_eta(response_stop_2, "70779")
display_eta(response_stop_3, "70780")
display_eta(response_stop_4, "70781")
display_eta(response_stop_5, "70783")
display_eta(response_stop_6, "70749")
display_eta(response_stop_7, "70777")
display_eta(response_stop_8, "70776")
display_eta(response_stop_9, "70787")
display_eta(response_stop_10, "70786")

