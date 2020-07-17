import ipyvolume as ipv
import numpy as np
from scipy.interpolate import interp1d

def get_tf():
    # First part is a simpler version of setting up the transfer function. Interpolation with higher order
    # splines does not work well, the original must do sth different
    colors = [[0.91, 0.7, 0.61, 0.0], [0.91, 0.7, 0.61, 80.0], [1.0, 1.0, 0.85, 82.0], [1.0, 1.0, 0.85, 256]]
    x = np.array([k[-1] for k in colors])
    rgb = np.array([k[:3] for k in colors])
    N = 256
    xnew = np.linspace(0, 256, N)
    tf_data = np.zeros((N, 4))
    kind = 'linear'
    for channel in range(3):
        f = interp1d(x, rgb[:, channel], kind=kind)
        ynew = f(xnew)
        tf_data[:, channel] = ynew
    alphas = [[0, 0], [0, 40], [0.2, 60], [0.05, 63], [0, 80], [0.9, 82], [1.0, 256]]
    x = np.array([k[1] * 1.0 for k in alphas])
    y = np.array([k[0] * 1.0 for k in alphas])
    f = interp1d(x, y, kind=kind)
    ynew = f(xnew)
    tf_data[:, 3] = ynew
    tf = ipv.TransferFunction(rgba=tf_data.astype(np.float32))
    
    return tf