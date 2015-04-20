import sys
import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
from pylab import  show, gca, savefig
from matplotlib import mlab  # for csv2rec in plotcsv
from matplotlib.cbook import dedent, silent_list, is_string_like, is_numlike


def plotcsv(fname, cols=(0,), plotfuncs=None,
             comments='#', skiprows=0, checkrows=5, delimiter=',',
             **kwargs):
    """
    plot the data in fname

    cols is a sequence of column identifiers to plot.  An identifier
    is either an int or a string.  if it is an int, it indicates the
    column number.  If it is a string, it indicates the column header.
    mpl will make column headers lower case, replace spaces with
    underscores, and remove all illegal characters; so 'Adj Close*'
    will have name 'adj_close'

    if len(cols)>=1, all elements will be the column
    indexes for multiple subplots

    plotfuncs, if not None, is a dictionary mapping identifier to an
    Axes plotting function as a string.  Default is 'plot', other
    choices are 'semilogy', 'fill', 'bar', etc...  You must use the
    same type of identifier in the cols vector as you use in the
    plotfuncs dictionary, eg integer column numbers in both or column
    names in both.

    comments, skiprows, checkrows, and delimiter are all passed on to
    matplotlib.mlab.csv2rec to load the data into a record array.  See
    the help there fore more information.

    kwargs are passed on to plotting functions

    Example usage:

      # plot the 2nd and 4th column in two subplots
      plotfile(fname, (1,3))

      # plot using column names; specify an alternate plot type for volume
      plotfile(fname, ('date', 'volume', 'adj_close'), plotfuncs={'volume': 'semilogy'})
    """

    fig = plt.figure()
    if len(cols)<1:
        raise ValueError('must have at least one column of data')

    if plotfuncs is None:
        plotfuncs = dict()
    r = mlab.csv2rec(fname, comments=comments,
                skiprows=skiprows, checkrows=checkrows, delimiter=delimiter)

    def getname_val(identifier):
        'return the name and column data for identifier'
        if is_string_like(identifier):
            return identifier, r[identifier]
        elif is_numlike(identifier):
            name = r.dtype.names[int(identifier)]
            return name, r[name]
        else:
            raise TypeError('identifier must be a string or integer')


    N = len(cols)
    for i in range(0,N):
        if i==0:
            ax = ax1 = fig.add_subplot(N,1,i+1)
            ax1.set_title(fname)
            ax.grid(True)
        else:
            ax = fig.add_subplot(N,1,i+1, sharex=ax1)
            ax.grid(True)


        yname, y = getname_val(cols[i])

        funcname = plotfuncs.get(cols[i], 'plot')
        func = getattr(ax, funcname)

        func(y, **kwargs)
        ax.set_ylabel(yname)
        ax.set_xlabel('')
        

    plt.draw_if_interactive()



plotcsv(sys.argv[1],(0,6))
# plotfile(sys.argv[1],(0,))
savefig(sys.argv[1]+'.png')
show()
