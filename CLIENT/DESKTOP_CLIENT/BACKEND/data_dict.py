class data() :
    def __init__(self) :
        self.text_strs = [
            "                                       ",
            "                                       ",
            "                                       ",
            "                                       ",
            "                                       ",
            "                                       ",
            "                  __                   ",
            "             w  c(..)o   (             ",
            "              \__(-)    __)            ",
            "                  /\   (               ",
            "                 /(_)___)              ",
            "                 w /|                  ",
            "                  | \\                 ",
            "                 m  m                  ",
            "                                       ",
            "               WELCOME!!               ",
            "                                       ",
            "                                       ",
            "                                       ",
            "                                       "]

        self.text_string_offset = 0
        self.length_of_string_list = len(self.text_strs)

    def set_offset_for_new_message(self, num_of_lines) :
        if (self.text_string_offset == (self.length_of_string_list - 20 - num_of_lines)) :
            self.text_string_offset += num_of_lines
        else : pass

    def set_offset_for_mouse_movement(self, units) :
        if units  < 0 :
            if self.text_string_offset == 0 :
                pass
            else :
                for _ in range(units, 0) :
                    try :
                        if (self.text_string_offset + _) >= 0 :
                            self.text_string_offset += _
                            break
                        else :
                            pass
                    except :
                        pass
        elif units > 0 :
            if (self.text_string_offset == (self.length_of_string_list - 20)) :
                pass
            else :
                for _ in range(units, 0, -1) :
                    try :
                        if (self.text_string_offset + _) <= (self.length_of_string_list - 20) :
                            self.text_string_offset += _
                            break
                        else :
                            pass
                    except :
                        pass

    def get_offset(self) :
        return self.text_string_offset

    def add_strings(self, message) :
        lines_added = 1
        lines_to_be_added = [""]
        temp_msg = message

        while len(temp_msg) >= 39 :
            lines_to_be_added.append(temp_msg[:39])
            #width = self.font_metrix(self.qfont(self.font, self.font_size, self.qfont.Bold)).width(temp_msg)
            #print(len(temp_msg[:39]))
            #print(width)
            temp_msg = temp_msg[39:]
            lines_added += 1
            
        if len(temp_msg) > 0 :
            lines_to_be_added.append(temp_msg)
            #width = self.font_metrix(self.qfont(self.font, self.font_size, self.qfont.Bold)).width(temp_msg)
            #print(len(temp_msg))
            #print(width)
            lines_added += 1
        
        self.text_strs.extend(lines_to_be_added)

        self.length_of_string_list += lines_added

        self.set_offset_for_new_message(lines_added)
            

    def get_string_for_index(self, index) :
        return self.text_strs[self.text_string_offset+index]

    def add_main_ui_reference(self, main_ui) :
        self.main_ui = main_ui

    def get_reference_for_calculation_of_width_of_string(self) :
        self.qfont = self.main_ui.qfont_reference()
        self.font_metrix = self.main_ui.qfontmetrix_reference()

    def get_label_data(self) :
        self.font_size, self.font = self.main_ui.label_data_fetch()

############################################################################################################################################################################################################
data_ = data()