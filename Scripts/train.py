# Created by taka the 2/11/21 at 2:23 PM

from datetime import datetime
import os
import config as cfg
from keras.models import Sequential
from keras.layers import Conv1D, Activation, Flatten, Dense, MaxPooling1D
import processing_utils as proc
import pandas as pd
import numpy as np

# create log rep
run_id = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
log_run_dir = os.path.join(cfg.log_path, run_id)
os.makedirs(log_run_dir, exist_ok=True)

# charge x_val and y_val
x_data = []
y_data = []
for i in range(2017, 2019):
    df_comps = pd.read_csv(os.path.join(cfg.data_path, 'comps_ids_{}_{}.csv'.format(i, i+1)), sep=',')
    df_matches = pd.read_csv(os.path.join(cfg.data_path, 'matches_{}_{}.csv'.format(i, i+1)), sep=',')
    x, y = proc.prepare_data(df_comps, df_matches)
    x_data.extend(x)
    y_data.extend(y)
    print("Data for season {}-{} prepared.".format(i, i+1))

#x_data = np.expand_dims(x_data, axis=2)
x_data = np.array(x_data)
x_data = x_data[..., np.newaxis]
# y_data = np.expand_dims(y_data, axis=2)

x_train = x_data[:int(len(x_data)*0.8)]
y_train = y_data[:int(len(y_data)*0.8)]
x_test = x_data[int(len(x_data)*0.8):]
y_test = y_data[int(len(y_data)*0.8):]

x_val = x_train[int(len(x_train)*0.9):]
y_val = y_train[int(len(y_train)*0.9):]
x_train = x_train[:int(len(x_train)*0.9)]
y_train = y_train[:int(len(y_train)*0.9)]


print(np.array(x_train).shape)
print(x_train[0])
print(len(y_train))
print(y_train[0])


print('Train and test data preprocessed.')

# =============================================
# Network
# =============================================
print('Creation of the model.')
model = Sequential()
model.add(Conv1D(16, (3), input_shape=(22, 1)))
model.add(Activation('relu'))
model.add(Conv1D(16, (3)))
model.add(Activation('relu'))
model.add(MaxPooling1D(pool_size=(2)))

model.add(Flatten())
model.add(Dense(128))
model.add(Activation('relu'))
model.add(Dense(3))
model.add(Activation('softmax'))

model.summary()
print('Model created.')


# Compile
model.compile(loss='categorical_crossentropy', optimizer='Adam', metrics=['accuracy'])

# Training
model.fit(np.array(x_train), np.array(y_train), validation_data=(np.array(x_val), np.array(y_val)),
          epochs=100, batch_size=8)


# Evaluate
accuracy_eval = model.evaluate(np.array(x_val), np.array(y_val), batch_size=8)
print('Loss : {}, Accuracy : {}'.format(accuracy_eval[0], accuracy_eval[1]))

# Predict
correct_preds = 0
for x, y in zip(x_test, y_test):
    print(x)
    pred = model.predict(x[np.newaxis, ...])
    ind_pred = np.argmax(pred)
    ind_y = np.argmax(y)
    print(pred)
    print(y)
    print(ind_pred, ind_y)
    if ind_pred == ind_y:
        correct_preds += 1

print('Accuracy : {}'.format((correct_preds/len(y_test))))

# Save model as .h5 file
model.save(os.path.join(log_run_dir, 'model_file.h5'))


