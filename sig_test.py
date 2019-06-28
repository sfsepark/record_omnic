import signal

a = True

def handler(signum,f):
    print(signum)
    a = False

signal.signal(35, handler)

while a :
    pass
