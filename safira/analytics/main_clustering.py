# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 17:43:53 2020

@author: custo
"""
import pandas as pd
import os
from sklearn.cluster import KMeans
from math import sqrt
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import pickle
from sklearn import metrics
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

def pca_use_n_components(xi, number_components):
    '''
    Constructor
    '''

    # Standardizing the features
    x = StandardScaler().fit_transform(xi)

    pca = PCA(n_components=number_components)
    principal_components = pca.fit_transform(x)
    principal_df = pd.DataFrame(data=principal_components,
                                columns=['principal component 1', 'principal component 2'])

    #    print(principalDf)

    print(f'A variância de cada componente principal é: {pca.explained_variance_ratio_ * 100} %')
    print(f'A variância total (informação) obtida é {sum(pca.explained_variance_ratio_) * 100} %')

    return principal_df


def pca_use_variance_ratio(xi, variance_ratio):
    '''
    Constructor
    '''

    # Standardizing the features
    x = StandardScaler().fit_transform(xi)

    pca = PCA(variance_ratio)
    principal_components = pca.fit_transform(x)
    principal_df = pd.DataFrame(data=principal_components)

    print(f'O número de componentes necessárias é {pca.n_components_} para uma \
variância de {sum(pca.explained_variance_ratio_) * 100} %')
    return principal_df

    # Concatenating
    # finalDf = pd.concat([principalDf, df[['target']]], axis = 1)

    # How much information was lost


def run_kmeans(X, n):
    # rodando o kmeans para nossa quantidade ótima de clusters
    km = KMeans(n_clusters=n, init="k-means++", n_init=10)
    clusters = km.fit_predict(X)
    cluster_centers = km.cluster_centers_
    return clusters, cluster_centers

def plotter(X, clusters, cluster_centers):
    
    fig = plt.figure(figsize = (8,8))
    ax = fig.add_subplot(1,1,1) 
    ax.set_xlabel('Principal Component 1', fontsize = 15)
    ax.set_ylabel('Principal Component 2', fontsize = 15)
    ax.set_title('2 component PCA', fontsize = 20)
    colors = ['r', 'g', 'b']
    ax.scatter(X[0].values
              , X[1].values
              , c = clusters)
    
#    cluster_centers_trans=cluster_centers.transpose()
#    ax.scatter(cluster_centers_trans[0],cluster_centers_trans[1], marker ="*",color='r', s=100)
#    plt.show()

if __name__ == "__main__":
    # Directory
    path = r'C:\Users\custo\Desktop\hackaton'
    file_name = 'data_perfil_investimento_agrupado'
    # Number of clusters
    n = 4
    # obs: the optimal number can be found using the elbow method.
    # In this case, we select 4 because we have 4 customer profiles.
    # Load dataframe
    df = pd.read_csv(f'{path}//{file_name}.csv')
    # PCA
    X = pca_use_variance_ratio(df[['Risco Baixo', 'Risco Moderado', 'Risco Alto']], 0.90)  # PCA engine initialization
    # Cluster
    clusters, cluster_centers = run_kmeans(X, n)
    # 2D Plot
    plotter(X, clusters, cluster_centers)
    # Metrics
    print('Number of clusters: %d' % len(clusters))
    print("Silhouette Coefficient: %0.3f"
          % metrics.silhouette_score(X, clusters))