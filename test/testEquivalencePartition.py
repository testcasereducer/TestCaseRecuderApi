import sys
import os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

import unittest
from techniques.EquivalencePartition.equivalencePartition import EquivalencePartition

class TestEquivalencePartition(unittest.TestCase):

    def test_parametros_validos(self):
        #
        # Caso se prueba con entradas validas
        params = {
            'param1': {
                'equiv_class1': {'valido': True, 'representante': 'value1'},
                'equiv_class2': {'valido': False, 'representante': 1}
            },
            'param2': {
                'equiv_class1': {'valido': True, 'representante': [1, 2, 3]},
                'equiv_class2': {'valido': False, 'representante': -1}
            }
        }
        EquivalencePartition(parameters=params)

    def test_parametros_invalidos(self):
        #
        # Caso de prueba cuando `representante` es None
        params = None
        with self.assertRaises(Exception):
            EquivalencePartition(parameters=params)


    def test_parametro_invalido_representate_es_none(self):
        #
        # Caso de prueba cuando `representante` es None
        params = {
            'param1': {
                'equiv_class1': {'valido': True, 'representante': 'value1'},
                'equiv_class2': {'valido': False, 'representante': None}
            },
            'param2': {
                'equiv_class1': {'valido': True, 'representante': 42},
                'equiv_class2': {'valido': False, 'representante': -1}
            }
        }

        with self.assertRaises(AssertionError):
            EquivalencePartition(parameters=params)

    def test_parametro_invalido_clave_none(self):
        #
        # Caso de prueba cuando la clave de `equiv_class1` es None
        params = {
            'param1': {
                'equiv_class1': {'valido': True, 'representante': 'value1'},
                'equiv_class2': {'valido': False, 'representante': None}
            },
            'param2': {
                'equiv_class1': None,
                'equiv_class2': {'valido': False, 'representante': -1}
            }
        }

        with self.assertRaises(AssertionError):
            EquivalencePartition(parameters=params)

    def test_parametro_invalido_valido_es_none(self):
        #
        # Caso de prueba cuando `valido` es None
        params = {
            'param1': {
                'equiv_class1': {'valido': True, 'representante': 'value1'},
                'equiv_class2': {'valido': False, 'representante': 'value2'}
            },
            'param2': {
                'equiv_class1': {'valido': True, 'representante': 42},
                'equiv_class2': {'valido': None, 'representante': -1}
            }
        }

        with self.assertRaises(AssertionError):
            EquivalencePartition(parameters=params)

    def test_generar_casos_de_prueba_cantidad_esperada_1(self):
        #
        # En este test validamos solo el numero de casos de prueba, para este en particular
        # el numero de casos de prueba validos son 27 (3x3x3), y el de invalidos es 0.
        parameters = {
            "param1": {
                "equiv_class1": {"valido": True, "representante": "value1"},
                "equiv_class2": {"valido": True, "representante": "value2"},
                "equiv_class3": {"valido": True, "representante": "value3"},
            },
            "param2": {
                "equiv_class1": {"valido": True, "representante": 10},
                "equiv_class2": {"valido": True, "representante": 20},
                "equiv_class3": {"valido": True, "representante": 30},
            },
            "param3": {
                "equiv_class1": {"valido": True, "representante": [1, 2, 3]},
                "equiv_class2": {"valido": True, "representante": [4, 5, 6]},
                "equiv_class3": {"valido": True, "representante": [7, 8, 9]},
            },
        }

        ep = EquivalencePartition(parameters)
        test_cases = ep.build_test_cases()
        test_cases_valids = test_cases.get('casos_validos', [])
        test_cases_invalids = test_cases.get('casos_invalidos', [])

        self.assertEqual(len(test_cases_valids), 27)
        self.assertEqual(len(test_cases_invalids), 0)

    def test_generar_casos_de_prueba_cantidad_esperada_2(self):
        #
        # En este test validamos solo el numero de casos de prueba, para este en particular
        # el numero de casos de prueba validos son 4, y el de invalidos es 4.
        parameters = {
            "param1": {
                "equiv_class1": {"valido": True, "representante": "value1"},
                "equiv_class2": {"valido": False, "representante": "value2"},
                "equiv_class3": {"valido": True, "representante": "value3"},
            },
            "param2": {
                "equiv_class1": {"valido": True, "representante": 10},
                "equiv_class2": {"valido": False, "representante": 20},
                "equiv_class3": {"valido": False, "representante": 30},
            },
            "param3": {
                "equiv_class1": {"valido": True, "representante": [1, 2, 3]},
                "equiv_class2": {"valido": False, "representante": [4, 5, 6]},
                "equiv_class3": {"valido": True, "representante": [7, 8, 9]},
            },
        }

        ep = EquivalencePartition(parameters)
        test_cases = ep.build_test_cases()
        test_cases_valids = test_cases.get('casos_validos', [])
        test_cases_invalids = test_cases.get('casos_invalidos', [])
        self.assertEqual(len(test_cases_valids), 4)
        self.assertEqual(len(test_cases_invalids), 4)

    def test_generar_casos_de_prueba_cantidad_esperada_3(self):
        #
        # En este test validamos solo el numero de casos de prueba, para este en particular
        # el numero de casos de prueba validos son 1, y el de invalidos es 6.
        parameters = {
            "param1": {
                "equiv_class1": {"valido": True, "representante": "value1"},
                "equiv_class2": {"valido": False, "representante": "value2"},
                "equiv_class3": {"valido": False, "representante": "value3"},
            },
            "param2": {
                "equiv_class1": {"valido": True, "representante": 10},
                "equiv_class2": {"valido": False, "representante": 20},
                "equiv_class3": {"valido": False, "representante": 30},
            },
            "param3": {
                "equiv_class1": {"valido": True, "representante": [1, 2, 3]},
                "equiv_class2": {"valido": False, "representante": [4, 5, 6]},
                "equiv_class3": {"valido": False, "representante": [7, 8, 9]},
            },
        }

        ep = EquivalencePartition(parameters)
        test_cases = ep.build_test_cases()
        test_cases_valids = test_cases.get('casos_validos', [])
        test_cases_invalids = test_cases.get('casos_invalidos', [])
        self.assertEqual(len(test_cases_valids), 1)
        self.assertEqual(len(test_cases_invalids), 6)

    def test_generar_casos_de_pruebas_salida_esperada_1(self):
        #
        # Caso de prueba cuando se espera una salida en especifica. (9 casos de prueba. 3x3)
        parameters = {
            'param1': {
                'class1': {'valido': True, 'representante': 1},
                'class2': {'valido': True, 'representante': 2},
                'class3': {'valido': True, 'representante': 3},
            },
            'param2': {
                'classA': {'valido': True, 'representante': 'A'},
                'classB': {'valido': True, 'representante': 'B'},
                'classC': {'valido': True, 'representante': 'C'},
            }
        }

        ep = EquivalencePartition(parameters)

        expected_valids = [
            {'param1': {'clase_equivalencia': 'class1', 'representante': 1},
             'param2': {'clase_equivalencia': 'classA', 'representante': 'A'}},

            {'param1': {'clase_equivalencia': 'class1', 'representante': 1},
             'param2': {'clase_equivalencia': 'classB', 'representante': 'B'}},

            {'param1': {'clase_equivalencia': 'class1', 'representante': 1},
             'param2': {'clase_equivalencia': 'classC', 'representante': 'C'}},

            {'param1': {'clase_equivalencia': 'class2', 'representante': 2},
             'param2': {'clase_equivalencia': 'classA', 'representante': 'A'}},

            {'param1': {'clase_equivalencia': 'class2', 'representante': 2},
             'param2': {'clase_equivalencia': 'classB', 'representante': 'B'}},

            {'param1': {'clase_equivalencia': 'class2', 'representante': 2},
             'param2': {'clase_equivalencia': 'classC', 'representante': 'C'}},

            {'param1': {'clase_equivalencia': 'class3', 'representante': 3},
             'param2': {'clase_equivalencia': 'classA', 'representante': 'A'}},

            {'param1': {'clase_equivalencia': 'class3', 'representante': 3},
             'param2': {'clase_equivalencia': 'classB', 'representante': 'B'}},

            {'param1': {'clase_equivalencia': 'class3', 'representante': 3},
             'param2': {'clase_equivalencia': 'classC', 'representante': 'C'}}
        ]

        expected_invalids = []
        test_cases = ep.build_test_cases()
        test_cases_valids = test_cases.get('casos_validos', [])
        test_cases_invalids = test_cases.get('casos_invalidos', [])

        self.assertEqual(test_cases_valids, expected_valids)
        self.assertEqual(test_cases_invalids, expected_invalids)

    def test_generar_casos_de_pruebas_salida_esperada_2(self):
        #
        # Caso de prueba cuando se espera una salida en especifica. (2 casos validos y 3 invalidos)
        parameters = {
            'edad': {
                'menor_18': {'valido': False, 'representante': 10},
                'entre_18_y_65': {'valido': True, 'representante': 30},
                'mayor_65': {'valido': True, 'representante': 70}
            },
            'salario': {
                'menor_a_1000': {'valido': False, 'representante': 500},
                'entre_1000_y_5000': {'valido': True, 'representante': 2000},
                'mayor_a_5000': {'valido': False, 'representante': 8000}
            }
        }

        ep = EquivalencePartition(parameters)

        expected_valids = [

            {'edad': {'clase_equivalencia': 'entre_18_y_65', 'representante': 30},
             'salario': {'clase_equivalencia': 'entre_1000_y_5000', 'representante': 2000}},

            {'edad': {'clase_equivalencia': 'mayor_65', 'representante': 70},
             'salario': {'clase_equivalencia': 'entre_1000_y_5000', 'representante': 2000}}
        ]

        expected_invalids = [
            {'edad': {'clase_equivalencia': 'menor_18', 'representante': 10},
             'salario': {'clase_equivalencia': 'entre_1000_y_5000', 'representante': 2000}},

            {'salario': {'clase_equivalencia': 'menor_a_1000', 'representante': 500},
             'edad': {'clase_equivalencia': 'entre_18_y_65', 'representante': 30}},

            {'salario': {'clase_equivalencia': 'mayor_a_5000', 'representante': 8000},
             'edad': {'clase_equivalencia': 'entre_18_y_65', 'representante': 30}}
        ]

        test_cases = ep.build_test_cases()
        test_cases_valids = test_cases.get('casos_validos', [])
        test_cases_invalids = test_cases.get('casos_invalidos', [])

        self.assertEqual(test_cases_valids, expected_valids)
        self.assertEqual(test_cases_invalids, expected_invalids)

    def test_generar_casos_de_pruebas_salida_esperada_3(self):
        #
        # Caso de prueba cuando se espera una salida en especifica.
        parameters = {
            'edad': {
                'menor_18': {'valido': False, 'representante': 10},
                'entre_18_y_65': {'valido': True, 'representante': 30},
                'mayor_65': {'valido': True, 'representante': 70}
            },
            'salario': {
                'menor_a_1000': {'valido': False, 'representante': 500},
                'entre_1000_y_5000': {'valido': True, 'representante': 2000},
                'mayor_a_5000': {'valido': False, 'representante': 8000}
            },
            'genero': {
                'masculino': {'valido': True, 'representante': 'M'},
                'femenino': {'valido': True, 'representante': 'F'},
                'otro': {'valido': False, 'representante': 'O'}
            }
        }

        ep = EquivalencePartition(parameters)

        expected_valids = [
            {'edad': {'clase_equivalencia': 'entre_18_y_65', 'representante': 30},
             'salario': {'clase_equivalencia': 'entre_1000_y_5000', 'representante': 2000},
             'genero': {'clase_equivalencia': 'masculino', 'representante': 'M'}},

            {'edad': {'clase_equivalencia': 'entre_18_y_65', 'representante': 30},
             'salario': {'clase_equivalencia': 'entre_1000_y_5000', 'representante': 2000},
             'genero': {'clase_equivalencia': 'femenino', 'representante': 'F'}}, 
            
            {'edad': {'clase_equivalencia': 'mayor_65', 'representante': 70},
             'salario': {'clase_equivalencia': 'entre_1000_y_5000', 'representante': 2000},
             'genero': {'clase_equivalencia': 'masculino', 'representante': 'M'}}, 
            
            {'edad': {'clase_equivalencia': 'mayor_65', 'representante': 70}, 
             'salario': {'clase_equivalencia': 'entre_1000_y_5000', 'representante': 2000}, 
             'genero': {'clase_equivalencia': 'femenino', 'representante': 'F'}}
        ]

        expected_invalids = [
            {'edad': {'clase_equivalencia': 'menor_18', 'representante': 10}, 
             'salario': {'clase_equivalencia': 'entre_1000_y_5000', 'representante': 2000},
             'genero': {'clase_equivalencia': 'masculino', 'representante': 'M'}},
            
            {'salario': {'clase_equivalencia': 'menor_a_1000', 'representante': 500}, 
             'genero': {'clase_equivalencia': 'masculino', 'representante': 'M'},
             'edad': {'clase_equivalencia': 'entre_18_y_65', 'representante': 30}}, 
            
            {'salario': {'clase_equivalencia': 'mayor_a_5000', 'representante': 8000}, 
             'genero': {'clase_equivalencia': 'masculino', 'representante': 'M'}, 
             'edad': {'clase_equivalencia': 'entre_18_y_65', 'representante': 30}}, 
            
            {'genero': {'clase_equivalencia': 'otro', 'representante': 'O'}, 
             'edad': {'clase_equivalencia': 'entre_18_y_65', 'representante': 30},
             'salario': {'clase_equivalencia': 'entre_1000_y_5000', 'representante': 2000}}
        ]

        test_cases = ep.build_test_cases()
        test_cases_valids = test_cases.get('casos_validos', [])
        test_cases_invalids = test_cases.get('casos_invalidos', [])

        self.assertEqual(test_cases_valids, expected_valids)
        self.assertEqual(test_cases_invalids, expected_invalids)
    
    def test_generar_casos_de_pruebas_salida_esperada_4(self):
        #
        # Caso de prueba cuando se espera una salida en especifica. (1 caso valido y 1 invalido)
        params = {
            'param1': {
                'equiv_class1': {'valido': True, 'representante': 'value1'},
                'equiv_class2': {'valido': False, 'representante': 1}
            }
        }
        ep = EquivalencePartition(parameters=params)
        test_cases = ep.build_test_cases()
        
        expected_valids = [
            {'param1': {'clase_equivalencia': 'equiv_class1', 'representante': 'value1'}}
        ]
        
        expected_invalids = [
            {'param1': {'clase_equivalencia': 'equiv_class2', 'representante': 1}}
        ]
        
        test_cases = ep.build_test_cases()
        test_cases_valids = test_cases.get('casos_validos', [])
        test_cases_invalids = test_cases.get('casos_invalidos', [])

        self.assertEqual(test_cases_valids, expected_valids)
        self.assertEqual(test_cases_invalids, expected_invalids)

