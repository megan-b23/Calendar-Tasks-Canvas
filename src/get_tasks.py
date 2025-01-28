import config

def writeTo(lines):
    path = config.TASKS_DESTINATION
    for line in lines:
        for name in config.LIST_OF_CLASSES:
            if f"[[{name}]]" in line:
                print(line)
                fn = f"{path}\\{name}\\TODO.md"
                with open(fn, 'a', encoding="utf-8") as new_cal:
                    new_cal.write(line.strip()+"\n")
                break

def run_get_tasks():
    classes_list = config.LIST_OF_CLASSES
    calendars_path = config.CALENDARS_DESTINATION

    tasks_list = []
    tasks_to_add = []
    dates_to_add = []
    task_name = ''

    for name in classes_list:
        tasks_to_add = []
        dates_to_add = []
        with open(f"{calendars_path}\\{name}.ics", 'r') as cal:
            for line in cal:
                if "SUMMARY:" in line:
                    rmv_pre = line.removeprefix("SUMMARY:")
                    split_str = rmv_pre.split("[")
                    task_name = split_str[0]
                    tasks_to_add.append(task_name)
                elif "DTSTART;VALUE=DATE;VALUE=DATE:" in line:
                    rmv_pre = line.removeprefix("DTSTART;VALUE=DATE;VALUE=DATE:")
                    date, year, month, day = '', '', '', ''
                    i = 0
                    while i < 4:
                        year += rmv_pre[i]
                        i+=1
                    date += f"{year}-"

                    while i < 6:
                        month += rmv_pre[i]
                        i+=1
                    date += f"{month}-"

                    while i < 8:
                        day += rmv_pre[i]
                        i+=1
                    date += day
                    dates_to_add.append(date)
            for task,date in zip(tasks_to_add,dates_to_add):
                new_task = "- [ ] " + task + f"[[TODO - {name}|{name}]] 📅 {date}" 
                tasks_list.append(new_task)
                #print(new_task)

    writeTo(tasks_list)

    print("\n---Tasks Process Complete---\n")