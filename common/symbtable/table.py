#!/usr/bin/python3

from common.utility.util import *

class SymbTable():
    def __init__(self):
        self.tabela = []
        self.init_table()

    def init_table(self):
        self.append_table('inicio', 'inicio')
        self.append_table('varinicio', 'varinicio')
        self.append_table('varfim', 'varfim')
        self.append_table('escreva', 'escreva')
        self.append_table('leia', 'leia')
        self.append_table('se', 'se')
        self.append_table('entao', 'entao')
        self.append_table('fimse', 'fimse')
        self.append_table('fim', 'fim')
        self.append_table('inteiro', 'inteiro')
        self.append_table('lit', 'lit')
        self.append_table('real', 'real')

    def append_table(self, lexema, token, tipo = ''):
        preencher_tabela = {'lexema':lexema,'token': token,'tipo':tipo}
        try:
            self.tabela.append(preencher_tabela)
            return True
        except:
            raise
        
    def get_symbol(self, lexema, token):
        for line in self.tabela:
            if line['token'] == token and line['lexema'] == lexema :
                return line
        return False

    def palavra_reservada(self, lexema):
        if self.get_symbol(lexema, lexema) is not False:
            return True
        else:
            return False

    def palavra_nao_reservada(self, lexema, token):
        if self.get_symbol(lexema, token) is not False:
            return True
        else:
            return False

    def print_table(self):
        impressao_bonita('linha')
        print(bcolors.BOLD +"|%-10s  %-10s %-10s TABELA DE SIMBOLOS %-10s  %-10s   %-10s |" % (' ', ' ', ' ', ' ',' ', ' ') + bcolors.END )
        impressao_bonita('linha')
        print(bcolors.BOLD+"|%-2s  %-25s| %-10s  %-10s %-5s| %-10s   %-15s|" % (' ', 'Lexema', ' ', 'Token', ' ',' ',' ')+bcolors.END)
        impressao_bonita('linha')

        for line in self.tabela:
            if line['lexema'] is line['token']:
                impressao_bonita('reservada', line['lexema'], line['token'])
            else:
                impressao_bonita('repetida', line['lexema'], line['token'])