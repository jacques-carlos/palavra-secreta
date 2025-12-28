import os
import pygame
import json
import unicodedata
from time import sleep
from emoji import emojize
from colorama import Fore, Back, Style, init


init(autoreset=True)


# gerenciador de áudio
class AudioManager:
    def __init__(self):
        # sons fixos
        self.victory = pygame.mixer.Sound('biblioteca/victory_sound.mp3')
        self.defeat = pygame.mixer.Sound('biblioteca/defeat_sound.mp3')
        self.time_out = pygame.mixer.Sound('biblioteca/time_sound.mp3')
        self.correct_secret = pygame.mixer.Sound(
            'biblioteca/correct_sound_2.mp3')
        self.wrong_secret = pygame.mixer.Sound('biblioteca/wrong_sound_2.mp3')

        # sons variáveis
        self.correct = pygame.mixer.Sound('biblioteca/correct_sound.mp3')
        self.wrong = pygame.mixer.Sound('biblioteca/wrong_sound.mp3')

    def tocar_musica(self, caminho):
        pygame.mixer.music.load(caminho)
        pygame.mixer.music.play(-1)

    def habilitar_modo_secret(self):
        # altera a música e os efeitos sonoros para o modo secret
        self.correct = self.correct_secret
        self.wrong = self.wrong_secret
        self.tocar_musica('biblioteca/secret_music.mp3')

    def habilitar_modo_padrao(self):
        # altera a música e os efeitos sonoros para o modo padrão
        self.correct = pygame.mixer.Sound('biblioteca/correct_sound.mp3')
        self.wrong = pygame.mixer.Sound('biblioteca/wrong_sound.mp3')
        self.tocar_musica('biblioteca/music.mp3')


# gerenciador de emojis
class EmojiMananger:
    def __init__(self):
        # emojis de nível
        self.easy = emojize(':smiling_face_with_halo:')
        self.hard = emojize(':hot_face:')
        self.impossible = emojize(':skull_and_crossbones:')
        self.secret = emojize(':smiling_face_with_horns:')

        # emojis de vida
        self.heart_red = emojize(':red_heart: ')
        self.heart_grey = emojize(':grey_heart: ')

        # emojis de título
        self.alien = emojize(':alien_monster:')
        self.trophy = emojize(':trophy:')
        self.cry = emojize(':loudly_crying_face:')

    def get_setup(self, nivel_atual):
        if nivel_atual == '666':
            return self.secret, self.secret, self.secret, self.heart_grey
        elif nivel_atual == '3':
            return self.impossible, self.trophy, self.impossible, self.heart_red
        else:
            return self.alien, self.trophy, self.cry, self.heart_red


# criar uma linha
def linha():
    print('=' * 200)


# pular uma linha
def espaco():
    print()


# limpar o terminal
def clear_terminal():
    # windows = 'nt' | linux/mac = 'posix'
    os.system('cls' if os.name == 'nt' else 'clear')


# criar um título
def titulo(entrada, fonte=Fore.YELLOW, fundo=Back.RESET, estilo=Style.BRIGHT):
    frase = entrada.upper().center(200)
    for x in range(2):
        espaco()
    print(f'{fonte}{fundo}{estilo}{frase}')
    for x in range(2):
        espaco()


# criar um título de erro
def erro(entrada, fonte=Fore.RED, fundo=Back.RESET, estilo=Style.BRIGHT):
    clear_terminal()
    frase = entrada.upper().center(200)
    for x in range(2):
        espaco()
    print(f'{fonte}{fundo}{estilo}{frase}')
    for x in range(2):
        espaco()


# iniciar jogo
def iniciar_jogo(emoji):
    clear_terminal()
    titulo(
        emojize(f'{emoji.alien} Pressione Enter para começar {emoji.alien}'))
    input()
    pygame.event.wait()
    clear_terminal()


# configurar os parâmetros de acordo com a dificuldade
def configurar_dificuldade(nivel_atual, audio):
    if nivel_atual == '1':
        return 'easy', 5, 20  # dificuldade, quantidade de vidas inicial, tempo de resposta

    elif nivel_atual == '2':
        return 'hard', 5, 15  # dificuldade, quantidade de vidas inicial, tempo de resposta

    elif nivel_atual == '3':
        # dificuldade, quantidade de vidas inicial, tempo de resposta
        return 'impossible', 3, 10

    elif nivel_atual == '666':
        # dificuldade, quantidade de vidas inicial, tempo de resposta
        return '?????', 3, 5


# exibir menu inicial
def exibir_menu_inicial(categoria_atual, dificuldade_atual, fonte=Fore.RED):
    clear_terminal()
    titulo('[1] Jogar')
    titulo('[2] Categoria | [3] Dificuldade')
    titulo(f'[{categoria_atual}] | [{dificuldade_atual}]')
    titulo('[4] Recordes | [5] Créditos')
    titulo('[6] Sair')


# exibir título inicial
def exibir_titulo_inicial(emoji_main):
    clear_terminal()
    titulo(
        emojize(f'{emoji_main} Você consegue adivinhar qual é a palavra secreta? {emoji_main}'))
