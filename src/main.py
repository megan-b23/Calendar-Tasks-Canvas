from edit_calendar import run_edit_calendar
from get_tasks import run_get_tasks
from retrieve_iCal import retrieveICSfile
import config

def main():
    retrieveICSfile()
    run_edit_calendar()

    if config.TASKS:
        run_get_tasks()

main()