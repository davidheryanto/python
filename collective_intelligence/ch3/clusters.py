# coding=utf-8
from math import sqrt
import random

from PIL import Image, ImageDraw

from cluster import Bicluster


def get_height(clust):
    # If endpoint, height is 1
    """

    :param clust:
    :return:
    """
    if clust.left == None and clust.right == None: return 1
    # Else it's the sum of the branches' height
    return get_height(clust.left) + get_height(clust.right)


def get_depth(clust):
    # Endpoint distance is 0
    """

    :param clust:
    :return:
    """
    if clust.left == None and clust.right == None: return 0;
    # Distance of branch is greater of its two sides plus own distance
    return max(get_depth(clust.left), get_depth(clust.right)) + clust.distance


def draw_node(draw, clust, x, y, scaling, labels):
    """

    :param draw:
    :param clust:
    :param x:
    :param y:
    :param scaling:
    :param labels:
    """
    if clust.id < 0:
        h1 = get_height(clust.left) * 20
        h2 = get_height(clust.right) * 20
        top = y - (h1 + h2) / 2
        bottom = y + (h1 + h2) / 2

        # Line length
        ll = clust.distance * scaling

        # Vertical line from this cluster to childer
        draw.line((x, top + h1 / 2, x, bottom - h2 / 2), fill=(255, 0, 0))
        # Horizontal line to left item
        draw.line((x, top + h1 / 2, x + ll, top + h1 / 2), fill=(255, 0, 0))
        # Horizontal line to right item
        draw.line((x, bottom - h2 / 2, x + ll, bottom - h2 / 2), fill=(255, 0, 0))

        # Call the function to draw the left and right nodes
        draw_node(
            draw,
            clust.left,
            x + ll,
            top + h1 / 2,
            scaling,
            labels,
        )
        draw_node(
            draw,
            clust.right,
            x + ll,
            bottom - h2 / 2,
            scaling,
            labels,
        )
    else:
        # This is and endpoint
        draw.text((x + 5, y - 7), labels[clust.id], (0, 0, 0))


def rotate_matrix(data):
    """

    :param data:
    :return:
    """
    new_data = []
    for i in range(len(data[0])):
        new_row = [data[j][i] for j in range(len(data))]
        new_data.append(new_row)
    return new_data


def draw_dendogram(clust, labels, jpeg='clusters.jpg'):
    """

    :param clust:
    :param labels:
    :param jpeg:
    """
    h = get_height(clust) * 20
    w = 1280

    depth = get_depth(clust)

    # Fixed width, so scale distances accordingly
    scaling = float(w - 150) / depth

    img = Image.new('RGB', (w, h), (250, 250, 250))
    draw = ImageDraw.Draw(img)

    draw.line((0, h / 2, 10, h / 2), fill=(255, 0, 0))

    # Draw first node
    draw_node(draw, clust, 10, (h / 2), scaling, labels)
    img.save(jpeg, 'JPEG')


def read_file(filename):
    """

    :param filename:
    :return:
    """
    lines = [line for line in file(filename)]
    colnames = lines[0].strip().split('\t')[1:]
    rownames = []
    data = []
    for line in lines[1:]:
        p = line.strip().split('\t')
        rownames.append(p[0])
        data.append([float(x) for x in p[1:]])
    return rownames, colnames, data


def pearson(v1, v2):
    """

    :param v1:
    :param v2:
    :return:
    """
    sum1 = sum(v1)
    sum2 = sum(v2)

    sum1Sq = sum([pow(v, 2) for v in v1])
    sum2Sq = sum([pow(v, 2) for v in v2])

    pSum = sum([v1[i] * v2[i] for i in range(len(v1))])

    num = pSum - (sum1 * sum2 / len(v1))
    den = sqrt((sum1Sq - pow(sum1, 2) / len(v1)) * (sum2Sq - pow(sum2, 2) / len(v1)))
    if den == 0: return 0

    return 1.0 - num / den


