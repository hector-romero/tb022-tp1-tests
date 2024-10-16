import subprocess
import typing
from pathlib import Path
import inspect

import pytest


def get_path(file_name, base_path=None):
    if not base_path:
        base_path = Path(__file__)
    return base_path.parent.joinpath(file_name)


@pytest.fixture
def run_bash_script():
    def _run_script(script: str, arguments: list[typing.Any], fail_on_error=True):
        script_path = get_path(script)
        cmd = [str(x) for x in [script_path] + (arguments or [])]
        result = subprocess.run(cmd, capture_output=True)
        if fail_on_error and result.returncode != 0:
            raise Exception(f"Script '{script}' failed with exit code {exit}")

        return result.stdout.decode(), result.returncode

    yield _run_script


@pytest.fixture
def tmp_files():
    files_created = []

    def create_files(file_name, file_content=None, base_path=None):
        file_path = get_path(file_name, base_path=base_path)

        if file_content is not None:
            with open(file_path, 'w+') as file:
                file.write(inspect.cleandoc(file_content))
        files_created.append(str(file_path))
        return str(file_path)

    yield create_files

    for file_created in files_created:
        Path.unlink(file_created, missing_ok=True)


def assert_file_content(file_name, expected_value):
    with open(file_name, 'r+') as file:
        value = file.read()
        assert inspect.cleandoc(value) == inspect.cleandoc(expected_value)


@pytest.fixture(params=[None, "", "giberishsaldas\nlsda"], ids=['ouput-non-existent', 'output-empty', 'output-non-empty'])
def output_pre_content(request):
    """Fixture that parametrizes the content of the output file."""
    return request.param


@pytest.mark.parametrize('input_file_name, output_file_name', [
    ('registro.txt', 'pato.txt'),
    ('otro_registro.txt', 'otro_pato.txt')
], ids=lambda file_name: file_name)
@pytest.mark.parametrize('input_content, output_hour', [
    ("""
        11:10 1 Pato comió un poco de "Sonrisa dulce"
        11:25 3 Pato rompió un sueter de Mabel
        11:33 4 Pato se dirigió a los charcos de barro
        12:01 5 Pato se resbaló en el barro
        12:10 7 Pato se limpió las pezuñas
        12:31 3 Pato se comió un album de "Varias veces"
        12:33 5 Pato masticó los lentes de Standford
        12:41 7 Pato se resbaló en el agua
        12:44 6 Pato se ensució las pezuñas con pelo de multioso
        12:51 7 Pato se limpió las pezuñas
        13:00 5 Pato masticó la la gorra de Soos
        13:21 4 Pato se acostó a dormir siesta
        14:25 7 Pato se resbaló en el barro        
        14:40 6 Pato tomó agua
        14:51 4 Pato comió un poco de "Sonrisa dulce"
        15:01 7 Pato mordió la gorra de Dipper
    """, "12:51"),
    ("""
        12:01 5 Pato se resbaló en el barro
        12:10 7 Pato se limpió las pezuñas
        12:31 3 Pato se comió un album de "Varias veces"
        12:33 5 Pato masticó los lentes de Standford
        12:41 7 Pato se resbaló en el agua
        12:44 6 Pato se ensució las pezuñas con pelo de multioso
        12:50 7 Pato se limpió las pezuñas
        13:00 5 Pato masticó la la gorra de Soos
        13:21 4 Pato se acostó a dormir siesta
        14:25 7 Pato se resbaló en el barro        
        14:40 6 Pato tomó agua
        14:51 4 Pato comió un poco de "Sonrisa dulce"
        15:01 7 Pato mordió la gorra de Dipper
    """, "14:25"),
    ("""
        12:01 5 Pato se resbaló en el barro
        12:10 7 Pato se limpió las pezuñas
        12:31 3 Pato se comió un album de "Varias veces"
        12:33 5 Pato masticó los lentes de Standford
        12:41 7 Pato se resbaló en el agua
        12:44 6 Pato se ensució las pezuñas con pelo de multioso
        12:50 7 Pato se limpió las pezuñas
        13:00 5 Pato masticó la la gorra de Soos
        13:21 4 Pato se acostó a dormir siesta
        14:20 7 Pato se resbaló en el barro        
        14:40 6 Pato tomó agua
        14:51 4 Pato comió un poco de "Sonrisa dulce"
        15:01 7 Pato mordió la gorra de Dipper
    """, ""),
    ("""
        01:25 7 Pato se durmió  
        06:10 9 Pato soñó con comida  
        19:55 6 Pato trató de morder la impresora  
        14:20 1 Pato comió "Sonrisa dulce"  
        10:30 4 Pato mordió una cortina  
        17:40 3 Pato buscó más comida
        18:01 7 Pato se resbaló en el barro 
        15:15 10 Pato se acostó a pensar  
        08:45 2 Pato soñó con la gorra de Dipper  
        12:05 8 Pato se metió a un charco con agua  
        02:35 9 Pato roncó  
        13:45 7 Pato se limpió las pezuñas  
        20:10 3 Pato trató de tirar la impresora  
        07:15 1 Pato soñó con Mabel  
        18:50 2 Pato se comió una manzana  
        11:30 5 Pato se enredó en la cortina  
        03:50 4 Pato se movió dormido  
        05:00 7 Pato cambió de posición para dormir  
        09:05 8 Pato se despertó  
        16:25 6 Pato tomó agua  
        23:55 10 Pato se quedó dormido  
    """, """13:45""")

], ids=lambda content: inspect.cleandoc(str(content))[:30])
def test_acertijo_1(run_bash_script, tmp_files, input_file_name, output_file_name, input_content, output_hour, output_pre_content):
    if output_hour:
        expected_output = f"Hora indicada para capturar a Pato: {output_hour}"
    else:
        expected_output = ''

    input_file = tmp_files(input_file_name, input_content)
    output_file = tmp_files(output_file_name, output_pre_content)

    run_bash_script('../acertijo1.sh', [input_file, output_file])

    assert_file_content(output_file, expected_output)


