# these function return our dataframe ----->
import matplotlib.pyplot as plt
import pandas as pd
import re
def preprocess(data):
    # Split the string into a list of messages
    messages = data.split('\n')

    # Define the regular expression pattern
    pattern = r'(\d{1,2}/\d{1,2}/\d{2}),\s(\d{1,2}:\d{2}\u202f[AP]M)\s-\s(.*)'

    # Lists to store extracted data
    dates_times = []
    users = []
    messages_list = []

    # Extract data from each message
    for message in messages:
        match = re.match(pattern, message)
        if match:
            date = match.group(1)
            time = match.group(2)
            content = match.group(3)

            # Combine date and time
            date_time = f"{date}, {time}"

            # Separate user and message
            if ': ' in content:
                user, msg = content.split(': ', 1)
            else:
                user = 'Unknown'
                msg = content

            dates_times.append(date_time)
            users.append(user)
            messages_list.append(msg)

    # Create a DataFrame
    df = pd.DataFrame({
        'Date_Time': dates_times,
        'User': users,
        'Message': messages_list
    })

    # Convert 'Date_Time' to datetime
    df['Date_Time'] = pd.to_datetime(df['Date_Time'], format='%m/%d/%y, %I:%M %p')
    df['year'] = df['Date_Time'].dt.year
    df['month_num'] = df['Date_Time'].dt.month
    df['month'] = df['Date_Time'].dt.month_name()
    df['day_name'] = df['Date_Time'].dt.day_name()
    df['day'] = df['Date_Time'].dt.day
    df['hour'] = df['Date_Time'].dt.hour
    df['minute'] = df['Date_Time'].dt.minute

    period = []
    # agar kahi par hour 10 hai toh 10-11 ho jayega
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str("00"))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df

