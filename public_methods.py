#for handle with_deleted q
def str_to_bool(value):
    if isinstance(value, bool):
        return value
    if value.lower() in ('true', '1', 't', 'y', 'yes'):
        return True
    elif value.lower() in ('false', '0', 'f', 'n', 'no'):
        return False
    return False
