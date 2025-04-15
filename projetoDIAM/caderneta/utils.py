from .models import *

def processar_compra_pacote(utilizador_id, pacote_id, cromos):
    try:
        #Obtem tanto o pacote como o utilizador
        utilizador = Utilizador.objects.get(id=utilizador_id)
        pacote = Pacote.objects.get(id=pacote_id)

        #Diminui saldo do utilizador
        utilizador.saldo -= pacote.preco
        utilizador.save()

        # Adicionar os cromos selecionados à caderneta do utilizador
        for cromo in cromos:
            # Verificar se o cromo já está na caderneta do utilizador
            caderneta = Caderneta.objects.filter(utilizador=utilizador, cromo=cromo).first()
            if caderneta:
                caderneta.quantidade += 1
                caderneta.save()
            else:
                Caderneta.objects.create(utilizador=utilizador, cromo=cromo,
                                         quantidade=1)

        return True
    except Exception:
        return Falsec