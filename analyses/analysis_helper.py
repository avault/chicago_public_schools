'''A notebook containing various helpers for analyzing Chicago Public Schools
data.
'''

import numpy as np
import pandas as pd
import palettable

import matplotlib
import matplotlib.pyplot as plt

########################################################################

def load_data():
    '''Load the data. Currently only works for CPS 2016-2017 data.
    '''

    # Make sure we can see all the data
    pd.set_option('display.max_rows', None)

    # Load Data
    profile_df = pd.read_csv(
        '../data/Chicago_Public_Schools_-_School_Profile_Information_SY1617.csv'
    )
    progress_df = pd.read_csv(
        '../data/Chicago_Public_Schools_-_School_Progress_Reports_SY1617.csv'
    )

    profile_df.set_index( 'School_ID', inplace=True )
    progress_df.set_index( 'School_ID', inplace=True )

    print( '{} school profiles'.format( len( profile_df ) ) )
    print( '{} school progress reports'.format( len( progress_df ) ) )

    # Combine into one df
    combined_df = pd.concat( [profile_df, progress_df ], axis=1 )

    # Choose high schools
    is_hs = profile_df['Is_High_School'] == 'Y'
    hs_df = combined_df.loc[is_hs]

    return combined_df, hs_df

########################################################################

def convert_qualitative_to_quantitiative(
    df,
    key,
    mapping,
    key_to_store = None,
):

    quant_values = []
    for qual_assessment in df[key]:
        quant_values.append( mapping[qual_assessment] )

    if key_to_store is None:
        key_to_store = '{}_Int'.format( key )

    df[key_to_store] = np.array( quant_values )

    return df

########################################################################

def histogram_plot( df, column, ax=None ):
    '''Simple histogram plot for the column of a data frame.'''

    if ax is None:
        fig = plt.figure( figsize=(12,8), facecolor='white' )
        ax = plt.gca()

    ax.hist(
      np.ma.fix_invalid( df[column] ).compressed()
    )

    ax.set_xlabel( column, fontsize=22 )

    plt.xticks( fontsize=20 )

########################################################################

def multi_hist_plot(
    df,
    hist_key,
    dep_key,
    mapping,
    bins = 16,
    hist_label = None,
    key_to_store = None,
    mpl_cmap = 'Plasma',
):

    # Convert quantitative to qualitative
    df = convert_qualitative_to_quantitiative(
        df,
        dep_key,
        mapping,
        key_to_store = key_to_store,
    )

    fig = plt.figure( figsize=(12,8), facecolor='white' )
    ax = plt.gca()

    # Get the colormap out
    cmap = getattr(
        palettable.matplotlib,
        '{}_{}'.format( mpl_cmap, len( mapping ) )
    )

    for i, qual in enumerate( mapping.keys() ):

        quant = mapping[qual]

        if quant < 0:
            continue

        is_qual = df[dep_key] == qual

        color = cmap.mpl_colors[int(quant-1)]

        ax.hist(
            np.ma.fix_invalid( df[hist_key].loc[is_qual] ).compressed(),
            histtype = 'step',
            linewidth = 10,
            color = color,
            bins = bins,
        )

    # Add a label
    if hist_label is None:
        hist_label = hist_key
    ax.set_xlabel( hist_label, fontsize=22 )

    plt.xticks( fontsize=20 )

########################################################################

def scatter_plot(
    df,
    x_key,
    y_key,
    x_mapping = None,
    jitter = None,
    x_label = None,
    y_label = None,
    x_lim = None,
    y_lim = None,
):
    '''Simple scatter plot comparing the two categories.
    '''
  
    fig = plt.figure( figsize=(12,11), facecolor='white' )
    ax = plt.gca()

    # Convert qualitative to quantitative
    if x_mapping is not None:
        key_to_store = '{}_Int'.format( x_key )
        df = convert_qualitative_to_quantitiative(
            df,
            x_key,
            x_mapping,
            key_to_store = key_to_store,
        )
        x_key = key_to_store

    if jitter is None:
        offset = 0.
    else:
        offset = np.random.uniform(
            -jitter,
            jitter,
            df[x_key].shape
        )

    ax.scatter(
      df[x_key] + offset,
      df[y_key]
    )

    if x_label is None:
        x_label = x_key
    if y_label is None:
        y_label = y_key

    ax.set_xlabel( x_label, fontsize=22 )
    ax.set_ylabel( y_label, fontsize=22 )

    plt.xticks( fontsize=20 )
    plt.yticks( fontsize=20 )

    if x_lim is not None:
        ax.set_xlim( x_lim )
    if y_lim is not None:
        ax.set_ylim( y_lim )

########################################################################

