from django.db import models
from django.conf import settings

class voo(models.Model):
    cod_voo = models.AutoField(primary_key=True)
    cod_companhia = models.ForeignKey('companhia', on_delete=models.CASCADE)
    cod_cid_origem = models.ForeignKey('cidades', on_delete=models.CASCADE, related_name='voos_origem', blank=True, null=True)
    cod_cid_destino = models.ForeignKey('cidades', on_delete=models.CASCADE, related_name='voos_destino', blank=True, null=True)
    data_hora_partida = models.DateTimeField()
    data_hora_chegada = models.DateTimeField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    ida_volta = models.BooleanField(default=False)
    promocao = models.BooleanField(default=False)
    capacidade = models.IntegerField(default=0)
    cod_aeroporto_origem = models.ForeignKey('aeroporto', on_delete=models.CASCADE, related_name='voos_aeroporto_origem', blank=True, null=True)
    cod_aeroporto_destino = models.ForeignKey('aeroporto', on_delete=models.CASCADE, related_name='voos_aeroporto_destino', blank=True, null=True)

    def __str__(self):
        return f"{self.cid_origem} -> {self.cid_destino} ({self.cod_companhia})"

class companhia(models.Model):
    cod_companhia = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=18, unique=True)

    def __str__(self):
        return self.nome

class hotel(models.Model):
    cod_hotel = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)
    endereco = models.CharField(max_length=200)
    cod_cidade = models.ForeignKey('cidades', on_delete=models.CASCADE, blank=True, null=True)
    imagem = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.nome

class quarto(models.Model):
    cod_quarto = models.AutoField(primary_key=True)
    cod_hotel = models.ForeignKey(hotel, on_delete=models.CASCADE)
    descricao = models.TextField()
    tipo = models.CharField(max_length=50)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    capacidade = models.IntegerField()

    def __str__(self):
        return f"{self.tipo} - {self.cod_hotel.nome}"

class cidades(models.Model):
    cod_cidade = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class aeroporto(models.Model):
    cod_aeroporto = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    endereco = models.CharField(max_length=200, default='', blank=True)
    cep = models.CharField(max_length=9, default='', blank=True)
    cod_cidade = models.ForeignKey(cidades, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

class reservaquarto(models.Model):
    cod_reservaquarto = models.AutoField(primary_key=True)
    cod_quarto = models.ForeignKey(quarto, on_delete=models.CASCADE)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    data_entrada = models.DateField()
    data_saida = models.DateField()
    status = models.CharField(max_length=20, default='Pendente')

class reservavoo(models.Model):
    cod_reservavoo = models.AutoField(primary_key=True)
    cod_voo = models.ForeignKey(quarto, on_delete=models.CASCADE)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='Pendente')