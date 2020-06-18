import pandas
from easyesn.optimizers import GradientOptimizer
from easyesn import PredictionESN
from easyesn.optimizers import GridSearchOptimizer
from easyesn import helper as hlp
import matplotlib.pyplot as plt

df = pandas.read_csv("data.csv")

inputLength = len(df)
training_start = int(inputLength * 0.5)
# dane do treningu zaczynają się wraz z podaniem lekarstwa
training_end = int(inputLength * 0.65)

# dane wejściowe to P* = P + Q + Qp (inaczej MTD)
inputData = df["MTD"]
# na wyjściu chcemy P, Q, Qp, a z ich sumy policzymy P*
outputData = df[["P", "Q", "Qp"]]

inputDataTraining = inputData[training_start:training_end]
inputDataValidation = inputData[training_end:]

outputDataTraining = outputData[training_start:training_end]
outputDataValidation = outputData[training_end:]

esn = PredictionESN(
    n_input=1,
    n_output=3,
    n_reservoir=50,
    leakingRate=0.2,
    regressionParameters=[1e-2],
    solver="lsqr",
    feedback=False,
)

esn.fit(inputDataTraining, outputDataTraining, transientTime="Auto", verbose=2)

one_step_prediction = esn.predict(inputDataValidation)


def show_param(column, prediction, i):
    plt.subplot(4, 1, i)
    plt.ylabel(f"{column.name}")
    plt.xlabel("t")
    plt.plot(range(inputLength), column, label="Real data")
    plt.plot(range(training_end, inputLength), prediction, label="Prediction")


plt.figure(figsize=(16, 16))

show_param(df["P"], one_step_prediction.T[0], 1)
show_param(df["Q"], one_step_prediction.T[1], 2)
show_param(df["Qp"], one_step_prediction.T[2], 3)

# predykcja P* policzona z sumy P, Q, Qp
MTD_pred = (
    one_step_prediction.T[0] + one_step_prediction.T[1] + one_step_prediction.T[2]
)

plt.subplot(4, 1, 4)
plt.ylabel("P*(t)")
plt.plot(range(inputLength), inputData, label="Real data")
plt.plot(range(training_end, inputLength), MTD_pred, label="Prediction")

plt.show()
