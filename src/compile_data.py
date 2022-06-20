import pandas as pd

def sample_data(subject_id, stimulus, EEG_data):
    sensor_positions = EEG_data.columns[5:]
    channels = [i for i in range(len(sensor_positions))]
    
    subject_df = EEG_data[(EEG_data['subject_id'] == subject_id) & (EEG_data['condition'] == stimulus)]
    
    #reorganizar em colunas sensor_position e sensor_value
    subject_df_info = subject_df.drop(subject_df.columns[5:], axis=1)
    subject_df_sensor_values = subject_df.drop(subject_df.columns[:5], axis=1)

    sensorT_df = pd.DataFrame(columns=['subject_id','group','time','condition','trial',
                                        'channel','sensor_position', 'sensor_value'])

    for i in range(len(subject_df_sensor_values)):
        temp_df = pd.DataFrame({'channel': channels,
                                'sensor_position': subject_df_sensor_values.iloc[i].T.index.tolist(),
                                'sensor_value': subject_df_sensor_values.iloc[i].T.values})
        
        for col in subject_df_info.columns:
            temp_df[col] = subject_df_info.iloc[i][col]

        temp_df = pd.concat([temp_df[['subject_id','group','time','condition','trial']],
                             temp_df[['channel','sensor_position','sensor_value']]], axis=1)

        sensorT_df = pd.concat([sensorT_df, temp_df], ignore_index=True)

    groups_idxs = sensorT_df.groupby(['channel','trial'])['time'].apply(lambda x: x.index.tolist())
    idxs = []
    for index, value in groups_idxs.items():
        idxs += value
    sensorT_df = sensorT_df.iloc[idxs].reset_index(drop=True)

    channel = sensorT_df['channel'].iloc[0]
    cont_sample_num = 0
    sample_num = []

    for i in range(len(sensorT_df)):
        if sensorT_df['channel'].iloc[i] == channel:
            cont_sample_num += 1
        else:
            sample_num += [i for i in range(cont_sample_num)]
            cont_sample_num = 1
            channel = sensorT_df['channel'].iloc[i]
        if i == len(sensorT_df)-1:
            sample_num += [i for i in range(cont_sample_num)]

    sensorT_df.insert(2, 'sample_num', sample_num)

    sensorT_df['time'] = sensorT_df['time'].astype(float)
    sensorT_df['trial'] = sensorT_df['trial'].astype(int)
    sensorT_df['channel'] = sensorT_df['channel'].astype(int)
    sensorT_df['sensor_value'] = sensorT_df['sensor_value'].astype(float)

    return sensorT_df

def subject_trial_data(subject_id, stimulu, EEG_trials):
    sub_stimulus = []
    for sub_id in EEG_trials['subject_id'].unique():
        if sub_id == subject_id:
            sub_stimulus = EEG_trials[EEG_trials['subject_id']==subject_id]['condition'].unique()
            for sub_stimulu in sub_stimulus:
                if sub_stimulu == stimulu:
                    S_sample_df = sample_data(subject_id, stimulu, EEG_trials)
                    df_data = S_sample_df[['sensor_position', 'time', 'sensor_value']]
                    raw_data = pd.pivot_table(df_data, values='sensor_value', index='time', columns='sensor_position', aggfunc='mean')
    
    return S_sample_df, raw_data

