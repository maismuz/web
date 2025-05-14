from rest_framework import serializers
from esportemuz.models import *

# Create your serializers here.
class ModalidadeSerializer(serializers.ModelSerializer):
    """
    Serializador para o modelo Modalidade.
    """

    class Meta:
        model = Modalidade
        fields = ['url', 'id', 'nome']

class EquipeSerializer(serializers.ModelSerializer):
    """
    Serializador para o modelo Equipe.
    """

    class Meta:
        model = Equipe
        fields = ['url', 'id', 'nome']

class TipoCampeonatoSerializer(serializers.ModelSerializer):
    """
    Serializador para o modelo TipoCampeonato.
    """

    class Meta:
        model = TipoCampeonato
        fields = ['url', 'id', 'nome']

class CampeonatoSerializer(serializers.ModelSerializer):
    """
    Serializador para o modelo Campeonato.
    """

    class Meta:
        model = Campeonato
        fields = ['url', 'id', 'nome', 'modalidade', 'tipo_campeonato', 'data_inicio', 'data_fim', 'equipes']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['modalidade'] = instance.modalidade.nome
        representation['tipo_campeonato'] = instance.tipo_campeonato.nome
        representation['equipes'] = [equipe.nome for equipe in instance.equipes.all()]

        return representation

class LocalPartidaSerializer(serializers.ModelSerializer):
    """
    Serializador para o modelo LocalPartida.
    """

    class Meta:
        model = LocalPartida
        fields = ['url', 'id', 'nome']

class PartidaSerializer(serializers.ModelSerializer):
    """
    Serializador para o modelo Partida.
    """

    class Meta:
        model = Partida
        fields = ['url', 'id', 'campeonato', 'equipe_mandante', 'equipe_visitante', 'data_hora', 'local', 'gols_mandante', 'gols_visitante', 'encerrada']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['campeonato'] = instance.campeonato.nome
        representation['equipe_mandante'] = instance.equipe_mandante.nome
        representation['equipe_visitante'] = instance.equipe_visitante.nome
        representation['local'] = instance.local.nome

        return representation

class ClassificacaoSerializer(serializers.ModelSerializer):
    """
    Serializador para o modelo Classificacao.
    """
    
    class Meta:
        model = Classificacao
        fields = ['url', 'id', 'campeonato', 'equipe', 'pontos', 'vitorias', 'empates', 'derrotas', 'gols_pro', 'gols_contra', 'saldo_gols']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['campeonato'] = instance.campeonato.nome
        representation['equipe'] = instance.equipe.nome

        return representation