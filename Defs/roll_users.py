import random

def roll_users(users: list):
    ran = random.sample(users, len(users))
    return {ran[i]: ran[(i + 1) % len(ran)] for i in range(len(ran))}