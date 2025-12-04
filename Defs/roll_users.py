import random

def roll_users(users: list):
    ran = random.sample(users, len(users))
    for idx in range(len(ran)):
        current = ran[idx]
        next_ = ran[(idx+1) % len(ran)]
        print(current, ">", next_)
        
