from funcoes.geral import *

# SEÇÃO CATEGORIAS


def exibir_menu_categorias():
    clear_terminal()
    titulo('--- Selecione a categoria ---')
    titulo(emojize(
        f'   [1] > Geral  '
        f'|  [2] > Animais  '
        f'|  [3] > Comida  '
        f'|  [4] > Profissões  '))


def selecionar_categoria():
    while True:
        categoria = input().strip()
        if categoria == '1':
            return 'geral'

        elif categoria == '2':
            return 'animais'

        elif categoria == '3':
            return 'comidas'

        elif categoria == '4':
            return 'profissoes'

        else:
            exibir_menu_categorias()
            print('ERRO! Digite uma opção válida.')


# SEÇÃO DIFICULDADES


def exibir_menu_dificuldades(emoji):
    clear_terminal()
    titulo('--- Selecione a dificuldade ---')
    titulo(emojize(
        f'   [1] > Fácil{emoji.easy}  '
        f'|  [2] > Difícil{emoji.hard}  '
        f'|  [3] > Impossível{emoji.impossible}  '))


def selecionar_nivel(emoji):
    while True:
        nivel = input('Selecione o nível de dificuldade : ')
        if nivel == '1' or nivel == '2' or nivel == '3' or nivel == '666':
            return nivel

        else:
            exibir_menu_dificuldades(emoji)
            print('ERRO! Digite 1, 2, ou 3 para selecionar o nível de dificuldade.')
