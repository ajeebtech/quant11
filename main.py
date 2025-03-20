import pandas as pd
df = pd.read_csv('schedule.csv')
import datetime
current_datetime = datetime.datetime.now()
df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Start'], format='%d-%b-%y %I:%M %p')
df['TimeDifference'] = (df['DateTime'] - current_datetime).dt.total_seconds().abs()
closest_match = df.loc[df['TimeDifference'].idxmin()]
home_team = closest_match['Home']
away_team = closest_match['Away']
print(closest_match)