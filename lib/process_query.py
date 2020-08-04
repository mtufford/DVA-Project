# These are functions to process query results so original sqlite database is untouched

import pandas


def convert_causes(df):
    # convert cause in dataframe and return updated dataframe

    dict_cause = {
        'Lightning': 'Natural',
        'Structure': 'Infrastructure Accident',
        'Powerline': 'Infrastructure Accident',
        'Railroad': 'Infrastructure Accident',
        'Fireworks': 'Human Accident',
        'Smoking': 'Human Accident',
        'Children': 'Human Accident',
        'Campfire': 'Human Accident',
        'Equipment Use': 'Human Accident',
        'Debris Burning': 'Human Accident',
        'Arson': 'Arson',
        'Missing/Undefined': 'Other',
        'Miscellaneous': 'Other'
    }

    # replace values in cause column if present
    if 'STAT_CAUSE_DESCR' in df.columns:
        df['STAT_CAUSE_DESCR'].replace(dict_cause, inplace=True)

    return df
