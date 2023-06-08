import re
import ast
import signal

from ..EquivalencePartition.equivalencePartition import EquivalencePartition

# Define a custom exception for the timeout
class TimeoutException(BaseException):
    pass

# Function to handle the timeout signal
def handle_timeout(signum, frame):
    raise Exception("La función tomo mucho tiempo en ejecutarse.")


class LimitValueAnalysis:
    
    """
    Una clase que realiza el análisis de valores límite para un conjunto de parámetros de prueba.

    Attributes:
    -----------
    MIN_OPT_SIZE : int
        El tamaño mínimo de la expresión matemática óptima. Por defecto, es 5.
    MAX_TIME : int
        El tiempo máximo en segundos que se permite que la ejecución de una función tarde.
        Por defecto, es 3 segundos.
    """
        
    MIN_OPT_SIZE : int = 5 # operacion min. 'a<x<b' | 'a>x>b'
    MAX_TIME : int = 4

    def __init__(self, parameters : dict) -> None:
        """
        Inicializa un objeto de prueba con los parámetros especificados.

        Parameters:
        -----------
        parameters : Dict[str, Dict[str, Union[str, int, float]]]
            Un diccionario que define los parámetros de prueba para el objeto.
            Cada clave del diccionario es el nombre del parámetro y su valor es 
            otro diccionario que contiene las siguientes claves:
            - "lambda": Una expresión matemática que define las restricciones para el parámetro de prueba.
            - "delta": El intervalo entre cada valor límite para el parámetro de prueba.

        Returns:
        --------
        None
        """
        self.__parameters = parameters
        self.__valid_parameters()


    def __valid_parameters(self):
        """
        Verifica que los parámetros de la instancia de LimitValueAnalysis sean válidos.

        Recorre los parámetros de la instancia y verifica que cada uno tenga una cadena lambda
        válida y un valor delta válido. Si un parámetro no cumple con los requisitos,
        se lanzará una excepción.
        Args:
        ------
        self : obj
            La instancia actual de la clase.
        Raises:
        ------
            KeyError: Si un parámetro no tiene una cadena lambda o un valor delta.
            TypeError: Si la cadena lambda o el valor delta no son del tipo correcto.
            ValueError: Si la cadena lambda no tiene la longitud correcta o contiene caracteres no permitidos.
            SyntaxError: Si la cadena lambda tiene una sintaxis inválida.

        """
        for key, value in self.__parameters.items():
            if self.__has_lambda(value):

                lambda_str = value['lambda']
                delta = value['delta']
                
                if type(lambda_str) != str:
                    raise TypeError(f'Tipo incorrecto {key}:{lambda_str}')
                if len(lambda_str) < LimitValueAnalysis.MIN_OPT_SIZE:
                    raise ValueError(f'El lambda de {key} debe ser almenos de {LimitValueAnalysis.MIN_OPT_SIZE}.')
                try:
                    ast.parse(lambda_str)
                    _ = lambda x : eval(lambda_str.replace('^', '**'))
                except SyntaxError:
                    raise SyntaxError(f'El lambda de {key} tiene una sintaxis inválida')

                if type(delta) != float and type(delta) != int:
                    raise TypeError(f'El tipo del delta/paso es incorrecto ({key}:{delta})')

    def __has_lambda(self, value : dict): 
        try:
            return set(value.keys()) == set(['lambda', 'delta'])
        except Exception as e:
            raise ValueError(f'El objeto {value} debe tener la clave delta y lambda.')
    def build_limits(self):

        """
        Construye una lista de objetos dict que representan los casos de prueba para cada
        parámetro en los valores proporcionados.

        Returns:
        --------
        List[Dict[str, Dict[str, Union[int, float]]]] : Una lista de objetos JSON, cada uno representando
        un caso de prueba para un parámetro.
        Cada objeto tiene una clave que representa el nombre del parámetro y un objeto anidado como valor
        que contiene los límites de prueba para ese parámetro.
        El objeto anidado tiene las siguientes claves:
            - "invalid_min": Un valor mínimo inválido para el parámetro.
            - "first_min": El primer valor mínimo válido para el parámetro.
            - "second_min": El segundo valor mínimo válido para el parámetro.
            - "middle": El valor medio para el parámetro.
            - "first_max": El primer valor máximo válido para el parámetro.
            - "second_max": El segundo valor máximo válido para el parámetro.
            - "invalid_max": Un valor máximo inválido para el parámetro.
        """

        limits = {}
        for key, value in self.__parameters.items():
            if self.__has_lambda(value):
                lambda_str = value['lambda']
                delta = value['delta']
                Fn = lambda x : eval(lambda_str.replace('^', '**'))
                min_value, max_value = self.__get_min_max(lambda_str)
                limit_values =  self.__get_values_aux(Fn, min_value, max_value, delta)
                limits[key] = limit_values 

        return limits
    
    def build_test_cases(self):
        limits = self.build_limits()
        for key, value in limits.items():
            self.__parameters[key] = {} 
            for value_key, value_value in value.items():
                self.__parameters[key][value_key] = {'valido' : not 'invalid' in value_key, 'representante' : value_value}

        equivalence = EquivalencePartition(parameters=self.__parameters)
        return equivalence.build_test_cases()

    
    
    def __get_min_max(self, lambda_str : str):
        """
        Determina el valor mínimo y máximo de una expresión matemática en formato de cadena.

        Parameters:
        -----------
        lambda_str : str
            La expresión matemática en formato de cadena.

        Returns:
        --------
        Tuple[Union[int, float], Union[int, float]] : Una tupla que contiene los valores mínimo y máximo
        de la expresión matemática. Los valores mínimo y máximo pueden ser enteros o flotantes.

        Raises:
        -------
        ValueError : Se produce si el valor mínimo es igual al valor máximo.

        Exception : Se produce si se produce un error al intentar determinar los valores mínimo y máximo de la expresión.
        """
        
        try:
            pattern = re.compile(r'-?\d+(?:\.\d+)?(?:\s*[+\-*/\*\*\^]\s*-?\d+(?:\.\d+)?)*|-?\d+(?:\.\d+)?')
            matches = re.findall(pattern, lambda_str)
            values = [eval(match.replace('^', '**')) for match in matches]
            min_value = min(values)
            max_value = max(values)
            if min_value == max_value:
                raise ValueError(f'Error, el valor mínimo debe ser mayor que el valor máximo. ({lambda_str})')
            return min_value, max_value
        except Exception as e:
            raise  Exception(f'Error al intentar determinar el valor mínimo y máximo del lambda. ({lambda_str})')
        

    def __get_values_aux(self, Fn, min_value, max_value, delta):


        """
        Obtiene los valores límite para un parámetro de prueba dado una función.

        Parameters:
        -----------
        Fn : Callable
            La función que define las restricciones para el parámetro de prueba.
        min_value : Union[int, float]
            El valor mínimo para el parámetro de prueba.
        max_value : Union[int, float]
            El valor máximo para el parámetro de prueba.
        delta : Union[int, float]
            El paso entre los valores para el parámetro de prueba

        Returns:
        --------
        Dict[str, Union[int, float]] : Un diccionario que contiene los valores límite para el parámetro de prueba.
        El diccionario tiene las siguientes claves:
            - "invalid_min": Un valor mínimo inválido para el parámetro.
            - "first_min": El primer valor mínimo válido para el parámetro.
            - "second_min": El segundo valor mínimo válido para el parámetro.
            - "middle": El valor medio para el parámetro.
            - "first_max": El primer valor máximo válido para el parámetro.
            - "second_max": El segundo valor máximo válido para el parámetro.
            - "invalid_max": Un valor máximo inválido para el parámetro.

        Raises:
        -------
        AssertionError : Se produce si alguno de los argumentos de entrada es de tipo incorrecto.

        AssertionError : Se produce si no se pueden obtener los valores límite válidos para el parámetro.
        """
        signal.signal(signal.SIGALRM, handle_timeout)
        signal.alarm(LimitValueAnalysis.MAX_TIME)

        assert type(min_value) == float or type(min_value) == int
        assert type(max_value) == float or type(max_value) == int
        assert type(delta) == float or type(delta) == int

        number_decimals = 0
        if type(delta) == float:
            number_decimals = len(re.findall(r'\d', str(delta).split('.')[1]))


        first_min, second_min = None, None
        first_max, second_max = None, None
        middle_value = None
        invalid_min, invalid_max = None, None

        number = min_value
        while number < max_value + delta:
            if Fn(number):
                if first_min is None: first_min = number
                elif second_min is None:
                    second_min = number
                    break
            number = round(number + delta, number_decimals)

        number =  max_value
        while number > min_value - delta:
            if Fn(number):
                if second_max is None: second_max = number
                elif first_max is None:
                    first_max = number
                    break
            number = round(number - delta, number_decimals)

        assert first_min != None and second_max != None, 'Error obteniendo los valores.'

        number = (second_max+first_min)//2
        while number > min_value:
            if Fn(number):
                middle_value = number
                break
            number = round(number - delta, number_decimals)

        invalid_min = round(first_min - delta, number_decimals)
        invalid_max = round(second_max + delta, number_decimals)

        signal.alarm(0)

        return {
                'valor_minimo_invalido': invalid_min,
                'primer_valor_minimo': first_min, 
                'segundo_valor_minimo': second_min, 
                'valor_medio': middle_value, 
                'primer_valor_maximo': first_max, 
                'segundo_valor_maximo': second_max,
                'valor_maximo_invalido': invalid_max
            }


