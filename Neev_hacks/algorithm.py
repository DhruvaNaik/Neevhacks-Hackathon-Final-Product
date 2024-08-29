from secrets import randbelow, choice

# Parameters
n = 2**10
q = 2**16
err = [0, 1]

# Function to generate a random vector of given length and range
def generate_random_vector(length, range_limit):
    return [randbelow(range_limit) for _ in range(length)]

# Function to generate an error vector - LWE
def generate_error_vector(length, error_values):
    return [choice(error_values) for _ in range(length)]

# Generate vectors
a = generate_random_vector(n, q)
s = generate_random_vector(n, q)
e = generate_error_vector(n, err)
r = generate_error_vector(n, err)

# Function to compute public key
def generate_public_key(a, s, e, modulus):
    return [((A * S) + E) % modulus for A, S, E in zip(a, s, e)]

b = generate_public_key(a, s, e, q)

# Function to convert a string to a binary list
def string_to_binary_list(input_string):
    binary_list = [int(bit) for char in input_string for bit in format(ord(char), '08b')]
    return binary_list

# Function to convert a binary list back to a string
def binary_list_to_string(binary_list):
    if len(binary_list) % 8 != 0:
        raise ValueError("The binary list length must be a multiple of 8.")
    
    string_output = "".join(chr(int(''.join(map(str, binary_list[i:i+8])), 2)) for i in range(0, len(binary_list), 8))
    return string_output

# Example usage
input_string = 'enter a string'
m = string_to_binary_list(input_string)
print("Binary representation of the message:", m)
print("Length of the binary message:", len(m))

# Function to encrypt the message
def encrypt_message(r, a, b, m, q):
    c1 = [(R * A) % q for R, A in zip(r, a)]
    c2 = [((R * B) + (M * (q // 2))) % q for R, B, M in zip(r, b, m)]
    return c1, c2

def en_message(message):
    m = string_to_binary_list(message)
    c1, c2 = encrypt_message(r, a, b, m, q)
    return c2

c1, c2 = encrypt_message(r, a, b, m, q)

# Function to decrypt the message
def decrypt_message(c1, c2, s, q):
    m_1 = [(C1 * S) % q for C1, S in zip(c1, s)]
    m_e = [(C2 - M1) % q for C2, M1 in zip(c2, m_1)]
    
    decoded_message = [
        0 if abs(d-0) < abs(d-(q/2)) else 1
        for d in m_e
    ]
    return decoded_message

def decr_message(message):
    m = decrypt_message(c1,message,s,q)
    final_msg = binary_list_to_string(m)
    return final_msg
    
decoded_message = decrypt_message(c1, c2, s, q)
print("Decrypted binary message:", decoded_message)

# Convert the decoded binary list back to a string
final_message = binary_list_to_string(decoded_message)
print("Decrypted string message:", final_message)

# Check if the original binary message and decoded message match
if a == decoded_message:
    print("Decrypted original binary message")

else: 
    print("Failed to decrypt - does not match")

print(en_message('gaurav'))
print(decr_message(c2))