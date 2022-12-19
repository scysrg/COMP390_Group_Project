"""Executes the starting code telling the program to begin"""
import command_funcs


if __name__ == '__main__':
    """Runs the code"""
    command_funcs.enter_database_data()
    print(f'\n-----\nHousehold Electronics, Inc. Marketplace Search\n-----', end='\n\n')
    while command_funcs.handle_query():
        pass
