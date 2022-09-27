
import read_table
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
#import sklearn

if __name__ == "__main__":
    Header = []
    DataTypes = []
    T = read_table.read_table("dataset_fibo.txt", Header, DataTypes, "\t")
    rows_count = len(T)
    columns_count = len(T[0])
    print("rows_count:", rows_count, "columns_count:", columns_count);
    print("Header:", Header)
    print("DataTypes:", DataTypes)
    print(T)

    X = np.zeros((rows_count, columns_count-2), float)  # минус столбец с буквами~серийный номер, минут столбец с результатом
    for i in range(len(T)):
        for j in range(1, len(T[i])-1):
            X[i][j-1] = float(T[i][j])
    print("------- X --------")
    print(X)

    Y = np.zeros((rows_count, ), float)
    for i in range(len(T)):
        Y[i] = float(T[i][columns_count-1])
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
