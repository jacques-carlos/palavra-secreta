from funcoes.geral import *


# SEÇÃO RECORDES


def exibir_recordes():
    clear_terminal()
    titulo('🏆 TOP 15 RECORDES 🏆')

    try:
        # ADICIONADO: 'as f'
        with open('recordes.json', 'r', encoding='utf-8') as f:
            # CORRIGIDO: Passamos 'f' (o arquivo aberto)
            dados = json.load(f)

            print(f"{'NOME':<15} | {'SCORE':<8} | {'DIFICULDADE'}")
            print("-" * 40)

            for r in dados:
                print(f"{r['nome']:<15} | {r['score']:<8} | {r['diff']}")
    except (FileNotFoundError, json.JSONDecodeError):
        titulo('Nenhum recorde registrado ainda!')

    espaco()


# SEÇÃO CRÉDITOS


creditos = [
    "JOGO PALAVRA SECRETA - VERSÃO ALPHA",
    "",
    "DESENVOLVIDO POR:",
    "JACK",
    "",
    "TECNOLOGIAS UTILIZADAS:",
    "Python 3.13",
    "Pygame (Áudio)",
    "Colorama (Cores)",
    "JSON (Ranking)",
    "",
    "AGRADECIMENTOS:",
    "Aos mestres da programação",
    "E a você, por jogar!",
    "",
    "2025 - PROJETO CONCLUÍDO (por enquanto)"
]


def exibir_creditos(fonte=Fore.CYAN, estilo=Style.BRIGHT):
    # Definimos quantas linhas de "pulo" o texto começa (ex: 15 linhas lá embaixo)
    for i in range(15, -5, -1):
        clear_terminal()

        # Cria os espaços no topo que vão diminuindo
        for _ in range(max(0, i)):
            espaco()

        # Imprime cada linha dos créditos centralizada
        for linha_texto in creditos:
            # Usamos o .center(200) para manter o padrão que você criou
            print(f"{fonte}{estilo}{linha_texto.center(200)}")

        sleep(0.5)  # Controla a velocidade da subida

        # Se o texto já subiu todo, paramos a animação
        if i == -4:
            break


# SEÇÃO ENCERRAMENTO


def encerrar_jogo(emoji_main):
    clear_terminal()
    titulo(
        emojize(f'{emoji_main} Volte sempre! {emoji_main}'))
    pygame.quit()
    exit()
