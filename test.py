

with open("vars.env", "r") as f:
    data = f.readlines()
    for i in data:
        if "PASSWORD" in i:
            password = i.strip().split("=", 1)
            break

    password = password[1]
    length = len(password)-1
    first, last = password[0], password[-1]
    if first == last:
        password = password.strip(f"{first}")
    print(password)