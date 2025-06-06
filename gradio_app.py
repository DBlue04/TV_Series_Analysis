import gradio as gr
from theme_classifier import ThemeClassifier
from character_network import NamedEntityOrganizer, CharacterNetworkGenerator



def get_themes(theme_list_str,subtitles_path,save_path):
    theme_list = theme_list_str.split(',')
    theme_classifier = ThemeClassifier(theme_list)
    output_df = theme_classifier.get_themes(subtitles_path,save_path)

    # Remove dialogue from the theme list
    theme_list = [theme for theme in theme_list if theme != 'dialogue']
    output_df = output_df[theme_list]

    output_df = output_df[theme_list].sum().reset_index()
    output_df.columns = ['Theme','Score']

    output_chart = gr.BarPlot(
        output_df,
        x="Theme",
        y="Score",
        title="Series Themes",
        tooltip=["Theme","Score"],
        vertical=False,
        width=500,
        height=260
    )

    return output_chart

def get_network_graph(subtitles_path, ner_path):
    ner = NamedEntityOrganizer()
    df = ner.get_ners(subtitles_path, ner_path)

    character_network_generator = CharacterNetworkGenerator()
    relationship_df = character_network_generator.generate_character_network(df)

    output = character_network_generator.draw_network_graph(relationship_df)

    return output



def main():
    with gr.Blocks() as iface:
        # Theme Classification Section
        with gr.Row():
            with gr.Column():
                gr.HTML("<h1>Theme Classification (Zero Shot Claasifiers)</h1>")
                with gr.Row():
                    with gr.Column():
                        plot = gr.BarPlot()
                    with gr.Column():
                        theme_list = gr.Textbox(label="Themes")
                        subtitles_path = gr.Textbox(label="Subtitles or script Path")
                        save_path = gr.Textbox(label="Save Path")
                        get_themes_button =gr.Button("Get Themes")
                        get_themes_button.click(get_themes, inputs=[theme_list,subtitles_path,save_path], outputs=[plot])
                        # get_themes_button.click(get_themes, ['friendship,hope, sacrifice,battle,self development,betrayal,love,dialogue',
                        #                                             'Users/kelvinnguyen/Projects/TV_Series_Analysis/data/Subtitles',
                        #                                             '/Users/kelvinnguyen/Projects/TV_Series_Analysis/stubs/theme_classifier_output.csv'], outputs=[plot])

        #Character Network sectrion
        # /Users/kelvinnguyen/Projects/TV_Series_Analysis/data/Subtitles
        # TV_Series_Analysis/stubs/ner_output.csv
        with gr.Row():
            with gr.Column():
                gr.HTML("<h1>Character Network (NERs and Graphs)</h1>")
                with gr.Row():
                    with gr.Column():
                        network_html = gr.HTML()
                    with gr.Column():
                        subtitles_path = gr.Textbox(label="Subtitles or Script Path")
                        ner_path = gr.Textbox(label="NERs Save Path")
                        get_network_graph_button = gr.Button("Get Character Network")
                        # get_themes_button =gr.Button("Get Themes")
                        get_network_graph_button.click(get_network_graph, inputs=[subtitles_path,ner_path], outputs=[network_html])



    iface.launch(share=True)
            

if __name__ == '__main__':
    main()

# friendship,hope, sacrifice,battle,self development,betrayal,love,dialogue
#/Users/kelvinnguyen/Projects/TV_Series_Analysis/data/Subtitles
# /Users/kelvinnguyen/Projects/TV_Series_Analysis/stubs/theme_classifier_output.csv