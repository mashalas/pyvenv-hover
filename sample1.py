
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
    X_rows_names = ["x", "y"] # список столбцов для формирования X
    X = np.zeros((rows_count, len(X_rows_names)), float)  # минус столбец с буквами~серийный номер, минут столбец с результатом
    for i in range(len(T["Data"])):
        k = 0
        for j in range(len(T["ColumnsNames"])):
            if T["ColumnsNames"][j] in X_rows_names:
                X[i][k] = float(T["Data"][i][j])
                k += 1
    print("------- X --------")
    print(X)

    # одна выходная переменная
    Y_rows_names = ["z"] # список столбцов для формирования Y
    Y = np.zeros((rows_count, ), float)
    for i in range(len(T["Data"])):
        for j in range(len(T["ColumnsNames"])):
            if T["ColumnsNames"][j] in Y_rows_names:
                Y[i] = float(T["Data"][i][j])
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
