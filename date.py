from datetime import datetime

print(datetime.now().strftime("%Y,%m,%d"))
date = datetime.now().strftime("%Y,%m,%d")
date = date.split(",")

year = date[0]
month = date[1]
day = date[2]

print(year, day, month)
