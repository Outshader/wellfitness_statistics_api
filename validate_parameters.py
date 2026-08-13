import os, dotenv

dotenv.load_dotenv()


def check_gym_ids(gym_ids):
    try: 
        gym_ids = gym_ids.split(",")
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
    webhook = os.getenv("WEBHOOK_URL", "")
    if not ("https://discordapp.com/api/webhooks/" in webhook):
        return False
    return True



