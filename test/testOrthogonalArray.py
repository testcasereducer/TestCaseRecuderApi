import sys
import os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

import unittest
from techniques.OrthogonalArray.orthogonalArray import OrthogonalArray


class TestOrthogonalArray(unittest.TestCase):


    def test_valores_vacios(self):
        
        parameters = {
            'param1' : [],
            'param2' : [],
            'param3' : []
        }

        with self.assertRaises(ValueError):
            OrthogonalArray(parameters)

    def test_keys_none(self):
        
        parameters = {
            None : [100, 200],
            'param2' : ['A', 'B'],
            'param3' : [1, 2, 3]
        }

        with self.assertRaises(ValueError):
            OrthogonalArray(parameters)

    def test_values_none_1(self):
        
        parameters = {
            'param1' : None,
            'param2' : None,
            'param3' : [1, 2, 3]
        }

        with self.assertRaises(ValueError):
            OrthogonalArray(parameters)

    def test_values_none_2(self):
        
        parameters = {
            'param1' : [1, 2, 3, None],
            'param2' : [None],
            'param3' : [1, 2, 3]
        }

        with self.assertRaises(ValueError):
            OrthogonalArray(parameters)

    def test_arreglo_ortogonal_fuera_de_rango(self):
        
        max_parameters,  max_values = 13, 10
        parameters = {}

        for i in range(max_parameters):
            parameters[f'param{i + 1}'] = [ i + value for value in range(max_values)]

        with self.assertRaises(ValueError):
            oa = OrthogonalArray(parameters)
            oa.build_test_cases()


    def test_array_L4_1(self):
        
        parameters = {
            'param1' : ['A', 'B'],
            'param2' : [1, 2],
            'param3' : ['value1']
        }

        oa = OrthogonalArray(parameters)

        expected_L = 'L4'
        expected_keys = ['param1', 'param2', 'param3']
        expected_array = [
            ['A', 1, 'value1'], 
            ['A', 2, 'value1'],
            ['B', 1, 'value1'], 
            ['B', 2, 'value1']
        ]

        output = oa.build_test_cases()
        keys = output.get('keys', [])
        array = output.get('array', [])
        L = output.get('L', '')

        self.assertEqual(array, expected_array)
        self.assertEqual(keys, expected_keys)
        self.assertEqual(L, expected_L)

    def test_array_L4_2(self):
        
        parameters = {
            'param1' : ['A', 'B'],
            'param2' : [1, 2],
            'param3' : ['value1', 'value2']
        }

        oa = OrthogonalArray(parameters)

        expected_L = 'L4'
        expected_keys = ['param1', 'param2', 'param3']
        expected_array = [
            ['A', 1, 'value1'], 
            ['A', 2, 'value2'],
            ['B', 1, 'value2'], 
            ['B', 2, 'value1']
        ]

        output = oa.build_test_cases()
        keys = output.get('keys', [])
        array = output.get('array', [])
        L = output.get('L', '')

        self.assertEqual(array, expected_array)
        self.assertEqual(keys, expected_keys)
        self.assertEqual(L, expected_L)

    def test_array_L8_1(self):
        
        parameters = {
            'param1' : ['A', 'B'],
            'param2' : [1, 2],
            'param3' : ['%', '#'],
            'param4' : ['P', 'Q'],
            'param5' : ['X', 'Y']
        }

        oa = OrthogonalArray(parameters)

        expected_L = 'L8'
        expected_keys = ['param1', 'param2', 'param3', 'param4', 'param5']
        expected_array = [
            ['A', 1, '%', 'P', 'X'], 
            ['A', 1, '%', 'Q', 'Y'], 
            ['A', 2, '#', 'P', 'X'],
            ['A', 2, '#', 'Q', 'Y'], 
            ['B', 1, '#', 'P', 'Y'], 
            ['B', 1, '#', 'Q', 'X'],
            ['B', 2, '%', 'P', 'Y'],
            ['B', 2, '%', 'Q', 'X']
        ]

        output = oa.build_test_cases()
        keys = output.get('keys', [])
        array = output.get('array', [])
        L = output.get('L', '')

        self.assertEqual(array, expected_array)
        self.assertEqual(keys, expected_keys)
        self.assertEqual(L, expected_L)

    def test_array_L8_2(self):
        
        parameters = {
            'param1' : ['A', 'B'],
            'param2' : [1, 2],
            'param3' : ['%', '#'],
            'param4' : ['P', 'Q'],
            'param5' : [100, 200],
            'param6' : ['+', '-'],
            'param7' : ['OS', 'WS']
        }

        oa = OrthogonalArray(parameters)

        expected_L = 'L8'
        expected_keys = ['param1', 'param2', 'param3', 'param4', 'param5', 'param6', 'param7']
        expected_array = [
            ['A', 1, '%', 'P', 100, '+', 'OS'], 
            ['A', 1, '%', 'Q', 200, '-', 'WS'], 
            ['A', 2, '#', 'P', 100, '-', 'WS'], 
            ['A', 2, '#', 'Q', 200, '+', 'OS'], 
            ['B', 1, '#', 'P', 200, '+', 'WS'], 
            ['B', 1, '#', 'Q', 100, '-', 'OS'], 
            ['B', 2, '%', 'P', 200, '-', 'OS'], 
            ['B', 2, '%', 'Q', 100, '+', 'WS']
        ]

        output = oa.build_test_cases()
        keys = output.get('keys', [])
        array = output.get('array', [])
        L = output.get('L', '')

        self.assertEqual(array, expected_array)
        self.assertEqual(keys, expected_keys)
        self.assertEqual(L, expected_L)

    def test_array_L9_1(self):
        
        parameters = {
            'param1' : ['A', 'B', 'C'],
            'param2' : [1, 2, 3],
            'param3' : ['%', '#', '$'],
            'param4' : ['P', 'Q', 'R']
        }

        oa = OrthogonalArray(parameters)

        expected_L = 'L9'
        expected_keys = ['param1', 'param2', 'param3', 'param4']
        expected_array = [
            ['A', 1, '%', 'P'], 
            ['B', 2, '#', 'Q'], 
            ['C', 3, '$', 'R'], 
            ['A', 2, '$', 'P'], 
            ['B', 3, '%', 'Q'], 
            ['C', 1, '#', 'R'], 
            ['A', 3, '#', 'R'], 
            ['B', 1, '$', 'P'], 
            ['C', 2, '%', 'Q']
        ]
    
        output = oa.build_test_cases()
        keys = output.get('keys', [])
        array = output.get('array', [])
        L = output.get('L', '')

        self.assertEqual(array, expected_array)
        self.assertEqual(keys, expected_keys)
        self.assertEqual(L, expected_L)

    def test_array_L11_1(self):
        
        parameters = {
            'param1' : ['A', 'B'],
            'param2' : [1, 2],
            'param3' : ['%', '#'],
            'param4' : ['&', '*'],
            'param5' : [100, 200],
            'param6' : [300, 400],
            'param7' : ['r', 'z'],
            'param8' : ['W', 'D']
        }

        oa = OrthogonalArray(parameters)

        expected_L = 'L12'
        expected_keys = [
            'param1', 'param2', 'param3', 'param4', 
            'param5', 'param6', 'param7', 'param8']
        expected_array = [
            ['A', 1, '%', '&', 100, 300, 'r', 'W'], 
            ['A', 1, '%', '&', 100, 400, 'z', 'D'], 
            ['A', 1, '#', '*', 200, 300, 'r', 'W'], 
            ['A', 2, '%', '*', 200, 300, 'z', 'D'], 
            ['A', 2, '#', '&', 200, 400, 'r', 'D'], 
            ['A', 2, '#', '*', 100, 400, 'z', 'W'], 
            ['B', 1, '#', '*', 100, 300, 'z', 'D'], 
            ['B', 1, '#', '&', 200, 400, 'z', 'W'], 
            ['B', 1, '%', '*', 200, 400, 'r', 'D'], 
            ['B', 2, '#', '&', 100, 300, 'r', 'D'], 
            ['B', 2, '%', '*', 100, 400, 'r', 'W'], 
            ['B', 2, '%', '&', 200, 300, 'z', 'W']
        ]

        output = oa.build_test_cases()
        keys = output.get('keys', [])
        array = output.get('array', [])
        L = output.get('L', '')
        self.assertEqual(array, expected_array)
        self.assertEqual(keys, expected_keys)
        self.assertEqual(L, expected_L)
