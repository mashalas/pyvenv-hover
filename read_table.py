#!/usr/bin/python3

import datetime
import math
import pprint
#import re


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


def symbol_is_digit(s, p):
    #if len(s) != 1:
    #    return False #длина не 1 символ
    #return s.isdigit()
    if len(s)-1 < p:
        return False # в строке нет символа с индексом p
    return s[p].isdigit()

def is_digit_range(s, since, stop):
    s1 = s[since:stop]
    return s1.isdigit()

def is_date(s):
    #if
    #matches = re.find(r"(\d\d).(\d\d).(\d\d\d\d)")
    #print(matches)
    # dd.mm.yyyy
    # 01234567890
    if len(s) < 10:
        return False # недостаточно символов, чтобы уместилась дата
    if is_digit_range(s, 0, 2) and is_digit_range(s, 3, 5) and is_digit_range(s, 6, 10) and s[2] in [".", "-"] and s[5] in [".", "-"]:
        # dd.mm.yyyy  или dd-mm-yyyy
        return True

    #yyyy.mm.dd
    #01234567890
    if is_digit_range(s, 0, 4) and is_digit_range(s, 5, 7) and is_digit_range(s, 8, 10) and s[4] in [".", "-"] and s[7] in [".", "-"]:
        return True
    #if symbol_is_digit(s[0]) and
    return False


def parse_str(s):
    # int
    try:
        x = int(s)
        return ["i", x]
    except:
        pass

    # float
    s1 = s.replace(",", ".")
    try:
        x = float(s1)
        return ["f", x]
    except:
        pass

    year = None
    month = None
    day = None
    hour = 0
    minute = 0
    second = 0
    # dd.mm.yyyy
    # 01234567890
    if is_digit_range(s, 0, 2) and is_digit_range(s, 3, 5) and is_digit_range(s, 6, 10): #and s[2] in [".", "-"] and s[5] in [".", "-"]:
        # dd.mm.yyyy или dd-mm-yyyy
        day = int(s[0:2])
        month = int(s[3:5])
        year = int(s[6:10])

    #yyyy.mm.dd
    #01234567890
    if is_digit_range(s, 0, 4) and is_digit_range(s, 5, 7) and is_digit_range(s, 8, 10): #and s[4] in [".", "-"] and s[7] in [".", "-"]:
        # yyyy.mm.dd или yyyy-mm-dd
        year = int(s[0:4])
        month = int(s[5:7])
        day = int(s[8:10])

    if year != None:
        # dd.mm.yyyy hh:mm:ss
        # 01234567890123456789
        if len(s) >= 13:
            if is_digit_range(s, 11, 13):
                hour = int(s[11:13])
            else:
                year = None
        if len(s) >= 16:
            if is_digit_range(s, 14, 16):
                minute = int(s[14:16])
            else:
                year =None

        if len(s) >= 19:
            if is_digit_range(s, 17, 19):
                second = int(s[17:19])
            else:
                year = None
        if len(s) > 19:
            year = None
        if year != None:
            try:
                x = datetime.datetime(year, month, day, hour, minute, second)
                return ["d", x]
            except:
                pass

    return ["s", s]

#s3 = "123,5.5";
#s3 = "29.09.2022 11:12:13"
#parsed = parse_str(s3)
#print(parsed)
#data_type, data_value = parse_str(s3)
#print(data_type, data_value)
#exit(0)
"""
s1 = "12.13.2025"
s2 = "2022.05.30"
t1 = is_date(s1)
t2 = is_date(s2)
print(s1, t1)
print(s2, t2)
#print(is_digit_range("12a", 2, 3))
exit(0)
"""

"""X = [5,6,7]
X.insert(0, 124)
print(X)
exit(0)"""

