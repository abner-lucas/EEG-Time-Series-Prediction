#raise SystemExit

format_log = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
mne.set_log_file('outputs_eeg/subject' + subject_id + '_log.log', output_format=format_log, overwrite=True)
with mne.use_log_level(True):
    logger.info('# Pre-processing EEG data from subject ' + subject_id)