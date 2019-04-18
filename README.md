# CompilerMGOL

Compilador desenvolvido em python para tradução de um código em uma linguagem fictícia (MGOL), para C

## Requisitos
Para execuço do compilador você precisará apenas de python3
```bash
$ sudo apt update
$ sudo apt isntall python3.6
$ sudo at install python3.6-pip
$ pip3 --version
```

## Divisão dos Arquivos
O projeto está divido da seguinte forma:
```bash
.
├── erro
│   ├── errno.py
├── lexico
│   ├── analisadorlexico.py
│   ├── DFA-lex.py
│   └── util
├── fontesMGOL
│   ├── fonte.alg
│   ├── texto.alg
├── main.py
├── LISCENCE
└── README.md
```
* Em ```lexico``` temos os scripts da análise léxica 
* Em ```fontesMGOL``` temos os programas exemplares em MGOL
* O srcript principal é ```main.py```
* Para lidar com impressões específicas dos erros na tela temos ```erro```

## Execução
Para execução do help
```bash
$ python3 main.py -h

usage: main.py [-h] [-l] filename

Compilador da linguagem MGOL - Por enquanto, apenas o analisador léxico

positional arguments:
  filename

optional arguments:
  -h, --help    show this help message and exit
  -l, --lexico  Realiza somente a analise léxica
```
Para executar a análise léxica

```bash 
$ python3 main.py fontesMGOL/algumarquivo.alg -l
```
## License
[MIT](https://choosealicense.com/licenses/mit/)
