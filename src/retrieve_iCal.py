import requests
import config

def download_ical_file(url, output_filename):
    try:
        # Fetch the iCal file from the provided URL
        response = requests.get(url)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Write the content to a local .ics file
            with open(output_filename, 'wb') as file:
                file.write(response.content)
            print(f"iCal file saved as {output_filename}")
        else:
            print(f"Failed to retrieve iCal file. HTTP status code: {response.status_code}")
    except Exception as e:
        print(f"Error occurred: {e}")


# Example usage
def retrieveICSfile():
    ical_url = config.ICAL_URL
    filename = config.PATH_TO_CANVAS_CALENDAR
    download_ical_file(ical_url, filename)
