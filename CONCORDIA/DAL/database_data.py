import os
import oracledb


def _get_connection():
    """
    This function initializes the Oracle client and returns a connection object to the database.

    Returns:
    cx_Oracle.Connection: A connection object to the database.
    """
    lib_dir = os.path.join(os.path.dirname(__file__), 'instantclient_21_11')
    oracledb.init_oracle_client(lib_dir=lib_dir)
    return oracledb.connect('etd/ETD@localhost:1521/iut12c')


def _dumpobject(obj):
    """
    Recursively converts an Oracle object into a dictionary.

    Args:
        obj (oracledb.Object): The Oracle object to convert.

    Returns:
        dict: A dictionary representation of the Oracle object.
    """
    if obj.type.iscollection:
        result = []
        for value in obj.aslist():
            if isinstance(value, oracledb.Object):
                result.append(_dumpobject(value))
            else:
                result.append(value)
    else:
        result = {}
        for attr in obj.type.attributes:
            value = getattr(obj, attr.name)
            if isinstance(value, oracledb.Object):
                result[attr.name] = _dumpobject(value)
            else:
                result[attr.name] = value
    return result


def _request_to_list(request):
    """
    Executes the given SQL request and returns the result as a list of objects.

    Args:
        request (str): The SQL request to execute.

    Returns:
        list: A list of objects returned by the SQL request.
    """
    with _get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(request)
            for obj, in cursor:
                return _dumpobject(obj)


def get_concordia_description():
    return _request_to_list("SELECT concordia_description FROM T_Concordia")


def get_concordia_numerals():
    return _request_to_list("SELECT concordia_numeral FROM T_Concordia")


def get_concordia_color_player():
    return _request_to_list("SELECT concordia_color_player FROM T_Concordia")


def get_concordia_goods():
    return _request_to_list("SELECT concordia_good FROM T_Concordia")


def get_concordia_city_tokens():
    return _request_to_list("SELECT concordia_city_token FROM T_Concordia")


def get_concordia_ways():
    return _request_to_list("SELECT concordia_way FROM T_Concordia")


def get_concordia_map():
    return _request_to_list("SELECT concordia_map FROM T_Concordia")


def get_concordia_gods():
    return _request_to_list("SELECT concordia_god FROM T_Concordia")


def get_concordia_cards():
    return _request_to_list("SELECT concordia_card FROM T_Concordia")


def get_concordia_display_area():
    return _request_to_list("SELECT concordia_display_area FROM T_Concordia")


def get_concordia_setup_player():
    return _request_to_list("SELECT concordia_setup_player FROM T_Concordia")
