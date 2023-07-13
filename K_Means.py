import pandas as pd
import numpy as np
import random
import math
import folium

uber_data = pd.read_csv("raw_uber_data.csv", usecols = ['Lat', 'Lon'])
lat_data = uber_data["Lat"].to_list()
lon_data = uber_data["Lon"].to_list()
data = [lat_data, lon_data]


def calc_distance(k, data, centroid):
    dist_matrix = []
    for row_1 in range(len(lon_data)):  # goes through every pt
        row_list = []
        for i in range(k):  # through ever cluster
            dist = math.sqrt((data[0][row_1] - centroid[i][0]) ** 2 + (data[1][row_1] - centroid[i][1]) ** 2)
            row_list.append(dist)  # adds dist from each cluster to pt
        dist_matrix.append(row_list)  # adds various dist from clusters to pt
    return dist_matrix


def cluster(dist_matrix, k):
    vector = []
    for row in dist_matrix:
        vector.append(np.argmin(row))  # gets closest pt and returns idx

    new_matrix = np.column_stack((lat_data, lon_data, vector))  # matrix with data and extra col that is vector

    centroid = [k*[0],k*[0]]

    total = k*[0]

    for row in new_matrix:  # adding each pt to a cluster for averaging
        cluster_indx = int(row[2])
        centroid[0][cluster_indx] += row[0]
        centroid[1][cluster_indx] += row[1]
        total[cluster_indx] += 1

    for i in range(k):  # dividing by total # of pts in cluster
        centroid[0][i] /= total[i]
        centroid[1][i] /= total[i]

    return np.column_stack(centroid)



def k_means(k, data):
    latitude = []
    longitude = []
    for point in range(k):  # taking random pt from data matrix as 1 of k centroids
        coord = random.randrange(len(lat_data))
        latitude.append(data[0][coord])
        longitude.append(data[1][coord])

    centroid = np.column_stack((latitude, longitude))

    for i in range(20):
        dist_matrix = calc_distance(k, data, centroid)
        centroid = cluster(dist_matrix, k)

    # for visualization purposes
    map = folium.Map(location=centroid[0,:], zoom_start=250)
    for point in range(len(centroid)):
        folium.Marker(centroid[point,:], popup = centroid[point,:]).add_to(map)
    map.save('index.html')

    return centroid


k_means(6, data)


# disregard this previous/incorrect implementation of kmeans
# class Kmeans():
#     def __init__(self, k, data):
#
#         latitude = []
#         longitude = []
#         for point in range(k):
#             coord = random.randrange(len(lat_data))
#             latitude.append(data[coord][0])
#             longitude.append(data[coord][1])
#
#         self.centroid = np.column_stack((latitude, longitude))
#         print(self.centroid)
#
#     def graph(self):
#         x = []
#         y = []
#         for point in self.centroid:
#             x.append(point[0])
#             y.append(point[1])
#
#         x_2 = []
#         y_2 = []
#         for point in self.data:
#             x_2.append(point[0])
#             y_2.append(point[1])
#
#         plt.scatter(x_2, y_2, c='black', marker='o', s=20)
#         plt.scatter(x, y, c='red', marker='P', s=40)
#         plt.show()
#
#
#
#     def run(self):
#         for i in range(2):
#             self.calc_distance()
#             centroid = cluster(self.calc_distance())
#             print(self.centroid)
#         map = folium.Map(location=self.centroid[0,:], zoom_start=250)
#         for point in range(len(self.centroid)):
#             folium.Marker(self.centroid[point,:], popup = self.centroid[point,:]).add_to(map)
#         map.save('index.html')
#
#         return self.centroid


