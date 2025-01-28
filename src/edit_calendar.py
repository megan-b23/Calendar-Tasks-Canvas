import os
import re
from ics import Calendar
from collections import defaultdict
import config  # Importing your config module

# Function to read an ICS file and return a calendar object
def read_ics_file(file_path):
    with open(file_path, 'r') as f:
        calendar = Calendar(f.read())
    return calendar

# Function to extract the course code from the event's SUMMARY field (e.g., PHY131, CSE355)
def extract_course_code(summary):
    # Match course code in the format [2025SpringC-T-COURSECODE-SOMENUMBER] or [2025SpringC-T-COURSECODE-SOMENUMBER-SOMENUMBER]
    match = re.search(r'\[.*?-(\w+)-\d+(-\d+)?\]', summary)
    if match:
        return match.group(1).upper()  # Return the course code in uppercase for case-insensitive comparison
    return None

# Function to group events by course (using the course code extracted from the SUMMARY field)
def group_events_by_course(calendar):
    course_events = defaultdict(list)
    
    # Iterate through each event and group by course code
    for event in calendar.events:
        course_code = extract_course_code(event.name)
        if course_code:
            course_events[course_code].append(event)
    
    return course_events

# Function to set the PRODID to "icalendar-ruby"
def set_prodid_to_icalendar_ruby(calendar):
    # Set the PRODID field in the calendar metadata
    calendar.prodid = "-//icalendar-ruby//NONSGML v1.0//EN"

# Function to save events of a specific course into an individual ICS file
def save_course_to_ics(course_code, events, output_dir):
    course_calendar = Calendar()
    
    # Add all the events for this course to the new calendar
    for event in events:
        course_calendar.events.add(event)

    # Set the PRODID to icalendar-ruby
    set_prodid_to_icalendar_ruby(course_calendar)
    
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Define the path for the new ICS file for this course
    output_path = os.path.join(output_dir, f"{course_code}.ics")

    course_calendar.prodid = "icalendar-ruby"

    # Write the new calendar to a file
    with open(output_path, 'w') as f:
        for line in course_calendar.serialize().splitlines():
            if 'PRODID:' in line:
                f.write('PRODID:icalendar-ruby\n')
            else:
                f.write(line + '\n')  # Write each line with a newline at the end
    print(f"Created ICS file for course '{course_code}' at {output_path}")

# Main function to process the input file and divide it by course
def split_courses_into_ics(input_ics_file, output_dir):
    # Read the input ICS file
    calendar = read_ics_file(input_ics_file)
    
    # Group events by course
    grouped_events = group_events_by_course(calendar)
    
    # Ensure that we create a calendar for each class in config.LIST_OF_CLASSES
    for course_code in config.LIST_OF_CLASSES:
        course_code = course_code.upper()  # Compare with uppercase
        events = grouped_events.get(course_code, [])  # Default to empty list if no events for this course
        save_course_to_ics(course_code, events, output_dir)

        if not events:
            print(f"Created empty ICS file for course '{course_code}' because it has no events.")

def run_edit_calendar():
    # Specify the input ICS file and the output directory
    input_ics_file = 'C:\\Users\\meggy\\OneDrive\\Documents\\GitHub\\Canvas-Tasks-and-Calendar-Obsidian\\canvas_calendar.ics'  # Path to your semester ICS file
    output_dir = 'C:\\Users\\meggy\\OneDrive\\Documents\\GitHub\\Calendars\\'         # Directory to save the individual ICS files
    # Call the function to split and save the courses
    split_courses_into_ics(input_ics_file, output_dir)
