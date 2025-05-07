from rest_framework.test import APITestCase
from rest_framework import status
from .models import Modalidade

# Create your tests here.
class ModalidadeAPITestCase(APITestCase):
    def setUp(self):
        self.modalidade_data = {
            'nome': 'Futebol'
        }

    def test_create_modalidade(self):
        response = self.client.post('/esportemuz/api/modalidades/', self.modalidade_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['nome'], self.modalidade_data['nome'])

    def test_get_modalidades(self):
        Modalidade.objects.create(nome='Futebol')
        response = self.client.get('/esportemuz/api/modalidades/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_modalidade(self):
        modalidade = Modalidade.objects.create(nome='Futebol')
        updated_data = {'nome': 'Futebol 7'}
        response = self.client.put(f'/esportemuz/api/modalidades/{modalidade.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nome'], updated_data['nome'])

    def test_delete_modalidade(self):
        modalidade = Modalidade.objects.create(nome='Futebol')
        response = self.client.delete(f'/esportemuz/api/modalidades/{modalidade.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)