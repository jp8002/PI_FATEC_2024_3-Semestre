import calendar
from django.test import TestCase
from core.services.MontarTendencias import montarTendencias  # Importe sua função

class TestMontarTendencias(TestCase):

    def test_montarTendencias_com_dados_completos(self):
        # Dados de entrada simulando a estrutura do MongoDB
        input_data = {
            'novas_assinaturas': [
                {'_id': 1, 'qtd': 100},
                {'_id': 3, 'qtd': 150}
            ],
            'renovacoes': [
                {'_id': 1, 'qtd': 200},
                {'_id': 2, 'qtd': 250}
            ],
            'cancelamentos': [
                {'_id': 3, 'qtd': 50},
                {'_id': 4, 'qtd': 75}
            ]
        }

        # Executa a função
        result = montarTendencias(input_data)
        
        # Verifica a estrutura básica
        self.assertEqual(len(result), 11)  # 11 meses (janeiro a novembro)
        
        # Testa meses específicos
        janeiro = result[0]
        self.assertEqual(janeiro['mes'], calendar.month_name[1])
        self.assertEqual(janeiro['novas'], 100)
        self.assertEqual(janeiro['renovacoes'], 200)
        self.assertEqual(janeiro['cancelados'], 0)

        fevereiro = result[1]
        self.assertEqual(fevereiro['mes'], calendar.month_name[2])
        self.assertEqual(fevereiro['novas'], 0)
        self.assertEqual(fevereiro['renovacoes'], 250)
        self.assertEqual(fevereiro['cancelados'], 0)

        marco = result[2]
        self.assertEqual(marco['mes'], calendar.month_name[3])
        self.assertEqual(marco['novas'], 150)
        self.assertEqual(marco['renovacoes'], 0)
        self.assertEqual(marco['cancelados'], 50)

    def test_montarTendencias_com_dados_vazios(self):
        # Dados vazios
        input_data = {
            'novas_assinaturas': [],
            'renovacoes': [],
            'cancelamentos': []
        }

        result = montarTendencias(input_data)
        
        # Verifica se todos os meses têm valores zero
        for mes in result:
            self.assertEqual(mes['novas'], 0)
            self.assertEqual(mes['renovacoes'], 0)
            self.assertEqual(mes['cancelados'], 0)