import os
from flask_login import login_required


class Miscellaneous:
    """Collection of functions to solve different problems"""
    @staticmethod
    def to_html_with_checkbox(df, col_to_checkbox, table_class=None):
        """
        Method that takes a data and returns a html table which contains a checkbox on column col_to_checkbox.

        Args:
            df: dataframe to create html table with checkbox
            col_to_checkbox: column to transform into a checkbox
            table_class: class of the table to get style from css file
        Returns: html table which contains a checkbox on column col_to_checkbox
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
    def float_to_currency(data, cols=None, format_to="£ {:,.2f}", type_of_input='dataframe'):
        """
        Method to transform variable from float to currency. It can be a float or a dataframe.
        If decimals are reduced, it rounds up.

        Args:
            data: data to convert to currency, can be a dataframe or a float
            cols: if data is a pandas dataframe, list of cols to cast
            format_to: format to apply to the input, by default it is to pounds
            type_of_input: defines if the input is a 'dataframe' or a 'float'
        Returns:
            - If data is a pandas dataframe, it returns a dataframe were all columns in col are cast to currency
            formatted as indicated in format_to
            - If data is a float, it returns a string formatted as indicated in format_to.
        """
        if type_of_input == 'dataframe':
            for col in cols:
                data[col] = data[col].apply(lambda row: format_to.format(row))

            return data

        elif type_of_input == 'float':
            string_to = format_to.format(data)

            return string_to

    @staticmethod
    def env_var_loader(file_name, file_path=None):
        """ Method that allows to load environment variables from a file.

        Args:
            file_name: path to file with environment variables
            file_path: path to the file, if it is not provided it is assumed that the file is in the root of the project
            """
        if file_path:
            env_path = os.path.join(file_path, file_name)
        else:
            wd = os.getcwd()
            env_path = os.path.join(wd, file_name)

        if os.path.isfile(env_path):
            with open(env_path) as file:
                for line in file:
                    line_list = line.split("=")
                    os.environ[line_list[0].strip()] = line_list[1].strip()

    @staticmethod
    def protect_dash_views_with_login(dash_app):
        """
        This method allows to apply CSRF protection (login authentication) to all pages of a dash app

        Args:
            dash_app: dash app to protect with login required
        """
        for view_func in dash_app.server.view_functions:
            if view_func.startswith(dash_app.config.routes_pathname_prefix):
                dash_app.server.view_functions[view_func] = login_required(dash_app.server.view_functions[view_func])
