#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Variaveis globais


erro = 0
vetor_erros = []

# Tokens
TOKEN = lambda x:x
TOKEN.num = 'num'
TOKEN.literal = 'literal'
TOKEN.id = 'id'
TOKEN.Comentario = 'Comentario'
TOKEN.eof = 'eof'
TOKEN.opr = 'opr'
TOKEN.rcb = 'rcb'
TOKEN.opm = 'opm'
TOKEN.ab_p = 'ab_p'
TOKEN.fc_p = 'fc_p'
TOKEN.pt_v = 'pt_v'
TOKEN.erro = 'erro'
TOKEN.noToken = 'noToken'

class bcolors:
    BOLD = '\033[1m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    RED = '\033[91m'
    END = '\033[0m'

'''
Traduzir o token para string
'''
def token_def(token):
	global TOKEN

	TOK = TOKEN
	if token == TOK.num:
		return 'num'
	elif token == TOK.literal:
		return 'literal'
	elif token == TOK.id:
		return 'id'
	elif token == TOK.Comentario:
		return 'Comentario'
	elif token == TOK.eof:
		return 'eof'
	elif token == TOK.opr:
		return 'opr'
	elif token == TOK.rcb:
		return 'rcb'
	elif token == TOK.opm:
		return 'opm'
	elif token == TOK.ab_p:
		return 'ab_p'
	elif token == TOK.fc_p:
		return 'fc_p'
	elif token == TOK.pt_v:
		return 'pt_v'
	elif token == TOK.erro:
		return 'erro'
	elif token == TOK.noToken:
		return ' '

def repeat_to_length(string_to_expand, length):
    return (string_to_expand * (int(length/len(string_to_expand))+1))[:length]

def impressao_bonita(id, acumulated = 0, token = '', tipo=''):
	if id == 'titulo':
		print(bcolors.BOLD +"|%-10s LEXEMA %-11s| %-10s TOKEN %-10s | %-10s TIPO  %-10s |" % (' ', ' ', ' ', ' ',' ', ' ') + bcolors.END )
	elif id == 'linha':
		print("+"+repeat_to_length('.', 29)+"+"+repeat_to_length('.', 29) + "+"+repeat_to_length('.', 29) + "+")
	elif id == 'corpo':
		if ('\n' in acumulated):
			acumulated = acumulated.replace('\n','\\n')
		print("|%-2s  %-25s| %-10s  %-10s %-5s| %-10s   %-15s|" % (' ', acumulated, ' ', token_def(token), ' ',' ',' '))
	elif id == 'reservada':
		if ('\n' in acumulated):
			acumulated = acumulated.replace('\n','\\n')
		print(bcolors.BOLD+"|%-2s  %-25s| %-10s  %-11s %-4s| %-10s  %-10s %-5s|" % (' ', acumulated, ' ', token, ' ',' ', tipo, ' ')+bcolors.END)
	elif id == 'repetida':
		if ('\n' in acumulated):
			acumulated = acumulated.replace('\n','\\n')
		print(bcolors.BOLD+"|%-2s  %-25s| %-10s  %-10s %-5s| %-10s  %-10s %-5s|" % (' ', acumulated, ' ', token_def(token), ' ',' ', tipo,' ')+bcolors.END)
	else:
		print("%-3s %-3s ERRO! %-5s Caracter: %-24s  %-43s" % (bcolors.RED , bcolors.BOLD, bcolors.END, acumulated,' '))
