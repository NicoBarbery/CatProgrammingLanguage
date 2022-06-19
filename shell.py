import cat

while True:
    text = input('Cat > ')
    result, error = cat.run('<stdin>', text)

    if error:
        print(error.as_string())
    else:
        print(result)