# -*- coding: UTF-8 -*-
import pymysql

tup = []


def table_creation(passw, table_name, tuplas):
    db = pymysql.connect(host='localhost', user='root', passwd=passw, db='bayes')
    print('Enter the names of the fields: ')

    for i in range(0, tuplas):
        name = input(f'Field name {i}:').lower()
        tup.append(name)

    cursor = db.cursor()
    if len(tup) == 3:
        var1, var2, var3 = tup[0], tup[1], tup[2]
        query = f"CREATE TABLE {table_name}(id INT AUTO_INCREMENT PRIMARY KEY, {var1} VARCHAR(30), " \
                f"{var2} VARCHAR(30), {var3} VARCHAR(30));"

    elif len(tup) == 4:
        var1, var2, var3, var4 = tup[0], tup[1], tup[2], tup[3]
        query = f"CREATE TABLE {table_name}(id INT AUTO_INCREMENT PRIMARY KEY, {var1} VARCHAR(30), " \
                f"{var2} VARCHAR(30), {var3} VARCHAR(30), {var4} VARCHAR(30));"

    elif len(tup) == 5:
        var1, var2, var3, var4, var5 = tup[0], tup[1], tup[2], tup[3], tup[4]
        query = f"CREATE TABLE {table_name}(id INT AUTO_INCREMENT PRIMARY KEY, {var1} VARCHAR(30), " \
                f"{var2} VARCHAR(30), {var3} VARCHAR(30), {var4} VARCHAR(30), {var5} VARCHAR(30));"

    elif len(tup) == 6:
        var1, var2, var3, var4, var5, var6 = tup[0], tup[1], tup[2], tup[3], tup[4], tup[5]
        query = f"CREATE TABLE {table_name}(id INT AUTO_INCREMENT PRIMARY KEY, {var1} VARCHAR(30), " \
                f"{var2} VARCHAR(30),{var3} VARCHAR(30), {var4} VARCHAR(30), {var5} VARCHAR(30), {var6} VARCHAR(30));"

    cursor.execute(query)
    cursor.close()
    db.close()


def data_injection(passw, table_name):
    data = []
    db = pymysql.connect(host='localhost', user='root', passwd=passw, db='bayes')
    cursor = db.cursor()
    query = f"DESCRIBE {table_name};"
    cursor.execute(query)
    field_names = [i[0] for i in cursor.fetchall()]
    num_field = len(field_names)
    print(f"You've to fill this values: {field_names}")

    for i in range(0, num_field):
        if field_names[i] == 'id':
            print("--->> ID is auto_increment, you should not insert anything\n")
        else:
            var = str(input(f'Enter the value for {field_names[i]}: '))
            data.append(var)

    if len(data) == 3:
        var1, var2, var3 = data[0], data[1], data[2]
        cursor.execute(f"INSERT INTO {table_name} VALUES (%s,%s,%s,%s)", (0, var1, var2, var3))

    elif len(data) == 4:
        var1, var2, var3, var4 = data[0], data[1], data[2], data[3]
        cursor.execute(f"INSERT INTO {table_name} VALUES (%s,%s,%s,%s,%s)", (0, var1, var2, var3, var4))

    elif len(data) == 5:
        var1, var2, var3, var4, var5 = data[0], data[1], data[2], data[3], data[4]
        cursor.execute(f"INSERT INTO {table_name} VALUES (%s,%s,%s,%s,%s,%s)", (0, var1, var2, var3, var4, var5))

    elif len(data) == 6:
        var1, var2, var3, var4, var5, var6 = data[0], data[1], data[2], data[3], data[4], data[5]
        cursor.execute(f"INSERT INTO {table_name} VALUES (%s,%s,%s,%s,%s,%s, %s)",
                       (0, var1, var2, var3, var4, var5, var6))

    cursor.close()
    db.commit()
    db.close()


def rename_fields(passw, table_name):
    db = pymysql.connect(host='localhost', user='root', passwd=passw, db='bayes')
    cursor = db.cursor()
    query = f"DESCRIBE {table_name};"
    cursor.execute(query)
    field_names = [i[0] for i in cursor.fetchall()]

    field = str(input(f"Table fields: {field_names} \n-> What field do you want to rename?"
                      f" (Remember that ID field can't be changed)\nInput: "))
    while field not in field_names or field == 'id' or field == "":
        field = str(input(f'Please select another field: '))

    new_field = str(input('New field name: '))
    cursor.execute(f"ALTER TABLE `{table_name}` CHANGE COLUMN `{field}` `{new_field}` varchar(30);")
    cursor.close()
    db.commit()
    db.close()


def update_data(passw, table_name):
    db = pymysql.connect(host='localhost', user='root', passwd=passw, db='bayes')
    cursor = db.cursor()
    query = f'DESCRIBE {table_name};'
    cursor.execute(query)
    field_names = [i[0] for i in cursor.fetchall()]
    print(field_names)
    num_fields = len(field_names)
    print(f'\nYou have {num_fields} registers')

    # Describe table function

    field = str(input(f"Which field do you want to make the change?\nInput: "))
    data = str(input('What is the new value to assign?\nInput: '))
    id_value = int(input('Enter the value of the id to which the record belongs:\nInput: '))

    cursor.execute(f"UPDATE {table_name} SET {field} = {data} WHERE id = {id_value};")
    cursor.close()
    db.commit()
    db.close()
