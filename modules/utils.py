import csv
from datetime import datetime

def readEventCollection (filename):
    file_contents = []
    with open(filename, 'r') as file:
        file_content = csv.DictReader(file)
        for row in file_content:
           file_contents.append(row)
    return file_contents


def formatDateTime (timeformat):
    splitdatetime = timeformat.split("T")
    date = splitdatetime[0]
    date = datetime.strptime(date, "%Y-%m-%d").date()
    date = f'{date.month}/{date.day}/{date.year}'
    timepart = splitdatetime[-1].split(":")
    hour = int(timepart[0])
    timeperiod = 'AM'

    if  hour > 12:
        hour = hour % 12
        timeperiod = 'PM'
    setime = f'{hour}:{timepart[1]} {timeperiod}'

    return date, setime