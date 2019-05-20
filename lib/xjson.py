
def readcom(file):
    """
    Read file, ignoring comments
    :param file: file, what is needed to read
    :return: text, found in file
    """
    f = open(file, "r")
    res = ''
    for i in f:
        res += i.split('//')[0] + '\n' * int(len(i.split('//')) > 1)
    return res