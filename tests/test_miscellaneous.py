from CommonResources.Classes.miscellaneous import *
import os
import pandas as pd
import pytest


@pytest.fixture()
def loading_env_var():
    """
    Fixture that creates a file with the content:
        TEST=1234
    After that yield data to test and finally on tear down deletes the file

    Returns:
        - file_name: name of file created
        - env_var_value: value of the environment variable saved on file
        - env_var_name: name of the environment variable saved on file
    """
    file_name = '.test_loading_env_var'
    file_path = os.path.join(os.getcwd(), file_name)

    env_var_value = '1234'
    env_var_name = 'TEST'
    file_content = '%s=%s' % (env_var_name, env_var_value)

    with open(file_path, "w") as f:
        f.write(file_content)

    yield file_name, env_var_value, env_var_name

    os.remove(file_path)


def test_env_var_loader(loading_env_var):
    """
    GIVEN a file with some env variables
    WHEN it is processed by Miscellaneous.env_var_loader()
    THEN check that environment variables are actually created
    """
    Miscellaneous.env_var_loader(loading_env_var[0])

    assert loading_env_var[1] == os.environ[loading_env_var[2]]


def test_to_html_with_checkbox():
    """
    GIVEN a pandas dataframe
    WHEN it is processed by Miscellaneous.to_html_with_checkbox()
    THEN check that the html table has the formatting desired
    """
    result = '<table> <thead> <tr style="text-align: center;"> <th>Id</th> <th>Model</th> <th>Year</th> </tr>' \
             ' </thead> <tbody>  <tr>  <td><input type="checkbox" id="Id1" name="Id1" value="1"></td> <td>Focus</td>' \
             '  <td>2012</td>  </tr>  <tr>  <td><input type="checkbox" id="Id2" name="Id2" value="2"></td>' \
             ' <td>Fiesta</td>  <td>2020</td>  </tr>  <tr>  <td><input type="checkbox" id="Id3" name="Id3"' \
             ' value="3"></td> <td>Corsa</td>  <td>2017</td>  </tr>  <tr>  <td><input type="checkbox" id="Id4" ' \
             'name="Id4" value="4"></td> <td>Insignia</td>  <td>2019</td>  </tr>  <tr>  <td><input' \
             ' type="checkbox" id="Id5" name="Id5" value="5"></td> <td>Vectra</td>  <td>2014</td>' \
             '  </tr>  </tbody> </table>'

    data = {
        'Id': [1, 2, 3, 4, 5],
        'Model': ['Focus', 'Fiesta', 'Corsa', 'Insignia', 'Vectra'],
        'Year': [2012, 2020, 2017, 2019, 2014]
    }
    df = pd.DataFrame.from_dict(data)

    assert Miscellaneous.to_html_with_checkbox(df, 'Id') == result


def test_float_to_currency_for_dataframe():
    """
    GIVEN a pandas dataframe
    WHEN it is processed by Miscellaneous.float_to_currency()
    THEN check that the columns are formatted as expected
    """
    data_to_test = {'Id': [1, 2, 3],
                    'Currency': [100, 200, 300]}
    raw = pd.DataFrame.from_dict(data_to_test)
    data_to_compare = {'Id': [1, 2, 3],
                       'Currency': ['£ 100.00', '£ 200.00', '£ 300.00']}
    expected_result = pd.DataFrame.from_dict(data_to_compare)

    df_to_test = Miscellaneous.float_to_currency(raw.copy(), cols=['Currency'])
    for iindex in df_to_test.index:
        assert df_to_test.loc[iindex, 'Currency'] == expected_result.loc[iindex, 'Currency']

@pytest.mark.parametrize(
    "currency, result, to_format",
    [
        (100, '£ 100.00', '£ {:,.2f}'),
        (100, '100.00€', '{:,.2f}€'),
        ("100.87", '101€', '{:,.0f}€'),
        (100.87, '$  100.9', '$  {:,.1f}')
    ],
)
def test_float_to_currency_for_float(currency, result, to_format):
    """
    GIVEN a float number
    WHEN it is processed by Miscellaneous.float_to_currency()
    THEN check that the string returned has the correct format
    """
    assert Miscellaneous.float_to_currency(float(currency), format_to=to_format, type_of_input='float') == result
