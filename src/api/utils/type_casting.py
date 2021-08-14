def type_casting(**kargs):
    return kargs

def str_to_dict(string):
    dic = {}
    for element in string.split(","):
        k_v = element.split('=')
        try:
            dic[k_v[0]] = int(k_v[1])
        except:
            dic[k_v[0]] = k_v[1]
    return dic