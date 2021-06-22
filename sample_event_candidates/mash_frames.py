import pandas
import glob
import functools
pandas.set_option('mode.chained_assignment', None)
#suppress annoying warning

def mash_csv_from_dir(path, columns_to_df):
    '''
    #cols_to_df are a list of the relevant cols
    #returns a data frame
    '''
    df = pandas.concat(map(functools.partial(pandas.read_csv, sep='\t', compression=None),
                        glob.glob(path+"*.csv")))
    print(df.columns)
    newdf = df[columns_to_df]

    newdf['protocol_terms'] = newdf['protocol_terms'].replace('#','',regex=True)
    #specific to the ElasticSearch highlight used in 'sample_event_ES_dataset_finder
    
    return newdf