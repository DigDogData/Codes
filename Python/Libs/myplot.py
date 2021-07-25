import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt

# pairplot with option to hide off-diagonal plots
def pair_plot(df, hue=None, diagkind='hist', offkind='scatter', s=15, alpha=1, palette=None, upper=False, lower=True, diag=True):
    sb.set_style('ticks')
    g = sb.pairplot(df,
                   hue = hue,
                   diag_kind = diagkind,
                   kind = offkind,
                   palette = palette,
                   plot_kws = dict(s=s, alpha=alpha),
                   height = 1.4,
                   aspect = 1.2)
    if not lower:
        upper = True
        for i, j in zip(*np.triu_indices_from(g.axes, 1)):
            g.axes[j, i].set_visible(False)
        g._legend.set_bbox_to_anchor((0.15,0.15))
    if not upper:
        for i, j in zip(*np.triu_indices_from(g.axes, 1)):
            g.axes[i, j].set_visible(False)
        g._legend.set_bbox_to_anchor((0.85,0.85))
    if not diag:
        for ax in g.diag_axes:
            ax.set_visible(False)
    plt.show()



# histogram plot
def hist_plot(df, variable, binsize, title=False, noplot=True):
    df[variable] = df[variable].astype("int64", copy=True)
    plt.close()
    fig, ax = plt.subplots()
    n, bins, patches = ax.hist(df[variable], bins=binsize, color="tab:blue", density= False)
    ax.set_xlabel(f"{variable} (bins={binsize})")
    ax.set_ylabel("count")
    if title:
        ax.set_title(f"{variable} bins")
    if noplot:
        plt.close()     # remove plot
    return list(n)      # return bin frequency

# heatmap plot
def hmap(df, xrotate=0, yrotate=0):
    plt.close()
    fig, ax = plt.subplots()
    fig.subplots_adjust(bottom=0.12, left=0.12) # make room for labels
    heatmap = ax.pcolor(df, cmap="RdBu")
    fig.colorbar(heatmap)
    # center ticklabels
    ax.set_xticks(np.arange(df.shape[1])+0.5, minor=False)
    ax.set_yticks(np.arange(df.shape[0])+0.5, minor=False)
    # set ticklabels + rotate if necessary
    ax.set_xticklabels(df.columns.levels[1], minor=False, rotation=xrotate)
    ax.set_yticklabels(df.index, minor=False, rotation=yrotate)

# correlation plot
def corr_plot(df, variable1, variable2):
    plt.close()
    fig, ax = plt.subplots()
    sb.regplot(x=variable1, y=variable2, data=df)
    plt.ylim(0,)

# box plot
def box_plot(df, variable1, variable2):
    plt.close()
    sb.catplot(x=variable1, y=variable2, kind="box", data=df)

# multiple box plots of categorical features and label
def box_plots(df, variables, label, nrows, ncols):
    plt.close()
    plt.figure(figsize=(15,10))
    for i, variable in enumerate(variables, 1):
        plt.subplot(nrows, ncols, i) 
        g = sb.boxplot(x=variable, y=label, data=df)
#        g.set(xlabel=None)
#        g.set(yticklabels=[])

# comparing distribution plots of prediction and data
def dist_plots(data, prediction, title=None):
    xmax = data.values.max()
    xmin = data.values.min()
    ax1 = sb.distplot(data,
                       hist = False,    # plot continuous distribution
#                       kde_kws = {"clip": (xmin, xmax)},
                       color = "r",
                       label = "Data")
    sb.distplot(prediction,
                 hist = False,
                 kde_kws = {"clip": (xmin, xmax)},
                 color = "b",
                 label = "Prediction",
                 ax = ax1)
    plt.title(title)
    plt.show()
    plt.close()

# comparing data scatterplot with predicted polynomial function
def poly_plot(xtrain, xtest, ytrain, ytest, model, poly, xlab, ylab):
    xmax = max([xtrain.values.max(), xtest.values.max()])
    xmin = min([xtrain.values.min(), xtest.values.min()])
    ymax = max([ytrain.values.max(), ytest.values.max()])
    ymin = min([ytrain.values.min(), ytest.values.min()])
    yrange = ymax - ymin
    ymin = ymin - yrange * 0.1
    ymax = ymax + yrange * 0.1
    x = np.arange(xmin, xmax, 0.1)
    plt.plot(xtrain, ytrain, 'ro', label = 'Training Data')
    plt.plot(xtest, ytest, 'go', label = 'Test Data')
    plt.plot(x = x,
             y = model.predict(poly.fit_transform(x.reshape(-1, 1))),
             label='Predicted Function')
    plt.ylim([ymin, ymax])
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.legend()

