def list_to_str(list_items):
    s = ""
    for item in list_items:
        s += item+","
    return s[:-1]

def datetime_to_m_d_y(date):
    return f"{date.month}/{date.day}/{date.year%100}"