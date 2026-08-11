import os, dotenv

dotenv.load_dotenv()


def check_gym_nr():
    try: 
        nr = os.getenv("GYM_NR")
        nr = nr.split(",")
        how_many = 0
        for i in nr:
            how_many += 1 
            int(i)
        if how_many > 105:
            return False

    except ValueError:
        return False
    return True


def check_webhook():
    webhook = os.getenv("WEBHOOK_URL")
    if not ("https://discordapp.com/api/webhooks/" in webhook):
        return False
    return True


def check_webhook_send():
    webhook_send = os.getenv("SEND_WEBHOOK")
    if webhook_send in [True, False]:
        return True
    return False


