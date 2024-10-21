import re

def valida_cpf(cpf):
    # Remove caracteres não numéricos
    cpf = re.sub(r'\D', '', cpf)
    
    # Verifica se o CPF tem 11 dígitos
    if len(cpf) != 11:
        return False
    
    # Verifica se todos os dígitos são iguais, o que torna o CPF inválido
    if cpf == cpf[0] * 11:
        return False

    # Calcula o primeiro dígito verificador
    soma = 0
    for i in range(9):
        soma += int(cpf[i]) * (10 - i)
    digito1 = (soma * 10 % 11) % 10

    # Calcula o segundo dígito verificador
    soma = 0
    for i in range(10):
        soma += int(cpf[i]) * (11 - i)
    digito2 = (soma * 10 % 11) % 10

    # Verifica se os dígitos verificadores calculados são iguais aos informados
    if cpf[-2:] == f'{digito1}{digito2}':
        return True
    else:
        return False


