import tkinter


class GeneticAlgorithmInterface(tkinter.Frame):
    def __init__(self, main):
        super().__init__(main)
        self.__main_window = main
        self.configure_main_window()

    def configure_main_window(self):
        self.__main_window.geometry('600x400')
        self.__main_window.resizable(False, False)
        self.__main_window.title("Genetic Algorithm")


if __name__ == "__main__":

    root = tkinter.Tk()
    GeneticAlgorithmInterface(root)
    root.mainloop()
