def list_to_str(list_items):
    s = ""
    for item in list_items:
        s += item+","
    return s[:-1]