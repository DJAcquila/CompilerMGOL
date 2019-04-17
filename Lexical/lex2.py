import hashlib
import string

_arquivo = open('fonte.alg', 'r')
lines = _arquivo.readlines()
eof = _arquivo.tell()
coluna = 0
linha = 1
erro = 0
vetor_erros = []

#Tabela de simbolos
tabela_simbolos = []
preencher_tabela = {'lexema':'inicio','token':'inicio','tipo':''}
tabela_simbolos.append(preencher_tabela)
preencher_tabela = {'lexema':'varinicio','token':'varinicio','tipo':''}
tabela_simbolos.append(preencher_tabela)
preencher_tabela = {'lexema':'varfim','token':'varfim','tipo':''}
tabela_simbolos.append(preencher_tabela)
preencher_tabela = {'lexema':'escreva','token':'escreva','tipo':''}
tabela_simbolos.append(preencher_tabela)
preencher_tabela = {'lexema':'leia','token':'leia','tipo':''}
tabela_simbolos.append(preencher_tabela)
preencher_tabela = {'lexema':'se','token':'se','tipo':''}
tabela_simbolos.append(preencher_tabela)
preencher_tabela = {'lexema':'entao','token':'entao','tipo':''}
tabela_simbolos.append(preencher_tabela)
preencher_tabela = {'lexema':'fimse','token':'fimse','tipo':''}
tabela_simbolos.append(preencher_tabela)
preencher_tabela = {'lexema':'fim','token':'fim','tipo':''}
tabela_simbolos.append(preencher_tabela)
preencher_tabela = {'lexema':'inteiro','token':'inteiro','tipo':''}
tabela_simbolos.append(preencher_tabela)
preencher_tabela = {'lexema':'lit','token':'lit','tipo':''}
tabela_simbolos.append(preencher_tabela)
preencher_tabela = {'lexema':'real','token':'real','tipo':''}
tabela_simbolos.append(preencher_tabela)


# Tokens
TOKEN = lambda x:x
TOKEN.num = 'num'
TOKEN.literal = 'literal'
TOKEN.id = 'id'
TOKEN.Comentario = 'Comentario'
TOKEN.eof = 'eof'
TOKEN.opr = 'opr'
TOKEN.rcb = 'rc'
TOKEN.opm = 'opm'
TOKEN.ab_p = 'ab_p'
TOKEN.fc_p = 'fc_p'
TOKEN.pt_v = 'pt_v'
TOKEN.erro = 'erro'
TOKEN.noToken = 'noToken'

class bcolors:
    BOLD = '\033[1m'
    GREEN = '\033[92m'
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

def impressao_bonita(id, acumulated = 0, token = ''):
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
		print(bcolors.BOLD+"|%-2s  %-25s| %-10s  %-10s %-5s| %-10s   %-15s|" % (' ', acumulated, ' ', token, ' ',' ',' ')+bcolors.END)
	elif id == 'repetida':
		if ('\n' in acumulated):
			acumulated = acumulated.replace('\n','\\n')
		print(bcolors.BOLD+"|%-2s  %-25s| %-10s  %-10s %-5s| %-10s   %-15s|" % (' ', acumulated, ' ', token_def(token), ' ',' ',' ')+bcolors.END)
	else:
		print("%-3s %-3s %-3s ERRO! %-5s Caracter: %-24s  %-43s" % (' ', bcolors.RED , bcolors.BOLD, bcolors.END, acumulated,' '))

