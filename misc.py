def open_file(path):
    f = open(path, "r")
    data = f.read().split("\n")
    f.close()
    return data
