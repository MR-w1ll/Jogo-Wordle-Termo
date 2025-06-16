import random
from colorama import Fore, Back, init
init(autoreset=True)
import unidecode
import os

lingua = input('Selecione a lingua >IN (INGLÊS) ou >PT (PORTUGUÊS): ').lower()

lang = 'pt-br'
if lingua == 'in':
    lang = 'en'

try:
    import time
    import gtts
    import pygame

    def falar_palavra(palavra):
        try:
            voz = gtts.gTTS(palavra,lang=lang)
            voz.save('palavra.mp3')
            pygame.init()
            pygame.mixer.music.load('palavra.mp3')
            pygame.mixer.music.play()
            pygame.event.wait()
            time.sleep(2)
            pygame.mixer.quit()
        except:
            pass
except:
    def falar_palavra(palavra):
        pass


tamanho_palavra = 6 # int(input(f'Isira o tamanho da(s) palavra(s): '))
quantidade = 4 # int(input(f'Isira o numero de palavra(s): '))
chances = 15 # int(input(f'Isira o numero de tentativas: '))
nome_arquivo = fr".\lista_palavras\Palavras_{tamanho_palavra}_letras.txt"

if lingua == 'in':
    nome_arquivo = fr'.\Dicionario Ingles\Palavras_{tamanho_palavra}_letras_ingles.txt'








def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def sortear_palavra(nome_arquivo, tamanho_palavra):
    palavras = ''
    
    with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
        for palavra in arquivo:
            palavras = palavras + palavra

    palavras = palavras.split('\n')
    palavra_selecionada = random.choice(palavras)
    # print(fr"{palavras}")
    return unidecode.unidecode(palavra_selecionada.lower())

def feadback_alfabeto(alfabeto, letra, full_corect=None):
    letra = letra.upper()

    if full_corect:
        cor = Back.GREEN
        final_save = Back.RESET
    elif full_corect == False:
        cor = Fore.YELLOW
        final_save = Fore.RESET
    else:
        cor = Fore.RED
        final_save = Fore.RESET

    # REALIZANDO O FEADBACK DO TECLADO (VISUALMENTE)
    Opcoes = ['', Back.GREEN, Fore.YELLOW, Fore.RED]
    for opc in Opcoes:
        try:

            if opc == "":
                final = ""
            elif opc == Back.GREEN:
                final = Back.RESET
            else:
                final = Fore.RESET

            id_letra = alfabeto.index(f'{opc}{letra}{final}')

            if id_letra > -1: 
                if opc == Back.GREEN:
                    cor = Back.GREEN
                    final_save = Back.RESET
                break

        except:
            pass
            
    letra = (f'{cor}{letra}{final_save}')
    alfabeto[id_letra] = letra
    # ===============================================

    return alfabeto

def coparar_palavra(tamanho_palavra, palavra, palavra_jogador, letras_feadback, acertou):

    palavra_saida = ''
    corespondencia = 0
    palavra_correta = False

    palavra_filtrada = unidecode.unidecode(palavra).lower()
    palavra_jogador = unidecode.unidecode(palavra_jogador).lower()

    for id, letra in enumerate(palavra_jogador):
        if letra == palavra_filtrada[id]: # LETRA EXISTE E ESTÁ NO LUGAR CERTO
            palavra_saida = (f'{palavra_saida}{Back.GREEN}{palavra[id]}{Back.RESET}')
            corespondencia += 1
            if not acertou:
                letras_feadback = feadback_alfabeto(letras_feadback, letra, True) # RESPONSAVEL POR COLORIR O TECLADO

        elif palavra_filtrada.find(letra) != -1: # LETRA EXISTE MAS ESTÁ NO LUGAR ERRADO
            palavra_saida = (f'{palavra_saida}{Fore.YELLOW}{letra}{Fore.RESET}')
            if not acertou:
                letras_feadback = feadback_alfabeto(letras_feadback, letra, False) # RESPONSAVEL POR COLORIR O TECLADO

        else: # LETRA NÃO EXISTE
            letras_feadback = feadback_alfabeto(letras_feadback, letra)
            palavra_saida = palavra_saida + letra

    if corespondencia == tamanho_palavra:
        palavra_correta = True
        falar_palavra(palavra)

    return palavra_saida, palavra_correta, letras_feadback

def limitar_palavras(nome_arquivo, palavra_jogador):
    liberado = False
    palavra_jogador = unidecode.unidecode(palavra_jogador)

    try:
        # Lê o conteúdo atual do arquivo
        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
            conteudo_atual = arquivo.read()

        conteudo_atual = conteudo_atual.split('\n')
        if conteudo_atual[len(conteudo_atual)-1] == '':
            conteudo_atual.pop(len(conteudo_atual)-1)

        for palavra in conteudo_atual:
            palavra = unidecode.unidecode(palavra)

            if palavra == palavra_jogador:
                liberado = True
                break

    except:
        print('ERRO INESPERADO!')

    return liberado

