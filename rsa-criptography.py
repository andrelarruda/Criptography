# PARTE 1 - Exponencial modular
def get_binary(num):
    return bin(num)[2::]

def exponencial_modular(a, b, n):
    r = 1
    x = a
    binary_exp = get_binary(b)
    for i in range(len(binary_exp)-1, -1, -1):
        result = x % n
        if(binary_exp[i] == str(1)):
            r *= result
        if(i != 0):
            x = result ^ 2
        else:
            break
    return r % n

# PARTE 3 - Criptografia RSA (fonte: docdroid.net/Hb50yD1/criptografia-criptografia-rsa-pdf#page=5)

def hasCommonDivisors(num1, num2):
    return gcd(num1, num2) != 1

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modular_multiplicative_inverse(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


# Algoritmo de geração de senhas:
def generate_passwords(char_quantity):
    if char_quantity < 1:
        return 0
    P = sage.sets.primes.Primes()
    initial_num = 10 ^ (char_quantity - 1)
    final_num = (10 ^ char_quantity) - 1
    result = []
    while len(result) < 2:
        random_num = randint(initial_num, final_num)
        prime = P.next(Integer(random_num))
        if len(str(prime)) == char_quantity and (prime not in result):
            result.append(prime)
    p, q = result
    n = p*q
    totient_n = (p - 1) * (q - 1)
    # encontrar e = numero arbitrário entre 1 e totient_n, mas que não possui nenhum divisor em comum com totient_n
    e_exists = False
    e = 0
    while e_exists is False:
        e = randint(2, totient_n-1)
        if(not(hasCommonDivisors(e, totient_n))):
            e_exists = True
    d = modular_multiplicative_inverse(e, totient_n)
    public_keys = [n, e]
    private_keys = [p, q, d]
    return public_keys, private_keys

# Encriptação

def convert_to_ascii(text):
    return [ord(c) for c in text]

def encrypt(m, n, e):
    result = ""
    message_ascii = convert_to_ascii(m)
    ciphered_ascii_list = []
    for plain_num in message_ascii:
        ciphered_num = exponencial_modular(plain_num, e, n) # utilizei esta função por questões de otimização
        ciphered_ascii_list.append(ciphered_num)
    return ciphered_ascii_list


# Decriptação
def from_ascii_to_text(ascii_list):
    return ''.join(chr(i) for i in ascii_list)

def decrypt(ciphered_list, n, d):
    plain_text_ascii = []
    for ciphered_letter_ascii in ciphered_list:
        plain_letter_ascii = exponencial_modular(ciphered_letter_ascii, d, n)
        plain_text_ascii.append(plain_letter_ascii)
    plain_text = from_ascii_to_text(plain_text_ascii)
    return plain_text


#Testing:
mensagem = "Esta é uma mensagem para teste do(s) algoritmo(s)!!! :D"
passwords = generate_passwords(2)
public = passwords[0]
private = passwords[1]
n, e = public
d = private[2]

ciphered_message_list = encrypt(mensagem, n, e)
print('Mensagem encriptada: ')
print(ciphered_message_list)
print('\n**********************************************************')
print('Mensagem decriptada:')
print(decrypt(ciphered_message_list, n, d))
