import schedule
import time

def sets_updater():
    print("Updating sets")
    time.sleep(5)
    print("Sets updated")

schedule.every(10).seconds.do(sets_updater)

while True:
    schedule.run_pending()