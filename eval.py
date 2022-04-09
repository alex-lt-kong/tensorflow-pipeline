from sklearn.metrics import roc_curve,roc_auc_score
from sklearn import metrics
from sklearn.metrics import classification_report, confusion_matrix, plot_confusion_matrix
from tensorflow import keras

import seaborn as sn
import logging
import matplotlib.pyplot as plt
import numpy as np
import utils
import pandas as pd


def get_true_and_pred(dataset):
  # X = np.concatenate([X for X, y in val_ds], axis=0)  
  # y_true = np.concatenate([y for x, y in val_ds], axis=0)
  # cannot use this approach as it loads all the samples into memory, which 
  # gets exhausted very fast.
  
  y_true = []
  y_pred = []
  count = 0
  for x, y in dataset:
    # Note that here x and y do not come one after another--they come in batches
    # whose size is defined by the batch_size parameter passed to the prepare_dataset
    # method.
    count += 1
    logging.info(f'Predicting {count}-th sample')
    y_true.extend(y.numpy().tolist())
    y_pred.extend(model.predict(x).ravel())
    #y_pred_cat.extend(np.where(y_pred > 0.5, 1, 0).tolist())
  return np.array(y_true), np.array(y_pred)

def plot_confusion_matrix(y_true, y_pred):
  y_pred_cat = np.where(y_pred > 0.5, 1, 0)
  cm = metrics.confusion_matrix(y_true, y_pred_cat)
  classes = ['0', '1']
  df_cm = pd.DataFrame(cm, index=classes, columns=classes)

  plt.figure(figsize = (16/2, 9/2))
  sn.heatmap(df_cm, cmap="YlGnBu", annot=True, fmt='g')  
  plt.xlabel('Predicted label')
  plt.ylabel('True label')
  plt.savefig(settings['diagnostics']['confusion_matrix'], bbox_inches='tight')
  print(cm)

  print(classification_report(y_true, y_pred_cat, target_names=['0','1']))

  #print(model.evaluate(dataset, verbose=1))


def plot_roc_curve(y_true, y_pred):
  fpr, tpr, thresholds = roc_curve(y_true, y_pred)
  plt.figure(figsize = (16/2, 9/2))
  plt.plot(fpr, tpr) 
  plt.axis([0, 1, 0, 1]) 
  plt.xlabel('False Positive Rate') 
  plt.ylabel('True Positive Rate') 
  plt.savefig(settings['diagnostics']['roc'], bbox_inches='tight')

settings = utils.read_config_file()
image_size = (
  settings['dataset']['image']['height'], settings['dataset']['image']['width']
)
batch_size = settings['model']['batch_size']
  
utils.initialize_logger(settings['misc']['log_path'])
train_ds, val_ds = utils.prepare_dataset(settings['dataset']['path'], image_size=image_size, batch_size=batch_size)
model = keras.models.load_model(settings['model']['save_to']['model'])
y_true, y_pred = get_true_and_pred(dataset=val_ds)

plot_roc_curve(y_true, y_pred)
plot_confusion_matrix(y_true, y_pred)