def entrada_do_usuario(nome_arquivo, tamanho_palavra, interface, letras_feadback):
    loop = True
    while loop:
        print('Insura sua palavra: ')
        palavra_jogador  = input(('_'*tamanho_palavra)+'\r').lower()

        liberado = limitar_palavras(nome_arquivo, palavra_jogador)

        if len(palavra_jogador) == tamanho_palavra and liberado:
            loop = False
            return palavra_jogador
        else:
            limpar_tela()
            interface.exibir(letras_feadback)





class Interface():

    def gerar(self, quantidade, tamanho_palavra):
        # Selfs
        self.id = 1
        self.tamanho_palavra = tamanho_palavra
        self.quantidade = quantidade


        interface = []

        linha = []
        for id in range(quantidade):
            linha.append(f'{" "*(3+0)}{f"{id+1}º Palavra".center(12)}  ')
        interface.append(linha)

        for _ in range(chances):
            linha = []
            add = 1
            for _ in range(quantidade):    
                linha.append(f'{" "*add}{("-"*tamanho_palavra).center(15)}')
                add = 2
            interface.append(linha)

        self.interface = interface

    def atualizar(self, lista_FeadBack, lista_Acertos):
        
        linha = []
        add = 1
        for id, palavra in enumerate(lista_FeadBack):
            if not lista_Acertos[id]:
                linha.append(f'{" "*add}{palavra.center(15+len(palavra)-self.tamanho_palavra)}')
            else:
                linha.append(f'{" "*add}{("-"*tamanho_palavra).center(15)}')
            add = 2

        try:
            self.interface[self.id] = linha
            self.id += 1
        except:
            pass
    
    def listagem_alfabeto(self, alfabetos):
        decoracao = 17 * (self.quantidade) + 1
        for alfabeto in alfabetos:
            print((' '*int((decoracao - len(alfabeto)*2)/2)) + (' '.join(alfabeto)))
        print(('='*decoracao)+'\n')

    def exibir(self, alfabetos):
        decoracao = ('='*(17 * (self.quantidade) + 1))
        print(decoracao)
        print('ADIVINHE A PALAVRA'.center(17 * (self.quantidade) + 1))

        print(decoracao)
        for linha in self.interface:
            print(''.join(linha))
        print(decoracao)
        self.listagem_alfabeto(alfabetos)

class Jogo():

    def __init__(self, quantidade, tamanho_palavra, chances, nome_arquivo):

        # CONFIGURAÇÕES
        self.quantidade = quantidade
        self.tamanho_palavra = tamanho_palavra
        self.chances = chances
        self.nome_arquivo = nome_arquivo

        # VARIAVEIS DE CONTROLE
        self.venceu = False

        # LISTAS DE GERENCIAMENTO
        self.lista_Acertos = [False] * self.quantidade
        self.lista_palavras = []
        #                                                                       LISTA DO TECLADO DE FEADBACK
        alfabeto = 'a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z'.upper()
        alfabeto = alfabeto.split(',')
        self.letras_feadback = [alfabeto.copy() for _ in range(self.quantidade)]
        
        # CRIANDO A INTERFACE
        self.interface = Interface()
        self.interface.gerar(quantidade=self.quantidade, tamanho_palavra=self.tamanho_palavra)
        self.interface.exibir(self.letras_feadback)

        # GERANDO AS PALAVRAS DO JOGO
        for _ in range(self.quantidade):
            self.palavra = sortear_palavra(self.nome_arquivo, self.tamanho_palavra)
            self.lista_palavras.append(self.palavra)

        self.jogo()

    def menssagem_fim_de_jogo(self):
        decoracao = (17 * (self.quantidade) + 1)
        
        if self.venceu:
            if decoracao % 2 == 0:
                menssagem = (f'{Fore.GREEN} VOCÊ VENCEU! {Fore.RESET}')
                print('\n' + ('='*decoracao))
                print((f'<{"="*int(((decoracao-15)/2))}{menssagem}{"="*int(((decoracao-15)/2))}>').center(decoracao+(len(menssagem)-self.tamanho_palavra-8)))
                print(('='*decoracao) + '\n\n')

            else:
                menssagem = (f'{Fore.GREEN} VOCÊ VENCEU {Fore.RESET}')
                print('\n' + ('='*decoracao))
                print((f'<{"="*int(((decoracao-15)/2))}{menssagem}{"="*int(((decoracao-15)/2))}>').center(decoracao+(len(menssagem)-self.tamanho_palavra-8)))
                print(('='*decoracao) + '\n\n')

        elif not self.venceu:
            if decoracao % 2 == 0:
                print((f'<{"="*int(((decoracao-15)/2))} PERDEU {"="*int(((decoracao-15)/2))}>').center(decoracao))
                print('')
                print('='*decoracao)
                if self.quantidade == 1:
                    print('|' + (f'A Palavra É:'.center(decoracao-2)) + '|')
                else:
                    print('|' + (f'As Palavras Eram'.center(decoracao-2)) + '|')

            else:
                print((f'<{"="*int(((decoracao-15)/2))} VOCÊ PERDEU {"="*int(((decoracao-15)/2))}>').center(decoracao))
                print('='*decoracao)
                print('|' + (f'As Palavras Eram:'.center(decoracao-2)) + '|')

            for palavra in self.lista_palavras:
                palavra = (f'{Fore.GREEN}{palavra}{Fore.RESET}')
                print('|' + (f'{palavra}'.center(decoracao-2+(len(palavra)-self.tamanho_palavra))) + '|')
            print('='*decoracao + '\n\n')


    def jogo(self):
        Lista_vencedora = [True] * self.quantidade

        for _ in range(self.chances):
            lista_Acertos_TEMP = self.lista_Acertos.copy()
            lista_FeadBack = []
            palavra_jogador = entrada_do_usuario(nome_arquivo, tamanho_palavra=tamanho_palavra, interface=self.interface, letras_feadback=self.letras_feadback)
            
            for id, palavra in enumerate(self.lista_palavras):                
                FeadBack, acertou, alfabeto = coparar_palavra(tamanho_palavra, palavra, palavra_jogador, self.letras_feadback[id], self.lista_Acertos[id])
                lista_FeadBack.append(FeadBack)
                if acertou:
                    lista_Acertos_TEMP[id] = acertou
                self.letras_feadback[id] = alfabeto
                

            limpar_tela()
            self.interface.atualizar(lista_FeadBack=lista_FeadBack, lista_Acertos=self.lista_Acertos)
            self.interface.exibir(self.letras_feadback)

            self.lista_Acertos = lista_Acertos_TEMP.copy()

            if self.lista_Acertos == Lista_vencedora:
                limpar_tela()
                self.interface.atualizar(lista_FeadBack=lista_FeadBack, lista_Acertos=self.lista_Acertos)
                self.interface.exibir(self.letras_feadback)
                self.venceu = True
                self.menssagem_fim_de_jogo()
                break

        if not self.venceu:
            self.menssagem_fim_de_jogo()






