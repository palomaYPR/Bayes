# -*- coding: UTF-8 -*-
from conexiones import db
from prediction import bayes as by

bd_name, table_name, option = '', '', 1

if __name__ == "__main__":
    print('Before running, create a database called Bayes...')
    password = str(input('Enter your MySQL password: '))

    while 1 <= option <= 5:
        try:
            option = int(input('\n-> Select an option:\n'
                               "1.- Data injection and Calculate prediction\n"
                               '2.- Create table\n'
                               '3.- Data injection\n'
                               '4.- Rename fields\n'
                               '5.- Update data\n'
                               'Input: '))

            if option == 1:
                print('\n********* Prediction **********')
                table_name = str(input('Enter table name: '))
                by.data_prediction(password, table_name)

            elif option == 2:
                print('\n********** Table Creation **********')
                table_name = str(input('Enter table name: '))
                fields = int(input('Number of fields (Without taking into account the ID): '))
                db.table_creation(password, table_name, fields)

            elif option == 3:
                print('\nm********* Data injection **********')
                table_name = str(input('Enter table name: '))
                db.data_injection(password, table_name)

            elif option == 4:
                print('\n********** Rename fields **********')
                table_name = str(input('Enter table name: '))
                db.rename_fields(password, table_name)

            elif option == 5:
                print('\n********** Update data in table **********')
                table_name = input('Enter table name: ')
                db.update_data(password, table_name)

        except ValueError:
            print('Oops! That was no valid number. Try Again...')
