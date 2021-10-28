import tkinter as tk
from datetime import timedelta
import datetime as dt

class DateEntry(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        dateTime = master.dateTime
        self.year = tk.StringVar()
        self.year.set(dateTime.year)
        self.year.trace("w", lambda *args: self._check(0, 4))
        self.year_entry = tk.Entry(self, width=4, font=('Helvetica', 18, "bold"), textvariable=self.year)
        self.year_entry.bind("<1>", lambda event, entry = self.year_entry: master.switch_input_frame(entry, master.conf['system_page_section']['label_year'], 4))

        self.label_1 = tk.Label(self, text='/', font=('Helvetica', 18, "bold"))

        self.month = tk.StringVar()
        self.month.set(self.convert(dateTime.month))
        self.month.trace("w", lambda *args: self._check(1, 2))
        self.month_entry = tk.Entry(self, width=2, font=('Helvetica', 18, "bold"), textvariable=self.month)
        self.month_entry.bind("<1>", lambda event, entry = self.month_entry: master.switch_input_frame(entry, master.conf['system_page_section']['label_month'], 2))

        self.label_2 = tk.Label(self, text='/', font=('Helvetica', 18, "bold"))

        self.day = tk.StringVar()
        self.day.set(self.convert(dateTime.day))
        self.day.trace("w", lambda *args: self._check(2, 2))
        self.day_entry = tk.Entry(self, width=2, font=('Helvetica', 18, "bold"), textvariable=self.day)
        self.day_entry.bind("<1>", lambda event, entry = self.day_entry: master.switch_input_frame(entry, master.conf['system_page_section']['label_day'], 2))

        self.year_entry.pack(side=tk.LEFT)
        self.label_1.pack(side=tk.LEFT)
        self.month_entry.pack(side=tk.LEFT)
        self.label_2.pack(side=tk.LEFT)
        self.day_entry.pack(side=tk.LEFT)

        self.entries = [self.year_entry, self.month_entry, self.day_entry]

    def _check(self, index, size):
        entry = self.entries[index]
        next_index = index + 1
        next_entry = self.entries[next_index] if next_index < len(self.entries) else None
        data = entry.get()

        if len(data) == size and self.year.get() and self.month.get() and self.day.get():
            try:
                dt.datetime.strptime(self.year.get() + self.month.get() + self.day.get() , "%Y%m%d")
            except:
                self.changecolor('#FF5151')
                self.master.valid_date = False
            else:
                self.changecolor('#FFFFFF')
                self.master.valid_date = True
            entry.focus_set()
            self.master.switch_button_status()

    def changecolor(self, color):
        for entry in self.entries:
            entry.configure(bg=color)

    def get(self):
        return [e.get() for e in self.entries]

    def convert(self, data):
        if data < 10:
            return "0" + str(data)
        else:
            return data