loop = True
while loop:
    Jogo(quantidade, tamanho_palavra, chances, nome_arquivo)
    opc = input('========================\n[0] Terminar\n[1] Nova partida\n========================\n')
    if opc == '0':
        loop = False
        break





# ==== VERSÃO 1 ==== #
def jogo():
    venceu = False

    lista_Acertos = [False] * quantidade
    lista_palavras = []
    
    interface = Interface()
    interface.gerar(quantidade=quantidade, tamanho_palavra=tamanho_palavra)
    interface.exibir()

    for _ in range(quantidade):
        palavra = sortear_palavra(nome_arquivo, tamanho_palavra)
        lista_palavras.append(palavra)

    # print(lista_palavras)
    
    for _ in range(chances):
        lista_Acertos_TEMP = lista_Acertos.copy()
        lista_FeadBack = []
        palavra_jogador = entrada_do_usuario(nome_arquivo, tamanho_palavra=tamanho_palavra, interface=interface)
        
        for id, palavra in enumerate(lista_palavras):
            FeadBack, acertou = coparar_palavra(tamanho_palavra, palavra, palavra_jogador)
            lista_FeadBack.append(FeadBack)
            if acertou:
                lista_Acertos_TEMP[id] = acertou

        limpar_tela()
        print(lista_palavras)
        interface.atualizar(lista_FeadBack=lista_FeadBack, lista_Acertos=lista_Acertos)
        interface.exibir()

        lista_Acertos = lista_Acertos_TEMP.copy()

        if lista_Acertos == [True] * quantidade:
            limpar_tela()
            interface.atualizar(lista_FeadBack=lista_FeadBack, lista_Acertos=lista_Acertos)
            interface.exibir()
            print('\nParabens você VENCEU!')
            venceu = True
            break
    
    if not venceu:
        decoracao = (17 * (quantidade) + 1)
        if decoracao % 2 == 0:
            print((f'<{"="*int(((decoracao-15)/2))} PERDEU {"="*int(((decoracao-15)/2))}>').center(decoracao))
            print('')
            print('='*decoracao)
            if quantidade == 1:
                print('|' + (f'A Palavra É:'.center(decoracao-2)) + '|')
            else:
                print('|' + (f'As Palavras Eram'.center(decoracao-2)) + '|')

        else:
            print((f'<{"="*int(((decoracao-15)/2))} VOCÊ PERDEU {"="*int(((decoracao-15)/2))}>').center(decoracao))
            print('='*decoracao)
            print('|' + (f'As Palavras Eram:'.center(decoracao-2)) + '|')

        for palavra in lista_palavras:
            palavra = (f'{Fore.GREEN}{palavra}{Fore.RESET}')
            print('|' + (f'{palavra}'.center(decoracao-2+(len(palavra)-tamanho_palavra))) + '|')
        print('='*decoracao + '\n\n')