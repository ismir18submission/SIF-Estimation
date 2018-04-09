import subprocess


def extract_ops_features(file_name, audio_path, ops_config_path, output_path):
    if file_name != '':
        executable = 'SMILExtract_Release.exe'
        op_s_command = [executable, '-C',
                        ops_config_path, '-I',
                        audio_path + '/' + file_name + '.wav', '-O', output_path + file_name + '.csv']
        subprocess.Popen(op_s_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
