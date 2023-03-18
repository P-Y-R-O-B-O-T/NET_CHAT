class color_scheme() : #creating class to store the color scheme of the ui elements all colors of the ui will be fetched and applied  
    def __init__(self) :
        self.colors = { "close_button" : "background-color : #030d22 ",
                        "close_button_text" : "color : #ff184c ",
                        "main_windows" : "background-color : #030d22 ",

                        "splash_screen":{"background_color":"background-color : #030d22 ",
                                         "heading":"color : #ff184c ",
                                         "progress_bar":"background-color : #90ff21 ",
                                         "progress_bar_side_rest":"border : 3px solid #00d0ff ; color : #00d0ff ; background-color : ",
                                         "status_reporter":"color : #e9ff45 ",
                                         "border":"border : 1px solid #ff4d21 "},
                        


                        "heading":"color : #ff184c ; background-color : #1c1347 ",
                        "close_button_text":"color : #ff184c ; background-color : #1c1347 ",
                        "text_label":"color : #00d0ff ",
                        "send_button":"color : #ff184c ; background-color : #1c1347 ",
                        "input_prompt":"border : 3px solid #6421ff ; color : #90ff21 ; background-color : "
                                        }

color = color_scheme()
