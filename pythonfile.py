import librosa
import soundfile
import os, glob, pickle
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, confusion_matrix

def extract_feature(file_name, mfcc=True, chroma=True, mel=True):
  X, sample_rate = librosa.load(file_name)
  result = np.array([])
  if mfcc:
      mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T, axis=0)
      result = np.hstack((result, mfccs))
  if chroma:
      stft = np.abs(librosa.stft(X))
      chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T, axis=0)
      result = np.hstack((result, chroma))
  if mel:
      mel = np.mean(librosa.feature.melspectrogram(y=X, sr=sample_rate).T, axis=0)
      result = np.hstack((result, mel))
  return result

emotions = {
    '01':'neutral',
    '02':'calm',
    '03':'happy',
    '04':'sad',
    '05':'angry',
    '06':'fealful',
    '07':'disgust',
    '08':'surprised'
}

#Emotions we want to observe
observed_emotions = ['calm', 'happy', 'fearful', 'disgust']

x, y = [], []
for folder in glob.glob('Actor_*'):
  print(folder)

  for file in glob.glob(folder + '/*.wav'):
    file_name = os.path.basename(file)

    emotion = emotions[file_name.split('-')[2]]
    if emotion not in observed_emotions:
      continue
    feature = extract_feature(file, mfcc = True, chroma = True, mel = True)
    x.append(feature)
    y.append(emotion)



def load_data(test_size = 0.2):
  x, y = [], []
  for folder in glob.glob('Actor_*'):
    print(folder)
    for file in glob.glob(folder + '/*.wav'):
      file_name = os.path.basename(file)
      emotion = emotions[file_name.split('-')[2]]
      if emotion not in observed_emotions:
        continue
      feature = extract_feature(file, mfcc = True, chroma = True, mel = True)
      x.append(feature)
      y.append(emotion)
  return train_test_split(np.array(x), y, test_size = test_size, random_state = 9)



x_train,x_test,y_train,y_test=load_data(test_size=0.2)

print((x_train.shape[0], x_test.shape[0]))
print(f'Features extracted: {x_train.shape[1]}')
print(x_test)

#Initialise Multi Layer Perceptron Classifier
model = MLPClassifier(alpha = 0.01, batch_size = 256, epsilon = 1e-08, hidden_layer_sizes = (300,), learning_rate = 'adaptive', max_iter = 500)

model.fit(x_train, y_train)



# Don't delete

# y_pred = model.predict(x_test)
# for file in glob.glob('Test-Audio'+'/*.wav'):
#     temp=extract_feature(file)
#     temp = np.reshape(temp, (1, -1))
#     x_data=model.predict(temp)
#     print(x_data)

# #Calculate Accuracy
# accuracy = accuracy_score(y_test, y_pred)
# print("Accuracy: {:.2f}%".format(accuracy*100))

