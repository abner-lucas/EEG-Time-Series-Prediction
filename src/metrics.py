import numpy as np

def RMSE(y_test, prediction):
    soma = 0
    for i in range(len(y_test)):
        soma += (y_test[i] - prediction[i]) ** 2
    media_erro = np.sqrt(soma / len(y_test))
    return media_erro.round(5)

def MAE(y_test, prediction):
    soma = 0
    for i in range(len(y_test)):
        soma += abs(y_test[i] - prediction[i])
    media_erro = soma / len(y_test)
    return media_erro.round(5)

def MAPE(y_test, prediction):
    soma = 0
    for i in range(len(y_test)):
        soma += abs((y_test[i] - prediction[i]) / y_test[i]) #* 100
    media_erro = soma / len(y_test)
    return media_erro.round(5)