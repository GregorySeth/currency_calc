from bs4 import BeautifulSoup
import requests
import html5lib
import lxml
from tkinter import *

class NBP_data:
    def __init__(self):
        request = requests.get("https://www.nbp.pl/home.aspx?f=/kursy/kursyc.html")
        content = request.content
        soup = BeautifulSoup(content, "html5lib")

        base_url = "https://www.nbp.pl"
        xml_link = base_url + soup.find("p", {"class":"file print_hidden"}).find("a", href=True)['href']


        request_xml = requests.get(xml_link)
        content_xml = request_xml.content
        soup_xml = BeautifulSoup(content_xml, "lxml")

        self.dict = {}

        for el, el2, el3, el4 in zip(soup_xml.select("nazwa_waluty"), soup_xml.select("kod_waluty"), soup_xml.select("kurs_kupna"), soup_xml.select("kurs_sprzedazy")):
            self.dict[el2.text] = [el.text, el3.text, el4.text]

class User_ui():
    def __init__(self, window, data):
        self.data = data # Data from website with current currencies values
        # Info frame
        top_frame = Frame(window, width=300, height=50)
        top_frame.grid(row=0, column=0, columnspan=3)
        label_top = Label(top_frame, text='Dane kupno/sprzedaż pochodzą \nz aktualnego kursu dostępnego na stronie: \n"www.nbp.pl"', font='Arial 12', bd=1, relief="solid")
        label_top.pack()
        # Frame for radiobuttons to choose currency
        left_frame = Frame(window, width=100, height=400, bd=1, relief="solid")
        left_frame.grid(row=1, column=0)
        currency = Label(left_frame, text="Waluta:", font='Arial 12 underline bold')
        currency.pack()
        # Radiobuttons
        self.v = StringVar()
        self.v.set("0,0") # initialize variable
        for el in data:
            b = Radiobutton(left_frame, text=el, variable=self.v, value=el, command=self.radio_click, width=6).pack()
        # Right frame
        right_frame = Frame(window, width=225, height=400)
        right_frame.grid(row=1, column=1)
        # Current rate - info
        self.exchange_label = Label(right_frame, text="Kurs:\nKupno: 0,0000PLN\nSprzedaż: 0,0000PLN")
        self.exchange_label.place(x=60, y=30)
        # Amount to be converted - user input
        amount_frame = Frame(right_frame, width=185, height=100)
        amount_frame.place(x=25, y=120)
        amount_label = Label(amount_frame, text="Wprowadź kwotę:", font='Arial 12 underline bold')
        amount_label.pack()
        self.v2 = DoubleVar()
        amount_entry = Entry(amount_frame, font='Arial 12', textvariable=self.v2, bd=3)
        amount_entry.pack(pady=(10,10))
        amount_button = Button(amount_frame, text="Oblicz", command=self.get_result)
        amount_button.pack()

        # Result
        self.result_label = Label(right_frame, text="Kupno: \n0,00PLN\n\nSprzedaż: \n0,00PLN", font='Arial 14')
        self.result_label.place(x=70, y=250)

        # Currency name
        rama_bottom = Frame(window, width=300, height=50)
        rama_bottom.grid(row=2, column=0, columnspan=3)
        self.label_bottom = Label(rama_bottom, text="", font='Arial 18 bold')
        self.label_bottom.pack(pady=(3,0))

    def radio_click(self):
        self.label_bottom['text'] = self.data[self.v.get()][0]
        self.exchange_label['text'] = "Kurs:\nKupno: " + self.data[self.v.get()][1] + "PLN \nSprzedaż: " + self.data[self.v.get()][2] + "PLN"

    def get_result(self):
        try:
            buy = self.data[self.v.get()][1].replace(",", ".")
            sell = self.data[self.v.get()][2].replace(",", ".")
            self.result_label.place(x=70, y=250)
            self.result_label['fg'] = "green"
            if self.v.get() == "HUF" or self.v.get() == "JPY":
                self.result_label['text'] = "Kupno: \n" + str(round(self.v2.get() * float(buy) / 100, 2)) + "PLN\n\nSprzedaż: \n" + str(round(self.v2.get() * float(sell) / 100, 2)) + "PLN"
            else:
                self.result_label['text'] = "Kupno: \n" + str(round(self.v2.get() * float(buy), 2)) + "PLN\n\nSprzedaż: \n" + str(round(self.v2.get() * float(sell), 2)) + "PLN"
        except TclError:
            self.result_label.place(x=35, y=250)
            self.result_label['text'] = "Wprowadź liczbę. \n\nMiejsca dzisiętne \noddziel znakiem ' . '"
            self.result_label['fg'] = "red"
        except KeyError:
            self.result_label.place(x=50, y=250)
            self.result_label['text'] = "Wybierz walutę."
            self.result_label['fg'] = "red"