def evoked_data(subject_id, EEG_data):
    sensor_positions = EEG_data.columns[3:]
    channels = [i for i in range(len(sensor_positions))]

    subject_df = EEG_data[EEG_data['subject_id'] == subject_id]
    
    #reorganizar em colunas sensor_position e sensor_value
    subject_df_info = subject_df.drop(subject_df.columns[3:], axis=1)
    subject_df_sensor_values = subject_df.drop(subject_df.columns[:3], axis=1)

    sensorT_df = pd.DataFrame(columns=['subject_id','group','time',
                                        'channel','sensor_position', 'sensor_value'])

    for i in range(len(subject_df_sensor_values)):
        temp_df = pd.DataFrame({'channel': channels,
                                'sensor_position': subject_df_sensor_values.iloc[i].T.index.tolist(),
                                'sensor_value': subject_df_sensor_values.iloc[i].T.values})
        
        for col in subject_df_info.columns:
            temp_df[col] = subject_df_info.iloc[i][col]

        temp_df = pd.concat([temp_df[['subject_id','group','time']],
                             temp_df[['channel','sensor_position','sensor_value']]], axis=1)

        sensorT_df = pd.concat([sensorT_df, temp_df], ignore_index=True)

    groups_idxs = sensorT_df.groupby('channel')['time'].apply(lambda x: x.index.tolist())
    idxs = []
    for index, value in groups_idxs.items():
        idxs += value
    sensorT_df = sensorT_df.iloc[idxs].reset_index(drop=True)

    channel = sensorT_df['channel'].iloc[0]
    cont_sample_num = 0
    sample_num = []
    for i in range(len(sensorT_df)):
        if sensorT_df['channel'].iloc[i] == channel:
            cont_sample_num += 1
        else:
            sample_num += [i for i in range(cont_sample_num)]
            cont_sample_num = 1
            channel = sensorT_df['channel'].iloc[i]
        if i == len(sensorT_df)-1:
            sample_num += [i for i in range(cont_sample_num)]

    sensorT_df.insert(2, 'sample_num', sample_num)

    sensorT_df['time'] = sensorT_df['time'].astype(float)
    sensorT_df['channel'] = sensorT_df['channel'].astype(int)
    sensorT_df['sensor_value'] = sensorT_df['sensor_value'].astype(float)

    df_data = sensorT_df[['sensor_position', 'time', 'sensor_value']]
    raw_data = pd.pivot_table(df_data, values='sensor_value', index='time', columns='sensor_position', aggfunc='mean')

    return sensorT_df, raw_data

def mean_evokeds(EEG_data):
    sensor_positions = EEG_data.columns[3:]
    channels = [i for i in range(len(sensor_positions))]
    group = EEG_data['group'].unique()[0]
    time = EEG_data['time'].unique()
    mean_subjects = EEG_data.groupby(axis=0, by='time').mean()

    sensorT_df = pd.DataFrame(columns=['group','time','channel','sensor_position', 'sensor_value'])

    for i in range(len(mean_subjects)):
        temp_df = pd.DataFrame({'channel': channels,
                                'sensor_position': mean_subjects.iloc[i].T.index.tolist(),
                                'sensor_value': mean_subjects.iloc[i].T.values})
        temp_df.insert(0, 'time', time[i])
        temp_df.insert(0, 'group', group)

        sensorT_df = pd.concat([sensorT_df, temp_df], ignore_index=True)

    groups_idxs = sensorT_df.groupby('channel')['time'].apply(lambda x: x.index.tolist())
    idxs = []
    for index, value in groups_idxs.items():
        idxs += value
    sensorT_df = sensorT_df.iloc[idxs].reset_index(drop=True)

    channel = sensorT_df['channel'].iloc[0]
    cont_sample_num = 0
    sample_num = []
    for i in range(len(sensorT_df)):
        if sensorT_df['channel'].iloc[i] == channel:
            cont_sample_num += 1
        else:
            sample_num += [i for i in range(cont_sample_num)]
            cont_sample_num = 1
            channel = sensorT_df['channel'].iloc[i]
        if i == len(sensorT_df)-1:
            sample_num += [i for i in range(cont_sample_num)]

    sensorT_df.insert(1, 'sample_num', sample_num)

    sensorT_df['time'] = sensorT_df['time'].astype(float)
    sensorT_df['channel'] = sensorT_df['channel'].astype(int)
    sensorT_df['sensor_value'] = sensorT_df['sensor_value'].astype(float)

    df_data = sensorT_df[['sensor_position', 'time', 'sensor_value']]
    raw_data = pd.pivot_table(df_data, values='sensor_value', index='time', columns='sensor_position', aggfunc='mean')

    return sensorT_df, raw_data

def mean_sensors(df, s_exclude):
    sample_df, data = mean_evokeds(df[~df['subject_id'].isin(s_exclude)])
    mean_sensors = data[data.columns[:]].mean(axis=1).reset_index(drop=True)
    return mean_sensors