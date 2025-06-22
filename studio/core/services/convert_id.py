def convert_idTo(newField,list):

    try:
        for i in list:
            i[newField] = i.get("_id")

    except Exception as e:
        raise Exception("Não foi possível converter _id",e)
