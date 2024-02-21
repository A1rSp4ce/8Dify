import threading
import math
import time
import os
import customtkinter
from customtkinter import CTkButton
from customtkinter import CTkFont as font
from PIL import Image
from PIL import ImageTk
import webcolors
from tkinter.filedialog import askopenfilename
import audiogeneration

freq_8D = 0.075
amount_8D=100
reverb_room_size=0.1
reverb_damping=0.5
reverb_wet_level=0.33
reverb_dry_level=0.4
reverb_width= 1.0

def hex_to_rgb(hex):
  
  return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

def lerp(a: float, b: float, t: float) -> float:
    return (1 - t) * a + t * b

def choose_audio_file():
    try:
        chosen_filename = askopenfilename(initialdir="/", title="Select Audio File",
                                            filetypes=(("Audio Files", ".wav .ogg .mp3"),   ("All Files", "*.*")))
        global audiofile
        audiofile = chosen_filename
        global trimmed_name_audio_file
        trimmed_name_audio_file = os.path.basename(audiofile)
        print(trimmed_name_audio_file)
        if audiofile:
            file_info_button_label.configure(text=f'Import Success!: {audiofile}')
    except Exception as error:
        file_info_button_label.configure(text=error)


app = customtkinter.CTk()
app.title('8Dify')
app.geometry("1400x900")
app_icon = Image.open('8DifyAppImage.PNG')

app_bg_color = '#020202'
canvas= customtkinter.CTkCanvas(app ,bg=app_bg_color, width=2000, height=1500, highlightthickness=0)
canvas.pack()

font_1 = font(family="Tw Cen MT Condensed",size=30, weight='bold') 
font_2 = font(family="Arial",size=36, weight='normal') 
font_3 = font(family="ArialCE",size=30, weight='bold') 
font_4 = font(family="Arial",size=20, weight='bold')
font_5 = font(family="Arial",size=16, weight='bold')
font_6 = font(family="Tw Cen MT Condensed",size=30, weight='bold') 
values_text = font(family="Arial",size=18, weight='bold')


app_icon_image = customtkinter.CTkImage(light_image=app_icon, size=(230,230))

app_icon_image_button = customtkinter.CTkButton(app, image=app_icon_image, text='', 
                                                        fg_color='transparent', 
                                                        hover=False,
                                                        border_width=4,
                                                        border_spacing= 0,
                                                        border_color= '#ae35e6',
                                                        bg_color=app_bg_color,
                                                        corner_radius=10)
app_icon_image_button.place(relx=0.5, rely=0.33-0.03, anchor='s')


upload_button = CTkButton(app, text='Choose File to 8DIFY', 
                          corner_radius=10, 
                          fg_color='#194651', 
                          border_color='#52DFFF', 
                          hover_color= '#384DBD',
                          bg_color=app_bg_color,
                          border_width=3, height=40, width=350, 
                          command=choose_audio_file,
                          font=font_1)

upload_button.place(relx=0.5, rely=0.495-0.05, anchor='center')

def alternating_color_widgets():
    iTime = 0
    initial_color_rgb_ub = hex_to_rgb(str(upload_button.cget('fg_color')).strip('#'))
    initial_color_rgb_img = hex_to_rgb(str(app_icon_image_button.cget('border_color')).strip('#'))
    
    
    while True:
        time.sleep(0.001)
        iTime += 0.05
        sw = abs(math.sin(iTime))
        r_colub, g_colub, b_colub = initial_color_rgb_ub
        r_colimg, g_colimg, b_colimg= initial_color_rgb_img
        upload_button.configure(fg_color=webcolors.rgb_to_hex((round(r_colub), round(g_colub-lerp(0,50,-sw)), round(b_colub+lerp(30,180,sw)))))
        app_icon_image_button.configure(border_color=webcolors.rgb_to_hex((round(r_colimg-lerp(0,200,-sw)), round(g_colimg-lerp(0,200,-sw)), round(b_colimg+lerp(0,180,sw)))))
        
        

alternating_color_widgets_thread = threading.Thread(target=alternating_color_widgets, args=())
alternating_color_widgets_thread.start()


file_info_button_label = customtkinter.CTkButton(app, width=700, height=50, hover=False,
                                                 fg_color="#1D1D1D",
                                                 border_color= "#989898",
                                                 border_width=3,
                                                 corner_radius=15,
                                                 bg_color=app_bg_color,
                                                 text= "File updates appear here",
                                                 font=font_2)

file_info_button_label.place(relx=0.5, rely=0.385-0.03,anchor='center')

#8D Settings Panel
settings_8d_pannel = customtkinter.CTkFrame(master=app, width=570, height=300, 
                                            fg_color='#090410', border_color='#bc4cff', 
                                            border_width=4, bg_color=app_bg_color,
                                            corner_radius=17)
settings_8d_pannel.place(relx=0.24, rely=0.52, anchor='n')

