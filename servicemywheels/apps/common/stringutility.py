def is_not_null_empty(check_string):
    if check_string == None:
        return False
    else:
        str_length = len(check_string)
        if str_length == 0:
            return False
        else:
            return True
