import spacy
from nltk import sent_tokenize
import pandas as pd
from ast import literal_eval
import os
import sys
import pathlib
folder_path = pathlib.Path().parent.resolve()
sys.path.append(os.path.join(folder_path,'../'))
from utils import load_subtitles_dataset


class NamedEntityOrganizer():
    def __init__(self):
        self.nlp_model = self.load_model()
        
    def load_model(self):
        nlp = spacy.load('en_core_web_trf')
        return nlp

    def generate_ner_inference(self, script):
        sentences = sent_tokenize(script)
        output = []
        for sentence in sentences:
            # script = ".".join(sentence)
            ners = set()
            doc = self.nlp_model(sentence)
            for entity in doc.ents:
                if entity.label_ == "PERSON":

                    first_name = entity.text.split(" ")[0]
                    first_name = first_name.strip()
                    ners.add(first_name)
            output.append(ners)
        return output
    
    def get_ners(self, dataset_path, save_path=None):
        # if save path exists and not None -> read csv from save_path and get ners column with literal_eval function :"D
        if save_path is not None and os.path.exists(save_path):
            df = pd.read_csv(save_path)
            df['ners'] = df['ners'].apply(lambda x: literal_eval(x) if isinstance(x,str) else x)
            return df
            
        df = load_subtitles_dataset(dataset_path)
        df = df.head(10)
        df['ners'] = df['script'].apply(self.generate_ner_inference)
        
        if save_path is not None:
            df.to_csv(save_path,index=False)

        return df