@pytest.mark.parametrize('input_file_name, output_file_name', [
    ('canciones.txt', 'venganza.txt'),
    ('input_file.txt', 'output_file.txt')
], ids=lambda file_name: file_name)
@pytest.mark.parametrize('input_content, expected_output', [
    ("""
        Sev’ral Timez
        Chica, me tienes tan locooo, loco, loco (cray, cray)
        Como me dices que no seras mi bebe
        NO estamos amenazando, bebe
        Alla vamos amor no volaras conmigo
        Tom4 mi m4n0 es el destino
        Mabel, solo toma mi mano, puede ser para siempre
        no necesitamos a nadie, si permanecemos juntos
        Eres el cielo chica, vamos a volar
        Ja, mira mis grandes ojos azules
        Otra como tu no hay Mabel
        Sev’ral Timez did it
    """, """
        zXmXT lXr’vXS
        CXmX mX dXcXs qXX nX sXrXs mX bXbX
        AllX vXmXs XmXr nX vXlXrXs cXnmXgX
        MXbXl, sXlX tXmX mX mXnX, pXXdX sXr pXrX sXXmprX
        ErXs Xl cXXlX chXcX, vXmXs X vXlXr
        JX, mXrX mXs grXndXs XjXs XzXlXs
        OtrX cXmX tX nX hXy MXbXl
        tX dXd zXmXT lXr’vXS
    """),
    ("Lorem itsum dolor sit amet", "LXrXm XtsXm dXlXr sXt XmXt"),
    ("AxrOm", "mOrxA"),
    ("4", ""),
    ("LL", ""),
    ("aa", ""),
    ("Laa", "XXL"),
    ("Laaa", ""),
    ("Lm np qr st", "ts rq pn mL"),
    ("Lm np qr st xy", "Lm np qr st xy"),
], ids=lambda content: inspect.cleandoc(str(content))[:30])
def test_acertijo_2(run_bash_script, tmp_files, input_file_name, output_file_name, input_content, expected_output, output_pre_content):

    input_file = tmp_files(input_file_name, input_content)
    output_file = tmp_files(output_file_name, output_pre_content)

    run_bash_script('../acertijo2.sh', [input_file, output_file])
    assert_file_content(output_file, expected_output)


