from core.CaesarCipher import caesarCipher

TEST_PASSKEY = "Supper secret password"
TEST_MESSAGE = "hello world"
TEST_MESSAGE_ENCODED_1 = "mjqqt btwqi"
TEST_MESSAGE_ENCODED_2 = "dahhk sknhz"

def test_encoding():
    coder = caesarCipher()
    result = coder.encode(5,TEST_MESSAGE)

    assert result == TEST_MESSAGE_ENCODED_1

def test_decoding():
    coder = caesarCipher()
    result = coder.decode(5,TEST_MESSAGE_ENCODED_1)

    assert result == TEST_MESSAGE

def test_encoding_with_passkey():
    coder = caesarCipher()
    shift = coder.string_to_shift(TEST_PASSKEY)
    result = coder.encode(shift,TEST_MESSAGE)

    assert result == TEST_MESSAGE_ENCODED_2

def test_decoding_with_passkey():
    coder = caesarCipher()
    shift = coder.string_to_shift(TEST_PASSKEY)
    result = coder.decode(shift, TEST_MESSAGE_ENCODED_2)

    assert result == TEST_MESSAGE
