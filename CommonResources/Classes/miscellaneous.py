import dash_html_components as html
import os
from dotenv import load_dotenv
from flask_login import login_required


class Miscellaneous:
    """Collection of function to solve different problems"""
    @staticmethod
    def to_html_with_checkbox(df, col_to_checkbox, table_class=None):
        """
        Method that takes a df and returns a html table which contains a checkbox on column col_to_checkbox.
        :param df: dataframe to create html table with checkbox
        :param col_to_checkbox: column to transform into a checkbox
        :param table_class: class of the table to get style from css file
        """
        if table_class:
            html_ = '<table class="%s"> <thead> <tr style="text-align: center;">' % table_class
        else:
            html_ = '<table> <thead> <tr style="text-align: center;">'

        cols = df.columns.values.tolist()
        for col in cols:
            html_ += ' <th>%s</th>' % col
        html_ += ' </tr> </thead> <tbody> '

        for iindex in df.index:
            html_ += ' <tr> '
            for col in cols:
                value = df.loc[iindex, col]
                if col == col_to_checkbox:
                    html_ += (' <td><input type="checkbox" id="%s%s" '
                              'name="%s%s" value="%s"></td>' % (col, value, col, value, value))
                else:
                    html_ += ' <td>%s</td> ' % value
            html_ += ' </tr> '

        html_ += ' </tbody> </table>'

        return html_

    @staticmethod
    def float_to_currency(df, cols=None, format_to="£ {:,.2f}", type_='dataframe'):
        """
        Method to transform columns(cols) from df from float to currency.
        :param df: input data, can be a dataframe or a float
        :param cols: list of cols to cast
        :param format_to: format to apply to the input, by default it is to pounds
        :param type_: defines if the input is a 'dataframe' or a 'float'
        """
        if type_ == 'dataframe':
            for col in cols:
                df[col] = df[col].apply(lambda row: format_to.format(row))

            return df

        elif type_ == 'float':
            string_to = format_to.format(df)

            return string_to

    @staticmethod
    def div_table_for_dash(cell_content, cell_width_size_through_class_name, cell_style,
                           table_style=None, table_class_name='div-table'):
        """
        Method that is a frame builder for tables with tag <div> in dash framework. Parameters cell_content,
        cell_width_size_through_classname & cell_style are lists which have to have same length.
        :param cell_content: is a list of elements valid for dash. It is mandatory
        :param cell_width_size_through_class_name: is to indicate the size of the cell in comparison with the others.
            It is Mandatory. For a cell with the half of the width of the table size:
            .two.adaptdevice {
                width: 50%;
                }
            and cell_width_size_through_class_name should be defined as ['two']
        :param cell_style: list of dicts with the style for each cell. It can be a list of None if no style is wanted.
        :param table_style: style for the table, its a dict.
        :param table_class_name: is the class as defined in the css file
        """

        if (len(cell_content) != len(cell_width_size_through_class_name)) | (len(cell_content) != len(cell_style)):
            raise Exception('Parameters cell_content, cell_width_size_through_class_name '
                            '& cell_style are lists which have to have the same length.')

        cells = []
        for x in range(0, len(cell_content)):
            if cell_style[x]:
                to_cell = html.Div([cell_content[x]],
                                   style=cell_style[x],
                                   className='%s adaptdevice' % cell_width_size_through_class_name[x])
            else:
                to_cell = html.Div([cell_content[x]],
                                   className='%s adaptdevice' % cell_width_size_through_class_name[x])
            cells.append(to_cell)

        if table_style:
            output = html.Div(cells, className=table_class_name, style=table_style)
        else:
            output = html.Div(cells, className=table_class_name)

        return output

    @staticmethod
    def env_var_loader(file_name, file_path=None):
        """ Method that allows to load env variables in local from a file.
        :param file_name: path to file with environment variables
        :param file_path: path to the file, if it is not provided it
                          is assumed that the file is in the root of the project
            """
        if file_path:
            env_path = os.path.join(file_path, file_name)
        else:
            wd = os.getcwd()
            env_path = os.path.join(wd, file_name)

        if os.path.isfile(env_path):
            load_dotenv(dotenv_path=env_path)

    @staticmethod
    def protect_dashviews_with_login(dash_app):
        """
        This method allows to apply login from a flask Server to all pages of a dash app
        :param dash_app: dashapp to protect with login required
        """
        for view_func in dash_app.server.view_functions:
            if view_func.startswith(dash_app.config.routes_pathname_prefix):
                dash_app.server.view_functions[view_func] = login_required(dash_app.server.view_functions[view_func])
