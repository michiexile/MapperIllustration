__author__ = 'mik'

from matplotlib import use
use('Agg')

from pylab import *
import scipy as sp
from scipy import spatial
from mpl_toolkits.mplot3d import Axes3D
import os, os.path
import subprocess

def draw_and_rotate(pts, func, cmap=cm.jet, dir='figure', fps=15):
    """
    Scatterplot and rotate the points in `pts` as described by the
    filter function in `func`.
    Save out .png files into the directory `dir` and at the end
    call `mencoder` to produce a video file of the entire process

    :param pts:  datapoints, Nx2 numpy array
    :param func: function values, Nx1 numpy array
    :param cmap: colormap for the scatter plot
    :param dir:  directory to save .png files
    :param fps:  FPS for the video generation
    :return:     None
    """

    if not os.path.exists(dir):
        os.mkdir(dir)

    fig = figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.view_init(90,0)
    ax.set_axis_off()

    filelist = open('filelist.txt', 'w')

    print('starting %s…' % dir)
    # flat starting view
    ax.scatter(pts[:,0],pts[:,1],zeros(pts[:,0].shape))
    savefig('%s/start.png' % dir)
    print('%s/start.png' % dir, file=filelist)
    ax.cla()

    # colored and offset by function
    ax.scatter(pts[:,0],pts[:,1],func, c=func, cmap=cmap)
    savefig('%s/colorized.png' % dir)
    print('%s/colorized.png' % dir, file=filelist)
    ax.view_init(90,0)
    ax.set_axis_off()


    print('rotate elevation…')
    # rotate bit by bit
    for i in range(90):
        ax.view_init(90-i,i)
        savefig('%s/elevate%03d.png' % (dir, i))
        print('%s/elevate%03d.png' % (dir, i), file=filelist)

    print('rotate azimuth…')
    for i in range(360):
        ax.view_init(0,i+90)
        savefig('%s/azimuth%03d.png' % (dir, i))
        print('%s/azimuth%03d.png' % (dir, i), file=filelist)

    close()
    filelist.close()

    print('creating video')
    subprocess.call(['mencoder',
                     'mf://@%s' % 'filelist.txt',
                     '-mf', 'fps=%d:type=png' % fps,
                     '-ovc', 'lavc', '-oac', 'copy',
                     '-o', '%s.avi' % dir])
