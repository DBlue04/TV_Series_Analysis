import torch
from transformers import pipeline
from nltk import sent_tokenize
import pandas as pd
import numpy as np

class ThemeClassifier():
    def __init__(self, theme_list):
        self.model_name = 'facebook/bart-large-mnli'
        self.device = 0 if torch.cuda.is_available() else 'cpu'
        self.theme_list = theme_list
        self.theme_classifier = self.load_model(self.device)

    def load_model(self, device):
        theme_classifier = pipeline(
            'zero-shot-classification',
            model = self.model_name,
            device=device
        )
        return theme_classifier
    
    def get_themes_inference(self, script):
        script_sentences = sent_tokenize(script)

        #Batch sentence
        sentence_batch_size = 20
        script_batches = []
        for index in range(0, len(script_sentences), sentence_batch_size):
            sent = ' '.join(script_sentences[index:index + sentence_batch_size])
            script_batches.append(sent)

        #Run Model
        theme_output = self.theme_classifier(
            script_batches[:2],
            self.theme_list,
            multi_label=True
        )

        # Wrangle output
        themes = {}
        for output in theme_output:
            for label, score in zip(output['labels'],output['scores']):
                if label not in themes:
                    themes[label] = []
                themes[label].append(score)

        themes = {key: np.mean(np.array(value)) for key, value in themes.items()}
        return themes
    
    def get_theme(self, dataset_path):
        
        #load dataset

        #run inference