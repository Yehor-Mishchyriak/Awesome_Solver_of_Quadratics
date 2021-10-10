# Kivy imports
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.screen import MDScreen
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRoundFlatButton, MDFillRoundFlatButton
# Other libraries imports
from sympy.printing.pretty.stringpict import stringPict
from sympy import pretty, symbols, init_printing
from sympy import sqrt as pretty_sqrt
from functools import reduce
from math import sqrt, gcd
# Initializing of sp
init_printing()
x = symbols('x')
d = symbols('D')
# Defining math functions
# This function distinguishes the type of an equation and derives coefficients from it


def coefficients_sort_of_equation(equation):
    a = []  # boxes
    b = []  # for coefficients

    # data input
    quadratic_equation = equation

    # data preparation
    quadratic_equation = quadratic_equation.lower()
    split_equation = list(quadratic_equation)
    while ' ' in split_equation:
        split_equation.remove(' ')
    # getting position of the second power in an equation
    try:
        if split_equation[-1] != '0':
            split_equation = 'ERROR'
        split_equation.remove('=')
        del split_equation[-1]
        # extracting coefficients
        # extracting 'a' coefficient:
        power2pos = split_equation.index('²')
        counter = power2pos
        for symbol in split_equation:
            if symbol.isalpha():
                variable = symbol
                break
        for i in split_equation[power2pos::-1]:
            a.append(i)
            counter = counter - 1
            if i == '+' or i == '-':
                break
        del split_equation[counter + 1:power2pos + 1]
        a.remove('²')
        a.remove(variable)

        if any(map(str.isdigit, a)):
            a.reverse()
            a_coeff = float(''.join(a))
        else:
            if '-' in a:
                a_coeff = -1.0
            else:
                a_coeff = 1.0
        # trying to identify the equation type:
        if not bool(split_equation):  # then it is type: "ax²=0"
            return ('ax²=0', a_coeff), variable

        if variable not in split_equation:  # then it is type: "ax²+c=0"
            return ('ax²+c=0', a_coeff, float(''.join(split_equation))), variable   # <=== 'c' coefficient

        # if 'x' in split_equation:     # then it is either type  "ax²+bx+c=0" or "ax²+bx=0"
        # extracting 'b' coefficient
        varpos = split_equation.index(variable)
        counter2 = varpos
        for i in split_equation[varpos::-1]:
            b.append(i)
            counter2 = counter2 - 1
            if i == '+' or i == '-':
                break
        del split_equation[counter2 + 1:varpos + 1]
        b.remove(variable)
        if any(map(str.isdigit, b)):
            b.reverse()
            b_coeff = float(''.join(b))
        else:
            if '-' in b:
                b_coeff = -1.0
            else:
                b_coeff = 1.0

        if not bool(split_equation):  # then it is type "ax²+bx=0"
            return ('ax²+bx=0', a_coeff, b_coeff), variable
        # if neither from aforementioned conditions occurred then it is type "ax²+bx+c=0"
        return ('ax²+bx+c=0', a_coeff, b_coeff, float(''.join(split_equation))), variable   # <=== 'c' coefficient

    except:
        return 'ERROR'


# This function turns coefficient whose type is float to str,
# BUT it is used to write coefficients in between other symbols.
# Moreover, instead of writing "...+1x" it'll write "...+x", thereby making it somewhat prettier.
# The idea is that it also adds "+" to the coeff, not "-", as "-" is automatically written in front of negative numbers.
def middle_mystr(coeff):
    if coeff == -1.0:
        return '-'
    elif coeff == 1.0:
        return '+'
    elif coeff > 0:
        return '+' + str(coeff)
    else:
        return str(coeff)


# This function turns coefficient whose type is float to str,
# BUT it is used to write coefficients at the beginning of an equation.
def beginning_mystr(coeff):
    if coeff == -1.0:
        return '-'
    elif coeff == 1.0:
        return ''
    else:
        return str(coeff)


# The same as "gcd", but works for 3 numbers
def nod(a, b, c=None):
    return ((a if b == 0 else nod(b, a % b)) if c is None
            else nod(nod(a, b), nod(a, c)))


# this two functions generate 'pretty' root output
def primfacs(n):
    i = 2
    primfac = []
    while i * i <= n:
        while n % i == 0:
            primfac.append(i)
            n = n / i
        i = i + 1
    if n > 1:
        primfac.append(n)
    return primfac


def nice_root(num):
    list_of_dividers = primfacs(num)
    outside_the_root = []
    for i in list_of_dividers:
        how_many_same_items = list_of_dividers.count(i)
        if how_many_same_items % 2 == 0:
            while i in list_of_dividers:
                outside_the_root.append(i)
                list_of_dividers.remove(i)
        else:
            while how_many_same_items != 1:
                outside_the_root.append(i)
                list_of_dividers.remove(i)
                how_many_same_items -= 1
    if bool(list_of_dividers):
        whole_part_inside_the_root = reduce(lambda x, y: x * y, list_of_dividers)
    else:
        whole_part_inside_the_root = 1
    if bool(outside_the_root):
        whole_part_outside_the_root = sqrt(reduce(lambda x, y: x * y, outside_the_root))
    else:
        whole_part_outside_the_root = 1
    return [whole_part_outside_the_root, whole_part_inside_the_root]