# Classe que define o dfa
class DFA():
		def __init__(self, statesNum = 21):
			global TOKEN
			T = TOKEN
			self.statesNum = statesNum # Pode estar errado
			self.transitions = [{} for i in range(statesNum)]
			self.acceptStates = [False] * self.statesNum
			self.statesToken = [T.noToken] * self.statesNum

		def set_DFA(self, src_state, char, target_state):
			self.transitions[src_state][char] = target_state

		def set_acceptState(self, state, token):
			self.acceptStates[state] = True
			self.statesToken[state] = token

		def accept(self, pt):
			global linha 
			global coluna
			global erro
			global vetor_erros
			global tabela_simbolos
			ponteiro = int(pt)
			state = 0
			token = self.statesToken[state]
			token_aceito = self.statesToken[state]
			lexema_aceito = ''
			ponteiro_aceito = ponteiro
			acumulated = ''
			try:
				while (ponteiro < eof):
					
					_arquivo.seek(ponteiro)
					c = _arquivo.read(1)
					#print ("Caracter lido: " + c)
					ponteiro+=1
					coluna+=1
					state = self.transitions[state][c]
					
					token = self.statesToken[state]
					ponteiro_aceito = ponteiro
					if state != 0:
						acumulated += c
					if c == '\n':
						linha += 1
						coluna = 0
													

				if token is 'id':
					teste1 = {'lexema':acumulated,'token':acumulated,'tipo':''}
					teste2 = {'lexema':acumulated,'token':token,'tipo':''}
					if teste1 in tabela_simbolos:
						impressao_bonita('reservada', acumulated, acumulated)
					elif teste2 in tabela_simbolos:
						impressao_bonita('repetida', acumulated, token)
					else:
						preencher_tabela = {'lexema':acumulated,'token':token,'tipo':''}
						tabela_simbolos.append(preencher_tabela)
						impressao_bonita('corpo', acumulated, token)
				else:
					impressao_bonita('corpo', acumulated, token)

				return self.acceptStates[state], token_def(self.statesToken[state])

			except KeyError:
				#first, st = input_line.split(input_line[input_line.find(stop)], 1)
				#print("Cont: {}".format(cont))
				#print ("\tSplit: {}".format(st))
				if state != 0:
					if token is 'id':
						if token is 'id':
							teste1 = {'lexema':acumulated,'token':acumulated,'tipo':''}
							teste2 = {'lexema':acumulated,'token':token,'tipo':''}
							if teste1 in tabela_simbolos:
								impressao_bonita('reservada', acumulated, acumulated)
							elif teste2 in tabela_simbolos:
								impressao_bonita('repetida', acumulated, token)
							else:
								preencher_tabela = {'lexema':acumulated,'token':token,'tipo':''}
								tabela_simbolos.append(preencher_tabela)
								impressao_bonita('corpo', acumulated, token)
					else:
						impressao_bonita('corpo', acumulated, token)
					ponteiro-=1
					coluna-=1
				elif state == 0:
					acumulated_string = c+ bcolors.GREEN + bcolors.BOLD +' linha: ' + bcolors.END + str(linha)+ bcolors.GREEN + bcolors.BOLD + ' coluna: '+ bcolors.END+str(coluna)
					dicionario_erro = {'acumulated': acumulated_string, 'token': token}
					vetor_erros.append(dicionario_erro)
					#impressao_bonita('erro', c+' linha: '+str(linha)+' coluna: '+str(coluna), token)
					erro+=1
				st = str(ponteiro)
				#print(st)
				return False, st


