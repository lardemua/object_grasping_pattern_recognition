import itertools
import json
import matplotlib.pyplot as plt
import numpy as np
import os

from collections import Counter
from sklearn.metrics import confusion_matrix


# Set the font type to be used for plotting
plt.rcParams['svg.fonttype'] = 'none'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 15


def read_dataset(folder_path="./preprocessed_dataset", objects=["bottle", "cube", "phone", "screwdriver"],
                  people=["joel", "manuel", "pedro"], sessions=["1", "2", "3", "4"], num_samples=None):
    x = []
    y = []

    object_ids = {o: objects.index(o) for o in objects}

    # Iterate over all files in the folder
    for filename in os.listdir(folder_path):
        # Create the absolute path to the file
        file_path = os.path.join(folder_path, filename)

        # Check if the file path is a file (not a directory)
        if os.path.isfile(file_path) and file_path.endswith(".json"):
            filename = filename.split("_")
            object_name = filename[0]
            person = filename[1]
            session = filename[2][0]

            if object_name in objects and person in people and session in sessions:
                # Open the file
                with open(file_path, "r") as f:
                    data = json.load(f)
                
                for i in range(len(data)):
                    x.append(data[i]["points"])
                    y.append(object_ids[object_name])

    x = np.array(x)
    y = np.array(y)
    
    if num_samples is not None:
        random_indices = np.random.choice(len(y), size=num_samples, replace=False)

        x = x[random_indices]
        y = y[random_indices]

    return x, y


def write_results(train_acc, val_acc, test_acc, train_loss, val_loss, test_loss,
        report, training_time="", save_path="./results/results.txt"):
    
    f = open(save_path, "w")
    if train_acc is not None:
        f.write(f"Training loss: {train_loss}\nTraining accuracy: {train_acc}\n")
    if val_acc is not None:
        f.write(f"Validation loss: {val_loss}\nValidation accuracy: {val_acc}\n")
    if test_acc is not None:
        f.write(f"Test loss: {test_loss}\nTest accuracy: {test_acc}\n\n")
    if report is not None:
        f.write(report)
    if training_time is not None:
        f.write(f"\nTraining time: {training_time} seconds\n")
    f.close()


#################################### Plots ####################################

def plot_accuracy_comparison(accs, title, legend, show=True, save_path=False):
    plt.figure(figsize = (10,5))
    for acc in accs:
        plt.plot(range(1, len(acc)+1), acc)

    #plt.xticks(range(1, epochs+1))
    #plt.title(title)
    plt.legend(legend)
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")

    if save_path:
        plt.tight_layout()
        plt.savefig(save_path)
    
    if show:
        plt.show()


def plot_confusion_matrix(cm, target_names=None, show=True, save_path=False):
    cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    
    fig = plt.figure()
    plt.imshow(cm, interpolation='nearest', cmap=plt.get_cmap('Blues'))

    ax = fig.gca()

    ax.tick_params(bottom=False, top=True, left=True, right=False)
    ax.tick_params(labelbottom=False, labeltop=True, labelleft=True, labelright=False)

    if target_names is not None:
        tick_marks = np.arange(len(target_names))
        plt.xticks(tick_marks, target_names)
        plt.yticks(tick_marks, target_names, rotation="vertical", va="center")

    thresh = cm.max() / 1.5
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, "{:0.2f}".format(cm[i, j]),
                    horizontalalignment="center",
                    color="white" if cm[i, j] > thresh else "black")

    plt.ylabel('True Label')
    plt.title('Predicted Label')

    if save_path:
        plt.tight_layout()
        plt.savefig(save_path) # , format="svg")
    
    if show:
        plt.show()


def plot_loss_comparison(losses, title, legend, show=True, save_path=False):
    plt.figure(figsize = (10,5))
    for loss in losses:
        plt.plot(range(1, len(loss)+1), loss)

    #plt.xticks(range(1, epochs+1))
    #plt.title(title)
    plt.legend(legend)
    plt.xlabel("Epochs")
    plt.ylabel("Loss")
    
    if save_path:
        plt.tight_layout()
        plt.savefig(save_path)
    
    if show:
        plt.show()


def draw_bar_chart(labels, show=True, save_path=False):
    fig, ax = plt.subplots(figsize=(10, 5))
    # Count the frequency of each label
    label_counts = Counter(labels)

    # Get the labels and their respective counts
    labels = list(label_counts.keys())
    counts = list(label_counts.values())

    # Set up the bar chart
    plt.bar(labels, counts)
    ax.set_xticks(labels)
    plt.xlabel('Labels')
    plt.ylabel('Quantity')
    plt.title('Quantity of Labels from Each Class')

    # Display the chart
    if save_path:
        plt.tight_layout()
        plt.savefig(save_path)
    
    if show:
        plt.show()
