from funcoes.geral import *
from funcoes.secao_1 import *
from funcoes.secao_2 import *
from funcoes.secao_3 import *
from random import choice
from inputimeout import inputimeout, TimeoutOccurred

# inciar pygame
pygame.init()

# criando gerenciadores
audio = AudioManager()
emoji = EmojiMananger()

# PADRÃO INICIAL
niveL_atual = '1'
categoria_atual = 'geral'
audio.habilitar_modo_padrao()

# INICIAR JOGO
iniciar_jogo(emoji)

# JOGO INICIADO
while True:
    # emojis que vão ser utilizados (podem mudar de acordo com o nível)
    emoji_main, emoji_win, emoji_lose, emoji_life = emoji.get_setup(
        niveL_atual)

    # configurar parâmetros de acordo com o nível de dificuldade
    dificuldade_atual, quantidade_vidas_inicial, tempo_limite = configurar_dificuldade(
        niveL_atual, audio)

    # sempre redireciona ao menu
    secao = 0

    # MENU INICIAL
    while secao == 0:
        exibir_menu_inicial(categoria_atual, dificuldade_atual)

        entrada = input('O que você quer fazer? ').strip()

        try:
            entrada = int(entrada)
        except:
            erro('ERRO! Selecione uma opção válida.')
        else:
            if entrada not in range(1, 7):
                erro('ERRO! Selecione uma opção válida.')
            else:
                secao = entrada

    # JOGO
    while secao == 1:
        # construção do caminho para acessar as palavras

        nome_diretorio = categoria_atual

        # a partir da chave é possível obter o nome do arquivo
        mapa_niveis = {'1': 'easy', '2': 'hard',
                       '3': 'impossible', '666': 'secret'}

        nome_arquivo = mapa_niveis.get(niveL_atual, 'easy')

        caminho = f'categorias/{nome_diretorio}/{nome_arquivo}.txt'

        palavras = carregar_palavras(caminho)

        # se o arquivo não existir ou estiver vazio, seleciona o geral/easy (padrão)
        if not palavras:
            niveL_atual = '1'
            categoria_atual = 'geral'
            palavras = carregar_palavras('categorias/geral/easy.txt')

        # reinciar dados:

        # palavra que será exibida ao usuário
        palavra_original = choice(palavras)

        # palavra que será trabalhada pelo programa
        palavra_logica = normalizar_texto(palavra_original)

        tamanho_palavra = len(palavra_logica)

        letras_tentadas = list()
        letras_acertadas = list()
        vidas_restantes = quantidade_vidas_inicial

        exibir_titulo_inicial(emoji_main)

        while True:
            # exibir a palavra para o usuário
            palavra = '   '.join(
                [palavra_original[i] if palavra_logica[i] in letras_acertadas else "_" for i in range(tamanho_palavra)])

            # letras tentadas (erros)
            erros = [l for l in letras_tentadas if l not in palavra_logica]
            letras_erradas = ', '.join(sorted(erros)).upper()

            # mostrar palavra, vida e erros
            mostrar_info(palavra, emoji_life, vidas_restantes,
                         letras_erradas)

            # fim de jogo
            fim_de_jogo = checar_final_jogo(
                palavra_original, palavra, vidas_restantes, audio, emoji_win, emoji_lose, dificuldade_atual)

            # jogar novamente?
            if fim_de_jogo:
                jogar_novamente = quer_jogar_novamente(emoji_main)

                if jogar_novamente:
                    break
                else:
                    secao = 0
                    break

            # o usuário digita uma letra, mas tem tempo!
            try:
                letra_digitada = inputimeout(
                    prompt='Digite uma letra: ', timeout=tempo_limite).lower()
            except TimeoutOccurred:
                clear_terminal()
                audio.time_out.play()
                erro('TEMPO ESGOTADO! Você perdeu um coração.')
                vidas_restantes -= 1
                continue  # Volta para o início do loop para mostrar a palavra e vidas atualizadas

            letra_digitada = normalizar_texto(letra_digitada)

            # validação da entrada e tratamento de erros
            verificar_erros = validar_entrada(letra_digitada, letras_tentadas)
            if verificar_erros:
                erro(verificar_erros)
                continue

            # adicina a letra digitada na lista de tentativas
            letras_tentadas.append(letra_digitada)

            # caso o usuário acerte
            if letra_digitada in palavra_logica:
                audio.correct.play()
                mensagem_acertou()
                letras_acertadas.append(letra_digitada)
            # caso o usuário erre
            else:
                audio.wrong.play()
                mensagem_errou()
                vidas_restantes -= 1

    # SEÇÃO DAS CATEGORIAS
    while secao == 2:
        exibir_menu_categorias()

        categoria_atual = selecionar_categoria()

        secao = 0  # volta ao menu inicial

    # MENU DE DIFICULDADES
    while secao == 3:
        exibir_menu_dificuldades(emoji)

        niveL_atual = selecionar_nivel(emoji)

        secao = 0  # volta ao menu inicial

    # SEÇÃO DOS RECORDES
    while secao == 4:
        exibir_recordes()

        input('Pressione Enter para voltar ao menu...')

        secao = 0  # volta ao menu inicial

    # SEÇÃO DOS CRÉDITOS
    while secao == 5:
        exibir_creditos()

        print("\n" + "Pressione Enter para voltar ao menu...".center(200))
        input()
        secao = 0

    # SAIR DO JOGO
    if secao == 6:
        encerrar_jogo(emoji_main)
