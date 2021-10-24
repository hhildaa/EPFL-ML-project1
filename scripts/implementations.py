import numpy as np
import matplotlib.pyplot as plt

def batch_iter(y, tx, batch_size, num_batches=1, shuffle=True):
    """
    Generate a minibatch iterator for a dataset.
    Takes as input two iterables (here the output desired values 'y' and the input data 'tx')
    Outputs an iterator which gives mini-batches of `batch_size` matching elements from `y` and `tx`.
    Data can be randomly shuffled to avoid ordering in the original data messing with the randomness of the minibatches.
    Example of use :
    for minibatch_y, minibatch_tx in batch_iter(y, tx, 32):
        <DO-SOMETHING>
    """
    data_size = len(y)

    if shuffle:
        shuffle_indices = np.random.permutation(np.arange(data_size))
        shuffled_y = y[shuffle_indices]
        shuffled_tx = tx[shuffle_indices]
    else:
        shuffled_y = y
        shuffled_tx = tx
    for batch_num in range(num_batches):
        start_index = batch_num * batch_size
        end_index = min((batch_num + 1) * batch_size, data_size)
        if start_index != end_index:
            yield shuffled_y[start_index:end_index], shuffled_tx[start_index:end_index]

            
def sigmoid(z):
    return 1.0 / (1 + np.exp(-z))


def clipping(h):
    abs_threshold = 15
    h[h > abs_threshold] = abs_threshold
    h[h < -abs_threshold] = -abs_threshold
    return h


def cross_entropy_loss(y, tx, w):
    # clipping values to avoid INF loss
    h = sigmoid(clipping(tx @ w))
    return np.squeeze((-y.T @ np.log(h)) + (-(1 - y).T @ np.log(1 - h)))
                  
    
def cross_entropy_gradient(y, tx, w):
    h = sigmoid(tx @ w)
    return (tx.T @ (h - y))


def regularized_cross_entropy_loss(y, tx, w, lambda_):
    return cross_entropy_loss(y, tx, w) + lambda_ * np.squeeze(w.T @ w)


def regularized_cross_entropy_gradient(y, tx, w, lambda_):
    return cross_entropy_gradient(y, tx, w) + 2 * lambda_ * w


def logistic_regression(y, tx, initial_w, max_iters, gamma, batch_size=1):
    w = initial_w
    for n_iter in range(max_iters):
        for minibatch_y, minibatch_tx in batch_iter(y, tx, batch_size):
            gr = cross_entropy_gradient(minibatch_y, minibatch_tx, w)
            w = w - gamma * gr
            
        loss = cross_entropy_loss(y, tx, w)
            
#        print("SGD ({bi}/{ti}): loss={l}, w0={w0}, w1={w1}".format(
#              bi=n_iter, ti=max_iters - 1, l=loss, w0=w[0], w1=w[1]))
    return (w, loss)


def reg_logistic_regression(y, tx, lambda_ , initial_w, max_iters, gamma, batch_size=1):
    w = initial_w
    for n_iter in range(max_iters):
        for minibatch_y, minibatch_tx in batch_iter(y, tx, batch_size):
            gr = regularized_cross_entropy_gradient(minibatch_y, minibatch_tx, w, lambda_)
            w = w - gamma * gr
            
        loss = regularized_cross_entropy_loss(y, tx, w, lambda_)
            
#        print("SGD({bi}/{ti}): loss={l}, w0={w0}, w1={w1}".format(
#              bi=n_iter, ti=max_iters - 1, l=loss, w0=w[0], w1=w[1]))
    return (w, loss)