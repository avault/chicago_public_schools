'''A notebook containing various helpers for analyzing Chicago Public Schools
data.
'''

import numpy as np
import pandas as pd

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

def histogram_plot( df, column ):
    '''Simple histogram plot for the column of a data frame.'''

    fig = plt.figure( figsize=(12,8), facecolor='white' )
    ax = plt.gca()

    ax.hist(
      np.ma.fix_invalid( df[column] ).compressed()
    )

    ax.set_xlabel( column, fontsize=22 )

    plt.xticks( fontsize=20 )

########################################################################

def scatter_plot( df, x_key, y_key, ):
    '''Simple scatter plot comparing the two categories.
    '''
  
    fig = plt.figure( figsize=(12,11), facecolor='white' )
    ax = plt.gca()

    ax.scatter(
      df[x_key],
      df[y_key]
    )

    ax.set_xlabel( x_key, fontsize=22 )
    ax.set_ylabel( y_key, fontsize=22 )

    plt.xticks( fontsize=20 )
    plt.yticks( fontsize=20 )

########################################################################

