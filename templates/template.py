import sys, os
sys.path.append(os.path.abspath(os.curdir))
from model.password import Password
from views.password_views import FernetHasher


repeat = True
action = 0

while(repeat):
    action = input('''Digite uma opção: 
1 para salvar uma nova senha
2 para ver uma senha salva
3 para sair do sistema 
''')
    match(action):
        case '1':

            if(len(Password.get())) == 0:
                key, path = FernetHasher.create_key(archive=True)
                print('Sua chave foi criada com sucesso, salve-a com cuidado.')
                print(f'Chave: {key.decode("utf-8")}')
                if(path):
                    print('Chave salva no arquivo, lembre-se de remover o arquivo após o transferir de local')
                    print(f'Caminho: {path}')
            else:
                key = input('Digite sua chave usada para criptografia, use sempre a mesma chave: ')

            domain = input('Dominio: ')
            password = input('Senha: ')

            fernet_user = FernetHasher(key)
            p1 = Password(domain=domain, password=fernet_user.encrypt(password).decode('utf-8'))
            p1.save()

        case '2':
            domain = input('Dominio: ')
            key = input('Chave: ')

            fernet_user = FernetHasher(key)
            data = Password.get()

            for i in data:
                if domain in i['domain']:
                    password = fernet_user.decrypt(i['password'])
            
            if password:
                print(f'Sua senha:{password}')
                password = None
            else:
                print('Nenhuma senha encontrada para esse domínio')

        case '3':
            print('Execução finalizada, obrigado por utilizar o gerenciador de senhas')
            repeat = False