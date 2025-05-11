from tkinter import Tk
from ui.ui import UI


def main():
    '''
    Main function to start the workout tracking application.
    It initializes the main window and starts the UI.
    '''
    window = Tk()
    window.title("Workout Tracking app")
    window.geometry("800x600")

    ui_view = UI(window)
    ui_view.start()

    window.mainloop()


if __name__ == "__main__":
    main()
