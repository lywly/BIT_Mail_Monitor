import os

from Mail_Push_Core.myprint import myprint


def kc_save(data):
    if not os.path.isdir('./cache'):
        os.makedirs('./cache')
    with open('./cache/cache.txt', 'w') as f:
        for value in data:
            f.write(str(value))
            f.write('\n')


def kc_load():
    new_data = []
    try:
        if not os.path.isdir('./cache'):
            os.makedirs('./cache')
        with open('./cache/cache.txt', 'r') as f:
            data = list(f)
            for value in data:
                new_value = value.replace('\n', '')
                new_data.append(new_value)
    except:
        pass
    return new_data


def cache_delete():
    try:
        os.remove('./cache/cache.txt')
        os.remove('./cache/print_cache.txt')
        myprint('    ---------------------------------')
        myprint('    |                               |')
        myprint('      |   关键词缓存与打印缓存已清理   |')
        myprint('    |                               |')
        myprint('    ---------------------------------')
    except:
        pass
