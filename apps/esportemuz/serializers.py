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
    # modalidade = serializers.StringRelatedField()
    # tipo_campeonato = serializers.StringRelatedField()
    # equipes = serializers.StringRelatedField(many=True)

    class Meta:
        model = Campeonato
        fields = ['url', 'id', 'nome', 'modalidade', 'tipo_campeonato', 'data_inicio', 'data_fim', 'equipes']

class EquipeSerializer(serializers.ModelSerializer):
    """
    Serializador para o modelo Equipe.
    """

    class Meta:
        model = Equipe
        fields = ['url', 'id', 'nome']

# class GrupoSerializer(serializers.ModelSerializer):
#     """
#     Serializador para o modelo Grupo.
#     """

#     # nome = serializers.StringRelatedField()
#     # campeonato = serializers.StringRelatedField()
#     # equipes = serializers.StringRelatedField(many=True)

#     class Meta:
#         model = Grupo
#         fields = ['url', 'id', 'nome', 'campeonato', 'equipes']

class StatusPartidaSerializer(serializers.ModelSerializer):
    """
    Serializador para o modelo StatusPartida.
    """
    class Meta:
        model = StatusPartida
        fields = '__all__'

class PartidaSerializer(serializers.ModelSerializer):
    """
    Serializador para o modelo Partida.
    """

    class Meta:
        model = Partida
        fields = '__all__'

class ClassificacaoSerializer(serializers.ModelSerializer):
    """
    Serializador para o modelo Classificacao.
    """
    class Meta:
        model = Classificacao
        fields = '__all__'