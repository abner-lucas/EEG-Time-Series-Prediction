import pandas as pd
from tqdm import tqdm

def load_trials(filenames_list):
    EEG_trials = pd.DataFrame({}) # criar um df vazio que conterá dados de cada arquivo
    for file_name in tqdm(filenames_list):
        if file_name.endswith('trials.csv'): # ler somente arquivos que terminam com 'trials.csv'
            # lendo do arquivo para df mantendo subject_id como string
            temp_df = pd.read_csv('D:/Documentos/Mestrado/2021/UFPA Ciência Computação/EEG/outputs_eeg/' + file_name, dtype={'subject_id': str})
            #temp_df = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/PPGCC/EEG/outputs_eeg/' + file_name, dtype={'subject_id': str})
            EEG_trials = pd.concat([EEG_trials, temp_df], ignore_index=True) # adicionando os dados do arquivo ao df principal
    return EEG_trials

def load_evoked(filenames_list):
    EEG_evoked = pd.DataFrame({}) # criar um df vazio que conterá dados de cada arquivo
    for file_name in tqdm(filenames_list):
        if file_name.endswith('evoked.csv'): # ler somente arquivos que terminam com 'trials.csv'
            # lendo do arquivo para df mantendo subject_id como string
            temp_df = pd.read_csv('D:/Documentos/Mestrado/2021/UFPA Ciência Computação/EEG/outputs_eeg/' + file_name, dtype={'subject_id': str})
            #temp_df = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/PPGCC/EEG/outputs_eeg/' + file_name, dtype={'subject_id': str})
            EEG_evoked = pd.concat([EEG_evoked, temp_df], ignore_index=True) # adicionando os dados do arquivo ao df principal
    return EEG_evoked

def load_ip(filenames_list):
    EEG_ip = pd.DataFrame({}) 
    for file_name in tqdm(filenames_list):
        if file_name.endswith('ip.csv'):
            temp_df = pd.read_csv('D:/Documentos/Mestrado/2021/UFPA Ciência Computação/EEG/outputs_eeg/' + file_name, dtype={'subject_id': str})
            #temp_df = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/PPGCC/EEG/outputs_eeg/' + file_name, dtype={'subject_id': str})
            EEG_ip = pd.concat([EEG_ip, temp_df], ignore_index=True)
    return EEG_ip