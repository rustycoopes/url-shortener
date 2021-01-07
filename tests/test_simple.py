from nanoid import generate


def test_pass():

    print(generate('1234567890abcdef', 5)) # => "4f9zd13a42"
    print(generate(size=10)) # => "IRFa-VaY2b"
    return True