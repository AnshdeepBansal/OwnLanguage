from components import run

try:
    while True:
        text = input('basic > ')
        if text.strip() == "":
            continue
        result, error = run('<stdin>', text)

        if error:
            print(error.as_string())
        elif result:
            if len(result.elements) == 1:
                print(repr(result.elements[0]))
            else:
                print(repr(result))
except KeyboardInterrupt:
    print("\nExiting...")
