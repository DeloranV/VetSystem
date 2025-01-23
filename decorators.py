
def check_number(func):
    def wrapper(*args, **kwargs):
        if args:
            return print(func(*args, **kwargs))
        elif not args:
            return print("No arguments")
    return wrapper

def suma(a,b): return a+b

check_number(suma)()