import sqlite3

""" SPENDBOSS WEBSITE - database_handler.py
    This is the main file for handling the database. Any input or output will be handled here.

    DEVELOPERS NOTE:
    - function open and closes database each time to enable multiple users.
    - Multi-threading for multiple user handling will be implemented in the future.
"""


def db_create():
    """ Create Database
    Open the database and execute the table building command.
     """
    conn = sqlite3.connect('SPENDBOSS_DATABASE.db')
    cur = conn.cursor()
    cur.execute(
        'CREATE TABLE IF NOT EXISTS user_base('
        'id INTEGER PRIMARY KEY, '
        'email TEXT NOT NULL, '
        'fname TEXT, '
        'surname TEXT, '
        'password TEXT NOT NULL, '
        'status INTEGER NOT NULL, '
        'date_joined NUMERIC NOT NULL)')
    cur.execute(
        'CREATE TABLE IF NOT EXISTS financial_base('
        'id INTEGER PRIMARY KEY, '
        'user_id INTEGER NOT NULL, '
        'date NUMERIC NOT NULL, '
        'days_after INTEGER NOT NULL, '
        'hand REAL, '
        'bank REAL, '
        'spent REAL, '
        'additional REAL, '
        'cutters REAL, '
        'work REAL, '
        'skip INTEGER)')
    cur.execute(
        'CREATE TABLE IF NOT EXISTS wish_list('
        'id INTEGER PRIMARY KEY, '
        'user_id INTEGER NOT NULL, '
        'price REAL NOT NULL, '
        'name TEXT)')
    conn.commit()
    conn.close()


def db_insert(input_table, entry):
    """ Insertion of variable to database
    Open the database, declare and build a string variable that 
    will be passed to the executable method. Then execute method.
    
    :param input_table: table name that you want to insert to
    :param entry: the variable inputs that you want to insert
    
    IF table inserted not exist
        :return: Print Database not exist
    ELSE IF database syntax error
        :return: Print Database insertion error
    ELSE
        no return, database close
    """
    conn = sqlite3.connect('SPENDBOSS_DATABASE.db')
    cur = conn.cursor()
    try:
        if input_table == "userbase":
            insert_tbl = 'INSERT INTO user_base (email, fname, surname, password, status, date_joined) VALUES ('
        elif input_table == "finance":
            insert_tbl = 'INSERT INTO financial_base (user_id, date, days_after, hand, bank, spent, additional, ' \
                         'cutters, work, skip) VALUES ('
        elif input_table == "wish":
            insert_tbl = 'INSERT INTO wish_list (user_id, price, name) VALUES ('
        else:
            return print("DATABASE TABLE NOT EXIST..\n")

        for value in entry:
            if type(value) == str:
                value = "'%s'" % value
            insert_tbl += str(value)
            insert_tbl += ", "

        insert_tbl = insert_tbl[:-2] + ");"
        cur.execute(insert_tbl)

    except Exception as e:
        print("DATABASE INSERTION ERROR: \n%s" % e)

    conn.commit()
    conn.close()


def db_query(value, table, condition):
    """ Querying of variables to database
    Open the database, declare and build a string variable that will be passed to the executable method. 
    Then execute method and set all return values to a variable. If data is empty then return.
    Structure the output value into a readable string (NEEDED FOR TESTING) and return the value tuple.
    
    :param value: string with value names
    :param table: string table name
    :param condition: None or string conditional
    IF query successful
        :return: tuple with data
    ELSE
        :return: False
    """
    conn = sqlite3.connect('SPENDBOSS_DATABASE.db')
    cur = conn.cursor()

    command = "SELECT %s FROM %s" % (value, table)
    if condition:
        command += " WHERE %s" % condition
    command += ";"

    try:
        cur.execute(command)
        ori_output = cur.fetchall()
        if not ori_output:
            print("\nDATA NOT FOUND\n")
            return False
        output_no = len(ori_output)
        element_no = len(ori_output[0])
        w_output = ""
        for x in range(output_no):
            data_tpl = ori_output[x]
            data_str = ""
            for y in range(element_no):
                data_str += str(data_tpl[y]) + "\t"
            w_output += data_str + "\n"
        print(w_output)
        return data_tpl

    except sqlite3.OperationalError:
        print("\nQUERY COMMAND CANNOT BE READ\n")
        return False


def database_config_testing():
    """ Database Unit Testing Function
    Each testing names could be seen on print string below.
    Print functions are to indicate the testing phase.
    
    Tested: 05/04/17
    Result: All Passed
    """
    print("1. Creating db")
    db_create()

    print("2. Insert userbase")
    db_insert("userbase", ["putraa", "adrian", "pratama putra", "password", "personal", "2010-12-30"])

    print("3. Insert finance")
    db_insert("finance", [1, "2011-12-32", 13, 23.0, 1324.43, 200, 10, 30, 5, 0])

    print("4. Insert wish")
    db_insert("wish", [1, 20, "iphone"])

    print("5. Select all data")
    db_query("*", "user_base", None)

    print("6. Select specific data")
    db_query("email, password", "user_base", None)

    print("7. Select specific data with conditional")
    a = db_query("email, password", "user_base", "id=%s AND password='%s'" % (1, "password"))
    print(a)

    print("# DONE #")




