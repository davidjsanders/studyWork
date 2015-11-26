error_list = []
for link in links:
    try:
        validate(links[link], schema)
    except exceptions.ValidationError as ve:
        error_list.append(links[link])
        print(ve.message)
for error in error_list:
    print(error)

