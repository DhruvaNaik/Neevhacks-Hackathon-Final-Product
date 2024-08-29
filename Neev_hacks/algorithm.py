from secrets import randbelow, choice

# Parameters
n = 2**10  # Vector length
q = 2**16  # Modulus for encryption
err = [0, 1]  # Error values for LWE

# Function to generate a random vector of given length and range
def generate_random_vector(length, range_limit):
    return [randbelow(range_limit) for _ in range(length)]

# Function to generate an error vector for LWE
def generate_error_vector(length, error_values):
    return [choice(error_values) for _ in range(length)]

# Function to compute public key
def generate_public_key(a, s, e, modulus):
    return [((A * S) + E) % modulus for A, S, E in zip(a, s, e)]

# Function to convert a string to a binary list
def string_to_binary_list(input_string):
    return [int(bit) for char in input_string for bit in format(ord(char), '08b')]

# Function to convert a binary list back to a string
def binary_list_to_string(binary_list):
    if len(binary_list) % 8 != 0:
        raise ValueError("The binary list length must be a multiple of 8.")
    return "".join(chr(int(''.join(map(str, binary_list[i:i+8])), 2)) for i in range(0, len(binary_list), 8))

# Function to encrypt the message
def encrypt_message(message, a, b, q):
    r = generate_error_vector(n, err)
    m = string_to_binary_list(message)
    c1 = [(R * A) % q for R, A in zip(r, a)]
    c2 = [((R * B) + (M * (q // 2))) % q for R, B, M in zip(r, b, m)]
    return c1, c2

# Function to decrypt the message
def decrypt_message(c1, c2, s, q):
    m_1 = [(C1 * S) % q for C1, S in zip(c1, s)]
    m_e = [(C2 - M1) % q for C2, M1 in zip(c2, m_1)]
    decoded_message = [0 if abs(d - 0) < abs(d - (q / 2)) else 1 for d in m_e]
    return binary_list_to_string(decoded_message)

# Encapsulated encryption function
def encrypt_text(text):
    a = generate_random_vector(n, q)
    s = generate_random_vector(n, q)
    e = generate_error_vector(n, err)
    b = generate_public_key(a, s, e, q)
    c1, c2 = encrypt_message(text, a, b, q)
    # Returning encrypted data and keys needed for decryption
    return {'cipher1': c1, 'cipher2': c2, 'secret_key': s, 'public_key': b, 'a': a}

# Encapsulated decryption function
def decrypt_text(encrypted_data):
    c1 = encrypted_data['cipher1']
    c2 = encrypted_data['cipher2']
    s = encrypted_data['secret_key']
    return decrypt_message(c1, c2, s, q)

# # Example usage
# text_to_encrypt = "Check"
# encrypted_data = encrypt_text(text_to_encrypt)
# print("Encrypted data:", encrypted_data)

# # Decrypt the message
# decrypted_message = decrypt_text(encrypted_data)
# print("Decrypted message:", decrypted_message)

# Check if the original and decrypted messages match
# assert text_to_encrypt == decrypted_message, "The original and decrypted messages do not match."

# Test with a different text
# print(decrypt_text(encrypt_text("Another test")))