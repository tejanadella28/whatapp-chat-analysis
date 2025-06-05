import re
import pandas as pd

def preprocess(data):
    # Step 1: Replace narrow no-break space (U+202F) with regular space
    data = data.replace('\u202f', ' ').replace(" ", " ")  # also catch invisible no-break

    # Step 2: Define regex pattern (capture datetime part)
    pattern = r'(\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2} ?[ap]m) - '

    # Step 3: Split while keeping the date entries
    messages = re.split(pattern, data)[1:]  # [date1, msg1, date2, msg2, ...]
    dates = messages[0::2]
    messages = messages[1::2]

    # Step 4: Sanity check
    if len(dates) != len(messages):
        print("❌ Length mismatch between dates and messages")
        return None

    # Step 5: Create DataFrame
    df = pd.DataFrame({'message_date': dates, 'user_message': messages})
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %I:%M %p')

    df.rename(columns={'message_date': 'date'}, inplace=True)

    # Step 6: Extract user/message
    users = []
    msgs = []
    for message in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            msgs.append(" ".join(entry[2:]))
        else:
            users.append("group_notification")
            msgs.append(entry[0])

    df['user'] = users
    df['message'] = msgs
    df.drop(columns=['user_message'], inplace=True)

    # Step 7: Add extra columns for timeline analysis
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    # Step 8: Create period column for hourly activity
    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append(f"{hour}-00")
        elif hour == 0:
            period.append("00-1")
        else:
            period.append(f"{hour}-{hour+1}")
    df['period'] = period

    return df
