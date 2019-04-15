import hashlib
import string

_arquivo = open('fonte.alg', 'r')

# Tokens
TOKEN = lambda x:x
TOKEN.num = 'num'
TOKEN.literal = 'literal'
TOKEN.id = 'id'
TOKEN.noToken = 'noToken'
TOKEN.eof = 'eof'
TOKEN.opr = 'opr'
TOKEN.rcb = 'rc'
TOKEN.opm = 'opm'
TOKEN.ab_p = 'ab_p'
TOKEN.fc_p = 'fc_p'
TOKEN.pt_v = 'pt_v'
TOKEN.erro = 'erro'

class bcolors:
    BOLD = '\033[1m'
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
	elif token == TOK.noToken: 
		return ' '
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

def impressao_bonita(id, acumulated = 0, token = ''):
	if id == 'titulo':
		print(bcolors.BOLD +"|%-10s LEXEMA %-11s| %-10s TOKEN %-10s | %-10s TIPO  %-10s |" % (' ', ' ', ' ', ' ',' ', ' ') + bcolors.END )
	elif id == 'linha':
		print("+"+repeat_to_length('.', 29)+"+"+repeat_to_length('.', 29) + "+"+repeat_to_length('.', 29) + "+")
	else:
		print("|%-2s  %-25s| %-10s  %-10s %-5s| %-10s  - %-14s|" % (' ', acumulated, ' ', token_def(token), ' ',' ',' '))


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

		def accept(self, ponteiro):
			state = 0
			token = self.statesToken[state]
			token_aceito = self.statesToken[state]
			lexema_aceito = ''
			ponteiro_aceito = 0
			acumulated = ''
			try:
				while (_arquivo.seek(ponteiro) is not None):
					
					_arquivo.seek(ponteiro)
					c = _arquivo.read(1)
					#print ("Caracter lido: " + c)

					state = self.transitions[state][c]
					
					token = self.statesToken[state]

					ponteiro+=1
					acumulated += c

				impressao_bonita('corpo', acumulated, token)

				return self.acceptStates[state], token_def(self.statesToken[state])

			except KeyError:

				impressao_bonita('corpo', acumulated, token)
				#first, st = input_line.split(input_line[input_line.find(stop)], 1)
				#print("Cont: {}".format(cont))
				#print ("\tSplit: {}".format(st))
				return False, ponteiro


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
		self.dfa.set_acceptState(10,T.ab_p)

		#Comentário
		self.dfa.set_DFA(0, '{', 11)
		for st in string.printable:
			self.dfa.set_DFA(11, st, 11)
		self.dfa.set_DFA(11,'}',12)
		self.dfa.set_acceptState(12,T.noToken)

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
	while(accept == False):
		if not(_arquivo.read(tok)):
			break
		#print ("\nEntrada: " +  new_input)
		accept, tok = lex.dfa.accept(tok)
	impressao_bonita('linha')
	#preset_print(accept, tok)