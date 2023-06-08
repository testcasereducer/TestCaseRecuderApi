import sys
import os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

import unittest
from techniques.LimitValueAnalysis.limitValueAnalysis import LimitValueAnalysis


class TestLimitValueAnalysis(unittest.TestCase) :

    def test_parametros_validos(self):
        parameters = {
            'param1' : {'lambda' : '-1.2<x<=4.3', 'delta' : 0.1},
            'param2' : {'lambda' : '1<=x<=10^6 and x%10000!=0', 'delta' : 10},
            'param3' : {'lambda' : '10<=x<=100 and x%2==0', 'delta' : 1}
        }
        LimitValueAnalysis(parameters)

    def test_parametros_invalidos_1(self):
        parameters = {'param1' : {'lambda'}}
        with self.assertRaises(ValueError):
            LimitValueAnalysis(parameters)

    def test_parametros_invalidos_2(self):
        parameters = {'param1' : {'lambda', 'delta'}}
        with self.assertRaises(ValueError):
            LimitValueAnalysis(parameters)


    def test_parametro_invalido_delta_none(self):
        #
        # Caso de prueba cuando el `delta` es None
        parameters = {
            'param1' : {'lambda' : '-1.2<x<=4.3', 'delta' : None},
            'param2' : {'lambda' : '1<=x<=10^6 and x%10000!=0', 'delta' : 10},
            'param3' : {'lambda' : '10<=x<=100 and x%2==0', 'delta' : 1}
        }

        with self.assertRaises(TypeError):
            LimitValueAnalysis(parameters)


    def test_parametro_invalido_lambda_syntaxError(self):
        #
        # Caso de prueba cuando el `lambda` esta mal escrito. (param2 :  X mayuscula)
        parameters = {
            'param1' : {'lambda' : '-1.2<x<=4.3', 'delta' : 1},
            'param2' : {'lambda' : '1<=x<=10^6 and x%10000!=0 and X != 200000', 'delta' : 10},
            'param3' : {'lambda' : '10<=x<=1p00 and x%2==0', 'delta' : 1}
        }
        
        with self.assertRaises(SyntaxError):
            LimitValueAnalysis(parameters)


    def test_parametro_invalido_lambda_type(self):
        #
        # Caso de prueba cuando el `lambda` esta mal escrito. (param2 :  X mayuscula)
        parameters = {
            'param1' : {'lambda' : None, 'delta' : 1}
        }
        
        with self.assertRaises(TypeError):
            LimitValueAnalysis(parameters)

    def test_parametro_invalido_lambda_incorrecto(self):
        #
        # Caso de prueba cuando el `lambda` esta mal definido
        parameters = {
            'param1' : {'lambda' : 'x>100 and x<100', 'delta' : 1}
        }
        
        analysis = LimitValueAnalysis(parameters)
        with self.assertRaises(Exception):
            analysis.build_limits()

    def test_parametro_invalido_lambda_size(self):
        #
        # Caso de prueba cuando el `lambda` esta mal definido
        parameters = {
            'param1' : {'lambda' : 'x>10', 'delta' : 1}
        }
        
        with self.assertRaises(ValueError):
            LimitValueAnalysis(parameters)

    def test_generar_limites_1(self):
        #
        # Caso de prueba con una salida esperada.
        parameters = {
            'param1' : {'lambda' : 'x >= 100 and x <= 10000 and x % 100 == 0', 'delta' : 1}
        }
        expected_test_cases = {
            'param1': {
                'valor_minimo_invalido': 99,
                'primer_valor_minimo': 100,
                'segundo_valor_minimo': 200,
                'valor_medio': 5000,
                'primer_valor_maximo': 9900,
                'segundo_valor_maximo': 10000,
                'valor_maximo_invalido': 10001
            }
        }

        analysis = LimitValueAnalysis(parameters)
        test_cases = analysis.build_limits()

        self.assertEqual(expected_test_cases, test_cases)


    def test_generar_limites_3(self):
        #
        # Caso de prueba con una salida esperada.
        parameters = {
            'param1' : {'lambda' : '-1.2<x<=4.3', 'delta' : 0.1},
            'param2' : {'lambda' : '1<=x<=10^6 and x%10000!=0', 'delta' : 10},
            'param3' : {'lambda' : '10<=x<=100 and x%2==0', 'delta' : 1}
        }
        expected_test_cases = {
            'param1': {
                'valor_minimo_invalido': -1.2,
                'primer_valor_minimo': -1.1,
                'segundo_valor_minimo': -1.0,
                'valor_medio': 1.0,
                'primer_valor_maximo': 4.2,
                'segundo_valor_maximo': 4.3,
                'valor_maximo_invalido': 4.4
            },
            'param2': {
                'valor_minimo_invalido': 0,
                'primer_valor_minimo': 10,
                'segundo_valor_minimo': 20,
                'valor_medio': 499990,
                'primer_valor_maximo': 999980,
                'segundo_valor_maximo': 999990,
                'valor_maximo_invalido': 1000000
            },
            'param3': {
                'valor_minimo_invalido': 9,
                'primer_valor_minimo': 10,
                'segundo_valor_minimo': 12,
                'valor_medio': 54,
                'primer_valor_maximo': 98,
                'segundo_valor_maximo': 100,
                'valor_maximo_invalido': 101
            }
        }

        analysis = LimitValueAnalysis(parameters)
        test_cases = analysis.build_limits()

        self.assertEqual(expected_test_cases, test_cases)


    def test_generar_limites_con_particion_de_equivalencias(self):
        #
        # Caso de prueba con una salida esperada.
        parameters = {
            'param1' : {'lambda' : '-1.2<x<=4.3', 'delta' : 0.1},
            'param2' : {'lambda' : '1<=x<=10^6 and x%10000!=0', 'delta' : 10},
            'param3' : {'lambda' : '10<=x<=100 and x%2==0', 'delta' : 1}
        }
        expected_limits = {
            'param1': {
                'valor_minimo_invalido': -1.2,
                'primer_valor_minimo': -1.1,
                'segundo_valor_minimo': -1.0,
                'valor_medio': 1.0,
                'primer_valor_maximo': 4.2,
                'segundo_valor_maximo': 4.3,
                'valor_maximo_invalido': 4.4
            },
            'param2': {
                'valor_minimo_invalido': 0,
                'primer_valor_minimo': 10,
                'segundo_valor_minimo': 20,
                'valor_medio': 499990,
                'primer_valor_maximo': 999980,
                'segundo_valor_maximo': 999990,
                'valor_maximo_invalido': 1000000
            },
            'param3': {
                'valor_minimo_invalido': 9,
                'primer_valor_minimo': 10,
                'segundo_valor_minimo': 12,
                'valor_medio': 54,
                'primer_valor_maximo': 98,
                'segundo_valor_maximo': 100,
                'valor_maximo_invalido': 101
            }
        }

        analysis = LimitValueAnalysis(parameters)
        limits = analysis.build_limits()
        test_cases = analysis.build_test_cases()
        n_valids = len(test_cases.get('casos_validos', 0))
        n_invalids = len(test_cases.get('casos_invalidos', 0))

        self.assertEqual(expected_limits, limits)
        self.assertEqual(n_valids, 125)
        self.assertEqual(n_invalids, 6)
        
    def test_generar_limites_timelimit(self):

        #
        # Caso de prueba cuando el algoritmo tarda demasiado en encontrar los limites
        parameters = {
            'param1' : {'lambda' : 'x >= 1 and x <= 1000000000000 and x % 100000 == 0', 'delta' : 0.1}
        }

        analysis = LimitValueAnalysis(parameters)
        with self.assertRaises(Exception):
            analysis.build_limits()
        

if __name__ == '__main__':
    unittest.main()
