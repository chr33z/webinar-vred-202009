from inspect import getframeinfo, stack

def info(message, caller = None):
    if caller is not None:
        message = "[{}]".format(caller.__class__.__name__) + " " + str(message)
    
    print(message)
    return message

def debug(message, caller = None):
    if caller is not None:
        message = "[{}]".format(caller.__class__.__name__) + " " + str(message)  

    caller = getframeinfo(stack()[1][0])
    message = '[L:{0}]'.format(caller.lineno) + " " + str(message)
    message = "[Debug]" + str(message)
    
    print(message)
    return message

def error(message, caller = None):
    if caller is not None:
        message = "[{}]".format(caller.__class__.__name__) + " " + str(message)

    if "[Error]" not in message:
        message = "[Error]" + str(message)
    print(message)
    return message