panel_settings8D_button_label = customtkinter.CTkButton(settings_8d_pannel, width=550, height=48, hover=False,
                                                 fg_color="#0B2045",
                                                 border_color= "#95BCFF",
                                                 bg_color=app_bg_color,
                                                 border_width=3,
                                                 corner_radius=13,
                                                 text= "8D Panning Settings", 
                                                 text_color="#FFFFFF",
                                                 font=font_3)

panel_settings8D_button_label.place(relx=0.5, rely=0.12,anchor='center')

def amount_8D_slider_event(value):
    amount_8D_value.configure(text=f'{str(round(value))}%')
    global amount_8D
    amount_8D = int(value)
  
def amount_frequency_slider_event(value):
    frequency_8D_value.configure(text=str(round(value, 3)))
    global freq_8D
    freq_8D = float(value)


amount_8D_slider = customtkinter.CTkSlider(master=settings_8d_pannel, width=276, height=21, from_= 0, to=100, button_color='#3D474E', 
                                           progress_color='#614894', fg_color='#B4CFE3', variable=customtkinter.IntVar(app,100), command=amount_8D_slider_event, bg_color='transparent')
amount_8D_slider.place(relx=0.64, rely=0.305,anchor='n')
amount_8D_label  = customtkinter.CTkLabel(master=settings_8d_pannel, width=70, height=20, text="8D Amount (0%-100%)", font=font_4)
amount_8D_label.place(relx=0.21, rely=0.293,anchor='n')
amount_8D_value = customtkinter.CTkLabel(master=settings_8d_pannel, width=20, height=20, text="100%", font=values_text)
amount_8D_value.place(relx=0.93, rely=0.2997,anchor='n')

frequency_8D_slider = customtkinter.CTkSlider(master=settings_8d_pannel, width=276, height=21, from_= 0, to=1, button_color='#3D474E',
                                               progress_color='#614894', fg_color='#B4CFE3', variable=customtkinter.DoubleVar(app,0.075), command=amount_frequency_slider_event, bg_color='transparent')
frequency_8D_slider.place(relx=0.64, rely=0.4575,anchor='n')
frequency_8D_label  = customtkinter.CTkLabel(master=settings_8d_pannel, width=10, height=10, text="Panning Frequency (0.0-1.0)", font=font_5)
frequency_8D_label.place(relx=0.21, rely=0.456,anchor='n')
frequency_8D_value = customtkinter.CTkLabel(master=settings_8d_pannel, width=20, height=20, text="0.075", font=values_text)
frequency_8D_value.place(relx=0.93, rely=0.44955,anchor='n')



#Reverb Settings Panel
settings_reverb_panel = customtkinter.CTkFrame(master=app, width=570, height=300, 
                                            fg_color='#090410', border_color='#bc4cff', 
                                            border_width=4, bg_color=app_bg_color, corner_radius=17)
settings_reverb_panel.place(relx=0.76, rely=0.52, anchor='n')


panel_settings_reverb_button_label = customtkinter.CTkButton(settings_reverb_panel, width=550, height=48, hover=False,
                                                 fg_color="#0B2045",
                                                 border_color= "#95BCFF",
                                                 bg_color=app_bg_color,
                                                 border_width=3,
                                                 corner_radius=13,
                                                 text= "Reverb Settings", 
                                                 text_color="#FFFFFF",
                                                 font=font_3)

panel_settings_reverb_button_label.place(relx=0.5, rely=0.12,anchor='center')

def room_size_slider_event(value):
    room_size_value.configure(text=str(round(value, 3)))
    global reverb_room_size
    reverb_room_size = float(value)
  
def damping_slider_event(value):
    damping_value.configure(text=str(round(value, 3)))
    global reverb_damping
    reverb_damping = float(value)

def wet_level_slider_event(value):
    wet_level_value.configure(text=str(round(value, 3)))
    global reverb_wet_level
    reverb_wet_level = float(value)

def dry_level_slider_event(value):
    dry_level_value.configure(text=str(round(value, 3)))
    global reverb_dry_level
    reverb_dry_level =  float(value)

def width_slider_event(value):
    width_value.configure(text=str(round(value, 3)))
    global reverb_width
    reverb_width = float(value)

room_size_slider = customtkinter.CTkSlider(master=settings_reverb_panel, width=276, height=21, from_= 0, to=1, button_color='#3D474E', 
                                           progress_color='#614894', fg_color='#B4CFE3', variable=customtkinter.DoubleVar(app,0.1), bg_color='transparent', command=room_size_slider_event)
room_size_slider.place(relx=0.6, rely=0.305,anchor='n')
room_size_label  = customtkinter.CTkLabel(master=settings_reverb_panel, width=70, height=20, text="Room Scale", font=font_4)
room_size_label.place(relx=0.21, rely=0.293,anchor='n')#
room_size_value = customtkinter.CTkLabel(master=settings_reverb_panel, width=20, height=20, text="0.1", font=values_text)
room_size_value.place(relx=0.93, rely=0.2997,anchor='n')

