
def data_merge(x,y):
    data = []

    for item_data_one in x:
        new_template = {}
        for item_data_two in y:
            if item_data_one["Community"] == item_data_two["Community"]:
                new_template = item_data_one | item_data_two
                break
        data.append(new_template)
    return data

def change_key_name(data, original, new):
    new_data = []
    for element in data:
        template = {}
        for key, value in element.items():
            template[key] = value
        template[new] = template[original]
        template.pop(original)
        new_data.append(template)

    return new_data 
