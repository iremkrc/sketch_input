# It WORKS!

import numpy as np
from sklearn.manifold import TSNE
import os
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties


directory = "./embeddings_dir/"

all_embeddings = []     # a list of tuples (key_id , embedding_vector, class_name)
latent_space = np.zeros((1, 128))
class_list = []
latent_dictionary = dict()

for filename in os.listdir(directory):
    if filename.endswith("embeddings_new.npz"):
        file_name = filename
        embeddings = np.load(directory + file_name, allow_pickle=True, encoding="latin1")
        for embedding in embeddings["embeddings"]:
            embed_vector = embedding[0]
            key_id = embedding[1]
            class_name_raw = embedding[2]
            class_name = class_name_raw.split(str(key_id))[0]
            latent_space = np.concatenate((latent_space, embed_vector))
            class_list.append(class_name)


latent_space = latent_space[1:, :]

# Now the latent space variable has NxD data in it. N: number of sketches. D: dimensions. D=128 in this case
latent_space_tsne = TSNE(n_components=2).fit_transform(latent_space)


for i in range(len(class_list)):
    label = class_list[i]
    x_float = (latent_space_tsne[i, :])[0]
    y_float = (latent_space_tsne[i, :])[1]
    if label not in latent_dictionary.keys():
        latent_dictionary[label] = [[x_float], [y_float]]
    else:
        old_value_list = latent_dictionary[label]
        old_value_list[0].append(x_float)
        old_value_list[1].append(y_float)
        latent_dictionary[label] = old_value_list

class_keys = latent_dictionary.keys()

legend_list = list()
scatter_input = tuple()   # (plt.scatter(np.zeros((1, 2)), np.zeros((1, 2))),)
recur = 0

for categ_names in class_keys:
    recur += 1
    if recur < 11:
        continue
    elif recur < 21:
        x_y_list = latent_dictionary[categ_names]
        x_array = np.array(x_y_list[0])
        y_array = np.array(x_y_list[1])
        legend_list.append(categ_names)
        scatter_input += (plt.scatter(x_array, y_array),)

legend_tuple = tuple(legend_list)

fontP = FontProperties()
fontP.set_size('x-small')
plt.legend(scatter_input,
           legend_tuple,
           scatterpoints=1,
           bbox_to_anchor=(1.05, 1),
           loc='upper left',
           prop=fontP,
           ncol=2)


plt.tight_layout()

plt.show()





