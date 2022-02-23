def get_cookie():
    with open('cookie.txt', 'r', encoding='utf-8') as f:
        cookie = f.readline()
    return cookie