@pytest.mark.parametrize('input_file_name, output_file1_name, output_file2_name', [
    ('infractores.csv', 'infractores.txt', 'acertijo3.txt'),
    ('random.csv', 'yearly_top.txt', 'historic_top.txt'),
], ids=lambda file_name: file_name)
@pytest.mark.parametrize('input_content, expected_output1, expected_output2', [
    ("""
        Blendin Blandin, 02/04/2020, 35
        Soos Ramirez, 12/08/2020, 12
        Soos Ramirez, 12/08/2021, 11
        Blendin Blandin, 02/04/2021, 26
        Stan Pines, 24/01/2020, 8
        John Doe, 24/01/2020, 130
        Stan Pines, 24/01/2021, 11
    """, """
        Stan Pines, 24/01/2020, 8
        Soos Ramirez, 12/08/2020, 12
        Blendin Blandin, 02/04/2020, 35
        Stan Pines, 24/01/2021, 11
        Soos Ramirez, 12/08/2021, 11
        Blendin Blandin, 02/04/2021, 26
    """, """
        Stan Pines, 24/01/2020, 8
        Stan Pines, 24/01/2021, 11
        Soos Ramirez, 12/08/2021, 11
    """),
    ("""
        2024, 11/02/2023, 35
        2025, 11/03/2023, 30
        2025, 11/03/2023, 50
        2025, 11/02/2023, 40
        Pepito, 11/02/2023, 123
        2025, 11/03/2020, 33
        2025, 11/03/2022, 1
    """, """
        2025, 11/03/2020, 33
        2025, 11/03/2022, 1
        2025, 11/03/2023, 30
        2024, 11/02/2023, 35
        2025, 11/02/2023, 40
    """, """
        2025, 11/03/2022, 1
        2025, 11/03/2023, 30
        2025, 11/03/2020, 33
    """
     )
], ids=lambda content: inspect.cleandoc(str(content))[:30])
def test_acertijo_3(run_bash_script, tmp_files, input_file_name, output_file1_name, output_file2_name, input_content, expected_output1, expected_output2, output_pre_content):
    input_file = tmp_files(input_file_name, input_content)
    output_file1 = tmp_files(output_file1_name, output_pre_content)
    output_file2 = tmp_files(output_file2_name, output_pre_content)

    default_output_file1 = tmp_files('infractores.txt', output_pre_content, Path())
    default_output_file2 = tmp_files('acertijo3.txt', output_pre_content, Path())

    run_bash_script('../acertijo3.sh', [input_file])
    assert_file_content(default_output_file1, expected_output1)
    assert_file_content(default_output_file2, expected_output2)
    run_bash_script('../acertijo3.sh', [input_file, output_file1, output_file2])
    # run_bash_script('../acertijo3.sh', [input_file])
    assert_file_content(output_file1, expected_output1)
    assert_file_content(output_file2, expected_output2)


@pytest.mark.parametrize('input_file_name, output_file_name', [
    ('papiro.txt', 'mensaje_papiro.txt'),
    ('message.txt', 'message_bk.txt')
], ids=lambda file_name: file_name)
@pytest.mark.parametrize('input_content, expected_output', [
    ("""
        1@5C%&*u*&E@!125&V*@#$a
        @#!S$%&e#24%1C*$!@r$%#E!@!#t&%!@A#@!@
        !#@P$%$!o%%&*C$@!@#o!@#$@!s!@#$!@
        !$@M#$%#@E@#$%#t@!@%r@!@@o@!!@$s%$&*!@
    """, "doblarizquierdadespuesderecha"),
    # ("cueva@secreta#pocos$metros%atras", "doblarizquierdadespuesderechaatras"),
    ("""
        !@#$ %^&* ()_+
        ^%$# !@#$ %^&*
        +_)( *&^% $#!@
        !@#$ ^&*() %^&*
    """, "")

], ids=lambda content: inspect.cleandoc(str(content))[:30])
def test_acertijo_4(run_bash_script, tmp_files, input_file_name, output_file_name, input_content, expected_output, output_pre_content):
    input_file = tmp_files(input_file_name, input_content)
    output_file = tmp_files(output_file_name, output_pre_content)

    run_bash_script('../acertijo4.sh', [input_file, output_file])
    assert_file_content(output_file, expected_output)


