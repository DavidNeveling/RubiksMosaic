import random, math, json, requests, sys, numpy
from PIL import Image
from functools import reduce
from collections import defaultdict
from tqdm import tqdm

MAX_ITERATIONS = 20
featureDomains = [(0, 255), (0, 255), (0, 255)]

def kmeans(pixels, size, k):

    numFeatures = 3
    centroids = getRandomCentroids(numFeatures, featureDomains, k)

    iterations = 0
    oldCentroids = None

    pbar = tqdm(total = MAX_ITERATIONS)
    while not shouldStop(oldCentroids, centroids, iterations):

        oldCentroids = centroids[:]
        iterations += 1

        labels = getLabels(pixels, size, centroids)
        threadsperblock = (16, 16)
        blockspergrid_x = math.ceil(size[0] / threadsperblock[0])
        blockspergrid_y = math.ceil(size[1] / threadsperblock[1])
        blockspergrid = (blockspergrid_x, blockspergrid_y) 
        labels_to_pixels = [[] for _ in range(k)] # change to numpy array
        for r in range(len(labels)):
            for c in range(len(labels[r])):
                labels_to_pixels[labels[r][c]].append(pixels[r, c])
        getCentroids(labels_to_pixels, pixels, labels, k, numFeatures, featureDomains, centroids)
        pbar.update(1)
    if iterations < MAX_ITERATIONS:
        pbar.update(MAX_ITERATIONS - iterations)
    return centroids

def shouldStop(oldCentroids, centroids, iterations):
    if iterations > MAX_ITERATIONS: return True
    return oldCentroids == centroids
 
def getLabels(pixels, size, centroids):
    labels = [[0 for _ in range(size[0])] for _ in range(size[1])]
    for r in range(len(labels)):
        for c in range(len(labels[r])):
            centroid_index = 0
            shortest_distance = float('inf')
            for index, centroid in enumerate(centroids):

                squared_differences = [(centroid[i] - pixels[r, c][i])**2 for i in range(len(centroid))]
                distance = math.sqrt(reduce(lambda x, y: x + y, squared_differences))
                if distance < shortest_distance:
                    shortest_distance = distance
                    centroid_index = index
            labels[r][c] = centroid_index
    return labels

def getCentroids(labels_to_pixels, pixels, labels, k, numFeatures, featureDomains, centroids):
    for label in range(len(labels_to_pixels)):
        if len(labels_to_pixels[label]) <= 0:
            centroids[label] = (random.randint(featureDomains[0][0], featureDomains[0][1]), random.randint(featureDomains[1][0], featureDomains[1][1]), random.randint(featureDomains[2][0], featureDomains[2][1]))
            continue 
        avg_pixel_list = [labels_to_pixels[label][0][0], labels_to_pixels[label][0][1], labels_to_pixels[label][0][2]]
        for i, pixel_value in enumerate(labels_to_pixels[label][1:]):
            avg_pixel_list[0] = ((i+1) * avg_pixel_list[0] + pixel_value[0]) / (i+2)
            avg_pixel_list[1] = ((i+1) * avg_pixel_list[1] + pixel_value[1]) / (i+2)
            avg_pixel_list[2] = ((i+1) * avg_pixel_list[2] + pixel_value[2]) / (i+2)
        centroids[label] = (avg_pixel_list[0], avg_pixel_list[1], avg_pixel_list[2])
    return sorted(centroids)

def getRandomCentroids(numFeatures, featureDomains, k):
    return sorted([getRandomCentroid(numFeatures, featureDomains) for _ in range(k)])

def getRandomCentroid(numFeatures, featureDomains):
    return tuple([random.randint(featureDomains[i][0], featureDomains[i][1]) for i in range(numFeatures)])

def main():
    k = 6
    image_name = sys.argv[1]
    with Image.open(image_name) as im:
        pixels = numpy.array(im)
        size = im.size

    centroids = kmeans(pixels, size, k)
    rounded_centroids = [tuple([round(j) for j in centroid]) for centroid in centroids]
    custom_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 127, 0), (255, 255, 0), (255, 255, 255)]
    use_custom = True

    for r in range(size[1]):
        for c in range(size[0]):
            centroid_index = 0
            shortest_distance = float('inf')
            for index, centroid in enumerate(centroids):
                squared_differences = [(centroid[i] - pixels[r, c][i])**2 for i in range(len(centroid))]
                distance = math.sqrt(reduce(lambda x, y: x + y, squared_differences))
                if distance < shortest_distance:
                    shortest_distance = distance
                    centroid_index = index
            if use_custom:
                pixels[r, c] = custom_colors[centroid_index]
            else:
                pixels[r, c] = rounded_centroids[centroid_index]
    im = Image.fromarray(pixels)
    im = im.resize((18, 18))
    im.save(image_name[:image_name.rfind('.')] + '.mosaic' + image_name[image_name.rfind('.'):])

if __name__ == '__main__':
    main()