# This func generates nice fractions
def nice_dividing(number, divider):
    if str(number)[str(number).index('.') + 1] == '0':
        number = int(number)
    if str(divider)[str(divider).index('.') + 1] == '0':
        divider = int(divider)
    if isinstance(number, float) and isinstance(divider, float):
        symb_len_num = len(str(number)[str(number).index('.')::]) - 1
        symb_len_div = len(str(divider)[str(divider).index('.')::]) - 1
        if symb_len_num > symb_len_div:
            number = int(number * 10 ** symb_len_num)
            divider = int(divider * 10 ** symb_len_num)
        else:
            number = int(number * 10 ** symb_len_div)
            divider = int(divider * 10 ** symb_len_div)
    elif isinstance(number, float):
        symb_len_num = len(str(number)[str(number).index('.')::]) - 1
        number = int(number * 10 ** symb_len_num)
        divider = int(divider * 10 ** symb_len_num)
    elif isinstance(divider, float):
        symb_len_div = len(str(divider)[str(divider).index('.')::]) - 1
        number = int(number * 10 ** symb_len_div)
        divider = int(divider * 10 ** symb_len_div)
    if number < 0:
        number = ['-', abs(number)]
    else:
        number = ['', abs(number)]

    if divider < 0:
        divider = ['-', abs(divider)]
    else:
        divider = ['', abs(divider)]
    if number[1] < divider[1]:
        # 0 - whole-part; 1 - numerator; 2 - denominator
        if number[0] == '-' and divider[0] == '-':
            return ['', number[1] / gcd(number[1], divider[1]), divider[1] / gcd(number[1], divider[1])]
        elif all([number[0] == '-', divider[0] == '']) or all([number[0] == '', divider[0] == '-']):
            return ['-', number[1] / gcd(number[1], divider[1]), divider[1] / gcd(number[1], divider[1])]
        else:
            return ['', number[1] / gcd(number[1], divider[1]), divider[1] / gcd(number[1], divider[1])]
    else:
        fractional_part = number[1] - (divider[1] * (number[1] // divider[1]))
        # 0 - whole-part; 1 - numerator; 2 - denominator
        if number[0] == '-' and divider[0] == '-':
            return [number[1] // divider[1], fractional_part / gcd(fractional_part, divider[1]),
                    divider[1] / gcd(fractional_part, divider[1])]
        elif all([number[0] == '-', divider[0] == '']) or all([number[0] == '', divider[0] == '-']):
            return [-(number[1] // divider[1]), fractional_part / gcd(fractional_part, divider[1]),
                    divider[1] / gcd(fractional_part, divider[1])]
        else:
            return [number[1] // divider[1], fractional_part / gcd(fractional_part, divider[1]),
                    divider[1] / gcd(fractional_part, divider[1])]


# It helps write fractions
def fraction_writer(prior_thing, split_frac, prior_thing_position=1):
    internal_split_frac = list(map(str, split_frac[::]))  # the of split fraction is whole-part, numerator, denominator
    expression = stringPict(prior_thing + internal_split_frac[0]).right(' ', stringPict(
        stringPict(internal_split_frac[1]).below(stringPict.LINE, internal_split_frac[2])[0], prior_thing_position))[0]
    return expression.replace('─', '―')


def operations_with_fractions(fraction1, operator, fraction2):
    return stringPict(stringPict(' ' + operator, -1).right(fraction2)[0]).left(fraction1)[0]


# It helps extract a root from a fraction
def root_writer(split_root, prior_thing=''):
    internal_split_root = split_root[::]  # the of split fraction is outside-part, inside-part of the root
    if internal_split_root[1] == 1.0:
        return str(internal_split_root[0])
    if internal_split_root[0] == 1:
        internal_split_root[0] = ''
    return stringPict(prior_thing + str(internal_split_root[0])).right('', stringPict(
        str(pretty(pretty_sqrt((internal_split_root[1]), evaluate=False), use_unicode=False)), 1))[0]


def check_int(expression):
    if len(str(expression)[str(expression).index('.')::]) == 2 and str(expression)[
        str(expression).index('.') + 1] == '0':
        return True
    else:
        return False


def check_float(expression):
    if len(str(expression)[str(expression).index('.')::]) == 2 and str(expression)[
        str(expression).index('.') + 1] == '0':
        return False
    else:
        return True


def make_it_int(sequence):
    # sequence - [STRING, FLOAT, FLOAT, ..., FLOAT]
    list_of_powers = []
    for coeff in sequence[1::]:
        list_of_powers.append(len(str(coeff)[str(coeff).index('.')::]) - 1)
    list_to_return = list(map(lambda i: i * 10 ** max(list_of_powers), sequence[1::]))
    list_to_return.insert(0, sequence[0])
    return [list_to_return, str(10 ** max(list_of_powers))]


def awesome_print(position, content):

    ''' Position - <float>,
        n.x : n - column
              x - row
        Content - <str>
    '''

    column = int(str(position).split('.')[0])
    row = int(str(position).split('.')[1])
    content_to_return = '\n' * column + ' ' * row + content
    return content_to_return

# ------------------------------------------------------------------


LabelBase.register(name='Youth Touch',
                   fn_regular='YouthTouchDemoRegular-4VwY.ttf')

LabelBase.register(name='Consolas',
                   fn_regular='consola.ttf')

LabelBase.register(name='IBM Plex Sans',
                   fn_regular='IBMPlexSans-MediumItalic.ttf')

LabelBase.register(name='Freestyle Script',
                   fn_regular='freestyle-script-normal.ttf')


# ------------------------------------------------------------------

class HomeScreen(MDScreen):
    pass


class SolvingScreen(MDScreen):

    def on_kv_post(self, base_widget):
        # Initialization
        self.data_input = self.ids.input_equation
        self.data_output = self.ids.solution_output

    def solve(self):
        global current_language, state_of_the_output
        self.solution = '<SOLUTION>'
        self.data_output.text = ''
        equation = self.data_input.text
        equation = equation.replace(' ', '')
        equation = equation.lower()
        gathered_data_all = coefficients_sort_of_equation(equation)
        gathered_data_coefficients = gathered_data_all[0]
        variable = gathered_data_all[1]
        # if entered data is incorrect:
        if gathered_data_all == 'ERROR':
            state_of_the_output = '<ERROR>'
            if current_language == 'English':
                self.solution = awesome_print(0.0, 'Oops, idk how to solve that :(')
            else:
                self.solution = awesome_print(0.0, 'Упс, я хз как это решать :(')
        else:
            state_of_the_output = '<SOLUTION>'
        # solution for "ax²=0": <<type-0, a-1>>
        if gathered_data_coefficients[0] == 'ax²=0':
            if gathered_data_coefficients[1] == 0:
                self.solution = awesome_print(0.0, '1) ' + equation)
                self.solution += awesome_print(2.0, '2) ' + variable + ' = R')
            else:
                self.solution = awesome_print(0.0, '1) ' + equation)
                self.solution += awesome_print(2.0, '2) ' + variable + ' = 0')
        # solution for "ax²+c=0": <<type-0, a-1, c-2>>
        elif gathered_data_coefficients[0] == 'ax²+c=0':
            if -gathered_data_coefficients[2] / gathered_data_coefficients[1] < 0:
                self.solution = awesome_print(0.0, '1) ' + equation)
                self.solution += awesome_print(2.0, '2) ' + beginning_mystr(gathered_data_coefficients[1]) + variable + '² = ' + str(gathered_data_coefficients[2] * -1))
                self.solution += awesome_print(2.0, '3) ' + variable + ' Є {}')
            else:
                self.solution = awesome_print(0.0, '1) ' + equation)
                self.solution += awesome_print(2.0, '2) ' + beginning_mystr(gathered_data_coefficients[1]) + variable + '² = ' + str(gathered_data_coefficients[2] * -1))
                self.solution += awesome_print(2.0, fraction_writer('3) ' + variable + '² = ', ['', -gathered_data_coefficients[2], gathered_data_coefficients[1]]))
                if check_int(gathered_data_coefficients[2] / gathered_data_coefficients[1]):
                    self.solution += awesome_print(2.0, '4) ' + variable + '² = ' + str(-gathered_data_coefficients[2] / gathered_data_coefficients[1]))
                    if -gathered_data_coefficients[2] / gathered_data_coefficients[1] == 1.0:
                        self.solution += awesome_print(2.0, '5) ' + variable + ' = ±1.0')
                        self.data_output.text = self.solution
                        return None
                    self.solution += awesome_print(2.0, root_writer([1, (-gathered_data_coefficients[2] / gathered_data_coefficients[1])], prior_thing='5) ' + variable + ' = ±'))
                    if len(str(sqrt(-gathered_data_coefficients[2] / gathered_data_coefficients[1]))[
                           str(sqrt(-gathered_data_coefficients[2] / gathered_data_coefficients[1])).index('.')::]) > 3 and -gathered_data_coefficients[2] / \
                            gathered_data_coefficients[1] != nice_root(-gathered_data_coefficients[2] / gathered_data_coefficients[1])[1]:

                        self.solution += awesome_print(2.0, root_writer(nice_root(-gathered_data_coefficients[2] / gathered_data_coefficients[1]), prior_thing='6) ' + variable + ' = ±'))

                        if current_language == 'Russian':  # - Russian
                            self.solution += awesome_print(2.0, 'Альтернативный ответ:')
                            self.solution += awesome_print(2.0, variable + ' = ±' + str(sqrt(-gathered_data_coefficients[2] / gathered_data_coefficients[1])))
                        else:   # - English
                            self.solution += awesome_print(2.0, 'Alternative answer:')
                            self.solution += awesome_print(2.0, variable + ' = ±' + str(sqrt(-gathered_data_coefficients[2] / gathered_data_coefficients[1])))

                    elif len(str(sqrt(-gathered_data_coefficients[2] / gathered_data_coefficients[1]))[
                             str(sqrt(-gathered_data_coefficients[2] / gathered_data_coefficients[1])).index('.')::]) < 3:
                        self.solution += awesome_print(2.0, '6) ' + variable + ' = ±' + str(sqrt(-gathered_data_coefficients[2] / gathered_data_coefficients[1])))

                    else:

                        if current_language == 'Russian':  # - Russian
                            self.solution += awesome_print(2.0, 'Альтернативный ответ:')
                            self.solution += awesome_print(2.0, variable + ' = ±' + str(sqrt(-gathered_data_coefficients[2] / gathered_data_coefficients[1])))
                        else:  # - English
                            self.solution += awesome_print(2.0, 'Alternative answer:')
                            self.solution += awesome_print(2.0, variable + ' = ±' + str(sqrt(-gathered_data_coefficients[2] / gathered_data_coefficients[1])))

                else:
                    if gathered_data_coefficients[1] < 0:
                        split_fraction = nice_dividing(gathered_data_coefficients[2], -gathered_data_coefficients[1])
                    else:
                        split_fraction = nice_dividing(-gathered_data_coefficients[2], gathered_data_coefficients[1])
                    self.solution += awesome_print(2.0, fraction_writer('4) ' + variable + '² = ', split_fraction))
                    try:
                        numerator = split_fraction[0] * split_fraction[2] + split_fraction[1]
                    except TypeError:
                        numerator = split_fraction[1]
                    # Here is quick solution of a bug, it's not pretty, but I'm tired and will leave it like this

                    if '/' in str(root_writer(nice_root(numerator))):
                        position = 2
                    else:
                        position = 1

                    # This is it
                    self.solution += awesome_print(2.0, fraction_writer('5) ' + variable + ' = ±', ['', root_writer([1.0, numerator]),
                                                            root_writer([1.0, split_fraction[2]])],
                                               prior_thing_position=2))
                    denominator = nice_root(split_fraction[2])
                    numerator = nice_root(numerator)
                    if denominator[0] == '':
                        denominator[0] = 1
                    if numerator[0] == '':
                        numerator[0] = 1
                    new_numerator = nice_root(numerator[1] * denominator[1])
                    denominator = denominator[0] * denominator[1]
                    numerator[0] = numerator[0] * new_numerator[0]
                    numerator[1] = new_numerator[1]
                    copy_of_the_numerator = numerator[::]
                    self.solution += awesome_print(2.0, fraction_writer('6) ' + variable + ' = ±', ['', root_writer(numerator), denominator],
                                           prior_thing_position=position))
                    nod_of_num_and_den = gcd(int(numerator[0]), int(denominator))
                    numerator[0] = numerator[0] / nod_of_num_and_den
                    denominator = denominator / nod_of_num_and_den
                    if copy_of_the_numerator[0] != numerator[0] or copy_of_the_numerator[1] != numerator[1]:
                        if denominator == 1:
                            self.solution += awesome_print(2.0, root_writer(numerator, prior_thing='7) ' + variable + ' = ±'))

                            if current_language == 'Russian':  # - Russian
                                self.solution += awesome_print(2.0, 'Альтернативный ответ:')
                                self.solution += awesome_print(2.0, variable + ' = ±' + str(sqrt(-gathered_data_coefficients[2] / gathered_data_coefficients[1])))
                            else:  # - English
                                self.solution += awesome_print(2.0, 'Alternative answer:')
                                self.solution += awesome_print(2.0, variable + ' = ±' + str(sqrt(-gathered_data_coefficients[2] / gathered_data_coefficients[1])))
                        else:
                            self.solution += awesome_print(2.0, fraction_writer('7) ' + variable + ' = ±', ['', root_writer(numerator), denominator],prior_thing_position=2))

                            if current_language == 'Russian':  # - Russian
                                self.solution += awesome_print(2.0, 'Альтернативный ответ:')
                                self.solution += awesome_print(2.0, variable + ' = ±' + str(sqrt(-gathered_data_coefficients[2] / gathered_data_coefficients[1])))
                            else:  # - English
                                self.solution += awesome_print(2.0, 'Alternative answer:')
                                self.solution += awesome_print(2.0, variable + ' = ±' + str(sqrt(-gathered_data_coefficients[2] / gathered_data_coefficients[1])))
                    else:
                        if current_language == 'Russian':  # - Russian
                            self.solution += awesome_print(2.0, 'Альтернативный ответ:')
                            self.solution += awesome_print(2.0, variable + ' = ±' + str(sqrt(-gathered_data_coefficients[2] / gathered_data_coefficients[1])))
                        else:  # - English
                            self.solution += awesome_print(2.0, 'Alternative answer:')
                            self.solution += awesome_print(2.0, variable + ' = ±' + str(sqrt(-gathered_data_coefficients[2] / gathered_data_coefficients[1])))

        # solution for "ax²+bx=0": <<type-0, a-1, b-2>>
        elif gathered_data_coefficients[0] == 'ax²+bx=0':
            self.solution = awesome_print(0.0, '1) ' + equation)
            self.solution += awesome_print(2.0, '2) ' + variable + ' * (' + beginning_mystr(gathered_data_coefficients[1]) + variable + middle_mystr(
                gathered_data_coefficients[2]) + ') = 0')
            self.solution += awesome_print(2.0, '3) ' + variable + '₁ = 0; ' + beginning_mystr(gathered_data_coefficients[1]) + variable + middle_mystr(gathered_data_coefficients[2]) + ' = 0')
            self.solution += awesome_print(2.0, '4) ' + beginning_mystr(gathered_data_coefficients[1]) + variable + ' = ' + str(-gathered_data_coefficients[2]))
            self.solution += awesome_print(2.0, fraction_writer('5) ' + variable + '₂ = ', ['', -gathered_data_coefficients[2], gathered_data_coefficients[1]]))
            if check_int(gathered_data_coefficients[2] / gathered_data_coefficients[1]):
                self.solution += awesome_print(2.0, '6) ' + variable + '₂ = ' + str(-gathered_data_coefficients[2] / gathered_data_coefficients[1]))
            else:
                if abs(nice_dividing(-gathered_data_coefficients[2], gathered_data_coefficients[1])[1]) != abs(-gathered_data_coefficients[2]):
                    self.solution += awesome_print(2.0, fraction_writer('6) ' + variable + '₂ = ', nice_dividing(-gathered_data_coefficients[2], gathered_data_coefficients[1])))

                if current_language == 'Russian':  # - Russian
                    self.solution += awesome_print(2.0, 'Альтернативный ответ:')
                    self.solution += awesome_print(2.0, variable + '₂ = ' + str(-gathered_data_coefficients[2] / gathered_data_coefficients[1]))
                else:   # - English
                    self.solution += awesome_print(2.0, 'Alternative answer:')
                    self.solution += awesome_print(2.0, variable + '₂ = ' + str(-gathered_data_coefficients[2] / gathered_data_coefficients[1]))

        # solution for "ax²+bx+c=0": <<type-0, a-1, b-2, c-3>>
        elif gathered_data_coefficients[0] == 'ax²+bx+c=0':
            discriminant = gathered_data_coefficients[2] ** 2 - 4 * gathered_data_coefficients[1] * gathered_data_coefficients[3]

            if discriminant < 0:
                self.solution = awesome_print(0.0, '1) ' + equation)
                self.solution += awesome_print(2.0, '2) D = b² - 4 * a * c')
                self.solution += awesome_print(2.0, '3) D = ' + str(gathered_data_coefficients[2]) + '² - 4 * ' + str(gathered_data_coefficients[1]) + ' * ' + str(gathered_data_coefficients[3]) + ' < 0;')
                self.solution += awesome_print(2.0, '4) ==> ' + variable + ' Є {}')

            elif discriminant == 0:
                self.solution = awesome_print(0.0, '1) ' + equation)
                self.solution += awesome_print(2.0, '2) D = b² - 4 * a * c')
                self.solution += awesome_print(2.0, '3) D = ' + str(gathered_data_coefficients[2]) + '² - 4 * ' + str(gathered_data_coefficients[1]) + ' * ' + str(gathered_data_coefficients[3]) + ' = 0;')
                self.solution += awesome_print(2.0, fraction_writer('4) ==> ' + variable + ' = ', ['', '-b', '2 * a']))
                # Here's a small bug
                self.solution += awesome_print(2.0, fraction_writer('5) ' + variable + ' = ', ['', -gathered_data_coefficients[2], 2 * gathered_data_coefficients[1]]))
                if check_int(-gathered_data_coefficients[2] / (2 * gathered_data_coefficients[1])):
                    self.solution += awesome_print(2.0, '6) ' + variable + ' = ' + str(-gathered_data_coefficients[2] / (2 * gathered_data_coefficients[1])))
                else:
                    self.solution += awesome_print(2.0, fraction_writer('6) ' + variable + ' = ', nice_dividing(-gathered_data_coefficients[2], 2 * gathered_data_coefficients[1])))

                    if current_language == 'Russian':  # - Russian
                        self.solution += awesome_print(2.0, 'Альтернативный ответ:')
                        self.solution += awesome_print(2.0, variable + ' = ' + str(-gathered_data_coefficients[2] / (2 * gathered_data_coefficients[1])))
                    else:  # - English
                        self.solution += awesome_print(2.0, 'Alternative answer:')
                        self.solution += awesome_print(2.0, variable + ' = ' + str(-gathered_data_coefficients[2] / (2 * gathered_data_coefficients[1])))

            else:
                if all([gathered_data_coefficients[1] == 1.0, check_int(sqrt(discriminant))]):
                    self.solution = awesome_print(0.0, '1) ' + equation)
                    self.solution += awesome_print(2.0, '2) ' + variable + '₁ + ' + variable + '₂ = -b;' + variable + '₁ * ' + variable + '₂ = c. ==>')
                    self.solution += awesome_print(2.0, '3) ' + variable + '₁ + ' + variable + '₂ = ' + str(-gathered_data_coefficients[2]) + '; ' + variable + '₁ * ' + variable + '₂ = ' + str(gathered_data_coefficients[3]))
                    self.solution += awesome_print(2.0, '4) ' + variable + '₁ = ' + str((-gathered_data_coefficients[2] - sqrt(discriminant)) / (2 * gathered_data_coefficients[1])) + '; ' + variable + '₂ = ' + str((-gathered_data_coefficients[2] + sqrt(discriminant)) / (2 * gathered_data_coefficients[1])))
                elif gathered_data_coefficients[1] != 1.0 or all(
                        [gathered_data_coefficients[1] == 1, len(str(sqrt(discriminant))[str(sqrt(discriminant)).index('.')::]) != 2]):
                    gcd_of_3_nums = abs(nod(gathered_data_coefficients[1], gathered_data_coefficients[2], gathered_data_coefficients[3]))
                    if all([gathered_data_coefficients[1] / gcd_of_3_nums == 1.0, check_int(sqrt(discriminant))]):
                        A, B, C = gathered_data_coefficients[1] / gcd_of_3_nums, gathered_data_coefficients[2] / gcd_of_3_nums, gathered_data_coefficients[
                            3] / gcd_of_3_nums
                        self.solution = awesome_print(0.0, '1) ' + equation)
                        self.solution += awesome_print(2.0, '2) ' + variable + '² ' + middle_mystr(B) + variable + ' ' + middle_mystr(C) + ' = 0')
                        self.solution += awesome_print(2.0, '3) ' + variable + '₁ + ' + variable + '₂ = -b; ' + variable + '₁ * ' + variable + '₂ = c. ==>')
                        self.solution += awesome_print(2.0, '4) ' + variable + '₁ + ' + variable + '₂ = ' + str(-B) + '; ' + variable + '₁ * ' + variable + '₂ = ' + str(C))
                        self.solution += awesome_print(2.0, '5) ' + variable + '₁ =' + str((-gathered_data_coefficients[2] - sqrt(discriminant)) / (2 * gathered_data_coefficients[1])) + '; ' + variable + '₂ = ' + str((-gathered_data_coefficients[2] + sqrt(discriminant)) / (2 * gathered_data_coefficients[1])))
                    elif abs(gathered_data_coefficients[2]) >= 8 and gathered_data_coefficients[2] % 2 == 0:
                        if any(map(check_float, gathered_data_coefficients[1::])):
                            multiplier = make_it_int(gathered_data_coefficients)[1]
                            gathered_data_coefficients = make_it_int(gathered_data_coefficients)[0]
                            self.solution = awesome_print(0.0, '1) ' + equation)
                            self.solution += awesome_print(2.0, '1.2) ' + equation + ' | * ' + multiplier)
                            self.solution += awesome_print(2.0, '1.3) ' + beginning_mystr(gathered_data_coefficients[1]) + variable + '²' + middle_mystr(gathered_data_coefficients[2]) + variable + middle_mystr(gathered_data_coefficients[3]) + '=0')

                        else:
                            self.solution = awesome_print(0.0, '1) ' + equation)

                        discriminant_divide_4 = ((gathered_data_coefficients[2] / 2) ** 2) - gathered_data_coefficients[1] * gathered_data_coefficients[3]
                        self.solution += awesome_print(2.0, stringPict(' - a * c', -1).left(stringPict(operations_with_fractions(fraction_writer('2) ', ['', 'D', '4']), '=',fraction_writer('', ['', 'b²', '4']))))[0])
                        # =====================
                        if gathered_data_coefficients[1] < 0:
                            self.solution += awesome_print(2.0, stringPict(' + ' + str(-gathered_data_coefficients[1]) + ' * ' + str(gathered_data_coefficients[3]),-1).left(stringPict(operations_with_fractions(fraction_writer('3) ', ['', 'D', '4']), '=',fraction_writer('',['', str(gathered_data_coefficients[2]) + '²','4']))))[0])
                        else:
                            self.solution += awesome_print(2.0, stringPict(' ' + str(-gathered_data_coefficients[1]) + ' * ' + str(gathered_data_coefficients[3]), -1).left(stringPict(operations_with_fractions(fraction_writer('3) ', ['', 'D', '4']), '=', fraction_writer('', ['', str(gathered_data_coefficients[2]) + '²', '4']))))[0])
                        # =====================
                        self.solution += awesome_print(2.0, stringPict(' = ' + str(discriminant_divide_4), -1).left(fraction_writer('4) ', ['', 'D', '4']))[0])
                        x_through_d_formula = stringPict(stringPict(' ±', -2).right(pretty(pretty_sqrt((d / 4), evaluate=False), use_unicode=False))[0],1).left(fraction_writer('', ['', '-b', '2']))[0]
                        formula = fraction_writer('', ['', x_through_d_formula, 'a'])
                        self.solution += awesome_print(2.0, stringPict('5) ' + variable + ' = ', -4).right(formula)[0])
                        x_through_d_formula = stringPict(stringPict(' ±', -2).right(fraction_writer('', ['', pretty(pretty_sqrt((discriminant_divide_4), evaluate=False), use_unicode=False), '1']))[0],1).left(fraction_writer('', ['', str(-gathered_data_coefficients[2]), '2']))[0]
                        formula = fraction_writer('', ['', x_through_d_formula, str(gathered_data_coefficients[1])])
                        self.solution += awesome_print(2.0, stringPict('6) ' + variable + ' = ', -4).right(formula)[0])
                        if check_int(sqrt(discriminant_divide_4)):
                            self.solution += awesome_print(2.0, fraction_writer('7) ' + variable + '₁ = ', ['', str(-gathered_data_coefficients[2] / 2) + ' + ' + str(sqrt(discriminant_divide_4)), str(gathered_data_coefficients[1])]))
                            self.solution += awesome_print(2.0, fraction_writer('   ' + variable + '₂ = ', ['', str(-gathered_data_coefficients[2] / 2) + ' - ' + str(sqrt(discriminant_divide_4)), str(gathered_data_coefficients[1])]))
                            # =========================================================================
                            # if both X's are integer
                            if check_int((-gathered_data_coefficients[2] / 2 + sqrt(discriminant_divide_4)) / gathered_data_coefficients[1]) and check_int((-gathered_data_coefficients[2] / 2 - sqrt(discriminant_divide_4)) / gathered_data_coefficients[1]):
                                self.solution += awesome_print(2.0, '8) ' + variable + '₁ = ' + str((-gathered_data_coefficients[2] / 2 + sqrt(discriminant_divide_4)) / gathered_data_coefficients[1]) + '; ' + variable + '₂ = ' + str((-gathered_data_coefficients[2] / 2 - sqrt(discriminant_divide_4)) / gathered_data_coefficients[1]))
                            # both or one of them aren't integer(s)
                            else:
                                # if the first is integer
                                if check_int((-gathered_data_coefficients[2] / 2 + sqrt(discriminant_divide_4)) / gathered_data_coefficients[1]):
                                    self.solution += awesome_print(2.0, '8) ' + variable + '₁ = ' + str((-gathered_data_coefficients[2] / 2 + sqrt(discriminant_divide_4)) / gathered_data_coefficients[1]))
                                    self.solution += awesome_print(2.0, fraction_writer('   ' + variable + '₂ = ', nice_dividing(-gathered_data_coefficients[2] / 2.0 - sqrt(discriminant_divide_4), gathered_data_coefficients[1])))
                                    if current_language == 'Russian':  # - Russian
                                        self.solution += awesome_print(2.0, 'Альтернативный ответ:')
                                        self.solution += awesome_print(2.0,  variable + '₂ = ' + str((-gathered_data_coefficients[2] / 2 - sqrt(discriminant_divide_4)) / gathered_data_coefficients[1]))
                                    else:   # English
                                        self.solution += awesome_print(2.0, 'Alternative answer:')
                                        self.solution += awesome_print(2.0, variable + '₂ = ' + str((-gathered_data_coefficients[2] / 2 - sqrt(discriminant_divide_4)) / gathered_data_coefficients[1]))
                                # if the second is integer
                                elif check_int((-gathered_data_coefficients[2] / 2 - sqrt(discriminant_divide_4)) / gathered_data_coefficients[1]):
                                    self.solution += awesome_print(2.0, fraction_writer('8) ' + variable + '₁ = ', nice_dividing(-gathered_data_coefficients[2] / 2.0 + sqrt(discriminant_divide_4), gathered_data_coefficients[1])))
                                    self.solution += awesome_print(2.0, '   ' + variable + '₂ = ' + str((-gathered_data_coefficients[2] / 2 - sqrt(discriminant_divide_4)) / gathered_data_coefficients[1]))
                                    if current_language == 'Russian':  # - Russian
                                        self.solution += awesome_print(2.0, 'Альтернативный ответ:')
                                        self.solution += awesome_print(2.0,  variable + '₁ = ' + str((-gathered_data_coefficients[2] / 2 + sqrt(discriminant_divide_4)) / gathered_data_coefficients[1]))
                                    else:   # English
                                        self.solution += awesome_print(2.0, 'Alternative answer:')
                                        self.solution += awesome_print(2.0, variable + '₁ = ' + str((-gathered_data_coefficients[2] / 2 + sqrt(discriminant_divide_4)) / gathered_data_coefficients[1]))
                                # if both are integers
                                else:
                                    self.solution += awesome_print(2.0, fraction_writer('8) ' + variable + '₁ = ', nice_dividing(-gathered_data_coefficients[2] / 2.0 + sqrt(discriminant_divide_4), gathered_data_coefficients[1])))
                                    self.solution += awesome_print(2.0, fraction_writer('   ' + variable + '₂ = ', nice_dividing(-gathered_data_coefficients[2] / 2.0 - sqrt(discriminant_divide_4), gathered_data_coefficients[1])))
                                    if current_language == 'Russian':  # - Russian
                                        self.solution += awesome_print(2.0, 'Альтернативный ответ:')
                                        self.solution += awesome_print(2.0, variable + '₁ = ' + str((-gathered_data_coefficients[2] / 2 + sqrt(discriminant_divide_4)) / gathered_data_coefficients[1]))
                                        self.solution += awesome_print(2.0, variable + '₂ = ' + str((-gathered_data_coefficients[2] / 2 - sqrt(discriminant_divide_4)) / gathered_data_coefficients[1]))
                                    else:   # English
                                        self.solution += awesome_print(2.0, 'Alternative answer:')
                                        self.solution += awesome_print(2.0, variable + '₁ = ' + str((-gathered_data_coefficients[2] / 2 + sqrt(discriminant_divide_4)) / gathered_data_coefficients[1]))
                                        self.solution += awesome_print(2.0, variable + '₂ = ' + str((-gathered_data_coefficients[2] / 2 - sqrt(discriminant_divide_4)) / gathered_data_coefficients[1]))
                            # =========================================================================
                        else:
                            if gathered_data_coefficients[1] == 1.0:
                                self.solution += awesome_print(2.0, root_writer(nice_root(discriminant_divide_4), prior_thing='7) ' + variable + ' = ' + str(-gathered_data_coefficients[2] / 2) + ' ± '))
                                self.solution += awesome_print(2.0, root_writer(nice_root(discriminant_divide_4), prior_thing='8) ' + variable + '₁ = ' + str(-gathered_data_coefficients[2] / 2) + ' + '))
                                self.solution += awesome_print(2.0, root_writer(nice_root(discriminant_divide_4), prior_thing='   ' + variable + '₂ = ' + str(-gathered_data_coefficients[2] / 2) + ' - '))
                            else:
                                self.solution += awesome_print(2.0, fraction_writer('7) ' + variable + ' = ', ['', stringPict(str(-gathered_data_coefficients[2] / 2) + ' ± ', -1).right(root_writer(nice_root(discriminant_divide_4)))[0], str(gathered_data_coefficients[1])]))
                                self.solution += awesome_print(2.0, fraction_writer('8) ' + variable + '₁ = ', ['', stringPict(str(-gathered_data_coefficients[2] / 2) + ' + ', -1).right(root_writer(nice_root(discriminant_divide_4)))[0], str(gathered_data_coefficients[1])]))
                                self.solution += awesome_print(2.0, fraction_writer('   ' + variable + '₂ = ', ['', stringPict(str(-gathered_data_coefficients[2] / 2) + ' - ', -1).right(root_writer(nice_root(discriminant_divide_4)))[0], str(gathered_data_coefficients[1])]))
                            if current_language == 'Russian':  # - Russian
                                self.solution += awesome_print(2.0, 'Альтернативный ответ:')
                                self.solution += awesome_print(2.0, variable + '₁ = ' + str((-gathered_data_coefficients[2] / 2 + sqrt(discriminant_divide_4)) / gathered_data_coefficients[1]))
                                self.solution += awesome_print(2.0, variable + '₂ = ' + str((-gathered_data_coefficients[2] / 2 - sqrt(discriminant_divide_4)) / gathered_data_coefficients[1]))
                            else:   # - English
                                self.solution += awesome_print(2.0, 'Alternative answer:')
                                self.solution += awesome_print(2.0, variable + '₁ = ' + str((-gathered_data_coefficients[2] / 2 + sqrt(discriminant_divide_4)) / gathered_data_coefficients[1]))
                                self.solution += awesome_print(2.0, variable + '₂ = ' + str((-gathered_data_coefficients[2] / 2 - sqrt(discriminant_divide_4)) / gathered_data_coefficients[1]))

                    else:

                        if any(map(check_float, gathered_data_coefficients[1::])):
                            multiplier = make_it_int(gathered_data_coefficients)[1]
                            gathered_data_coefficients = make_it_int(gathered_data_coefficients)[0]
                            self.solution = awesome_print(0.0, '1) ' + equation)
                            self.solution += awesome_print(2.0, '1.2) ' + equation + ' | * ' + multiplier)
                            self.solution += awesome_print(2.0, '1.3) ' + beginning_mystr(gathered_data_coefficients[1]) + variable + '²' + middle_mystr(gathered_data_coefficients[2]) + variable + middle_mystr(gathered_data_coefficients[3]) + '=0')

                        else:
                            self.solution = awesome_print(0.0, '1) ' + equation)

                        discriminant = gathered_data_coefficients[2] ** 2 - 4 * gathered_data_coefficients[1] * gathered_data_coefficients[3]
                        self.solution += awesome_print(2.0, '2) D = b² - 4 * a * c')
                        self.solution += awesome_print(2.0, '3) D = ' + str(gathered_data_coefficients[2]) + '² - 4 * ' + str(gathered_data_coefficients[1]) + ' * ' + str(gathered_data_coefficients[3]))
                        self.solution += awesome_print(2.0, '4) D = ' + str(discriminant))
                        self.solution += awesome_print(2.0, fraction_writer('5) ' + variable + ' = ', ['', '-b ± √D', '2 * a']))
                        self.solution += awesome_print(2.0, fraction_writer('6) ' + variable + ' = ', ['', stringPict(str(-gathered_data_coefficients[2]) + ' ± ', -1).right(str(root_writer([1, discriminant])))[0], '2 * ' + str(gathered_data_coefficients[1])]))
                        if check_int(sqrt(discriminant)):
                            self.solution += awesome_print(2.0, fraction_writer('7) ' + variable + '₁ = ', ['', str(-gathered_data_coefficients[2]) + ' + ' + str(sqrt(discriminant)), str(2.0 * gathered_data_coefficients[1])]))
                            self.solution += awesome_print(2.0, fraction_writer('   ' + variable + '₂ = ', ['', str(-gathered_data_coefficients[2]) + ' - ' + str(sqrt(discriminant)), str(2.0 * gathered_data_coefficients[1])]))
                            if check_int((-gathered_data_coefficients[2] - sqrt(discriminant)) / (2 * gathered_data_coefficients[1])) and check_int((-gathered_data_coefficients[2] + sqrt(discriminant)) / (2 * gathered_data_coefficients[1])):
                                self.solution += awesome_print(2.0, '8) ' + variable + '₁ = ' + str((-gathered_data_coefficients[2] - sqrt(discriminant)) / (2 * gathered_data_coefficients[1])))
                                self.solution += awesome_print(2.0, '   ' + variable + '₂ = ' + str((-gathered_data_coefficients[2] + sqrt(discriminant)) / (2 * gathered_data_coefficients[1])))
                            elif check_int((-gathered_data_coefficients[2] - sqrt(discriminant)) / (2 * gathered_data_coefficients[1])):
                                self.solution += awesome_print(2.0, '9) ' + variable + '₁ = ' + str((-gathered_data_coefficients[2] - sqrt(discriminant)) / (2 * gathered_data_coefficients[1])))
                                self.solution += awesome_print(2.0, fraction_writer('   ' + variable + '₂ = ', nice_dividing(-gathered_data_coefficients[2] + sqrt(discriminant), 2 * gathered_data_coefficients[1])))
                                if current_language == 'Russian':  # - Russian
                                    self.solution += awesome_print(2.0, 'Альтернативный ответ:')
                                    self.solution += awesome_print(2.0, variable + '₂ = ' + str((-gathered_data_coefficients[2] + sqrt(discriminant)) / (2 * gathered_data_coefficients[1])))
                                else:   # - English
                                    self.solution += awesome_print(2.0, 'Alternative answer:')
                                    self.solution += awesome_print(2.0, variable + '₂ = ' + str((-gathered_data_coefficients[2] + sqrt(discriminant)) / (2 * gathered_data_coefficients[1])))
                            elif check_int((-gathered_data_coefficients[2] + sqrt(discriminant)) / (2 * gathered_data_coefficients[1])):
                                self.solution += awesome_print(2.0, '9) ' + variable + '₁ = ' + str((-gathered_data_coefficients[2] + sqrt(discriminant)) / (2 * gathered_data_coefficients[1])))
                                self.solution += awesome_print(2.0, fraction_writer('   ' + variable + '₂ = ', nice_dividing(-gathered_data_coefficients[2] - sqrt(discriminant), 2 * gathered_data_coefficients[1])))
                                if current_language == 'Russian':  # - Russian
                                    self.solution += awesome_print(2.0, 'Альтернативный ответ:')
                                    self.solution += awesome_print(2.0, variable + '₂ = ' + str((-gathered_data_coefficients[2] - sqrt(discriminant)) / (2 * gathered_data_coefficients[1])))
                                else:
                                    self.solution += awesome_print(2.0, 'Alternative answer:')
                                    self.solution += awesome_print(2.0, variable + '₂ = ' + str((-gathered_data_coefficients[2] - sqrt(discriminant)) / (2 * gathered_data_coefficients[1])))
                            else:
                                self.solution += awesome_print(2.0, fraction_writer('9) ' + variable + '₁ = ', nice_dividing(-gathered_data_coefficients[2] - sqrt(discriminant), 2 * gathered_data_coefficients[1])))
                                self.solution += awesome_print(2.0, fraction_writer('   ' + variable + '₂ = ', nice_dividing(-gathered_data_coefficients[2] + sqrt(discriminant), 2 * gathered_data_coefficients[1])))
                                if current_language == 'Russian':  # - Russian
                                    self.solution += awesome_print(2.0, 'Альтернативный ответ:')
                                    self.solution += awesome_print(2.0, variable + '₁ = ' + str((-gathered_data_coefficients[2] - sqrt(discriminant)) / (2 * gathered_data_coefficients[1])))
                                    self.solution += awesome_print(2.0, variable + '₂ = ' + str((-gathered_data_coefficients[2] + sqrt(discriminant)) / (2 * gathered_data_coefficients[1])))
                                else:   # - English
                                    self.solution += awesome_print(2.0, 'Alternative answer:')
                                    self.solution += awesome_print(2.0, variable + '₁ = ' + str((-gathered_data_coefficients[2] - sqrt(discriminant)) / (2 * gathered_data_coefficients[1])))
                                    self.solution += awesome_print(2.0, variable + '₂ = ' + str((-gathered_data_coefficients[2] + sqrt(discriminant)) / (2 * gathered_data_coefficients[1])))

                        else:
                            split_root = nice_root(discriminant)
                            self.solution += awesome_print(2.0, fraction_writer('7) ' + variable + '₁ = ', ['', stringPict(str(-gathered_data_coefficients[2]) + ' + ', -1).right(root_writer(split_root))[0], str(2.0 * gathered_data_coefficients[1])]))
                            self.solution += awesome_print(2.0, fraction_writer('   ' + variable + '₂ = ', ['', stringPict(str(-gathered_data_coefficients[2]) + ' - ', -1).right(root_writer(split_root))[0], str(2.0 * gathered_data_coefficients[1])]))
                            nod_of_num_den = nod(gathered_data_coefficients[2], split_root[0], 2.0 * gathered_data_coefficients[1])
                            if nod_of_num_den != 1.0:
                                split_root[0] = split_root[0] / nod_of_num_den
                                if (2.0 * gathered_data_coefficients[1]) / nod_of_num_den == 1.0:
                                    if split_root[0] < 0:
                                        split_root[0] = abs(split_root[0])
                                        self.solution += awesome_print(2.0, stringPict('8) ' + variable + '₁ = ' + str(-gathered_data_coefficients[2] / nod_of_num_den) + ' - ', -1).right(root_writer(split_root))[0])
                                        self.solution += awesome_print(2.0, stringPict('   ' + variable + '₂ = ' + str(-gathered_data_coefficients[2] / nod_of_num_den) + ' + ', -1).right(root_writer(split_root))[0])
                                    else:
                                        self.solution += awesome_print(2.0, stringPict('8) ' + variable + '₁ = ' + str(-gathered_data_coefficients[2] / nod_of_num_den) + ' + ', -1).right(root_writer(split_root))[0])
                                        self.solution += awesome_print(2.0, stringPict('   ' + variable + '₂ = ' + str(-gathered_data_coefficients[2] / nod_of_num_den) + ' - ', -1).right(root_writer(split_root))[0])
                                else:
                                    if split_root[0] < 0:
                                        split_root[0] = abs(split_root[0])
                                        self.solution += awesome_print(2.0, fraction_writer('8) ' + variable + '₁ = ', ['', stringPict(str(-gathered_data_coefficients[2] / nod_of_num_den) + ' - ', -1).right(root_writer(split_root))[0], str((2.0 * gathered_data_coefficients[1]) / nod_of_num_den)]))
                                        self.solution += awesome_print(2.0, fraction_writer('   ' + variable + '₂ = ', ['', stringPict(str(-gathered_data_coefficients[2] / nod_of_num_den) + ' + ', -1).right(root_writer(split_root))[0], str((2.0 * gathered_data_coefficients[1]) / nod_of_num_den)]))
                                    else:
                                        self.solution += awesome_print(2.0, fraction_writer('8) ' + variable + '₁ = ', ['', stringPict(str(-gathered_data_coefficients[2] / nod_of_num_den) + ' + ', -1).right(root_writer(split_root))[0], str((2.0 * gathered_data_coefficients[1]) / nod_of_num_den)]))
                                        self.solution += awesome_print(2.0, fraction_writer('   ' + variable + '₂ = ', ['', stringPict(str(-gathered_data_coefficients[2] / nod_of_num_den) + ' - ', -1).right(root_writer(split_root))[0], str((2.0 * gathered_data_coefficients[1]) / nod_of_num_den)]))

                            if current_language == 'Russian':  # - Russian
                                self.solution += awesome_print(2.0, 'Альтернативный ответ:')
                                self.solution += awesome_print(2.0, variable + '₁ = ' + str((-gathered_data_coefficients[2] - sqrt(discriminant)) / (2 * gathered_data_coefficients[1])))
                                self.solution += awesome_print(2.0, variable + '₂ = ' + str((-gathered_data_coefficients[2] + sqrt(discriminant)) / (2 * gathered_data_coefficients[1])))
                            else:   # - English
                                self.solution += awesome_print(2.0, 'Alternative answer:')
                                self.solution += awesome_print(2.0, variable + '₁ = ' + str((-gathered_data_coefficients[2] - sqrt(discriminant)) / (2 * gathered_data_coefficients[1])))
                                self.solution += awesome_print(2.0, variable + '₂ = ' + str((-gathered_data_coefficients[2] + sqrt(discriminant)) / (2 * gathered_data_coefficients[1])))

        self.data_output.text = self.solution

    def insert_2nd_power(self):
        self.data_input.insert_text('²')

    def insert_x(self):
        self.data_input.insert_text('x')

    def delete(self):
        global state_of_the_output
        state_of_the_output = '<BLANK>'
        self.data_input.text = ''
        if current_language == 'English':
            self.data_output.text = 'Solution will be printed here :)'
        else:
            self.data_output.text = 'Решение будет напечатано здесь :)'


class SupportScreen(MDScreen):
    pass


class HelpScreen(MDScreen):
    pass


class SettingsScreen(MDScreen):

    def on_kv_post(self, base_widget):
        # Initialization

        # Widgets

        # Buttons
        self.buttons_with_icon = [
            # Home screen
            self.manager.get_screen('home').ids.solver_menu_button,
            self.manager.get_screen('home').ids.settings_menu_button,
            self.manager.get_screen('home').ids.support_menu_button,
            self.manager.get_screen('home').ids.help_menu_button,
            self.manager.get_screen('home').ids.exit_menu_button,

            # Solving Screen
            self.manager.get_screen('solution').ids.home_button_solving_screen,

            # Settings Screen
            self.ids.home_button_settings_screen,

            # Support Screen
            self.manager.get_screen('support').ids.home_button_support_screen,

            # Help Screen
            self.manager.get_screen('help').ids.home_button_help_screen
        ]

        self.buttons_without_icon = [
            self.manager.get_screen('solution').ids.solve_button,
            self.manager.get_screen('solution').ids.delete_button,
            self.manager.get_screen('solution').ids.power_button,
            self.manager.get_screen('solution').ids.x_button
        ]

        self.buttons_icon = [
            self.ids.eng_lang_button,
            self.ids.rus_lang_button,
            self.manager.get_screen('support').ids.copy_button
        ]

        # Text fields
        self.data_input = self.manager.get_screen('solution').ids.input_equation
        self.data_output = self.manager.get_screen('solution').ids.solution_output

        # Backgrounds
        self.backgrounds = [
            self.manager.get_screen('home').ids.background_image_home_screen,
            self.manager.get_screen('solution').ids.background_image_solving_screen,
            self.manager.get_screen('support').ids.background_image_support_screen,
            self.manager.get_screen('help').ids.background_image_help_screen,
            self.ids.background_image_settings_screen
        ]

        # Labels
        self.labels = [
            self.ids.lang_label,
            self.ids.rus_lang_label,
            self.ids.eng_lang_label,
            self.ids.theme_label,
            self.manager.get_screen('support').ids.support_card_label1,

            self.manager.get_screen('support').ids.support_card_label2,
            self.manager.get_screen('support').ids.support_card_label3,
            self.manager.get_screen('support').ids.support_card_label4,
            self.manager.get_screen('support').ids.support_card_label5,
            self.manager.get_screen('support').ids.support_card_label6,
            self.manager.get_screen('support').ids.support_card_label7,
            self.manager.get_screen('support').ids.support_card_label8,
            self.manager.get_screen('support').ids.support_card_label9,
            self.manager.get_screen('support').ids.support_card_label10,
            self.manager.get_screen('support').ids.support_card_label11,
            self.manager.get_screen('help').ids.help_card_label1,
            self.manager.get_screen('help').ids.help_card_label2,
            self.manager.get_screen('help').ids.help_card_label3,
            self.manager.get_screen('help').ids.help_card_label4,
            self.manager.get_screen('help').ids.help_card_label5,
            self.manager.get_screen('help').ids.help_card_label6,
            self.manager.get_screen('help').ids.help_card_label7,
            self.manager.get_screen('help').ids.help_label8
        ]

        # Cards
        self.cards = [
            self.manager.get_screen('support').ids.support_screen_card,
            self.manager.get_screen('help').ids.help_screen_card,
            self.manager.get_screen('solution').ids.solution_output_card
        ]

    def russian_language(self):
        global current_language, state_of_the_output
        # Buttons
        self.ids.rus_lang_button.icon = 'checkbox-blank-circle'
        self.ids.eng_lang_button.icon = 'checkbox-blank-circle-outline'
        for home_button in self.buttons_with_icon[5::]:
            home_button.text = '[font=Freestyle Script]Домой[/font]'
        self.buttons_without_icon[0].text = '[font=Freestyle Script]Решить[/font]'
        self.buttons_without_icon[1].text = '[font=Freestyle Script]Удалить[/font]'
        self.buttons_without_icon[1].font_size = QES.resolution_coefficient * 34
        self.buttons_with_icon[0].text = '[font=Freestyle Script]Решатель уравнений[/font]'
        self.buttons_with_icon[0].font_size = QES.resolution_coefficient * 46
        self.buttons_with_icon[1].text = '[font=Freestyle Script]Настройки[/font]'
        self.buttons_with_icon[2].text = '[font=Freestyle Script]Поддержка[/font]'
        self.buttons_with_icon[3].text = '[font=Freestyle Script]Помощь[/font]'
        self.buttons_with_icon[4].text = '[font=Freestyle Script]Выйти[/font]'
        # Labels
        self.labels[0].text = '[font=Consolas]Язык:[/font]'
        self.labels[0].pos_hint = {'center_x': 0.55, 'center_y': 0.93}
        # 1
        # 2
        self.labels[3].text = 'Тема:'
        # 4
        # ==============================================================================================================
        self.labels[5].text = '[font=Consolas]хоть и являеться лучшим, все равно абсолютно бесплатный и не содержит рекламы.[/font]'
        self.labels[6].text = '[font=Consolas]Следовательно,[/font]'
        self.labels[7].text = '[font=Consolas]Я бы хотел попросить Вас поддержать проект.[/font]'
        self.labels[8].text = '[font=Consolas]Выбор за Вами: как именно поддержать его.[/font]'
        self.labels[9].text = '[font=Consolas]Есть несколько способов это сделать,[/font]'
        self.labels[10].text = '[font=Consolas]все они хороши, и нет ничего страшного в том, чтобы их комбинировать.[/font]'
        self.labels[11].text = '[font=Consolas]Первый способ - поддержать финансово:[/font]'
        self.labels[13].text = '[font=Consolas]Второй способ - рассказать друзьям о приложении[/font]'
        self.labels[14].text = '[font=Consolas]Третий способ - поставить 5* в Play Market[/font]'
        # ==============================================================================================================
        self.labels[15].text = '[font=Consolas]Не знаете как использовать приложение?[/font]'
        self.labels[16].text = '[font=Consolas]Не проблема, это совсем не сложно![/font]'
        self.labels[17].text = '[font=Consolas]1) Нажмите на кнопку \"Решатель уравнений\".[/font]'
        self.labels[18].text = '[font=Consolas]2) Введите уравнение принадлежащее одному из следующих типов:[/font]'
        # 19
        self.labels[20].text = '[font=Consolas]4) Позиция коэффициентов не имеет значения.[/font]'
        self.labels[21].text = '[font=Consolas]5) Помните, что уравнение должно содержать как миниму одну переменную (т.е. x, y, t и т.д.) и только одну "²".[/font]'
        self.labels[22].text = '[font=IBM Plex Sans]Наслаждайтесь![/font]'
        self.labels[22].font_size = QES.resolution_coefficient * 40
        self.data_input.hint_text = 'Введите уравнение'

        if state_of_the_output == '<BLANK>':
            self.data_output.text = 'Решение будет напечатано здесь :)'
        elif state_of_the_output == '<ERROR>':
            self.data_output.text = 'Упс, я хз как это решить :('
        else:
            self.data_output.text = self.data_output.text.replace('Alternative answer:', 'Альтернативный ответ:')

        current_language = 'Russian'

    def english_language(self):
        global current_language, state_of_the_output
        self.ids.rus_lang_button.icon = 'checkbox-blank-circle-outline'
        self.ids.eng_lang_button.icon = 'checkbox-blank-circle'
        for home_button in self.buttons_with_icon[5::]:
            home_button.text = '[font=Freestyle Script]Home[/font]'
        self.buttons_without_icon[0].text = '[font=Freestyle Script]Solve[/font]'
        self.buttons_without_icon[1].text = '[font=Freestyle Script]Delete[/font]'
        self.buttons_without_icon[1].font_size = QES.resolution_coefficient * 38
        self.buttons_with_icon[0].text = '[font=Freestyle Script]Equation-Solver[/font]'
        self.buttons_with_icon[0].font_size = QES.resolution_coefficient * 54
        self.buttons_with_icon[1].text = '[font=Freestyle Script]Settings[/font]'
        self.buttons_with_icon[2].text = '[font=Freestyle Script]Support[/font]'
        self.buttons_with_icon[3].text = '[font=Freestyle Script]Help[/font]'
        self.buttons_with_icon[4].text = '[font=Freestyle Script]Exit[/font]'
        # Labels
        self.labels[0].text = '[font=Consolas]Language:[/font]'
        self.labels[0].pos_hint = {'center_x': 0.55, 'center_y': 0.93}
        # 1
        # 2
        self.labels[3].text = 'Theme:'
        # 4
        # ==============================================================================================================
        self.labels[5].text = '[font=Consolas]although being the best, is still absolutely free and contains no advertisements.[/font]'
        self.labels[6].text = '[font=Consolas]Consequently,[/font]'
        self.labels[7].text = '[font=Consolas]I\'d like to ask you to support the project.[/font]'
        self.labels[8].text = '[font=Consolas]It is up to you: how exactly you support this app.[/font]'
        self.labels[9].text = '[font=Consolas]There are several ways to do it,[/font]'
        self.labels[10].text = '[font=Consolas]all of them are equally good, and there is no shame in combing them.[/font]'
        self.labels[11].text = '[font=Consolas]The first way - assist financially:[/font]'
        self.labels[13].text = '[font=Consolas]The second way - tell your friends about it[/font]'
        self.labels[14].text = '[font=Consolas]The third way - set 5* in Play Market[/font]'
        # ==============================================================================================================
        self.labels[15].text = '[font=Consolas]Don\'t know how to use the app?[/font]'
        self.labels[16].text = '[font=Consolas]No problem, that\'s not complicated at all![/font]'
        self.labels[17].text = '[font=Consolas]1) Click \"Equation-Solver\" button.[/font]'
        self.labels[18].text = '[font=Consolas]2) Enter a quadratic equation belonging to one of the following types:[/font]'
        # 19
        self.labels[20].text = '[font=Consolas]4) Position of coefficients doesn\'t matter.[/font]'
        self.labels[21].text = '[font=Consolas]5) Keep in mind that an equation should contain at least one variable (f.e. x, y, t, etc.) and only one "²".[/font]'
        self.labels[22].text = '[font=IBM Plex Sans]Enjoy![/font]'
        self.labels[22].font_size = QES.resolution_coefficient * 55
        self.data_input.hint_text = 'Enter an equation'
        if state_of_the_output == '<BLANK>':
            self.data_output.text = 'Solution will be printed here :)'
        elif state_of_the_output == '<ERROR>':
            self.data_output.text = 'Oops, idk how to solve that :('
        else:
            self.data_output.text = self.data_output.text.replace('Альтернативный ответ:', 'Alternative answer:')
        current_language = 'English'

    # ACCENTS

    @staticmethod
    def set_custom_accent(btns_with_ic, btns_without_ic, icns, lbls, toolbar, widget_output, color):

        for button in btns_with_ic:
            button.text_color = color
            button.line_color = color
            button.icon_color = color

        for button in btns_without_ic:
            button.text_color = color
            button.line_color = color

        for button in icns:
            button.text_color = color

        for label in lbls:
            label.text_color = color

        toolbar.md_bg_color = color

        widget_output.text_color = color


    def set_reddish_accent(self):
        self.set_custom_accent(self.buttons_with_icon, self.buttons_without_icon, self.buttons_icon,
                               self.labels, self.manager.get_screen('home').ids.title, self.data_output, color=[.85, .2, .1, 1])

    def set_orange_accent(self):
        self.set_custom_accent(self.buttons_with_icon, self.buttons_without_icon, self.buttons_icon,
                               self.labels, self.manager.get_screen('home').ids.title, self.data_output, color=[.93, .54, .04, 1])

    def set_yellowish_accent(self):
        self.set_custom_accent(self.buttons_with_icon, self.buttons_without_icon, self.buttons_icon,
                               self.labels, self.manager.get_screen('home').ids.title, self.data_output, color=[.93, .81, .02, 1])

    def set_greenish_accent(self):
        self.set_custom_accent(self.buttons_with_icon, self.buttons_without_icon, self.buttons_icon,
                               self.labels, self.manager.get_screen('home').ids.title, self.data_output, color=[.02, .9, .18, 1])

    def set_malachite_accent(self):
        self.set_custom_accent(self.buttons_with_icon, self.buttons_without_icon, self.buttons_icon,
                               self.labels, self.manager.get_screen('home').ids.title, self.data_output, color=[0, .47, .42, 1])

    def set_purple_accent(self):
        self.set_custom_accent(self.buttons_with_icon, self.buttons_without_icon, self.buttons_icon,
                               self.labels, self.manager.get_screen('home').ids.title, self.data_output, color=[.57, .02, .72, 1])

    def set_space_accent(self):
        self.set_custom_accent(self.buttons_with_icon, self.buttons_without_icon, self.buttons_icon,
                               self.labels, self.manager.get_screen('home').ids.title, self.data_output, color=[.7, .65, .82, 1])

    def set_dark_blue_accent(self):
        self.set_custom_accent(self.buttons_with_icon, self.buttons_without_icon, self.buttons_icon,
                               self.labels, self.manager.get_screen('home').ids.title, self.data_output, color=[.02, .31, .79, 1])

    # BGs
    def set_light_bg(self):
        for bg in self.backgrounds:
            bg.source = 'Light_theme.png'
        for card in self.cards:
            card.md_bg_color = .68, .68, .68, 1

    def set_dark_bg(self):
        for bg in self.backgrounds:
            bg.source = 'Dark_theme.png'
        for card in self.cards:
            card.md_bg_color = .11, .11, .11, 1

    def set_sky_blue_bg(self):
        for bg in self.backgrounds:
            bg.source = 'Skyblue_theme.png'
        for card in self.cards:
            card.md_bg_color = 0, .44, .45, 1

    def set_ruby_bg(self):
        for bg in self.backgrounds:
            bg.source = 'Ruby_theme.png'
        for card in self.cards:
            card.md_bg_color = .59, .06, .13, 1

    def set_raspberry_bg(self):
        for bg in self.backgrounds:
            bg.source = 'Raspberry_theme.png'
        for card in self.cards:
            card.md_bg_color = .61, .18, .27, 1

    def set_purple_bg(self):
        for bg in self.backgrounds:
            bg.source = 'Purple_theme.png'
        for card in self.cards:
            card.md_bg_color = .28, .07, .37, 1

    def set_gradient_bg(self):
        for bg in self.backgrounds:
            bg.source = 'Gradient_theme.png'
        for card in self.cards:
            card.md_bg_color = .37, .11, .23, 1

    def set_dark_blue_bg(self):
        for bg in self.backgrounds:
            bg.source = 'DarkBlue_theme.png'
        for card in self.cards:
            card.md_bg_color = 0, .08, .67, 1


class WindowManager(ScreenManager):
    pass

# Global variables
current_language = 'English'
# possible variants are 1) '<BLANK>' ; 2) '<SOLUTION>' ; 3) 'ERROR'
state_of_the_output = '<BLANK>'

# Designate .kv design file
Interface = 'new_gui.kv'


class QES(MDApp):

    have_been_popped = None
    # resolution coefficient: width of CURRENT device's screen / width of INITIAL device's screen
    resolution_coefficient = Window.width / 450
    @staticmethod
    def close_application(obj):
        # closing application
        MDApp.get_running_app().stop()
        # removing window
        Window.close()

    def show_alert(self):
        if not self.have_been_popped:
            self.alert_window = MDDialog(
                title='Already leaving?',
                text='Are you sure that you want to exit?',
                buttons=[
                    MDFillRoundFlatButton(text='CANCEL', on_release=self.close_alert_window),
                    MDRoundFlatButton(text='YES', on_release=self.close_application)])
            self.have_been_popped = False

        self.alert_window.open()

    def close_alert_window(self, obj):
        self.alert_window.dismiss()

    def build(self):
        self.theme_cls.primary_hue = '700'
        self.theme_cls.primary_palette = 'Teal'
        self.theme_cls.accent_palette = 'BlueGray'
        self.theme_cls.accent_hue = '900'
        return Builder.load_file(Interface)


QES().run()