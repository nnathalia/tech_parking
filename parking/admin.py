from django.contrib import admin
from .models import Proprietario, Veiculo, Vaga, Reserva, Monitoramento, Navegacao

admin.site.register(Proprietario)
admin.site.register(Veiculo)
admin.site.register(Vaga)
admin.site.register(Reserva)
admin.site.register(Monitoramento)
admin.site.register(Navegacao)
