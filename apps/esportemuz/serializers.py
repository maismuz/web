from rest_framework import serializers
from esportemuz.models import *

# Create your serializers here.
class ModalidadeSerializer(serializers.ModelSerializer):
    """
    Serializador para o modelo Modalidade.
    """
    class Meta:
        model = Modalidade
        fields = '__all__'

    def create(self, validated_data):
        """
        Cria uma nova modalidade.
        """
        return Modalidade.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        """
        Atualiza uma modalidade existente.
        """
        instance.nome = validated_data.get('nome', instance.nome)
        instance.save()
        return instance

class TipoCampeonatoSerializer(serializers.ModelSerializer):
    """
    Serializador para o modelo TipoCampeonato.
    """
    class Meta:
        model = TipoCampeonato
        fields = '__all__'

class CampeonatoSerializer(serializers.ModelSerializer):
    """
    Serializador para o modelo Campeonato.
    """
    modalidade = serializers.StringRelatedField()
    tipo_campeonato = serializers.StringRelatedField()

    class Meta:
        model = Campeonato
        fields = '__all__'

# class EquipeSerializer(serializers.ModelSerializer):
#     """
#     Serializador para o modelo Equipe.
#     """
#     class Meta:
#         model = Equipe
#         fields = '__all__'

# class GrupoSerializer(serializers.ModelSerializer):
#     """
#     Serializador para o modelo Grupo.
#     """
#     equipes = EquipeSerializer(many=True)

#     class Meta:
#         model = Grupo
#         fields = '__all__'

# class StatusPartidaSerializer(serializers.ModelSerializer):
#     """
#     Serializador para o modelo StatusPartida.
#     """
#     class Meta:
#         model = StatusPartida
#         fields = '__all__'

# class PartidaSerializer(serializers.ModelSerializer):
#     """
#     Serializador para o modelo Partida.
#     """
#     equipe_mandante = EquipeSerializer()
#     equipe_visitante = EquipeSerializer()
#     status = StatusPartidaSerializer()

#     class Meta:
#         model = Partida
#         fields = '__all__'

# class ClassificacaoSerializer(serializers.ModelSerializer):
#     """
#     Serializador para o modelo Classificacao.
#     """
#     equipe = EquipeSerializer()

#     class Meta:
#         model = Classificacao
#         fields = '__all__'