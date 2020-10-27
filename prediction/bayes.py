from functools import reduce
from typing import List

import pymysql

normal: List[int]
data, normal = [], []


def rule(cas):
    if chr(97) <= cas[0] <= chr(122):
        return 1
    else:
        return 0


def normalize_table(passw, table_name):
    try:
        count = 1
        db = pymysql.connect(host='localhost', user='root', passwd=passw, db='bayes')
        cursor = db.cursor()
        cursor.execute(f'DESCRIBE {table_name}')

        field_names = [i[0] for i in cursor.fetchall()]

        limit = cursor.execute(f"SELECT * FROM {table_name};")
        limited = limit + 2

        for j in field_names:
            if count != limited:
                if j != 'id':
                    cursor.execute(f'SELECT {j} FROM {table_name};')
                    num = cursor.fetchall()
                    for k in num:
                        cas = ''.join(k)

                        """ Casting if you need a int """
                        if cas != "":
                            flag = rule(cas)

                            if flag == 0:
                                global converted_value
                                converted_value = int(cas)

                                if j == 'edad' or j == 'Edad' and num != '':
                                    """Age normalization"""
                                    if 1 <= converted_value <= 37:
                                        cursor.execute(f"UPDATE {table_name} SET {j} = 'joven' WHERE id = {count};")
                                        db.commit()
                                    else:
                                        cursor.execute(f"UPDATE {table_name} SET {j} = 'mayor' WHERE id = {count};")
                                        db.commit()

                                elif j == 'Hijos' or j == 'hijos' and num != '':
                                    """Children normalization"""
                                    if converted_value >= 1:
                                        cursor.execute(f"UPDATE {table_name} SET {j} = 'si' WHERE id = {count};")
                                        db.commit()
                                    else:
                                        cursor.execute(f"UPDATE {table_name} SET {j} = 'no' WHERE id = {count};")
                                        db.commit()

                                elif j == 'Salario' or j == 'salario' and num != '':
                                    if 0 <= converted_value <= 5000:
                                        cursor.execute(f"UPDATE {table_name} SET {j} = 'bajo' WHERE id = {count};")
                                        db.commit()
                                    elif 5000 < converted_value <= 20000:
                                        cursor.execute(f"UPDATE {table_name} SET {j} = 'medio' WHERE id = {count};")
                                        db.commit()
                                    elif converted_value >= 20000:
                                        cursor.execute(f"UPDATE {table_name} SET {j} = 'alto' WHERE id = {count};")
                                        db.commit()

                            elif k == 'si' or k == 'no':
                                """not change"""

                            converted_value, cas = '', ''
                            count = count + 1

            count = 1
        cursor.close()
        db.close()
    except IOError:
        print(IOError)


def caster(rows):
    i = ''.join(map(str, rows))
    for j in i:
        if chr(48) <= j <= chr(57):
            final_value = int(j)
            break

    return final_value


def castingRows(rows):
    final_value = ''
    i = ''.join(map(str, rows))
    for j in i:
        if chr(48) <= j <= chr(57):
            final_value += str(j)
    var_fin = int(final_value)
    return var_fin


def count_rows(table_name, passw):
    db = pymysql.connect(host='localhost', user='root', passwd=passw, db='bayes')
    cursor = db.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
    rows = cursor.fetchall()
    final = castingRows(rows)

    return final


def prediction(passw, table_name, value_to_calculate):
    try:
        global value
        db = pymysql.connect(host='localhost', user='root', passwd=passw, db='bayes')
        cursor = db.cursor()
        query = f'DESCRIBE {table_name}'
        cursor.execute(query)

        final_rows = count_rows(table_name, passw)
        f = final_rows - 1

        field_names = [i[0] for i in cursor.fetchall()]

        print(f'\nYou have: {final_rows} registers (The last record needs a piece of information)\n')
        id_value = int(input('Enter the id of the field you want to calculate:\nInput: '))
        while id_value > final_rows or id_value <= 0:
            id_value = int(input('Please, enter a correct id: '))

        type_result = str(input('\nDo you want to know if the result is YES or NO? Please, enter y/n: ')).lower()
        while 'y' != type_result and type_result != 'n':
            type_result = str(input('Please, only y/n: ')).lower()

        """ BAYES FORMULA: P(H|E)=P(E|H)*P(H) """
        h, r = value_to_calculate, type_result

        """ FIRST STEP """
        if r == 'y':
            cursor.execute(f"SELECT COUNT(*) FROM {table_name} WHERE {h} = 'si';")
            obtain = cursor.fetchall()
            value = caster(obtain)
            first_step = (value / f)

            """ SECOND STEP """
            for i in field_names:
                if i != value_to_calculate and i != 'id':
                    cursor.execute(f"SELECT {i} FROM {table_name} WHERE id={id_value};")
                    condition = cursor.fetchone()

                    """CASTING TUPLE"""
                    cast = ''.join(condition)

                    cursor.execute(
                        f"SELECT COUNT({i}) FROM {table_name} WHERE {i} = '{cast}' and {value_to_calculate} = 'si';")
                    result = cursor.fetchall()
                    cas = caster(result)
                    res = (cas / value)
                    normal.append(res)

            second_step = reduce(lambda x, y: x * y, normal)

            """ THIRD STEP """
            p = (second_step * first_step)
            final_percent = (p * 100)

        else:
            cursor.execute(f"SELECT COUNT(*) FROM {table_name} WHERE {h} = 'no';")
            obtain = cursor.fetchall()
            value = caster(obtain)
            first_step = (value / f)

            """ SECOND STEP """
            for i in field_names:
                if i != value_to_calculate and i != 'id':
                    cursor.execute(f"SELECT {i} FROM {table_name} WHERE id={id_value};")
                    condition = cursor.fetchone()

                    """CASTING TUPLE"""
                    cast = ''.join(condition)

                    cursor.execute(
                        f"SELECT COUNT({i}) FROM {table_name} WHERE {i} = '{cast}' and {value_to_calculate} = 'si';")
                    result = cursor.fetchall()
                    cas = caster(result)
                    res = (cas / value)
                    normal.append(res)

            second_step = reduce(lambda x, y: x * y, normal)

            """ THIRD STEP """
            p = (second_step * first_step)
            final_percent = (p * 100)

        """ UPDATING FINAL DATA"""
        if final_percent > 6.0:
            print('\nYES :) WITH A: ', final_percent)
            cursor.execute(f"UPDATE {table_name} SET {value_to_calculate} = 'si' WHERE id = {id_value};")
        else:
            print('\nNO :( WITH A: ', final_percent)
            cursor.execute(f"UPDATE {table_name} SET {value_to_calculate} = 'no' WHERE id = {id_value};")

        cursor.close()
        db.commit()
        db.close()
    except IOError:
        print(IOError)