def read_table(filename, divider = ",", read_since_line = 0, skip_first_data_rows_count = 0, data_rows_max_count = -1, continue_on_wrong_columns_count = False, add_serial_number_column_with_name = ""):
    Result = {"Data":[], "ColumnsNames":[], "ColumnsTypes":[], "Errors":[], "filename": filename}
    try:
        f = open(filename, "rt")
    except:
        Result["Errors"].append("Cannot open file \"{}\"" . format(filename))
        return Result
    data_rows_count = 0
    raw_row_number = -1
    #file_columns_count = -1 # количество столбцов в файле; определяется по первой строке не являющейся комментарием; при добавлении столбца с серийным номером строки будет на 1 меньше Result["ColumnsNames"]
    for s in f:
        raw_row_number += 1
        s = s.strip()
        if s[0] == "#": # комментарий
            continue
        Parts = s.split(divider)
        if len(Result["ColumnsNames"]) == 0:
            # читается первая строка с названиями столбцов, количество столбцов во всей таблице должно совпадать с количеством столбцов в первой прочитанной строке
            #file_columns_count = len(Parts)
            if len(add_serial_number_column_with_name) > 0:
                # добавить столбец с сериным номером строки
                Result["ColumnsNames"].append(add_serial_number_column_with_name)
            for i in range(len(Parts)):
                Result["ColumnsNames"].append(Parts[i])
            continue
        if len(add_serial_number_column_with_name) > 0:
            # добавить столбец с серийным номером
            Parts.insert(0, data_rows_count)
        if len(Parts) != len(Result["ColumnsNames"]):
            # в новой строке количество столбцов отличается от количества столбцов в предыдущих строках
            if continue_on_wrong_columns_count:
                continue # пропустить эту строку и перейти к следующей
            # выход с ошибкой
            fact_columns_count = len(Parts)
            need_columns_count = len(Result["ColumnsNames"])
            if len(add_serial_number_column_with_name) > 0:
               fact_columns_count -= 1
               need_columns_count -= 1
            Result["Errors"].append("At row={} columns_count={} but shoudl be {} [{}]" . format(raw_row_number, fact_columns_count, need_columns_count, s))
            break
        if len(Result["ColumnsTypes"]) == 0:
            # типы данных ещё не определялись
            for i in range(len(Parts)):
                data_type, data_value = parse_str(Parts[i])
                Result["ColumnsTypes"].append(data_type)
        Result["Data"].append([])
        for i in range(len(Parts)):
            data_type, data_value = parse_str(Parts[i])
            if data_type == "i" and Result["ColumnsTypes"][i] == "f":
                data_type = "f"
                data_value = float(data_value)
            if data_type != "s" and Result["ColumnsTypes"][i] == "s":
                data_type = "s"
                data_value = str(data_value)
            if data_type == "f" and Result["ColumnsTypes"][i] == "i":
                for j in range(data_rows_count):
                    Result["Data"][j][i] = float(Result["Data"][j][i])
                Result["ColumnsTypes"][i] = "f"
            if data_type == "s" and Result["ColumnsTypes"][i] != "s":
                for j in range(data_rows_count):
                    Result["Data"][j][i] = str(Result["Data"][j][i])
                Result["ColumnsTypes"][i] = "s"
            if data_type == Result["ColumnsTypes"][i]:
                Result["Data"][data_rows_count].append(data_value)
            else:
                Result["Errors"].append("Wrong datatype at {}:{} [{}]" . format(raw_row_number, i, s))
                break
        if len(Result["Errors"]) > 0:
            break
        data_rows_count += 1
        if data_rows_max_count > 0 and data_rows_count >= data_rows_max_count:
            break
    f.close()
    return Result


def mean(X):
    return float(sum(X)) / float(len(X))

def stddev(X):
    m = mean(X)
    st = 0.0
    for i in range(len(X)):
        d = X[i] - m;
        st += d*d
    st /= len(X)
    st = math.sqrt(st)
    return st


def array_to_str(X, divider = " ", max_count = -1):
    s = ""
    for i in range(len(X)):
        if max_count >= 0 and i >= max_count:
            s += divider + "..."
            break
        if s != "":
            s += divider
        s += str(X[i])
    return s


