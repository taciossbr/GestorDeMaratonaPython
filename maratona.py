# maratona.h

import getpass
import os
import struct

# typedef struct {
#     int id;
#     char login[8];
#     char senha[21];
#     char nome[31];
# } time;

# typedef struct {
#     int dia;
#     int mes;
#     int ano;
# } data;

# typedef struct {
#     int id;
#     int id_time;
#     char nome[61];
#     char email[41];
#     data nasc;
# } competidor;


ARQ_TIME = "time.dat"
ARQ_COMP = "competidor.dat"
ARQ_EMAILS = "emails.txt"
ARQ_ETIQUETAS = "etiquetas.txt"
ARQ_LISTAGEM = "listagem.txt"
TIME_STRUCT_FORMAT = "i8s20s30s"
COMP_STRUCT_FORMAT = "ii60s40siii"


def cadastrar_time():
    print('-' * 60)
    print('CADASTRO DE TIMES'.center(60))
    print('-' * 60)
    print()

    id_time = None
    nome_time = None
    with open(ARQ_TIME, 'ab') as times:
        id_time = times.tell() // struct.calcsize(TIME_STRUCT_FORMAT) + 1
        print('ID:', id_time)
        login = 'team{}'.format(id_time)
        print('Login:', login)
        senha = getpass.getpass('Senha [20]: ')
        nome_time = input('Nome [30]: ')
        time = struct.pack('i8s20s30s', id_time, bytes(login, "utf8"),
                           bytes(senha, 'utf8'), bytes(nome_time, 'utf-8'))
        times.write(time)

    print()
    print('\tTime gravado com sucesso!')
    print()

    print('Cadastro de competidores')
    print('-' * 30)
    print()

    with open(ARQ_COMP, 'ab') as competidores:
        id_inicial = competidores.tell() // struct.calcsize(COMP_STRUCT_FORMAT) + 1
        for i in range(3):
            print('ID:', id_inicial + i)
            print('Time:', nome_time)
            nome = input('Nome [40]:')
            email = input('Email [60]:')
            ent = input('Data [dd/mm/yyyy]: ')
            dia, mes, ano = [int(x) for x in ent.split('/')]
            comp = struct.pack(COMP_STRUCT_FORMAT, id_inicial + i,
                               id_time, bytes(nome, 'utf-8'),
                               bytes(email, 'utf-8'), ano, mes, dia)
            competidores.write(comp)
            print()
            print('\tCompetidor gravado com sucesso!')
            print()


def consultar_time():
    print('-' * 60)
    print('CONSULTA DE TIMES'.center(60))
    print('-' * 60)
    print()

    with open(ARQ_TIME, 'rb') as times, open(ARQ_COMP, 'rb') as comps:
        id_time = int(input('ID do time: '))

        tam_arq_times = os.stat(ARQ_TIME).st_size
        max_id = tam_arq_times // struct.calcsize(TIME_STRUCT_FORMAT)

        if id_time > max_id:
            print()
            print('ID INVALIDO!')
            print()
            return

        times.seek((id_time - 1) * struct.calcsize(TIME_STRUCT_FORMAT))
        time_bin = times.read(struct.calcsize(TIME_STRUCT_FORMAT))
        time_unpacked = struct.unpack(TIME_STRUCT_FORMAT, time_bin)

        time = {
            'id': time_unpacked[0],
            'login': time_unpacked[1].decode('utf-8'),
            'senha': time_unpacked[2].decode('utf-8'),
            'nome':  time_unpacked[3].decode('utf-8'),
        }
        print('ID:', time['id'])
        print('Login:', time['login'].strip())
        print('Senha:', '*' * len(time['senha'].strip()))
        print('Nome:', time['nome'].strip())

        print()
        print('Competidores')
        print('-' * 30)
        print()

        comps.seek(((id_time - 1) * 3) * struct.calcsize(COMP_STRUCT_FORMAT))
        for i in range(3):
            comp_bin = comps.read(struct.calcsize(COMP_STRUCT_FORMAT))
            comp_unpacked = struct.unpack(COMP_STRUCT_FORMAT, comp_bin)
            comp = {
                'id': comp_unpacked[0],
                'id_time': comp_unpacked[1],
                'nome': comp_unpacked[2].decode('utf-8'),
                'email': comp_unpacked[3].decode('utf-8'),
                'nasc': (comp_unpacked[4], comp_unpacked[5], comp_unpacked[6])
            }
            print('ID:', comp['id'])
            print('Time:', time['nome'].strip())
            print('Nome:', comp['nome'].strip())
            print('Email:', comp['email'].strip())
            print('Data: %02d/%02d/%04d' % comp['nasc'])
            print()
        print()


