import time

def print_log(log_text) :
    print('[' + time.strftime("%Y_%m_%d_%H_%M_%S") + '] : ' + str(log_text))
def get_log_text(log_text): 
    return '[' + time.strftime("%Y_%m_%d_%H_%M_%S") + '] : ' + str(log_text)
