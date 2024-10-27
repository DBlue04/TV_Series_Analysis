from glob import glob
import pandas as pd


def load_subtitles_data(dataset_path):
    subtitle_paths = glob(dataset_path+'/*.ass')

    scripts = []
    episode_number = []

    for path in subtitle_paths:

        with open(path, 'r') as file:
            lines = file.readlines()[27:]
            lines = [ ','.join(line.split(',')[9:]) for line in lines]
        lines = [line.replace('\\N', ' ') for line in lines]
        script = ' '.join(lines)

        episode = int(path.split('-')[-1].split('.')[0].strip())

        scripts.append(script)
        episode_number.append(episode)

    return pd.DataFrame.from_dict({'episode':episode_number,'script':scripts})
     