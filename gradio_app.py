import gradio as gr

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
                        subtitle_path = gr.Textbox(label='Subtitle or Script Path')
                        save_path = gr.Textbox(label='Save path')
                        get_themes_button = gr.Button('Get Themes')



    iface.launch(share=True)
            

if __name__ == '__main__':
    main()