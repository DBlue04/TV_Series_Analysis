import pandas as pd
import networkx as nx
from pyvis.network import Network

class CharacterNetworkGenerator():
    def __init__(self):
        pass
    def generate_character_network(self, df):
        n = 10 # Limit find relationships within 10 sentences (actually it's is the last 10 entity :v)

        entity_relationship = []

        for episode in df['ners']:

            entities = []
            for sentence in episode:
                entities.append(list(sentence))
                entities = entities[-n:]
                flattened_entities = sum(entities, [])

                for entity1 in sentence:
                    for entity2 in flattened_entities:
                        if entity1 != entity2:
                            entity_relationship.append(sorted([entity1,entity2]))

        df = pd.DataFrame({"value": entity_relationship})
        df['source'] = df['value'].apply(lambda x : x[0])
        df['target'] = df['value'].apply(lambda x : x[1])
        df = df.groupby(['source', 'target']).count().reset_index()

        df = df.sort_values('value', ascending=False)

        return df
    
    def draw_network_graph(self, df):
        df = df.sort_values('value', ascending=False)
        df = df.head(200)

        G = nx.from_pandas_edgelist(
            df,
            source='source',
            target='target',
            edge_attr='value',
            create_using=nx.Graph()
        )

        node_degree = dict(G.degree)
        nx.set_node_attributes(G,node_degree,'size')
        net = Network(notebook=True, width='1000px', height='700px', bgcolor="#222222", font_color="white", cdn_resources="remote")
        net.from_nx(G) 
        
        html = net.generate_html()
        html = html.replace("'","\"")
        output_html = f"""<iframe style="width: 100%; height: 600px;margin:0 auto" name="result" allow="midi; geolocation; microphone; camera;
                        display-capture; encrypted-media;" sandbox="allow-modals allow-forms
                        allow-scripts allow-same-origin allow-popups
                        allow-top-navigation-by-user-activation allow-downloads" allowfullscreen=""
                        allowpaymentrequest="" frameborder="0" srcdoc='{html}'></iframe>"""
        
        return output_html




