def colorize(string, color):
    return "%{F"+color+"}"+string+"%{F-}"

def bg(string, color):
    return "%{B"+color+"}"+string+"%{B-}"

def underline(string, color):
    return "%{U"+color+"}%{+u}"+string+"%{-u}"

def clickable(string, command):
    return "%{A:"+command+":}"+string+"%{A}"

def pad(string, num):
    return num*" "+string+" "*num

def is_num(string, field):
    """
    returns:
        success:    tuple of (True, [INT])
        fail:       tuple of (False, error_msg)
    """
    try:
        return int(string)
    except:
        print("{} needs to be a number, you supplied {}".format(field, string))
        return False