@pytest.mark.parametrize('input_file_name, output_file_name', [
    ('paginaDiario.txt', 'lector_clave_secreta.txt'),
    ('input_file.txt', 'output_file.txt')
], ids=lambda file_name: file_name)
@pytest.mark.parametrize('input_content, mabel_count, expected_output', [
    ("""
        En el pueblo de Gravity Falls, el misterio es la esencia principal.
        Todos los rincones de la ciudad ocultan secretos que traen nuevos misterios que los
        hermanos pines deben resolver.
        El bosque que rodea el pueblo esta repleto de criaturas extrañas y de fenómenos que
        nadie puede explicar. La "Tienda de curiosidades" del tío Pines también muestra esa
        esencia tenebrosa y misteriosa de Gravity Falls. Incluso sus habitantes tienen su
            lado
        enigmatico, que contribuye a la atmósfera de puro misterio: Gideon, Stan, el Gnomo
            Rey
        y muchos más. A lo largo que transcurre el verano, van resolviendo todos aquellos
        misterios de la ciudad con la ayuda del diario número 3 y sus amigos
    """, 6, """
        2
        720
    """),
    ("""
        misterioso misterio misterio
        asmisterio admisterios misterio
    """, 5, "3\n5"),
    ("misterio", 0, "1\n1"),
    ("misterio", 1, "1\n1"),
    ("", 2, "0\n2"),
    ("", 3, "0\n2"),
    ("", 4, "0\n24"),
    ("", 5, "0\n5"),
    ("", 7, "0\n13"),
], ids=lambda content: inspect.cleandoc(str(content))[:30])
def test_acertijo_5(run_bash_script, tmp_files, input_file_name, output_file_name, input_content, mabel_count, expected_output, output_pre_content):
    input_file = tmp_files(input_file_name, input_content)
    output_file = tmp_files(output_file_name, output_pre_content)

    run_bash_script('../acertijo5.sh', [input_file, mabel_count, output_file])
    assert_file_content(output_file, expected_output)


@pytest.mark.parametrize("mabel_count, factorial", [
    (0, 1),
    (2, 2),
    (4, 24),
    (6, 720),
    (8, 40320),
    (10, 3628800),
    (12, 479001600),
    (20, 479001600),
])
def test_acertijo_5_shuld_return_factorial_when_mabel_is_an_even_number(run_bash_script, tmp_files, mabel_count, factorial):
    input_file = tmp_files('papiro.txt', "")
    output_file = tmp_files('mensaje_papiro.txt')

    run_bash_script('../acertijo5.sh', [input_file, mabel_count, output_file])
    assert_file_content(output_file, f"0\n{factorial}")


@pytest.mark.parametrize("mabel_count, fibonacci", [
    (1, 1),
    (3, 2),
    (5, 5),
    (7, 13),
    (9, 34),
    (11, 89),
    (13, 233),
    (43, 433494437),
])
def test_acertijo_5_shuld_return_fibonacci_when_mabel_is_an_odd_number(run_bash_script, tmp_files, mabel_count, fibonacci):
    input_file = tmp_files('papiro.txt', "")
    output_file = tmp_files('mensaje_papiro.txt')

    run_bash_script('../acertijo5.sh', [input_file, mabel_count, output_file])
    assert_file_content(output_file, f"0\n{fibonacci}")


@pytest.mark.parametrize("mabel", [
    "a", "_", "-12", ".12", "adl21", "12dsd", "12.34", ""
])
def test_acertijo_5_should_fail_when_mabel_is_not_a_valid_number(run_bash_script, tmp_files, mabel):
    input_file = tmp_files('input_file.txt', "")
    result, error_code = run_bash_script('../acertijo5.sh', [input_file, mabel, "file2"], fail_on_error=False)
    assert result == f"El parametro <repeticiones mabel> debe ser un numero entero positivo no '{mabel}'\n"
    assert error_code == 1


