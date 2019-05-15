#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pandas as pd
import string

tabela_acoes = pd.read_csv("tabela-sintatica-acoes.csv")
#print(tabela_acoes.loc[3]['id'])

tabela_desvios = pd.read_csv("tabela-sintatica-desvios.csv")
#print (tabela_desvios.loc[0]['P'])

#gramatica, usadas no algoritmo para o reduce
regras = pd.read_csv("gramatica.csv")

class Pilha(object):
	def __init__(self):
		self.dados = []

	def empilha(self, simbolo):
		self.dados.append(simbolo)

	def desempilha(self):
		if not self.vazia():
			return self.dados.pop(-1)

	def vazia(self):
		return len(self.dados) == 0

def Shift_Reduce():
	pilha = Pilha()
	pilha.empilha(18)
	a = 'id' #simbolo do lexico
	while True:
		s = int(pilha.desempilha())
		if 's' in tabela_acoes.loc[s][a]:
			print('acao shift')
			t = tabela_acoes.loc[s][a]
			t = t.split('s')
			t = int(t[1])
			pilha.empilha(int(t))
			#a = #proximo simbolo de entrada
		elif 'r' in tabela_acoes.loc[s][a]:
			print('acao reduce')
			red = tabela_acoes.loc[s][a]
			red = red.split('r')
			red = int(red[1])
			B_simbols = int(regras.loc[red]['B_number'])
			while (B_simbols > 0):
				print(pilha.desempilha())
				B_simbols-= B_simbols
			t = pilha.desempilha()
			A = regras.loc[red]['Antecedente']
			print(A)
			pilha.empilha(tabela_desvios.loc[t][A])
			print(regras.loc[red]['Antecedente']+'->'+regras.loc[red]['Consequente'])

		elif 'acc' in tabela_acoes.loc[s][a]:
			print('aceita')
			break
		else:
			print('erro')

#while True:
#	topo_pilha_s = 
#	if ACTION(topo_pilha_s,token_a) == st:
#		empilha(t)
		
if __name__ == "__main__":

	Shift_Reduce()