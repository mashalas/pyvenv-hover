
import read_table
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
#import sklearn

if __name__ == "__main__":
    T = read_table.read_table("dataset_fibo.txt", "\t")
    read_table.table_info(T)
    rows_count = len(T["Data"])
    columns_count = len(T["ColumnsNames"])
    print("rows_count:", rows_count, "columns_count:", columns_count);
    print(T)

    # две входные переменные
    X = read_table.table_to_numpy__by_names(T, ["x", "y"])
    print("------- X --------")
    print(X)

    # одна выходная переменная
    Y = read_table.table_to_numpy__by_names(T, ["z"])
    print("------- Y --------")
    print(Y)

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, train_size=0.67, random_state=42)
    print("------- X_train --------")
    print(X_train)
    print("------- X_test --------")
    print(X_test)
    print("------- Y_train --------")
    print(Y_train)
    print("------- Y_test --------")
    print(Y_test)
