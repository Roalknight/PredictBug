import numpy as np
import pickle
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

with open("py2vec\py2vec_model3.pkl", "rb") as f:
    embeddings = pickle.load(f)
with open("py2vec\cen.pkl", "rb") as f:
     cen = pickle.load(f)
with open("py2vec\parray.pkl", "rb") as f:
    nparray = pickle.load(f)
with open("py2vec\index.pkl", "rb") as f:
    ndx = pickle.load(f)


def kmeans(data, k, num_iter, print_progress=True):
    """
    K-means clustering algorithm

    Input:
    data - Mảng 2D numpy chứa tất cả các điểm
    k - số clusters
    num_iter - số iterations

    Output:
    centroids - điểm trung tâm
    c - tổng số các điểm
    biểu diễn số nguyên của cụm mà điểm được gán cho
    """
    c = np.zeros(data.shape[0])
    centroids = np.random.rand(k, data.shape[1])

    # Main loop.
    for i in range(num_iter):
        for j in range(data.shape[0]):
            min_dist = np.sum((data[j, :] - centroids[0, :])**2)
            c[j] = 0
            for l in range(1, k):
                dist = np.sum((data[j, :] - centroids[l, :])**2)
                if dist < min_dist:
                    min_dist = dist
                    c[j] = l
        for j in range(k):
            clusters = np.where(c == j)
            centroids[j, :] = np.sum(data[clusters, :], axis=1) / len(clusters[0])
        # Print progress.
        if i % 10 == 0 and print_progress:
            print(str(i))
    return centroids, c


def get_low_dim_embs(vectors):
    """
    t-SNE là một thuật toán học máy để trực quan hóa dữ liệu
    nó biến đổi các vectơ chiều cao hơn thành các chiều thấp hơn
    theo một cách rất phi tuyến tính, bảo toàn được nhiều thông tin.

    Input:
    vectors - high dimensional vectors

    Output:
    2-D vectors
    """
    tsne = TSNE(
        perplexity=30, n_components=2, init='pca', n_iter=250)
    return tsne.fit_transform(vectors)


high_dim_embs = []
labels = []
for key, value in embeddings.items():
    high_dim_embs.append(value)
    labels.append(key)

nclusters = 20


def plot_with_labels(words):
    """
    Plots every word embedding and labels only a list of specified words.

    Input:
    words - A list of words to be labeled.

    Output:
    None, but generates a matplotlib graph
    """
    ndx = []
    fig, ax = plt.subplots()

    for word in words:
        for i in range(len(labels)):
            if labels[i] == word:
                ndx.append(i)
    ax.scatter(nparray[:, 0], nparray[:, 1], s=30, color='burlywood')
    for i in range(len(ndx)):
        ax.scatter(nparray[ndx[i], 0], nparray[ndx[i], 1], s=30, color='chartreuse')
        plt.text(nparray[ndx[i], 0], nparray[ndx[i], 1], words[i])
    # Display graph
    plt.show()

def plot_kmeans_clusters(n_clusters, label):
    colors = ['DarkOrchid', 'DarkRed', 'DarkSlateBlue', 'ForestGreen', 'GoldenRod', 'MediumVioletRed',
              'MidnightBlue', 'SlateGrey', 'BurlyWood', 'Plum', 'MediumAquaMarine', 'RosyBrown',
              'Lime', 'MediumBlue', 'MediumSeaGreen', 'Olive', 'PaleVioletRed', 'y',
              'c', 'r']
    clusters = []
    fig, ax = plt.subplots()
    for i in range(n_clusters):
        clusters.append(nparray[np.where(ndx == i)[0], :])
        ax.scatter(clusters[i][:, 0], clusters[i][:, 1], s=30, color=colors[i], label='Cluster ' + str(i))

    if label:
        z = 0
        for i in range(nparray.shape[0]):
            plt.text(nparray[z][0], nparray[z][1], labels[z])
            z = z + 50
            if z >= nparray.shape[0]:
                break
    # Display graph.
    plt.show()


plot_kmeans_clusters(nclusters, True)
