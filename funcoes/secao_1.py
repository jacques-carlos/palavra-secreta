from funcoes.geral import *


# RODANDO O JOGO


# carregar os níveis e suas palavras
def carregar_palavras(caminho_arquivo):
    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        # lê cada linha, remove espaços e ignora linhas vazias
        return [linha.strip() for linha in arquivo if linha.strip()]


# tratar acentos e caracteres especiais
def normalizar_texto(texto):
    # forma NFD: caractere separado do acento
    texto_decomposto = unicodedata.normalize('NFD', texto)
    texto_normalizado = ''.join(
        c for c in texto_decomposto if unicodedata.category(c) != 'Mn')
    return texto_normalizado.lower()


# mostrar quantas vida o usuário têm
def mostrar_vida(entrada):
    frase = entrada
    for x in range(2):
        espaco()
    print(frase)
    for x in range(2):
        espaco()


# mostrar palavra, vida e letras erradas
def mostrar_info(resposta, heart, vidas, letras_tentadas):
    titulo(resposta)
    mostrar_vida(emojize(heart)*vidas)
    titulo(f'Letras erradas: {letras_tentadas}')
    linha()


# validação de dados e tratamento de erros
def validar_entrada(letra, letras_tentadas):
    # retorna erro caso o usuário não digite uma letra
    if not letra.isalpha():
        return ('ERRO! Digite uma letra.')
    # retorna erro caso o usuário digite mais de uma letra
    elif len(letra) > 1:
        return ('ERRO! Digite apenas uma letra.')
    # retorna erro caso o usuário já tenha digitado essa letra antes
    elif letra in letras_tentadas:
        return ('ERRO! Você já tentou essa letra.')
    return None


# quando o usuário acertar uma letra
def mensagem_acertou(fonte=Fore.GREEN, fundo=Back.RESET, estilo=Style.BRIGHT):
    clear_terminal()
    frase = 'Você acertou!'.upper().center(200)
    for x in range(2):
        espaco()
    print(f'{fonte}{fundo}{estilo}{frase}')
    for x in range(2):
        espaco()


# quando o usuário errar uma letra
def mensagem_errou(fonte=Fore.RED, fundo=Back.RESET, estilo=Style.BRIGHT):
    clear_terminal()
    frase = 'Você errou!'.upper().center(200)
    for x in range(2):
        espaco()
    print(f'{fonte}{fundo}{estilo}{frase}')
    for x in range(2):
        espaco()


def checar_final_jogo(palavra_exibida, resposta, vidas_restantes, audio, emoji_win, emoji_lose, dificuldade):
    venceu = '_' not in resposta
    perdeu = vidas_restantes <= 0

    if venceu:
        clear_terminal()
        audio.victory.play()
        titulo(emojize(f'{emoji_win} Você ganhou parabéns {emoji_win}'))
        titulo(f'A palavra era: "{palavra_exibida}"')
        while True:
            salvar = input(
                'Deseja salvar esse recorde? [S/N]: ').strip().upper()
            if salvar[0] == 'S':
                nome = input('Digite seu nome para o ranking: ').strip()
                if not nome:
                    nome = 'Anônimo'
                salvar_recorde(nome, vidas_restantes, dificuldade)
                break
            elif salvar[0] == 'N':
                break
            else:
                erro('ERRO! Digite S ou N.')
        return True

    elif perdeu:
        clear_terminal()
        audio.defeat.play()
        titulo(emojize(f'{emoji_lose} Você perdeu infelizmente {emoji_lose}'))
        titulo(f'A palavra era: "{palavra_exibida}"')
        sleep(2)
        return True


def salvar_recorde(nome, vidas_restantes, dificuldade):
    arquivo_nome = 'recordes.json'

    multiplicadores = {'easy': 1, 'hard': 2, 'impossible': 5, '?????': 10}
    potuacao = vidas_restantes * multiplicadores.get(dificuldade, 1)

    # Tentar carregar os dados existentes
    try:
        # ADICIONADO: 'as arquivo' para referenciar o arquivo aberto
        with open(arquivo_nome, 'r', encoding='utf-8') as arquivo:
            # CORRIGIDO: Passamos 'arquivo' (objeto), não 'arquivo_nome' (texto)
            dados = json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        dados = []

    # Adicionar novo recorde e ordenar
    dados.append({'nome': nome, 'score': potuacao, 'diff': dificuldade})
    dados = sorted(dados, key=lambda x: x['score'], reverse=True)[:15]

    # Salvar os dados atualizados
    # ADICIONADO: 'as arquivo'
    with open(arquivo_nome, 'w', encoding='utf-8') as arquivo:
        # CORRIGIDO: json.dump(o_que_salvar, onde_salvar, ...)
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)


def quer_jogar_novamente(emoji_main):
    while True:
        jogar_novamente = input(
            'Deseja jogar novamente? [S/N]: ').strip().upper()
        if jogar_novamente.startswith(('S', 'N')):
            break
        print('Resposta inválida! Digite S ou N.')

    if jogar_novamente[0] == 'S':
        return True
    else:
        clear_terminal()
        titulo(
            emojize(f'{emoji_main} Obrigado por jogar! {emoji_main}'))
        sleep(2)
        return False