# Construção do automato para o analisador léxico
class LEX_DFA():

	def __init__(self):
		self.dfa = DFA(21)
		self.load_DFA()
		
	'''
		Constroi o DFA
	'''
	def load_DFA(self):
		global TOKEN
		T = TOKEN 
		#Ignora (comentario, pulo de linha e espaço)
		self.dfa.set_DFA(0, ' ', 0)
		self.dfa.set_DFA(0, '\n', 0)
		self.dfa.set_DFA(0, '\t', 0)

		# Num
		self.dfa.set_DFA(1,'.',2)
		self.dfa.set_DFA(1,'E',4)
		self.dfa.set_DFA(1,'e',4)
		self.dfa.set_DFA(3,'E',4)
		self.dfa.set_DFA(3,'e',4)
		self.dfa.set_DFA(4,'+',5)
		self.dfa.set_DFA(4,'-',5)
		for digit in range(10):
			self.dfa.set_DFA(0,str(digit),1)
			self.dfa.set_DFA(1,str(digit),1)
			self.dfa.set_DFA(2,str(digit),3)
			self.dfa.set_DFA(3,str(digit),3)
			self.dfa.set_DFA(4,str(digit),6)
			self.dfa.set_DFA(5,str(digit),6)
			self.dfa.set_DFA(6,str(digit),6)
		self.dfa.set_acceptState(1, T.num)
		self.dfa.set_acceptState(3, T.num)
		self.dfa.set_acceptState(6, T.num)

		#Ponto e vírgula
		self.dfa.set_DFA(0, ';', 7)
		self.dfa.set_acceptState(7, T.pt_v)

		# Literal
		self.dfa.set_DFA(0, '"', 8)
		for st1 in string.printable:
			self.dfa.set_DFA(8, st1, 8)
		self.dfa.set_DFA(8, '"', 9)
		self.dfa.set_acceptState(9, T.literal)

		#Fecha parênteses
		self.dfa.set_DFA(0, ')', 10)
		self.dfa.set_acceptState(10,T.fc_p)

		#Abre parênteses
		self.dfa.set_DFA(0, '(', 13)
		self.dfa.set_acceptState(13,T.ab_p)

		#Comentário
		self.dfa.set_DFA(0, '{', 11)
		for st in string.printable:
			self.dfa.set_DFA(11, st, 11)
		self.dfa.set_DFA(11,'}',12)
		self.dfa.set_acceptState(12,T.Comentario)

		#EOF (fim de arquivo)
		self.dfa.set_DFA(0, "eof", 14)
		self.dfa.set_acceptState(14, T.eof)

		#Operações relacionais / atribuição
		self.dfa.set_DFA(0, '>', 16)
		self.dfa.set_DFA(0, '<', 15)
		self.dfa.set_DFA(0, '=', 18)
		self.dfa.set_DFA(15, '>', 18)
		self.dfa.set_DFA(15, '=', 18)
		self.dfa.set_DFA(15, '-', 17)
		self.dfa.set_DFA(16, '=', 18)
		self.dfa.set_acceptState(16, T.opr)
		self.dfa.set_acceptState(15, T.opr)
		self.dfa.set_acceptState(18, T.opr)
		self.dfa.set_acceptState(17, T.rcb)

		#Operações aritméticas
		self.dfa.set_DFA(0, '+', 20)
		self.dfa.set_DFA(0, '-', 20)
		self.dfa.set_DFA(0, '*', 20)
		self.dfa.set_DFA(0, '/', 20)
		self.dfa.set_acceptState(20, T.opm)

		#Id
		normalString = string.ascii_lowercase + string.ascii_uppercase
		for st in normalString:
			self.dfa.set_DFA(0, st, 19)
			self.dfa.set_DFA(19, st, 19)
		for digit in range(10):
			self.dfa.set_DFA(19, str(digit), 19)

		self.dfa.set_DFA(19, '_', 19)
		self.dfa.set_acceptState(19, T.id)


def preset_print(accept, tok):

	if accept:
		token = tok
		if token != ' ':
			print ("Token: " + token)

	if not accept:
		print ("Erro")

def repeat_to_length(string_to_expand, length):
    return (string_to_expand * (int(length/len(string_to_expand))+1))[:length]

if __name__ == "__main__":

	lex = LEX_DFA()
	#contents = _input.read()
	#contents = contents.replace('\n', ' ')
	
	impressao_bonita('linha')
	impressao_bonita('titulo')
	impressao_bonita('linha')
	#contents = input("Input a string ")
	#print ("\nEntrada: " +  _input)
	accept, tok = lex.dfa.accept(0)
	p = int(tok)
	while(accept == False):
		if (p < eof):
			p = int(tok)
			accept, tok = lex.dfa.accept(p)
		else:
			break
	impressao_bonita('linha')
	if (erro>0):
		print("Foram encontrados "+ str(erro)+ bcolors.RED + bcolors.BOLD + " erros" + bcolors.END + " na análise léxica!")
		impressao_bonita('linha')
		for err in vetor_erros:
			impressao_bonita('erro', err['acumulated'], err['token'])
		impressao_bonita('linha')

	print(bcolors.BOLD +"|%-10s  %-10s %-10s TABELA DE SIMBOLOS %-10s  %-10s   %-10s |" % (' ', ' ', ' ', ' ',' ', ' ') + bcolors.END )
	impressao_bonita('linha')
	impressao_bonita('titulo')
	impressao_bonita('linha')
	for tab in tabela_simbolos:
		if tab['lexema'] is tab['token']:
			impressao_bonita('reservada', tab['lexema'], tab['token'])
		else:
			impressao_bonita('repetida', tab['lexema'], tab['token'])
	impressao_bonita('linha')
	#preset_print(accept, tok)