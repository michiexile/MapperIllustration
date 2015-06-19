#!/usr/bin/env python3
__author__ = 'mik'

import argparse
parse = argparse.ArgumentParser()
parse.add_argument('-codensity', action='store_true')
parse.add_argument('-density', action='store_true')
parse.add_argument('-centrality', action='store_true')
opts = parse.parse_args()

from pylab import *
import scipy as sp
from scipy import spatial
from draw_and_rotate import draw_and_rotate

# smoothness parameter for kNN density estimator
knn = 5

pts = r_[sp.random.multivariate_normal((0,0), 1*eye(2), 200),
         sp.random.multivariate_normal((5,0), 0.5*eye(2), 200),
         sp.random.multivariate_normal((0,5), 0.25*eye(2), 200)]

N = pts.shape[0]

# density, centrality
dists = spatial.distance.pdist(pts)
kde = spatial.KDTree(pts)
codensity = zeros((N,))
for i in range(N):
    codensity[i] = kde.query(pts[i,:], knn)[0][-1]
density = 1./codensity
centrality = (spatial.distance.squareform(dists) - eye(N)).max(axis=0)

if opts.codensity:
    draw_and_rotate(pts, codensity, dir='codensity')

if opts.centrality:
    draw_and_rotate(pts, centrality, dir='centrality')

if opts.density:
    draw_and_rotate(pts, density, dir='density')
