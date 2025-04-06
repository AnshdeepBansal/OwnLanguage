import components

while True:
    text = input('basic > ')
    result, error = components.run('<stdin>', text)

    if error: print(error.as_string())
    else: print(result)
