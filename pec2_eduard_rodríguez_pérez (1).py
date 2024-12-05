# -*- coding: utf-8 -*-
"""PEC2_Eduard_Rodríguez_Pérez.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1LULHFAUaycrunQS0IumcBGKBMPwKl-LM

# **PEC2: Actividad y Debate**

## **Actividad (70%)**

### 1- Cargar los datos (wine1.data).
"""

import numpy as np
import pandas as pd
datos_raw = pd.read_csv("wine1.data", names=['Grape Type','Alcohol', 'Malic acid',
                                         'Ash', 'Alcalinity of ash', 'Magnesium'
                                         , 'Total phenols', 'Flavanoids',
                                         'Nonflavanoid phenols',
                                         'Proanthocyanins', 'Color intensity',
                                         'Hue', 'Purity of diluted wines',
                                         'Proline'])
display(datos_raw)

### Cambiaremos la variable Grape Type para hacerla numérica y favorecer el proceso.
datos = datos_raw
for i in datos.index:
    if datos.iloc[i,0] == "A":
      datos.at[i,"Grape Type"] = 1;
    elif datos.iloc[i,0] == "B":
      datos.at[i,"Grape Type"] = 2;
    elif datos.iloc[i,0] == "C":
      datos.at[i,"Grape Type"] = 3;

## Comprobamos
datos.head()

datos.tail()

"""### 2- Realizar un estudio exploratorio de los datos con gráficos y tablas. Puede ser tanto univariante como multivariante."""

## Comprobamos el tipo de datos
print(datos.info())

"""Comrobamos que todos los valores, excepto los de la variable a predecir, son numéricos."""

# convertimos a float las columnas Magnesium y Proline
datos['Magnesium'] = datos['Magnesium'].astype(float)
datos['Proline'] = datos['Proline'].astype(float)
print(datos.info())

## Hacemos una breve descripción estadística de los datos
datos.describe()

import matplotlib.pyplot as plt
matriz_disp=pd.plotting.scatter_matrix(datos.loc[:, "Alcohol":"Proline"],
                                       diagonal="kde", figsize=(20,15))
plt.show()

"""NOTA: estos datos se parecen sospechosamente a los de: https://www.kaggle.com/code/sanikamal/introduction-to-multivariate-analysis

Sea como fuere, el análisis que haremos será el mismo, ya que resulta obvio que nos interesa comparar cómo se relaciona cada par de variables de composición química según el tipo de vino, ya que será relevante para el modelo de predicción.

Veamos:
"""

import seaborn as sns
columnames=['Alcohol', 'Malic acid', 'Ash', 'Alcalinity of ash',
       'Magnesium', 'Total phenols', 'Flavanoids', 'Nonflavanoid phenols',
       'Proanthocyanins', 'Color intensity','Hue',
       'Purity of diluted wines','Proline']
for i in range (1,12):
  sns.lmplot(data=datos, x=columnames[i], y=columnames[i+1], hue="Grape Type", fit_reg=False);

"""Veamos la correlación entre variables:

"""

X = datos.loc[:, "Alcohol":]
corrmat = X.corr()
corrmat
sns.heatmap(corrmat, vmax=1., xticklabels =False, square=False).xaxis.tick_top()

"""### 3- En caso necesario, normalizar las expresiones con la transformación minmax. Justificar respuesta.

No realizaremos este paso aquí, ya que implementaremos Keras.

### 4- Separar los datos en train (2/3) y test (1/3).
"""

#(EXTRAÍDO DEL EJEMPLO DISPONIBLE DE LA ASIGNATURA)
test_dataframe = datos.sample(frac=1/3, random_state=1337)
train_dataframe = datos.drop(test_dataframe.index)

test_dataframe=test_dataframe.astype(np.float32)
train_dataframe=train_dataframe.astype(np.float32)

# Commented out IPython magic to ensure Python compatibility.
## Comprobamos el tamaño de ambos grupos de muestras

print(
    "Tenemos %d muestras para entrenamiento y %d para realizar test"
#     % (len(train_dataframe), len(test_dataframe))
)

"""### 5- Definir el modelo 1, que consiste en una red neuronal con una capa oculta densa de 8 nodos, con activación relu. Añadir un 30% de dropout. Proporcionar el summary del modelo y justificar el total de parámetros de cada capa.

[PREPARACIÓN DE LOS DATOS ANTES DE CREAR LOS MODELOS]
"""

def dataframe_to_dataset(dataframe):
    dataframe = dataframe.copy()
    labels = dataframe.pop("Grape Type")
    ds = tf.data.Dataset.from_tensor_slices((dict(dataframe), labels))
    ds = ds.shuffle(buffer_size=len(dataframe))
    return ds

train_ds = dataframe_to_dataset(train_dataframe)
test_ds = dataframe_to_dataset(test_dataframe)



display(test_ds)


