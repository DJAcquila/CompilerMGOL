# CompilerMGOL

Compilador desenvolvido em python para tradução de MGOL para C

## Requisitos
Para execução do compilador você precisará apenas de python3
```bash
$ sudo apt update
$ sudo apt install python3.6
$ sudo apt install python3.6-pip
$ pip3 --version
```
## Execução
Para execução do help
```bash
$ python3 main.py -h

usage: main.py [-h] [-l] [-v] filename

Compilador da linguagem MGOL - Por enquanto, apenas o analisador léxico

positional arguments:
  filename

optional arguments:
  -h, --help     show this help message and exit
  -l, --lexico   Realiza somente a analise léxica
  -v, --verbose  Ativa o modo verboso do compilador
```
Para executar a análise léxica

```bash 
$ python3 main.py fontesMGOL/algumarquivo.alg -l
```
## License
[MIT](https://choosealicense.com/licenses/mit/)
