import os, dotenv

dotenv.load_dotenv()



def check_gym_nr():
    try: 
        nr = os.getenv("gym_nr")
        nr = nr.split(",")
        for i in nr:
            int(i)
    except ValueError:
        return False
    return True

def check_webhook():
    webhook = os.getenv("webhook_url")
    if not ("https://discordapp.com/api/webhooks/" in webhook):
        return False
    return True


def check_webhook_send():
    webhook_send = os.getenv("webhook_send")
    if webhook_send in [True, False]:
        return True
    else:
        return False


