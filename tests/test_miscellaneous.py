from CommonResources.Classes.miscellaneous import *
import os


def test_env_var_loader(loading_env_var):
    Miscellaneous.env_var_loader(loading_env_var[0])

    assert loading_env_var[1] == os.environ[loading_env_var[2]]


def test_to_html_with_checkbox(df_to_html):
    result = '<table> <thead> <tr style="text-align: center;"> <th>Id</th> <th>Model</th> <th>Year</th> </tr>' \
             ' </thead> <tbody>  <tr>  <td><input type="checkbox" id="Id1" name="Id1" value="1"></td> <td>Focus</td>' \
             '  <td>2012</td>  </tr>  <tr>  <td><input type="checkbox" id="Id2" name="Id2" value="2"></td>' \
             ' <td>Fiesta</td>  <td>2020</td>  </tr>  <tr>  <td><input type="checkbox" id="Id3" name="Id3"' \
             ' value="3"></td> <td>Corsa</td>  <td>2017</td>  </tr>  <tr>  <td><input type="checkbox" id="Id4" ' \
             'name="Id4" value="4"></td> <td>Insignia</td>  <td>2019</td>  </tr>  <tr>  <td><input' \
             ' type="checkbox" id="Id5" name="Id5" value="5"></td> <td>Vectra</td>  <td>2014</td>' \
             '  </tr>  </tbody> </table>'

    assert Miscellaneous.to_html_with_checkbox(df_to_html, 'Id') == result


def test_float_to_currency(dataframes):
    # testing dataframe type_
    df_to_test = Miscellaneous.float_to_currency(dataframes[0].copy(), cols=['Currency'])
    for iindex in df_to_test.index:
        assert df_to_test.loc[iindex, 'Currency'] == dataframes[1].loc[iindex, 'Currency']

    # testing float type_
    for iindex in dataframes[0].index:
        assert Miscellaneous.float_to_currency(float(dataframes[0].loc[iindex, 'Currency']),
                                               type_='float') == dataframes[1].loc[iindex, 'Currency']
