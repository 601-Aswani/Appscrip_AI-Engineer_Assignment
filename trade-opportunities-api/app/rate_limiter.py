import time

RATE_LIMIT = 5  # requests
WINDOW = 60     # seconds

user_requests = {}


def check_rate_limit(token: str):
    now = time.time()

    if token not in user_requests:
        user_requests[token] = []

    user_requests[token] = [
        t for t in user_requests[token] if now - t < WINDOW
    ]

    if len(user_requests[token]) >= RATE_LIMIT:
        raise Exception("Rate limit exceeded")

    user_requests[token].append(now)