for x, y in train_ds.take(1):
    print("Input:", x)
    print("Target:", y)

train_ds = train_ds.batch(30)
test_ds = test_ds.batch(30)

from tensorflow.keras.layers import IntegerLookup
from tensorflow.keras.layers import Normalization
from tensorflow.keras.layers import StringLookup

def encode_numerical_feature(feature, name, dataset):
    # CAPA DE NORMALIZACIÓN (DE AHÍ QUE NO HICIERAMOS MINMAX ANTERIORMENTE)
    normalizer = Normalization()

    # PREPARAMOS DATASET
    feature_ds = dataset.map(lambda x, y: x[name])
    feature_ds = feature_ds.map(lambda x: tf.expand_dims(x, -1))

    # Learn the statistics of the data
    normalizer.adapt(feature_ds)

    # Normalize the input feature
    encoded_feature = normalizer(feature)
    return encoded_feature

# DEFINIMOS LAS VARIABLES NUMÉRICAS
Alcohol = keras.Input(shape=(1,), name="Alcohol")
MalicAcid = keras.Input(shape=(1,), name="Malic acid")
Ash = keras.Input(shape=(1,), name="Ash")
AlcalinityOfAsh = keras.Input(shape=(1,), name="Alcalinity of ash")
Magnesium = keras.Input(shape=(1,), name="Magnesium")
TotalPhenols = keras.Input(shape=(1,), name="Total phenols")
Flavanoids = keras.Input(shape=(1,), name="Flavanoids")
NonflavanoidPhenols = keras.Input(shape=(1,), name="Nonflavanoid phenols")
Proanthocyanins = keras.Input(shape=(1,), name="Proanthocyanins")
ColorIntensity = keras.Input(shape=(1,), name="Color intensity")
Hue = keras.Input(shape=(1,), name="Hue")
PurityOfDilutedwines = keras.Input(shape=(1,), name="Purity of diluted wines")
Proline = keras.Input(shape=(1,), name="Proline")

all_inputs = [
    Alcohol,
    MalicAcid,
    Ash,
    AlcalinityOfAsh,
    Magnesium,
    TotalPhenols,
    Flavanoids,
    NonflavanoidPhenols,
    Proanthocyanins,
    ColorIntensity,
    Hue,
    PurityOfDilutedwines,
    Proline
]

# Codificamos las variables
Alcohol_encoded = encode_numerical_feature(Alcohol, "Alcohol", train_ds)
MalicAcid_encoded = encode_numerical_feature(MalicAcid, "Malic acid", train_ds)
Ash_encoded = encode_numerical_feature(Ash, "Ash", train_ds)
AlcalinityOfAsh_encoded = encode_numerical_feature(AlcalinityOfAsh, "Alcalinity of ash", train_ds)
Magnesium_encoded = encode_numerical_feature(Magnesium, "Magnesium", train_ds)
TotalPhenols_encoded = encode_numerical_feature(TotalPhenols, "Total phenols", train_ds)
Flavanoids_encoded = encode_numerical_feature(Flavanoids, "Flavanoids", train_ds)
NonflavanoidPhenols_encoded = encode_numerical_feature(NonflavanoidPhenols, "Nonflavanoid phenols", train_ds)
Proanthocyanins_encoded = encode_numerical_feature(Proanthocyanins, "Proanthocyanins", train_ds)
ColorIntensity_encoded = encode_numerical_feature(ColorIntensity, "Color intensity", train_ds)
Hue_encoded = encode_numerical_feature(Hue, "Hue", train_ds)
PurityOfDilutedwines_encoded = encode_numerical_feature(PurityOfDilutedwines, "Purity of diluted wines", train_ds)
Proline_encoded = encode_numerical_feature(Proline, "Proline", train_ds)

all_features = layers.concatenate(
    [
        Alcohol_encoded,
        MalicAcid_encoded,
        Ash_encoded,
        AlcalinityOfAsh_encoded,
        Magnesium_encoded,
        TotalPhenols_encoded,
        Flavanoids_encoded,
        NonflavanoidPhenols_encoded,
        Proanthocyanins_encoded,
        ColorIntensity_encoded,
        Hue_encoded,
        PurityOfDilutedwines_encoded,
        Proline_encoded,
    ]
)

# MODELO 1: definimos la red: entrada all_features; salida 1 sola variable (tipo de uva)
x = layers.Dense(8, activation="relu")(all_features)
x = layers.Dropout(0.3)(x)
output = layers.Dense(1, activation="relu")(x)  ## relu permite un output>1
modelo1 = keras.Model(all_inputs, output)

# debemos compilar el modelo, indicando una loss indicada (problema de clasificación binario)
modelo1.compile("adam", "binary_crossentropy", metrics=["accuracy"])

modelo1.summary()

#  podemos visualizar el modelo
keras.utils.plot_model(modelo1, show_shapes=True, rankdir="LR")

