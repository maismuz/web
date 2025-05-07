from rest_framework.test import APITestCase
from rest_framework import status
from .models import *

# Create your tests here.
# class ModalidadeAPITestCase(APITestCase):
#     def setUp(self):
#         self.modalidade_data = {
#             'nome': 'Futebol'
#         }

#     def test_create_modalidade(self):
#         response = self.client.post('/esportemuz/api/modalidades/', self.modalidade_data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(response.data['nome'], self.modalidade_data['nome'])

#     def test_get_modalidades(self):
#         Modalidade.objects.create(nome='Futebol')
#         response = self.client.get('/esportemuz/api/modalidades/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)

#     def test_update_modalidade(self):
#         modalidade = Modalidade.objects.create(nome='Futebol')
#         updated_data = {'nome': 'Futebol 7'}
#         response = self.client.put(f'/esportemuz/api/modalidades/{modalidade.id}/', updated_data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['nome'], updated_data['nome'])

#     def test_delete_modalidade(self):
#         modalidade = Modalidade.objects.create(nome='Futebol')
#         response = self.client.delete(f'/esportemuz/api/modalidades/{modalidade.id}/')
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

# class CampeonatoAPITestCase(APITestCase):
#     def setUp(self):
#         # Criação de dados para o teste
#         modalidade, _ = Modalidade.objects.get_or_create(nome="Futebol")
#         tipo_campeonato, _ = TipoCampeonato.objects.get_or_create(nome="Pontos Corridos")[0]
#         self.campeonato_data = {
#             'nome': 'Campeonato Estadual',
#             'modalidade': modalidade.id,
#             'tipo_campeonato': tipo_campeonato.id,
#             'data_inicio': '2025-06-01',
#             'data_fim': '2025-06-30'
#         }

#     def test_create_campeonato(self):
#         response = self.client.post('/esportemuz/api/campeonatos/', self.campeonato_data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(response.data['nome'], self.campeonato_data['nome'])

#     def test_organizar_pontos_corridos(self):
#         # Criando equipes e campeonato
#         modalidade = Modalidade.objects.create(nome="Futebol")
#         tipo_campeonato = TipoCampeonato.objects.create(nome="Pontos Corridos")
#         campeonato = Campeonato.objects.create(
#             nome="Campeonato Estadual",
#             modalidade=modalidade,
#             tipo_campeonato=tipo_campeonato,
#             data_inicio="2025-06-01",
#             data_fim="2025-06-30"
#         )
#         equipe1 = Equipe.objects.create(nome="Time A", campeonato=campeonato)
#         equipe2 = Equipe.objects.create(nome="Time B", campeonato=campeonato)

#         # Organizar campeonato
#         response = self.client.post(f'/esportemuz/api/campeonatos/{campeonato.id}/organizar/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_organizar_fase_grupos(self):
#         # Criando equipes e campeonato
#         modalidade = Modalidade.objects.create(nome="Futebol")
#         tipo_campeonato = TipoCampeonato.objects.create(nome="Fase de Grupos")
#         campeonato = Campeonato.objects.create(
#             nome="Campeonato Estadual",
#             modalidade=modalidade,
#             tipo_campeonato=tipo_campeonato,
#             data_inicio="2025-06-01",
#             data_fim="2025-06-30"
#         )
#         equipe1 = Equipe.objects.create(nome="Time A", campeonato=campeonato)
#         equipe2 = Equipe.objects.create(nome="Time B", campeonato=campeonato)

#         # Organizar campeonato com 1 grupo
#         response = self.client.post(f'/esportemuz/api/campeonatos/{campeonato.id}/organizar/', {'num_grupos': 1}, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)