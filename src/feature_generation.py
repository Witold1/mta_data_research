import pandas as pd
import numpy as np

def add_stations(df, path_to_stations_dataset):
    """Appends station dataset.

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe which to add generated features
    path_to_stations_coords : str
        Relative or absolute path to file with extra features
    """
    df_stations = pd.read_csv(path_to_stations_dataset)
    df = pd.merge(df, df_stations, left_on=['C/A', 'UNIT'], right_on=['Booth', 'Remote'], how='left')
    df = df.drop(columns = ['Remote', 'Booth'])

    return df

def add_coordinates(df, path_to_stations_coords):
    """Appends geocoded station coordinates to main table.

        # External dataset credits to Chris Whong - nycturnstiles,
            https://github.com/chriswhong/nycturnstiles/blob/master/geocoded.csv
            ' cos I was to lazy to geocode from scratch.

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe which to add generated features
    path_to_stations_coords : str
        Relative or absolute path to file with extra features
    """
    # stations_coords columns={0:'UNIT', 1:'C/A', 2:'Station', 3:'Line Name', 4:'Division', 5:'Lat', 6:'Lon'}
    df_stations_coords = pd.read_csv(path_to_stations_coords, header=None)
    df = pd.merge(df, df_stations_coords, left_on=['C/A', 'UNIT'], right_on=[1, 0], how='left')
    df = df.drop(columns=[0, 1, 2, 3, 4]).rename(columns={5:'Lat', 6:'Lon'})

    return df

def calc_features_from_datetime(df, from_date=True, from_time=True):
    """"Extracts basic date and time features from date & time type column(s).
            Extracts: year, month number, day of week number from DATE field
            Extracts: hour, minute from TIME field

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe containing source columns and which to add generated features
    from_date : bool
        Yes/No generate features from date column
    from_time : bool
        Yes/No generate features from time column
    """

    df['AUDIT_DATE_TIME'] = pd.to_datetime(df.DATE + " " + df.TIME)
    #df['DATE'] = df.DATE.astype('datetime64[ns]')
    if from_date:
        df['AUDIT_YEAR'] = df.DATE.astype('datetime64[ns]').dt.year
        df['AUDIT_MONTH'] = df.DATE.astype('datetime64[ns]').dt.month
        df['AUDIT_WEEK'] = df.DATE.astype('datetime64[ns]').dt.week
        df['AUDIT_DOW'] = df.DATE.astype('datetime64[ns]').dt.weekday
        #df['IS_WEEKEND_FLAG'] = df['AUDIT_DOW'].isin([5, 6]) # count holidays here?
    if from_time:
        df['AUDIT_HOUR'] = df.TIME.astype('datetime64[ns]').dt.hour
        df['AUDIT_MINUTE'] = df.TIME.astype('datetime64[ns]').dt.minute

    return df

def _cacl_time_difference_between_audits(df):
    """Calculates time difference between consequential audits.
        For instance, between audits at 12:00:00 and at 12:01:59, or at 14:00:00 and 15:00:00

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe containing source columns and which to add generated features
    """
    TIME_DIFF = df.AUDIT_DATE_TIME - df.AUDIT_DATE_TIME.shift(1)
    # TIME_DIFF > 1 day -= null
    # z['Time_diff'] = df.groupby(['C/A','UNIT','SCP']).AUDIT_DATE_TIME.diff(1).fillna(np.timedelta64(0, 'D'))
    # z['Time_diff'] = z.Time_diff.where((z.Time_diff < np.timedelta64(1, 'D')), np.timedelta64(0, 'D'))
    df['TIME_DIFF'] = TIME_DIFF

    return df

def calc_features_from_cumulative_records(df):
    """Calculates relative `EXIT` and `ENTRY` values between two consequential audits.
            (!) Note these aren’t counts per interval, but equivalent to an “odometer”
            reading for each device
        Also, cleanes 'outliers' (negative or too big relative values)
        Also, calculates `busy-ness` metric defined as sum of entries and exits

        Code idea and code credits to Two Sigma Data Clinic - MTA,
            https://github.com/tsdataclinic/mta/blob/master/src/turnstile/turnstile.py#L41

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe containing source columns and which to add generated features
    """

    df['ENTRIES_DIFF'] = df.groupby(['C/A','UNIT','SCP']).ENTRIES.diff(1) # may use apply(func) too
    df['EXITS_DIFF'] = df.groupby(['C/A','UNIT','SCP']).EXITS.diff(1) # may use apply(func) too

    # set negative or too large values to empty value
    df['ENTRIES_DIFF'] = df.ENTRIES_DIFF.where((df.ENTRIES_DIFF >= 0) & (df.ENTRIES_DIFF < 10000), np.nan)
    df['EXITS_DIFF'] = df.EXITS_DIFF.where((df.EXITS_DIFF >= 0) & (df.EXITS_DIFF < 10000), np.nan)
    #df['ENTRIES_CLEAN'] = df.groupby(['C/A','UNIT','SCP']).ENTRIES_DIFF.cumsum()
    #df['EXITS_CLEAN'] = df.groupby(['C/A','UNIT','SCP']).EXITS_DIFF.cumsum()

    df['BUSYNESS'] = df['ENTRIES_DIFF'] + df['EXITS_DIFF']

    return df

### not used now, functional is in func `calc_features_from_cumulative_records`
def _calc_entries_diff(df : pd.DataFrame):
    """NOT USED NOW Calculates difference in cumulative ENTRIES of two consequential audits
        The 'ENTRIES' variable recorded in the MTA data are cumulative entries of the turnstile per row.
        Considering the data for a single turnstile machine (unique SCP, C/A, and UNIT),
        we want to add a new column symbolizing the incremental number of entries since the last recording time.

        Code credits to http://www.columbia.edu/~yh2693/MTA_data.html

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe containing source columns and which to add generated features
    """
    HOURLY_ENTRIES = df.ENTRIES - df.ENTRIES.shift(1)
    df['HOURLY_ENTRIES'] = HOURLY_ENTRIES#.fillna(np.nan)
    return df

### not used now, functional is in func `calc_features_from_cumulative_records`
def _calc_exits_diff(df : pd.DataFrame):
    """NOT USED NOW Calculates difference in cumulative EXITS of two consequential audits
        The 'EXITS' variable recorded in the MTA data are cumulative exits of the turnstile per row.
        Considering the data for a single turnstile machine (unique SCP, C/A, and UNIT),
        we want to add a new column symbolizing the incremental number of exits since the last recording time.

        Code credits to http://www.columbia.edu/~yh2693/MTA_data.html

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe containing source columns and which to add generated features
    """
    HOURLY_EXITS = df.EXITS - df.EXITS.shift(1)
    df['HOURLY_EXITS'] = HOURLY_EXITS#.fillna(np.nan)
    return df

### not used now, functional is in func `calc_features_from_cumulative_records`
def _calc_busyness(df : pd.DataFrame):
    """NOT USED NOW Calculates `busy-ness metric` using `ENTRY` and `EXIT` numbers
        We define `busyness` metric as sum of entries and exits.

        Code credits to http://www.columbia.edu/~yh2693/MTA_data.html

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe containing source columns and which to add generated features
    """
    BUSYNESS = df.HOURLY_ENTRIES + df.HOURLY_EXITS
    df['BUSYNESS'] = BUSYNESS
    return df
