from tkinter import *
import tkintermapview

def add_marker(pos: (float, float), text: str) -> None:
    map_widget.set_marker(pos[0], pos[1], text=text)


root = Tk()
root.geometry("1280x720")
root.title("TITLE ME!!!")

########################################
# Map
map_widget = tkintermapview.TkinterMapView(root)
map_widget.pack(fill=BOTH, expand=True) # Maximize
map_widget.set_tile_server("https://cartodb-basemaps-1.global.ssl.fastly.net/rastertiles/voyager/{z}/{x}/{y}{r}.png", max_zoom=19) # Map provider

# Default pos
map_widget.set_position(49.695638, 22.745782)
map_widget.set_zoom(13)

map_widget.pack()

########################################
# Checkbox list
# def print_selected():
#     selected_options = [options[i] for i in range(len(options)) if var_list[i].get() == 1]
#     print("Selected options:", selected_options)
# options = ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"]
# var_list = []
# for option in options:
#     var = IntVar()
#     checkbox = Checkbutton(root, text=option, variable=var)
#     checkbox.pack(anchor='ne')
#     var_list.append(var)

print_button = Button(root, text="Print Selected", command=print_selected)
print_button.pack(side=RIGHT)


########################################
# Test
add_marker((49.695300, 22.745213), "Fredropol")


if __name__ == '__main__':
    root.mainloop()