def listar_times():
    print('-' * 60)
    print('LISTAGEM DE TIMES'.center(60))
    print('-' * 60)
    print()

    with open(ARQ_TIME, 'rb') as times:
        length = os.stat(ARQ_TIME).st_size
        print('ID'.rjust(4), 'login'.ljust(8), 'time'.ljust(30), sep=' | ')
        print('=' * 48)
        while times.tell() < length:
            time_bin = times.read(struct.calcsize(TIME_STRUCT_FORMAT))
            time_unpacked = struct.unpack(TIME_STRUCT_FORMAT, time_bin)
            time = {
                'id': time_unpacked[0],
                'login': time_unpacked[1].decode('utf-8'),
                'senha': time_unpacked[2].decode('utf-8'),
                'nome':  time_unpacked[3].decode('utf-8'),
            }
            print(str(time['id']).rjust(4, '0'), 
                  time['login'].strip('\x00').ljust(8),
                  time['nome'].strip('\x00').ljust(30), sep=' | ')
        print()


def listar_competidores():
    print('-' * 60)
    print('LISTAGEM DE COMPETIDORES'.center(60))
    print('-' * 60)

    competidores = []
    with open(ARQ_COMP, 'rb') as comps:
        length = os.stat(ARQ_COMP).st_size
        print('ID'.rjust(5), 'nome'.ljust(13), 'email'.ljust(19),
              'time'.ljust(9), 'Nascimento'.ljust(10), sep='|')
        while comps.tell() < length:
            comp_bin = comps.read(struct.calcsize(COMP_STRUCT_FORMAT))
            comp_unpacked = struct.unpack(COMP_STRUCT_FORMAT, comp_bin)
            comp = {
                'id': comp_unpacked[0],
                'id_time': comp_unpacked[1],
                'time': _get_time(comp_unpacked[1]),
                'nome': comp_unpacked[2].decode('utf-8').strip('\x00'),
                'email': comp_unpacked[3].decode('utf-8').strip('\x00'),
                'nasc': (comp_unpacked[4], comp_unpacked[5], comp_unpacked[6])
            }
            print(str(comp['id']).rjust(5), comp['nome'].ljust(13),
                  comp['email'].ljust(19), comp['time'].ljust(9),
                  '/'.join([str(x) for x in comp['nasc']]).rjust(10), sep='|')
            competidores.append(comp)
    print()
    if input('Deseja salvar a listagem? [Y/n]') == 'Y':
        print()
        _save_listagem_competidores(competidores)
        print('Listagem salva em:', ARQ_LISTAGEM)
    print()


def gerar_emails():
    print()

    length = os.stat(ARQ_COMP).st_size
    with open(ARQ_EMAILS, 'w') as emails, open(ARQ_COMP, 'rb') as comps:
        while comps.tell() < length:
            comp_bin = comps.read(struct.calcsize(COMP_STRUCT_FORMAT))
            comp_unpacked = struct.unpack(COMP_STRUCT_FORMAT, comp_bin)
            emails.write(comp_unpacked[3].decode('utf-8').strip('\x00') + ',')

    print('Emails salvos em:', ARQ_EMAILS)
    print()


def gerar_etiquetas():
    with open(ARQ_TIME, 'rb') as times, open(ARQ_ETIQUETAS, 'w') as et:
        length = os.stat(ARQ_TIME).st_size
        while times.tell() < length:
            time_bin = times.read(struct.calcsize(TIME_STRUCT_FORMAT))
            time_unpacked = struct.unpack(TIME_STRUCT_FORMAT, time_bin)
            time = {
                'id': time_unpacked[0],
                'login': time_unpacked[1].decode('utf-8').strip('\x00'),
                'senha': time_unpacked[2].decode('utf-8').strip('\x00'),
                'nome':  time_unpacked[3].decode('utf-8').strip('\x00'),
            }
            print(time['nome'], file=et)
            print(time['login'], file=et)
            print(time['senha'], file=et)
            print('(', ', '.join(_get_comps_name_time(time['id'])), ')', 
                  sep='', file=et)
            print(file=et)


def _get_time(id):
    with open(ARQ_TIME, 'rb') as times:
        times.seek((id - 1) * struct.calcsize(TIME_STRUCT_FORMAT))
        time_bin = times.read(struct.calcsize(TIME_STRUCT_FORMAT))
        time_unpacked = struct.unpack(TIME_STRUCT_FORMAT, time_bin)
        return time_unpacked[1].decode('utf-8').strip('\x00')


def _save_listagem_competidores(comps):
    with open(ARQ_LISTAGEM, 'w') as file:
        print('ID'.rjust(5), 'nome'.ljust(60), 'email'.ljust(40),
              'time'.ljust(30), 'Nascimento'.ljust(10), sep='|', file=file)
        for comp in comps:
            print(str(comp['id']).rjust(5), comp['nome'].ljust(13),
                  comp['email'].ljust(19), comp['time'].ljust(9),
                  '/'.join([str(x) for x in comp['nasc']]).rjust(10),
                  sep='|', file=file)


def _get_comps_name_time(id):
    with open(ARQ_COMP, 'rb') as comps:

        comps.seek(((id - 1) * 3) * struct.calcsize(COMP_STRUCT_FORMAT))
        comp_bin = comps.read(struct.calcsize(COMP_STRUCT_FORMAT))
        comp_unpacked = struct.unpack(COMP_STRUCT_FORMAT, comp_bin)
        names = []
        for i in range(3):
            names.append(comp_unpacked[2].decode('utf-8').strip('\x00'))
        return names
