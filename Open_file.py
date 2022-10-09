try:
    filepath = 'test_fiile.txt'
    with open(filepath, 'r') as fio:
        result = fio.readlines()
    if not result:
        raise Exception('File is empty')

except (IOError, Exception) as e:
    result = []
    print(e)