@pytest.mark.parametrize('input_file_name, output_file_name', [
    ('pared.txt', 'codigo_secreto.txt'),
    ('input_file.txt', 'output_file.txt')
], ids=lambda file_name: file_name)
@pytest.mark.parametrize('input_content, expected_output', [
    ("""
        TbrA8X8FvnjhX9th773QWSXdWcYBUD
        0808E8JQb3TABFCKHEWf1zy3UXZZ53
        99999080118082280808228080aHh4
        99080900110082208080220808aSds
        99999008118082280008228800akmg
        99080900110082200808228800aKgT
        99999000118082222228222222aPX3
        08080808080808080808800808wqXa
        T3QPXvnc07cUrTKYRFl86HUOLgw6WE
    """, """
        TbrA_X_FvnjhXXth773QWSXdWcYBUD
        ____E_JQb3TABFCKHEWfXzy3UXZZ53
        XXXXX___XX___XX_____XX____aHh4
        XX___X__XX___XX_____XX____aSds
        XXXXX___XX___XX_____XX____akmg
        XX___X__XX___XX_____XX____aKgT
        XXXXX___XX___XXXXXX_XXXXXXaPX3
        __________________________wqXa
        T3QPXvnc_7cUrTKYRFl_6HUOLgw6WE
    """)
], ids=lambda content: inspect.cleandoc(str(content))[:30])
def test_acertijo_6(run_bash_script, tmp_files, input_file_name, output_file_name, input_content, expected_output, output_pre_content):

    input_file = tmp_files(input_file_name, input_content)
    output_file = tmp_files(output_file_name, output_pre_content)

    run_bash_script('../acertijo6.sh', [input_file, output_file])
    assert_file_content(output_file, expected_output)


@pytest.mark.parametrize('script, params, error', [
    ('../acertijo1.sh', [], f"Uso: {get_path('../acertijo1.sh')} <archivo registro> <archivo captura>\n"),
    ('../acertijo1.sh', ['param'], f"Uso: {get_path('../acertijo1.sh')} <archivo registro> <archivo captura>\n"),
    ('../acertijo2.sh', [],  f"Uso: {get_path('../acertijo2.sh')} <archivo canciones> <archivo venganza>\n"),
    ('../acertijo2.sh', ['param'],  f"Uso: {get_path('../acertijo2.sh')} <archivo canciones> <archivo venganza>\n"),
    ('../acertijo3.sh', [],  f"Uso: {get_path('../acertijo3.sh')} <archivo infractores>\n"),
    ('../acertijo4.sh', [], f"Uso: {get_path('../acertijo4.sh')} <archivo papiro> <archivo mensaje>\n"),
    ('../acertijo4.sh', ["param"], f"Uso: {get_path('../acertijo4.sh')} <archivo papiro> <archivo mensaje>\n"),
    ('../acertijo5.sh', [], f"Uso: {get_path('../acertijo5.sh')} <archivo pagina diario> <repeticiones mabel> <archivo clave secreta>\n"),
    ('../acertijo5.sh', ["param"], f"Uso: {get_path('../acertijo5.sh')} <archivo pagina diario> <repeticiones mabel> <archivo clave secreta>\n"),
    ('../acertijo5.sh', ["param", "param2"], f"Uso: {get_path('../acertijo5.sh')} <archivo pagina diario> <repeticiones mabel> <archivo clave secreta>\n"),
    ('../acertijo6.sh', [], f"Uso: {get_path('../acertijo6.sh')} <archivo pared> <archivo codigo>\n"),
    ('../acertijo6.sh', ["param"], f"Uso: {get_path('../acertijo6.sh')} <archivo pared> <archivo codigo>\n"),
])
def test_scripts_should_fail_when_missing_params(run_bash_script, script, params, error):
    result, error_code = run_bash_script(script, params, fail_on_error=False)
    assert result == error
    assert error_code == 1


@pytest.mark.parametrize('script', [
    '../acertijo1.sh',
    '../acertijo2.sh',
    '../acertijo3.sh',
    '../acertijo4.sh',
    '../acertijo5.sh',
    '../acertijo6.sh',
])
def test_scripts_should_fail_with_invalid_input_file(run_bash_script, script):
    result, error_code = run_bash_script(script, ['invalid_file', 'param2', 'param3'], fail_on_error=False)
    assert result == "El archivo 'invalid_file' no existe\n"
    assert error_code == 1
