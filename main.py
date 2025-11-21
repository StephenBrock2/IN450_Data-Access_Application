import logic
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter.font as tkfont

# Application Layer
class Application():
    #Initialize with business layer parameter
    def __init__(self, logic: logic.Logic):
        self.logic = logic

        root = Tk()

        root.title('PostgreSQL Data Access Application')
        root.geometry('500x400')

        #Button command to display rowcount query 
        def rowcount_btn(output, tbl):
            query = logic.row_count(tbl)
            output.delete('1.0', END)
            text = (f'There are {query} rows.')
            output.insert(END, text)

        #Button command to display name list query 
        def namelist_btn(output):
            query = logic.name_list()
            output.delete('1.0', END)
            for i, n in query:
                output.insert(END, f'{i} {n}\n')

        #Login credential fetch/check
        def login_fetch():
            user = user_entry.get()
            password = password_entry.get()
            return user, password
        
        def log_in():
            user, password = login_fetch()
            print(logic.login_check(user, password))
            
            login.destroy()
            root.deiconify()

    #Root Label
        lbl = ttk.Label(root, text= 'Data Access Commands', justify= 'left')
        lbl.pack(padx=10, pady=10, anchor= 'w')

    #Root Button Frame
        btn_frame = Frame(root)

        btn1 = ttk.Button(btn_frame, text= 'Get Rows A', width= 15, command=lambda: rowcount_btn(output_win, 'in450a'))
        btn2 = ttk.Button(btn_frame, text= 'Name List', width= 15, command=lambda: namelist_btn(output_win))
        btn3 = ttk.Button(btn_frame, text= 'Get Rows C', width= 15, command=lambda: rowcount_btn(output_win, 'in450c'))
        btn4 = ttk.Button(btn_frame, text= 'Clear', width= 15, command=lambda: output_win.delete('1.0', END))
        
        btn_frame.pack(pady=10)
        btn1.grid(column=1, row=1)
        btn2.grid(column=2, row=1)
        btn3.grid(column=3, row=1)
        btn4.grid(column=4, row=1)

    #Root Output Frame
        win_frame = Frame(root)
        
        scroll_y = ttk.Scrollbar(win_frame, orient= 'vertical')
        output_win = Text(win_frame, height=20, width=50, padx=5, pady=5, yscrollcommand= scroll_y.set)
        scroll_y.config(command= output_win.yview)
        win_font = tkfont.Font(family='Arial', size=10)
        output_win.configure(font=win_font)

        win_frame.pack(fill=X, pady=10)
        scroll_y.pack(side= RIGHT, fill= Y)
        output_win.pack()

    #Login Window
        login = Toplevel()
        login.geometry('500x120')

        log_lbl = ttk.Label(login, text= 'Data Access Login', justify= 'center')

        user_entry = Entry(login)
        password_entry = Entry(login)

        log_btn1 = ttk.Button(login, text= 'Log In', width= 15, command=lambda: log_in())
        log_btn2 = ttk.Button(login, text= 'Exit', width= 15, command=lambda: root.destroy())

        log_lbl.pack()
        user_entry.pack()
        password_entry.pack()
        log_btn1.pack()
        log_btn2.pack()

        root.withdraw()
        root.mainloop()

#Application Execution

if __name__ == '__main__':

    db = logic.Logic()
    main = Application(db)