"""El número de parámetros de cada capa se obtiene del número de variables +1 (tamaño tensor de entrada) multiplicada por el número de nodos de la capa...

Primero tenemos 13 entradas normalizadas, creando 3 parámetros cada una: 13x3 = 39
En la capa densa tenemos 13 entradas de la capa anterior y tiene 8 nodos (uno por clase)... (13+1)x8 = 112

En la capa de salida tenemos 8 entradas y un solo nódulo... (8+1)*1= 9


Lo que hacen un total de 39+112+9 parámetros= 160. De los cuales los 39 primeros no requieren entrenamiento.

### 6- Ajustar el modelo 1 con un 20% de validación, mostrando la curva de aprendizaje de entrenamiento y validación con 100 épocas.
"""

evolucion1 = modelo1.fit(train_ds, epochs=100, validation_split=0.2, validation_data=train_ds)
import matplotlib.pyplot as plt
plt.plot(evolucion1.history['accuracy'])
plt.plot(evolucion1.history['val_accuracy'])
plt.title('Precisión del modelo')
plt.ylabel('Precisión')
plt.xlabel('Iteración')
plt.legend(['Entrenamiento', 'Validación'], loc='lower right')
plt.show()

"""### 7- Obtener la tabla de clasificación errónea en test. Y las métricas usuales de evaluación."""

## evaluamos el modelo a partir del test


y_pred = np.argmax(modelo1.predict(test_ds), axis=1)

actual = np.array(test_dataframe["Grape Type"])

## creamos la Matriz de confusión

from sklearn import metrics
import matplotlib.pyplot as plt

confusion_matrix = metrics.confusion_matrix(actual, y_pred)

cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = confusion_matrix)
cm_display.plot()
plt.show()

"""Tenemos una precisión del 0%, ya que por algún error predice valor 0, o bien la arquitectura de tan pocas capas no permite entrenar en tan poco tiempo para tantas variables de entrada.

### 8- Definir el modelo 2, que consiste en una red neuronal con dos capas ocultas densas de 10 nodos y 5 nodos, con activación relu. Añadir un 30% de dropout en ambas capas. Proporcionar el summary del modelo y justificar el total de parámetros de cada capa.
"""

# MODELO 2: definimos la red: entrada all_features; salida 1 sola variable (tipo de uva)
x = layers.Dense(10, activation="relu")(all_features)
x = layers.Dropout(0.3)(x)
x = layers.Dense(5, activation="relu")(x)
x = layers.Dropout(0.3)(x)
output = layers.Dense(1, activation="relu")(x)
modelo2 = keras.Model(all_inputs, output)

# debemos compilar el modelo, indicando una loss indicada (problema de clasificación binario)
modelo2.compile("adam", "binary_crossentropy", metrics=["accuracy"])

modelo2.summary()

"""El número de parámetros de cada capa se obtiene del número de variables +1 (tamaño tensor de entrada) multiplicada por el número de nodos de la capa...

Primero tenemos 13 entradas normalizadas, creando 3 parámetros cada una: 13x3 = 39 En la capa densa tenemos 13 entradas de la capa anterior y tiene 10 nodos (uno por clase)... (13+1)x10 = 140

En la segunda capa, con tantas entradas como nódulos anteriores, tenemos 5 nodos... (10+1)*5=55

En la capa de salida tenemos 5 entradas y un solo nódulo... (5+1)*1= 6

Lo que hacen un total de 39+140+55+6 parámetros= 240. De los cuales los 39 primeros no requieren entrenamiento.

### 9- Ajustar el modelo 2 con un 20% de validación, mostrando la curva de aprendizaje de entrenamiento y validación con 100 épocas.
"""

evolucion2 = modelo2.fit(train_ds, epochs=100, validation_split=0.2,
                         validation_data=train_ds)

import matplotlib.pyplot as plt
plt.plot(evolucion2.history['accuracy'])
plt.plot(evolucion2.history['val_accuracy'])
plt.title('Precisión del modelo')
plt.ylabel('Precisión')
plt.xlabel('Iteración')
plt.legend(['Entrenamiento', 'Validación'], loc='lower right')
plt.show()

"""### 10- Comparar ambos modelos usando los datos de test mediante las métricas de evaluación."""

## evaluamos el modelo a partir del test

y_pred2 = np.argmax(modelo2.predict(test_ds), axis=1)

print(y_pred2)

confusion_matrix2 = metrics.confusion_matrix(actual, y_pred2)

cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = confusion_matrix2)
cm_display.plot()
plt.show()

"""Por algún motivo, sigue prediciendo un tipo 0 de vino que no existe en los datos de entrenamiento. Si no hay un error en el procesamiento de datos, debemos atribuirlo a una arquitectura insuficiente de la red o un entrenamiento demasiado corto."""