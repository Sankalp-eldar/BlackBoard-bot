import time
from datetime import datetime as dt
import datetime as dtp
import re, csv
from collections import OrderedDict




string = r"(21...-\d\d\d):(.):: Gp-(.)"
pattern = re.compile(string)


timestamps = {
    "09:40 - 10:20 AM" : "09:40",
    "10:30 - 11:10 AM" : "10:30",
    "11:20 - 12:00 PM" : "11:20",
    "1:00 - 1:40 PM" : "13:00",
    "1:50 - 2:30 PM" : "13:50",
    "2:40 - 3:20 PM" : "14:40",
    "3:30 - 4:10 PM" : "15:30"
}

cources = {
    "21CSH-101" : "CS",
    "21ECP-102" : "DT",
    "21ELH-101" : "BEEE",
    "21GPT-121" : "Gen",
    "21MEP-102" : "CAD",
    "21SMT-121" : "Math",
    "21SPH-141" : "Phy",
    "21UCH-105" : "Comm.",
    "21UCT-101" : "DTC",
    "21UCT-103" : "LS"
}
cources_unique = {"DT", "Math"}
fields = ["Session", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]


def get_today_course(day, filename):
    with open(filename, 'r') as f:
        reader = csv.DictReader(f, fieldnames = fields)
        next(reader)
        today = OrderedDict()
        for i in reader:
            _time = i['Session']
            _class = i[day]
            if _class:
                today[_time] = _class
    return today


def find_current_course(current_time :dt, cources):
    for i in cources:
        now = current_time.strftime("%H %M").split()
        now = list(map(int, now))
        course_time = list(map(int, i.split(":") ))

        try:
            class_time
        except NameError:
            class_time = course_time, i

        if now >= course_time:
            class_time = course_time, i

    return class_time


# current_time = dt.now()

# day = current_time.strftime("%a")

# cources = get_today_course(day, 'hi.csv')

# N = dt(2021, 10, 7, 14, 51, 00)

# x = find_current_course(N, cources)
# cources[ x[1] ]




def read_csv(filename):
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)
        for line in reader:
            if len(line) >= 3:
                yield line

def write_csv(filename, data : list):
    with open( filename , 'w', newline = "\n") as f:
        csv.writer(f).writerows(data)

def add_course(row, CourseCode):
    subject = pattern.search(CourseCode)
    if subject:
        sub = cources[subject.group(1)]

        if sub in cources_unique:
            sub = f'{sub}{"-A" if subject.group(3) == "A" else "-B"}'

        row.append(sub)
        return
    row.append("")

def create_rows(data):
    head = [fields]
    prev_session = ''
    row = []
    for i in data:
        if i[0] == prev_session:
            add_course(row, i[-1])
        else:
            head.append(row) if row else None
            row = [
                timestamps[i[0]]
                ]
            add_course(row, i[-1])
        prev_session = i[0]
    head.append(row)
    return head


def generate_course(input_file, output_file):
    data = read_csv(input_file)

    rows = create_rows(data)

    write_csv(output_file, rows)
    return output_file


