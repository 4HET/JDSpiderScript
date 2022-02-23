import time

import schedule
import send_message
import get_com_all_inform_json
import login


def test():
    print("running...")
def send():
    send_message.main()

schedule.every().day.at("07:00").do(send)
schedule.every(43200).minutes.do(login.login)

login.login()
# get_com_all_inform_json.main()

while True:
    get_com_all_inform_json.main()
    schedule.run_pending()
    time.sleep(1)