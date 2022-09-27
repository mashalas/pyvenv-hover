#!/usr/bin/python3

import re
import pprint

filename = "iris.csv"

def get_data_type(s):
    if len(s) == 0:
        return "-"
    try:
        x = int(s)
        return "i"
    except:
        pass
    try:
        s1 = s.replace(",", ".")
        x = float(s1)
        return "f"
    except:
        pass
    return "s"


def is_int(s):
    try:
        x = int(s)
        return True
    except:
        pass
    return False


def is_float(s):
    s = s.replace(",", ".")
    try:
        x = float(s)
        return True
    except:
        pass
    return False


def read_table(filename, Header, DataTypes, divider = ",", first_row_is_header = True, data_rows_max_count = -1, continue_on_wrong_columns_count = False):
    DataTable = []
    Header.clear()
    DataTypes.clear()
    f = open(filename, "rt")
    data_rows_count = 0
    columns_count = -1
    for s in f:
        s = s.strip()
        if s[0] == "#": # комментарий
            continue
        Parts = s.split(divider)
        if columns_count < 0:
            # читается первая строка с данным, количество столбцов во всей таблице должно совпадать с количеством столбцов в первой прочитанной строке
            columns_count = len(Parts)
            if first_row_is_header: # первая строка - названия столбцов
                for i in range(len(Parts)):
                    Header.append(Parts[i])
                continue
        if len(Parts) != columns_count:
            # в новой строке количество столбцов отличается от количества столбцов в предыдущих строках
            if continue_on_wrong_columns_count:
                continue
            DataTable = None
            break
        if len(DataTypes) == 0:
            # типы данных ещё не определялись
            for i in range(len(Parts)):
                if is_int(Parts[i]):
                    DataTypes.append("i")
                    continue
                if is_float(Parts[i]):
                    DataTypes.append("f")
                    continue
                DataTypes.append("s")
        DataTable.append([])
        for i in range(len(Parts)):
            if DataTypes[i] == "i":
                DataTable[data_rows_count].append(int(Parts[i]))
            elif DataTypes[i] == "f":
                DataTable[data_rows_count].append(float(Parts[i].replace(",", ".")))
            else:
                DataTable[data_rows_count].append(Parts[i])
        data_rows_count += 1
        if data_rows_max_count > 0 and data_rows_count >= data_rows_max_count:
            break
    f.close()
    return DataTable

if __name__ == "__main__":
    Header = ["some", "thing", "unnecessary"]
    DataTypes = []
    tbl = read_table(filename, Header, DataTypes, divider = ",")
    pprint.pprint(tbl[0:5])
    print("Header:", Header)
    print("DataTypes:", DataTypes)