def kcluster(rows, distance=pearson, k=4):
    # Find max and min for each point
    ranges = [(min([row[i] for row in rows]), max([row[i] for row in rows]))
              for i in range(len(rows[0]))]

    # Create k randomly placed centroids
    clusters = [[random.random() * (ranges[i][1] - ranges[i][0]) + ranges[i][0]
                 for i in range(len(rows[0]))]
                for j in range(k)]

    last_matches = None
    for t in range(100):
        print('Iteration %d' % t)
        best_matches = [[] for i in range(k)]

        # Find which centroid is closest for each row
        for j in range(len(rows)):
            row = rows[j]
            best_match = 0
            for i in range(k):
                d = distance(clusters[i], row)
                if d < distance(clusters[best_match], row): best_match = i

            best_matches[best_match].append(j)

        # If the results are the same as last, done
        if best_matches == last_matches: break
        last_matches = best_matches

        # Move the centroids to the avg of their numbers
        for i in range(k):
            avgs = [0.0] * len(rows[0])
            if len(best_matches[i]) > 0:
                for row_id in best_matches[i]:
                    for m in range(len(rows[row_id])):
                        avgs[m] += rows[row_id][m]
                for j in range(len(avgs)):
                    avgs[j] /= len(best_matches[i])
                clusters[i] = avgs

    return best_matches


def hcluster(rows, distance=pearson, verbose=False):
    """
    Hierarchical clustering
    :param rows:
    :param distance:
    :param verbose:
    :return:
    """
    distances = {}
    current_cluster_id = -1

    # initially clust is all the rows
    clust = [Bicluster(rows[i], id=i) for i in range(len(rows))]

    while len(clust) > 1:
        lowestpair = (0, 1)
        closest = distance(clust[0].vec, clust[1].vec)

        for i in range(len(clust)):
            for j in range(i + 1, len(clust)):
                # Check cache
                if (clust[i].id, clust[j].id) not in distances:
                    distances[(clust[i].id, clust[j].id)] = distance(clust[i].vec, clust[j].vec)

                d = distances[(clust[i].id, clust[j].id)]

                if d < closest:
                    closest = d
                    lowestpair = (i, j)

        # calculate average of two clusters
        mergevec = [
            (clust[lowestpair[0]].vec[i] + clust[lowestpair[1]].vec[i]) / 2.0
            for i in range(len(clust[0].vec))
        ]

        # create new cluster
        newcluster = Bicluster(mergevec,
                               left=clust[lowestpair[0]],
                               right=clust[lowestpair[1]],
                               distance=closest,
                               id=current_cluster_id)

        # cluster ids that werent in the originial set are -ve
        current_cluster_id -= 1
        del clust[lowestpair[1]]
        del clust[lowestpair[0]]
        clust.append(newcluster)

        if verbose:
            print('appending cluster_id: ' + str(current_cluster_id))

    return clust[0]


def run():
    """
    Run the clustering
    """
    blognames, words, data = read_file('blogdata.txt')
    rdata = rotate_matrix(data)  # rotated data
    # clust = hcluster(rdata, verbose=True)
    # draw_dendogram(clust, labels=words, jpeg='blogclust.jpg')

    kclust = kcluster(data, k=10)
    print kclust


def printclust(clust, labels=None, n=0):
    # indent to make hierarchy
    """

    :param clust:
    :param labels:
    :param n:
    """
    for i in range(n): print ' ',
    if clust.id < 0:
        # -ve means branch
        print('-')
    else:
        # +ve is endpoint
        if labels == None:
            print(clust.id)
        else:
            print(labels[clust.id])

    # Print left right
    if clust.left != None: printclust(clust.left, labels=labels, n=n + 1)
    if clust.right != None: printclust(clust.right, labels=labels, n=n + 1)


if __name__ == '__main__':
    run()