from tkinter import *
import tkintermapview


def main() -> None:
    root = Tk()
    root.geometry("1280x720")

    map_widget = tkintermapview.TkinterMapView(root)
    map_widget.pack(fill=BOTH, expand=True)

    map_widget.set_position(49.695638, 22.745782)
    map_widget.set_zoom(13)

    tile_url = "https://cartodb-basemaps-1.global.ssl.fastly.net/rastertiles/voyager/{z}/{x}/{y}{r}.png"
    map_widget.set_tile_server(tile_url, max_zoom=19)

    map_widget.pack()

    def add_marker(pos: (float, float), text: str) -> None:
        map_widget.set_marker(pos[0], pos[1], text=text)

    add_marker((49.695300, 22.745213), "Fredropol")

    root.mainloop()



if __name__ == '__main__':
    main()

