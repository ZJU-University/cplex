import logging

LOGGER = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    datefmt='%m/%d/%Y %H:%M:%S'
)


def try_except(func):
    def handler(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            print(e)

    return handler


if __name__ == '__main__':
    from prettytable import PrettyTable

    def create_class4_q2():
        table = PrettyTable(['factory', 'BS', 'LSKL', 'DLS'])
        table.add_row(['JSBT', 12, 15, 17])
        table.add_row(['DWE', 14, 9, 10])
        table.add_row(['MK', 13, 20, 11])
        table.add_row(['SEM', 17, 16, 19])
        table.add_row(['GLB', 7, 14, 12])
        table.add_row(['YLD', 22, 16, 18])
        print(table)

        table = PrettyTable(['factory', 'Weekly Waste Volume (barrels)'])
        table.add_row(['JSBT', 35])
        table.add_row(['DWR', 26])
        table.add_row(['MK', 42])
        table.add_row(['SEM', 53])
        table.add_row(['GLB', 29])
        table.add_row(['YLD', 38])
        print(table)

        table = PrettyTable(['factory', 'JSBT', 'DWR', 'MK', 'SEM', 'GLB', 'YLD'])
        table.add_row(['JSBT', 0, 6, 4, 9, 7, 8])
        table.add_row(['DWR', 6, 0, 11, 10, 12, 7])
        table.add_row(['MK', 5, 11, 0, 3, 7, 15])
        table.add_row(['SEM', 9, 10, 3, 0, 3, 16])
        table.add_row(['GLB', 7, 12, 7, 3, 0, 14])
        table.add_row(['YLD', 8, 7, 15, 16, 14, 0])
        print(table)

        table = PrettyTable(['Refuse disposal point', 'BS', 'LSKL', 'DLS'])
        table.add_row(['BS', 0, 12, 10])
        table.add_row(['LSKL', 12, 0, 15])
        table.add_row(['DLS', 10, 15, 0])
        print(table)

    create_class4_q2()
