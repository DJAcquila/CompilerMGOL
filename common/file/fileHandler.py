#!/usr/bin/python3
from common.utility.util import *

class FileHandler():
    def __init__(self, name):
        self. name = name
        self._arquivo = open(name, 'r')
        self.lines = self._arquivo.readlines()
        self.eof = self._arquivo.tell()
        self.coluna = 0
        self.linha = 1
        self.ponteiro = 0

    def file_seek(self):
        self._arquivo.seek(self.ponteiro)
        
    def get_char(self):
        return self._arquivo.read(1)

    def inc_lin(self):
        self.linha = self.linha + 1
    
    def inc_col(self):
        self.coluna = self.coluna + 1
    
    def inc_ponteiro(self):
        self.ponteiro = self.ponteiro + 1

    def dec_lin(self):
        self.linha = self.linha - 1
    
    def dec_col(self):
        self.coluna = self.coluna - 1
    
    def dec_ponteiro(self):
        self.ponteiro = self.ponteiro - 1

    def set_col(self, n):
        self.coluna = n

    def set_lin(self, n):
        self.lin = n

    def set_ponteiro(self, n):
        self.ponteiro = n