damping_slider = customtkinter.CTkSlider(master=settings_reverb_panel, width=276, height=21, from_= 0, to=1, button_color='#3D474E',
                                               progress_color='#614894', fg_color='#B4CFE3', variable=customtkinter.DoubleVar(app,0.5), bg_color='transparent', command=damping_slider_event)
damping_slider.place(relx=0.6, rely=0.4575,anchor='n')
damping_label  = customtkinter.CTkLabel(master=settings_reverb_panel, width=10, height=10, text="Damping", font=font_4)
damping_label.place(relx=0.21, rely=0.456,anchor='n')
damping_value = customtkinter.CTkLabel(master=settings_reverb_panel, width=20, height=20, text="0.5", font=values_text)
damping_value.place(relx=0.93, rely=0.44955,anchor='n')\

wet_level_slider = customtkinter.CTkSlider(master=settings_reverb_panel, width=276, height=21, from_= 0, to=1, button_color='#3D474E',
                                               progress_color='#614894', fg_color='#B4CFE3', variable=customtkinter.DoubleVar(app,0.33), bg_color='transparent', command=wet_level_slider_event)
wet_level_slider.place(relx=0.6, rely=0.4575*1.35,anchor='n')
wet_level_label  = customtkinter.CTkLabel(master=settings_reverb_panel, width=10, height=10, text="Wet Level", font=font_4)
wet_level_label.place(relx=0.21, rely=0.456*1.35,anchor='n')
wet_level_value = customtkinter.CTkLabel(master=settings_reverb_panel, width=20, height=20, text="0.33", font=values_text)
wet_level_value.place(relx=0.93, rely=0.44955*1.35,anchor='n')

dry_level_slider = customtkinter.CTkSlider(master=settings_reverb_panel, width=276, height=21, from_= 0, to=1, button_color='#3D474E',
                                               progress_color='#614894', fg_color='#B4CFE3', variable=customtkinter.DoubleVar(app,0.4), bg_color='transparent',command=dry_level_slider_event)
dry_level_slider.place(relx=0.6, rely=(0.4575*1.35)*1.23,anchor='n')
dry_level_label  = customtkinter.CTkLabel(master=settings_reverb_panel, width=10, height=10, text="Dry Level", font=font_4)
dry_level_label.place(relx=0.21, rely=(0.456*1.35)*1.23,anchor='n')
dry_level_value = customtkinter.CTkLabel(master=settings_reverb_panel, width=20, height=20, text="0.4", font=values_text)
dry_level_value.place(relx=0.93, rely=(0.44955*1.35)*1.23,anchor='n')

width_slider = customtkinter.CTkSlider(master=settings_reverb_panel, width=276, height=21, from_= 0, to=1, button_color='#3D474E',
                                               progress_color='#614894', fg_color='#B4CFE3', variable=customtkinter.DoubleVar(app,1), bg_color='transparent', command=width_slider_event)
width_slider.place(relx=0.6, rely=((0.4575*1.35)*1.25)*1.16,anchor='n')
width_label  = customtkinter.CTkLabel(master=settings_reverb_panel, width=10, height=10, text="Width", font=font_4)
width_label.place(relx=0.21, rely=((0.456*1.35)*1.25)*1.16,anchor='n')
width_value = customtkinter.CTkLabel(master=settings_reverb_panel, width=20, height=20, text="1", font=values_text)
width_value.place(relx=0.93, rely=((0.44955*1.35)*1.25)*1.16,anchor='n')

def gen_audio():
    audiogeneration.generate_8D_Audio(audiofile=audiofile, freq_8D=freq_8D, amount_8D=amount_8D, reverb_room_size=reverb_room_size, reverb_damping=reverb_damping, reverb_wet_level=reverb_wet_level, reverb_dry_level=reverb_dry_level, reverb_width=reverb_width, trimmed_file=trimmed_name_audio_file)
    file_info_button_label.configure(text=f'Generated 8Dified {trimmed_name_audio_file}!') 
    
generate_button = customtkinter.CTkButton(app, width=500, height=50,
                                                 fg_color="#239144",
                                                 border_color= "#34eb6b",
                                                 hover_color='#7ac290',
                                                 border_width=3,
                                                 corner_radius=10,
                                                 bg_color=app_bg_color,
                                                 text= "Generate Audio!",
                                                 font=font_6, command=lambda: gen_audio())



generate_button.place(relx=0.5, rely=0.93,anchor='center')
#Window Icon
iconpath = ImageTk.PhotoImage(file='8DifyAppLogo.jpg', master=app)
app.wm_iconbitmap()
app.iconphoto(True, iconpath)
app.mainloop()

