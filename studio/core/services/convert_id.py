def convert_idTo(newField,list):
    for i in list:
        i[newField] = i.get("_id")
