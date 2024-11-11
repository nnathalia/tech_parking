from django.contrib import admin
from parking.models import Veiculo, Vaga, Reserva, Monitoramento, Navegacao

admin.site.register(Veiculo)
admin.site.register(Vaga)
admin.site.register(Reserva)
admin.site.register(Monitoramento)
admin.site.register(Navegacao)


