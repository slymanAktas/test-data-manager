from tdm.constant import csv_resources_path
from tdm.helpers.decorators import timer


def read_from_csv(csv_name):
    file = open(csv_resources_path + csv_name, "r", encoding="utf - 8")
    data_list = file.readlines()
    file.close()

    return list(map(lambda x: x.replace("\n", ""), data_list))


@timer
def write_to_csv(csv_path, text):
    seperator = '\n' if str(csv_path).__contains__('sku') else ',\n'
    with open(csv_path, "w+", encoding="utf-8") as file:
        for i in text:
            file.write(i + seperator)