def data_prediction(passw, table_name):
    db = pymysql.connect(host='localhost', user='root', passwd=passw, db='bayes')
    cursor = db.cursor()
    query = f'DESCRIBE {table_name}'
    cursor.execute(query)

    field_names = [i[0] for i in cursor.fetchall()]
    print(f'Available values: {field_names}')

    value_to_calculate = str(input('No counting ID, what value do you want to calculate?\nInput: '))
    position = field_names.index(value_to_calculate)
    void = ""
    num_field = len(field_names)
    for i in range(0, num_field):
        if field_names[i] != 'id' and field_names[i] != value_to_calculate:
            value = str(input(f'Enter the value for {field_names[i]}: '))
            data.append(value)

    if len(data) == 2:
        if num_field == 4:
            if position == 1:
                cursor.execute(f'INSERT INTO {table_name} VALUES (%s,%s,%s,%s)', (0, void, data[0], data[1]))
            elif position == 2:
                cursor.execute(f'INSERT INTO {table_name} VALUES (%s,%s,%s,%s)', (0, data[0], void, data[1]))
            elif position == 3:
                cursor.execute(f'INSERT INTO {table_name} VALUES (%s,%s,%s,%s)', (0, data[0], data[1], void))
    elif len(data) == 3:
        if num_field == 5:
            if position == 1:
                cursor.execute(f'INSERT INTO {table_name} VALUES (%s,%s,%s,%s,%s)',
                               (0, void, data[0], data[1], data[2]))
            elif position == 2:
                cursor.execute(f'INSERT INTO {table_name} VALUES (%s,%s,%s,%s,%s)',
                               (0, data[0], void, data[1], data[2]))
            elif position == 3:
                cursor.execute(f'INSERT INTO {table_name} VALUES (%s,%s,%s,%s,%s)',
                               (0, data[0], data[1], void, data[2]))
            elif position == 4:
                cursor.execute(f'INSERT INTO {table_name} VALUES (%s,%s,%s,%s,%s)', (0, data[0], data[1], data[2], void))
    elif len(data) == 4:
        if num_field == 6:
            if position == 1:
                cursor.execute(f'INSERT INTO {table_name} VALUES (%s,%s,%s,%s,%s,%s)',
                               (0, void, data[0], data[1], data[2], data[3]))
            elif position == 2:
                cursor.execute(f'INSERT INTO {table_name} VALUES (%s,%s,%s,%s,%s,%s)',
                               (0, data[0], void, data[1], data[2], data[3]))
            elif position == 3:
                cursor.execute(f'INSERT INTO {table_name} VALUES (%s,%s,%s,%s,%s,%s)',
                               (0, data[0], data[1], void, data[2]), data[3])
            elif position == 4:
                cursor.execute(f'INSERT INTO {table_name} VALUES (%s,%s,%s,%s,%s,%s)',
                               (0, data[0], data[1], data[2], void, data[3]))
            elif position == 5:
                cursor.execute(f'INSERT INTO {table_name} VALUES (%s,%s,%s,%s,%s,%s)',
                               (0, data[0], data[1], data[2], data[3], void))
    elif len(data) == 5:
        if num_field == 7:
            if position == 1:
                cursor.execute(f'INSERT INTO {table_name} VALUES (%s,%s,%s,%s,%s,%s,%s)',
                               (0, void, data[0], data[1], data[2], data[3], data[4]))
            elif position == 2:
                cursor.execute(f'INSERT INTO {table_name} VALUES (%s,%s,%s,%s,%s,%s,%s)',
                               (0, data[0], void, data[1], data[2], data[3], data[4]))
            elif position == 3:
                cursor.execute(f'INSERT INTO {table_name} VALUES (%s,%s,%s,%s,%s,%s,%s)',
                               (0, data[0], data[1], void, data[2], data[3], data[4]))
            elif position == 4:
                cursor.execute(f'INSERT INTO {table_name} VALUES (%s,%s,%s,%s,%s,%s,%s)',
                               (0, data[0], data[1], data[2], void, data[3], data[4]))
            elif position == 5:
                cursor.execute(f'INSERT INTO {table_name} VALUES (%s,%s,%s,%s,%s,%s,%s)',
                               (0, data[0], data[1], data[2], data[3], void, data[4]))
            elif position == 6:
                cursor.execute(f'INSERT INTO {table_name} VALUES (%s,%s,%s,%s,%s,%s,%s)',
                               (0, data[0], data[1], data[2], data[3], data[4], void))

    cursor.close()
    db.commit()
    db.close()

    normalize_table(passw, table_name)
    prediction(passw, table_name, value_to_calculate)
