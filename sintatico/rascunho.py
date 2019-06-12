resultado = regras.loc[red]['Semantico']
if resultado == '-':
    pass
else:
    num_semantico = int(resultado)
    if num_semantico == 5:
        arq_obj = open('programa.c', 'a+')
        arq_obj.write('\n\n\n')
        arq_obj.close()
        pilha_semantico.desempilha()
        pilha_semantico.desempilha()
        val_semantico = {'lexema':'', 'token':'','tipo':''}
        pilha_semantico.empilha(val_semantico)
    elif num_semantico == 6:
        arq_obj = open('programa.c', 'a+')
        tipo = pilha_semantico.desempilha()
        ident = pilha_semantico.desempilha()
        tabela_simbolos.put_tipo(ident['lexema'],ident['token'],tipo['tipo'])
        val_semantico = {'lexema':'', 'token':'','tipo':''}
        arq_obj.write(tipo['tipo'])
        arq_obj.write(' ')
        arq_obj.write(ident['lexema'])
        arq_obj.close()
    elif num_semantico == 7:
        pass
    elif num_semantico == 8:
        pass
    elif num_semantico == 9:
        pass
    elif num_semantico == 11:
        pass
    elif num_semantico == 12:
        pass
    elif num_semantico == 13:
        pass
    elif num_semantico == 14:
        pass
    elif num_semantico == 15:
        pass
    elif num_semantico == 16:
        pass
    elif num_semantico == 17:
        pass
    elif num_semantico == 18:
        pass
    elif num_semantico == 19:
        pass
    elif num_semantico == 20:
        pass
    elif num_semantico == 21:
        pass
    elif num_semantico == 23:
        arq_obj = open('programa.c', 'a+')
        arq_obj.write('}')
        arq_obj.close()
    elif num_semantico == 24:
        pass
    elif num_semantico == 25:
        pass
    elif num_semantico == 33:
        arq_obj = open('programa.c', 'a+')
        arq_obj.write('}')
        arq_obj.close()
    elif num_semantico == 34:
        pass
