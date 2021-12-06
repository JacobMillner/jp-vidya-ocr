import PySimpleGUI as sg

sg.SetOptions(margins=(0, 0), element_padding=(0, 0))

layout = [[sg.Graph(canvas_size=(600, 150), graph_bottom_left=(-600, -150),
                    graph_top_right=(600, 150), background_color='green', key='graph')],
          [sg.Text('Target Text')],
          [sg.Multiline(size=(100, 5), key='textbox')],
          [sg.Button('Grab'), sg.Button('Copy'), sg.Button('Exit')]]

window = sg.Window('Japanese Text OCR', layout, background_color='green', transparent_color='green',
                   no_titlebar=True, alpha_channel=.12, grab_anywhere=True, resizable=True).Finalize()


# GUI event loop
while True:
    event, values = window.Read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break

    if event == 'Grab':
        window['textbox'].update('じゃがいも')

# gui event loop is over, cleanup time
window.close()
