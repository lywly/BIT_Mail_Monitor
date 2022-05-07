import os


def myprint(data):
    print(data)
    if not os.path.isdir('./cache'):
        os.makedirs('./cache')
    with open('./cache/print_cache.txt', 'a') as f:
        print(data, file=f)
