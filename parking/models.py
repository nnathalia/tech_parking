from django.db import models
from django.contrib.auth import get_user_model

class Veiculo(models.Model):
    placa = models.CharField(max_length=10, unique=True)
    modelo = models.CharField(max_length=50)
    cor = models.CharField(max_length=20)
    proprietario = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.placa} - {self.modelo}'


class Vaga(models.Model):
    TIPO_VAGA_CHOICES = [
        ('carro', 'Carro'),
        ('moto', 'Moto'),
        ('deficiente', 'Deficiente'),
    ]

    codigo_vaga = models.CharField(max_length=10, unique=True)
    tipo_vaga = models.CharField(max_length=20, choices=TIPO_VAGA_CHOICES)
    ocupada = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.codigo_vaga


class Reserva(models.Model):
    vaga = models.ForeignKey(Vaga, on_delete=models.SET_NULL, null=True)
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    data_reserva = models.DateTimeField(auto_now_add=True)
    inicio_reserva = models.DateTimeField()
    fim_reserva = models.DateTimeField()

    def __str__(self):
        return f'Reserva para {self.veiculo} na vaga {self.vaga}'


class Monitoramento(models.Model):
    vaga = models.ForeignKey(Vaga, on_delete=models.CASCADE)
    status_vaga = models.CharField(max_length=20)
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE, null=True, blank=True)
    data_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Monitoramento da vaga {self.vaga} em {self.data_hora}'


class Navegacao(models.Model):
    vaga = models.ForeignKey(Vaga, on_delete=models.CASCADE)
    coordenadas = models.CharField(max_length=100)
    instrucoes = models.TextField()

    def __str__(self):
        return f'Instruções para {self.vaga}'