def table_info(A, print_since=0, print_stop=3, digits = 5, lower_procentile=0.02, upper_procentile=0.98):
    PRINT_MAX_COUNT = 10 # максимальное количество отображаемых строк или целых чисел
    print("----- Data -----")
    print("Rows since={} until={}" . format(print_since, print_stop))
    pprint.pprint(A["Data"][print_since:print_stop])
    print("----------------")
    if len(A["filename"]) > 0:
        print("filename: " + A["filename"])
    print("Errors:", A["Errors"])
    print("ColumnsCount: " + str(len(A["ColumnsNames"])))
    print("RowsCount: " + str(len(A["Data"])))
    print("ColumnsNames:", A["ColumnsNames"])
    print("ColumnsTypes:", A["ColumnsTypes"])
    space = "  "

    # для строк список значений
    str_columns_count = 0
    for i in range(len(A["ColumnsNames"])):
        if A["ColumnsTypes"][i] == "s":
            str_columns_count += 1
            if str_columns_count == 1:
                print("StringColumns:")
            #print(space + A["ColumnsNames"][i])
            str_values_list = []
            str_values_counting = {}
            min_len = len(A["Data"][0][i])
            max_len = len(A["Data"][0][i])
            for j in range(len(A["Data"])):
                s = A["Data"][j][i]
                if len(s) < min_len:
                    min_len = len(s)
                if len(s) > max_len:
                    max_len = len(s)
                #if s not in str_values_list:
                if s not in str_values_counting:
                    str_values_list.append(s)
                    #str_values_counting.append(1)
                    str_values_counting[s] = 1
                else:
                    str_values_counting[s] += 1

            msg = A["ColumnsNames"][i] + ":"
            msg += " min_len=" + str(min_len)
            msg += " max_len=" + str(max_len)
            msg += " diff_count" + str(len(str_values_list))
            print(space + msg)
            #print(space + space + "min_len:" + str(min_len))
            #print(space + space + "max_len:" + str(max_len))
            #print(space + space + "count: " + str(len(str_values_list)))
            print_count = len(str_values_list)
            if print_count > PRINT_MAX_COUNT:
                msg = "first " + str(PRINT_MAX_COUNT) + " values:"
                print_count = PRINT_MAX_COUNT
            else:
                msg = "values:"
            for j in range(print_count):
                msg += " " + str_values_list[j] + "=" + str(str_values_counting[str_values_list[j]])
            if print_count < len(str_values_list):
                msg += " " + "..."
            print(space + space + msg)

    # для дробных среднее, стандартное отклонение, мин/макс, квартили
    float_columns_count = 0
    for i in range(len(A["ColumnsNames"])):
        if A["ColumnsTypes"][i] == "f":
            float_columns_count += 1
            if float_columns_count == 1:
                print("FloatColumns:")
            X = []
            for j in range(len(A["Data"])):
                X.append(A["Data"][j][i])
            X.sort()
            lower_procentile_position = int(lower_procentile * len(X))
            upper_procentile_position = int(upper_procentile * len(X))
            lower_procentile_value = X[lower_procentile_position]
            upper_procentile_value = X[upper_procentile_position]
            msg = A["ColumnsNames"][i] + ":"
            msg += " min=" + str(round(min(X), digits))
            msg += " mean=" + str(round(mean(X), digits))
            msg += " max=" + str(round(max(X), digits))
            msg += " stddev=" + str(round(stddev(X), digits))
            msg += " prc(" + str(lower_procentile) + ")=" + str(lower_procentile_value)
            msg += " prc(" + str(upper_procentile) + ")=" + str(upper_procentile_value)
            print(space + msg)

    # для целых список значений + статистики как для дробных
    int_columns_count = 0
    for i in range(len(A["ColumnsNames"])):
        if A["ColumnsTypes"][i] == "i":
            int_columns_count += 1
            if int_columns_count == 1:
                print("IntegerColumns:")
            X = []
            for j in range(len(A["Data"])):
                X.append(float(A["Data"][j][i]))
            X.sort()
            lower_procentile_position = int(lower_procentile * len(X))
            upper_procentile_position = int(upper_procentile * len(X))
            lower_procentile_value = int(X[lower_procentile_position])
            upper_procentile_value = int(X[upper_procentile_position])
            msg = A["ColumnsNames"][i] + ":"
            msg += " min=" + str(int(min(X)))
            msg += " mean=" + str(round(mean(X), digits))
            msg += " max=" + str(int(max(X)))
            msg += " stddev=" + str(round(stddev(X), digits))
            msg += " prc(" + str(lower_procentile) + ")=" + str(lower_procentile_value)
            msg += " prc(" + str(upper_procentile) + ")=" + str(upper_procentile_value)
            print(space + msg)

    # для дат минимальное и максимальное значения
    date_columns_count = 0
    for i in range(len(A["ColumnsNames"])):
        if A["ColumnsTypes"][i] == "d":
            date_columns_count += 1
            if date_columns_count == 1:
                print("DateColumns:")
            min_value = A["Data"][j][i]
            max_value = A["Data"][j][i]
            for j in range(len(A["Data"])):
                if A["Data"][j][i] < min_value:
                    min_value = A["Data"][j][i]
                if A["Data"][j][i] > max_value:
                    max_value = A["Data"][j][i]
            msg = A["ColumnsNames"][i] + ":"
            msg += " [" + str(min_value) + "] .. [" + str(max_value) + "]"
            #msg += " min=" + str(min_value)
            #msg += " max=" + str(max_value)
            print(space + msg)

if __name__ == "__main__":
    #Fibo = read_table("dataset_fibo.txt", divider = "\t")
    #pprint.pprint(Fibo)

    #Iris = read_table("iris.csv", divider = ",", add_serial_number_column_with_name = "sn")
    #table_info(Iris)

    FX = read_table("/mnt/lindata/c1.xls", divider="\t")
    table_info(FX)
