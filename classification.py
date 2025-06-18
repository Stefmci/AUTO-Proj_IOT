import neurokit2 as nk
import numpy as np
import pandas as pd
import seaborn as sns

# Alternate heart rate and noise levels
ecg50 = nk.ecg_simulate(duration=10, noise=0.05, heart_rate=50)
ecg100 = nk.ecg_simulate(duration=10, noise=0.01, heart_rate=100)

# Visualize
ecg_df = pd.DataFrame({"ECG_100": ecg100, "ECG_50": ecg50})

nk.signal_plot(ecg_df, subplots=True)

data = {}

typ = "Ruhe EKG"
for i in range(100):
    heart_rate = np.random.normal(70, 35)
    # Ensure heart rate is positive
    if heart_rate < 40:
        heart_rate = 40
    data[i] = {}
    data[i]["EGK"] = nk.ecg_simulate(duration=10, noise=0.1, heart_rate=heart_rate)
    data[i]["Type"] = typ
print(i)


typ = "Belastung EKG"
for i in range(100,200):
    heart_rate = np.random.normal(140, 60)
    if heart_rate < 40:
        heart_rate = 40
    data[i] = {}
    data[i]["EGK"] = nk.ecg_simulate(duration=10, noise=0.1, heart_rate=heart_rate)
    data[i]["Type"] = typ
print(i)

data[0]

# Visualize
ecg_df = pd.DataFrame({"Ruhe_1": data[0]["EGK"], "Belastung_1": data[100]["EGK"]})

nk.signal_plot(ecg_df, subplots=True)

## make a dataframe with the mean and standard deviation of the ECG signals

df = pd.DataFrame(data).T
df["Mean"] = df["EGK"].apply(np.mean)
df["STD"] = df["EGK"].apply(np.std)
df.head()


# make a boxplot of the mean of the ECG signals

sns.boxplot(x="Type", y="Mean", data=df)

# make a boxplot of the mean of the ECG signals

sns.boxplot(x="Type", y="STD", data=df)