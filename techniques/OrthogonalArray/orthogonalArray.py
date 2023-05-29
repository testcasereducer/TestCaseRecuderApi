

from .arrays import orthogonal_arrays


class OrthogonalArray:
    def __init__(self, parameters : dict):
        
        self.__parameters = parameters
        self.__orthogonal_arrays = orthogonal_arrays

        self.__num_factors = len(self.__parameters.keys())
        self.__max_level = len(max(self.__parameters.values(), key=len))

        self.__valide_parameteres()

    def __err_get_L(self):
        """
        Calcula la propiedad de longitud (L) para un conjunto de parámetros dados.

        Returns:
            Una cadena que describe la propiedad de longitud (L) en términos de las longitudes de los valores de los parámetros.
            La cadena tiene el formato 'L( Level1^Factor1 Level2^Factor2 ... )', donde 'LevelX' las posibles valores que pueden tomas
            las variables 'Factor'
        """
        length_counts = {}
        for _, value in self.__parameters.items():
            length = len(value)
            length_counts[length] = length_counts.get(length, 0) + 1

        L = 'L( '
        for length, count in length_counts.items(): 
            L = L + f'{length}^{count} '
        return L + ')'


    def __get_orthogonal_array(self):
        for key, value in self.__orthogonal_arrays.items():
            if value['levels'] == self.__max_level and self.__num_factors <= value['factors']:
                return key, value['array']
                
        raise ValueError(f'No hay arreglo ortogonal para {self.__err_get_L()}')
     
    def __valide_parameteres(self):
        for key, value in self.__parameters.items():
            if key is None:
                raise ValueError(f'Clave inválida {key}')
            if type(value) != list:
                raise ValueError(f'El valor de {key} no es una lista.')
            if len(value) == 0:
                raise ValueError(f'La longitud del valor de {key} debe ser al menos 1.')
            if None in value:
                raise ValueError(f'Los valores de {key} deben ser diferentes de None.')



    def build_test_cases(self):
        L, array =  self.__get_orthogonal_array()

        sorted_parameters = dict(sorted(self.__parameters.items(), key=lambda x: len(x[1]), reverse=True))

        keys = list(sorted_parameters.keys())
        N, M = len(array), len(keys)
        test_cases = [[0 for _ in range(M)] for _ in range(N)]
        
        for column, key in enumerate(keys):
            values = sorted_parameters[key]
            queue = values.copy()
            for row in range(N):
                idx = array[row][column] - 1
                value = None
                if idx < 0: 
                    raise IndexError(f'Invalid idx {idx}')
                if -1 < idx < len(values): value = values[idx] 
                else: value = queue[0]; queue = queue[1:] + [queue[0]]
                test_cases[row][column] =  value

        return {
            'L' : L,
            'keys' : keys,
            'array' : test_cases
        }
