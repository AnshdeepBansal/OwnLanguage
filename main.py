from components.helper import basic

try:
    ans = input("Do you want to see internal working? type - Y or N\n")
    if ans == 'Y' or ans == 'y':
        while True:
            text = input('basic > ')
            if text.strip() == "":
                continue
            result, error = basic.run('<stdin>', text)
            
            if error:
                print(error.as_string())
            elif result:
                if len(result.elements) == 1:
                    print(repr(result.elements[0]))
                else:
                    print(repr(result))
    else:
        while True:
            text = input('basic > ')
            if text.strip() == "":
                continue
            result, error = basic.run_without_prints('<stdin>', text)
            
            if error:
                print(error.as_string())
            elif result:
                if len(result.elements) == 1:
                    print(repr(result.elements[0]))
                else:
                    print(repr(result))
        
except KeyboardInterrupt:
    print("\nExiting...")
