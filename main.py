# main.c

import sys

import maratona

CADASTRAR_TIME = 1
CONSULTAR_TIME = 2
LISTAR_TIMES = 3
LISTAR_COMPETIDORES = 4
GERAR_EMAILS = 5
GERAR_ETIQUETAS = 6
SAIR = 7


def main():
    opcoes = [
        "Cadastrar Time",
        "Consultar Time",
        "Listar Times",
        "Listar Competidores",
        "Gerar E-mails",
        "Gerar Etiquetas",
        "Sair do Programa",
    ]

    op = menu(opcoes)
    router(op)
    while op != SAIR:
        op = menu(opcoes)
        router(op)


def menu(opcoes):
    print('-' * 60)
    print('MENU'.center(60))
    print('-' * 60)
    print()

    for i, opcao in enumerate(opcoes):
        print('{id} -\t{opcao}'.format(id=i + 1, opcao=opcao))
    print()
    op = int(input("Opção: "))
    print()
    return op


def router(op):
    if op == SAIR:
        return
    a = {
        CADASTRAR_TIME: maratona.cadastrar_time,
        CONSULTAR_TIME: maratona.consultar_time,
        LISTAR_TIMES: maratona.listar_times,
        LISTAR_COMPETIDORES: maratona.listar_competidores,
        GERAR_EMAILS: maratona.gerar_emails,
        GERAR_ETIQUETAS: maratona.gerar_etiquetas,
    }
    if op in a.keys():
        a[op]()
    else:
        print("\tOpção inválida!\n", file=sys.stderr)

if __name__ == '__main__':
    main()
