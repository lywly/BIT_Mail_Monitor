import os


def kc_save(data):
    with open('cache.txt', 'w') as f:
        for value in data:
            f.write(str(value))
            f.write('\n')


def kc_load():
    new_data = []
    try:
        with open('cache.txt', 'r') as f:
            data = list(f)
            for value in data:
                new_value = value.replace('\n', '')
                new_data.append(new_value)
    except:
        pass
    return new_data


def kc_delete():
    try:
        os.remove('cache.txt')
        print('    ---------------------------------')
        print('    |                               |')
        print('       |      关键词缓存已清理       |')
        print('       |      关键词缓存已清理      |')
        print('    |                               |')
        print('    ---------------------------------')
    except:
        pass