# waffle chart (displays contribution of each category to total in area map)
"""
def waffle_chart(df, categories, values, height, width, colormap=plt.cm.coolwarm, value_sign=''):
    print ('I am here')
    import matplotlib.patches as mpatches # needed for waffle Charts

    # compute the proportion of each category with respect to the total
    total_values = sum(values)
    category_proportions = [(float(value) / total_values) for value in values]
    print ('I am here')

    # compute the total number of tiles
    total_num_tiles = width * height # total number of tiles
    print ('Total number of tiles is', total_num_tiles)
    
    # compute the number of tiles for each catagory
    tiles_per_category = [round(proportion * total_num_tiles) for proportion in category_proportions]

    # print out number of tiles per category
    for i, tiles in enumerate(tiles_per_category):
        print (df.index.values[i] + ': ' + str(tiles))
    
    # initialize the waffle chart as an empty matrix
    waffle_chart = np.zeros((height, width))

    # define indices to loop through waffle chart
    category_index = 0
    tile_index = 0

    # populate the waffle chart
    for col in range(width):
        for row in range(height):
            tile_index += 1

            # if the number of tiles populated for the current category 
            # is equal to its corresponding allocated tiles...
            if tile_index > sum(tiles_per_category[0:category_index]):
                # ...proceed to the next category
                category_index += 1       
            
            # set the class value to an integer, which increases with class
            waffle_chart[row, col] = category_index
    
    # instantiate a new figure object
    fig = plt.figure()

    # use matshow to display the waffle chart
    colormap = plt.cm.coolwarm
    plt.matshow(waffle_chart, cmap=colormap)
    plt.colorbar()

    # get the axis
    ax = plt.gca()

    # set minor ticks
    ax.set_xticks(np.arange(-.5, (width), 1), minor=True)
    ax.set_yticks(np.arange(-.5, (height), 1), minor=True)
    
    # add dridlines based on minor ticks
    ax.grid(which='minor', color='w', linestyle='-', linewidth=2)

    plt.xticks([])
    plt.yticks([])

    # compute cumulative sum of individual categories to match color schemes between chart and legend
    values_cumsum = np.cumsum(values)
    total_values = values_cumsum[len(values_cumsum) - 1]

    # create legend
    legend_handles = []
    for i, category in enumerate(categories):
        if value_sign == '%':
            label_str = category + ' (' + str(values[i]) + value_sign + ')'
        else:
            label_str = category + ' (' + value_sign + str(values[i]) + ')'
            
        color_val = colormap(float(values_cumsum[i])/total_values)
        legend_handles.append(mpatches.Patch(color=color_val, label=label_str))

    # add legend to chart
    plt.legend(
        handles=legend_handles,
        loc='lower center', 
        ncol=len(categories),
        bbox_to_anchor=(0., -0.2, 0.95, .1)
    )

# this function prints and plots confusion matrix.
def plot_cfmatrix(cm, classes, normalize=False):
    import itertools
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    print("Confusion Matrix:")
    print(cm)
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    if normalize:
        plt.title("Confusion Matrix (normalized)")
    else:
        plt.title("Confusion Matrix")
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
"""
# set map axes + add ticks based on map extent
def set_axes(ax, extent, proj):
    from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
    ax.set_extent(extent,crs=proj)
    ax.set_xticks(np.linspace(extent[0],extent[1],7),crs=proj) # set longitude indicators
    ax.set_yticks(np.linspace(extent[2],extent[3],7)[1:],crs=proj) # set latitude indicators
    lon_formatter = LongitudeFormatter(number_format='0.1f',degree_symbol='',dateline_direction_label=True) # format lons
    lat_formatter = LatitudeFormatter(number_format='0.1f',degree_symbol='') # format lats
    ax.xaxis.set_major_formatter(lon_formatter) # set lons
    ax.yaxis.set_major_formatter(lat_formatter) # set lats
    ax.xaxis.set_tick_params(labelsize=10)
    ax.yaxis.set_tick_params(labelsize=10)
    return ax