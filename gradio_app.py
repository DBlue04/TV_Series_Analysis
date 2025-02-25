import gradio as gr
from theme_classifier import ThemeClassifier

def get_themes(theme_list_str, subtitles_path,save_path):
    theme_list = theme_list_str.split(',')
    theme_classifier = ThemeClassifier(theme_list)
    output_df = theme_classifier.get_themes(subtitles_path, save_path)

    #remove dialogue from the theme list
    theme_list = [theme for theme in theme_list if theme != 'dialogue']
    output_df = output_df[theme_list]
    
    output_df = output_df[theme_list].sum().reset_index()
    output_df.columns = ['theme','score']

    output_chart = gr.BarPlot(
        output_df,
        x='theme'
        y='score',
        title='Series Themes',
        tooltip=['Theme','Score'],
        vertical=False,
        width = 500,
        height=260
    )

    return output_chart
    

def main():
    with gr.Blocks() as iface:
        with gr.Row():
            with gr.Column():
                gr.HTML("<h1>Theme Classification (Zero Shot Classifiers)</h1>")
                with gr.Row():
                    with gr.Column():
                        plot = gr.BarPlot()
                    with gr.Column():
                        theme_list = gr.Textbox(label='Themes')
                        subtitles_path = gr.Textbox(label='Subtitle or Script Path')
                        save_path = gr.Textbox(label='Save path')
                        get_themes_button = gr.Button('Get Themes')
                        get_themes_button.click(get_themes,input=[theme_list,subtitles_path, save_path], outputs=[plot])



    iface.launch(share=True)
            

if __name__ == '__main__':
    main()