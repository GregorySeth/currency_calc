from tkinter import Tk
import calc_back

main_window = Tk()
main_window.title("Kalkulator walut")
main_window.geometry("300x500")
main_window.resizable(False, False)

data = calc_back.NBP_data()
wind = calc_back.User_ui(main_window, data.dict)

main_window.mainloop()
