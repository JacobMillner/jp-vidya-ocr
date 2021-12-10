import PySimpleGUI as sg
import numpy as np
from PIL import ImageGrab
import easyocr
import pyperclip
import webbrowser
import urllib

# setup easyocr with japanese/english
reader = easyocr.Reader(['ja', 'en'])

# web url for ichi.moe
url = 'https://ichi.moe/cl/qr/?q='

sg.SetOptions(margins=(0, 0), element_padding=(0, 0))

layout = [[sg.Graph(canvas_size=(600, 150), graph_bottom_left=(-600, -150),
                    graph_top_right=(600, 150), background_color='green', key='graph')],
          [sg.Text('Target Text')],
          [sg.Multiline(size=(100, 5), key='textbox')],
          [sg.Button('Grab'), sg.Button('Copy'), sg.Button('+'), sg.Button('-'), sg.Button('web'), sg.Button('Exit')]]

window = sg.Window('Japanese Text OCR', layout, background_color='green', transparent_color='green',
                   no_titlebar=True, alpha_channel=.12, grab_anywhere=True, resizable=True).Finalize()


# GUI event loop
while True:
    event, values = window.Read(100)
    if event in (sg.WIN_CLOSED, 'Exit'):
        break

    if event == 'Grab':
        # take a screenshot
        win_size = window.Size
        win_loc = window.CurrentLocation()
        # bbox is a tuple (left_x, top_y, right_x, bottom_y)
        # -120 because of textbox
        box_size = (win_loc[0], win_loc[1],
                    win_loc[0] + win_size[0], win_loc[1] + win_size[1] - 120)
        img1 = ImageGrab.grab(
            bbox=box_size)
        np_im = np.array(img1)

        # time to read the text from the screenshot
        result = reader.readtext(np_im)
        # loop over results and build your text
        text = ""
        for val in result:
            text = text + val[1] + " "
        window['textbox'].update(text)

    if event == 'Copy':
        text = window['textbox'].get()
        pyperclip.copy(text)

    if event == 'web':
        text = window['textbox'].get()
        text = urllib.parse.quote(text)
        webbrowser.open(url + text)

    if event == '-':
        if window.alpha_channel >= 0.12:
            window.alpha_channel = window.alpha_channel - 0.05

    if event == '+':
        if window.alpha_channel <= 1:
            window.alpha_channel = window.alpha_channel + 0.05

# gui event loop is over, cleanup time
window.close()
