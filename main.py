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

        #Button command to display rowcount query or permission error
        def rowcount_btn(output, tbl):
            output.delete('1.0', END)
            try:
                query = logic.row_count(tbl)
                text = (f'There are {query} rows.')
            except:
                text = ('Your account does not have permission to view.')
            output.insert(END, text)

        #Button command to display name list query or permissison error
        def namelist_btn(output):
            output.delete('1.0', END)
            try:
                query = logic.name_list()
                for i, n in query:
                    output.insert(END, f'{i} {n}\n')
            except:
                text = ('Your account does not have permission to view.')
                output.insert(END, text)

        #Login credential fetch from enty
        def login_fetch():
            user = user_entry.get()
            password = password_entry.get()
            return user, password
        
        #Checks credentials against the database and returns an error if incorrect
        def log_in():
            user, password = login_fetch()
            try:
                print(logic.login_check(user, password))
                login.destroy()
                root.deiconify()
            except:
                messagebox.showinfo("Login Error", "Incorrect username or password.")
                user_entry.delete(0, END)
                password_entry.delete(0, END)

    #Root Window
        lbl = ttk.Label(root, text= 'Data Access Commands', justify= 'left')

        # Button Frame
        btn_frame = Frame(root)

        btn1 = ttk.Button(btn_frame, text= 'Get Rows A', width= 15, command=lambda: rowcount_btn(output_win, 'in450a'))
        btn2 = ttk.Button(btn_frame, text= 'Name List', width= 15, command=lambda: namelist_btn(output_win))
        btn3 = ttk.Button(btn_frame, text= 'Get Rows C', width= 15, command=lambda: rowcount_btn(output_win, 'in450c'))
        btn4 = ttk.Button(btn_frame, text= 'Clear', width= 15, command=lambda: output_win.delete('1.0', END))

        # Output Frame
        win_frame = Frame(root)
        
        scroll_y = ttk.Scrollbar(win_frame, orient= 'vertical')
        output_win = Text(win_frame, height=20, width=50, padx=5, pady=5, yscrollcommand= scroll_y.set)
        scroll_y.config(command= output_win.yview)
        win_font = tkfont.Font(family='Arial', size=10)
        output_win.configure(font=win_font)


        lbl.pack(padx=10, pady=10, anchor= 'w')
        btn_frame.pack(pady=10)
        btn1.grid(column=1, row=1)
        btn2.grid(column=2, row=1)
        btn3.grid(column=3, row=1)
        btn4.grid(column=4, row=1)
        win_frame.pack(fill=X, pady=10)
        scroll_y.pack(side= RIGHT, fill= Y)
        output_win.pack()

    #Login Window
        login = Toplevel()
        login.geometry('500x120')
        log_lbl = ttk.Label(login, text= 'Data Access Login', justify= 'center')

        # Entry Frame
        entry_frame = Frame(login)
        user_lbl = ttk.Label(entry_frame, text= 'Username')
        user_entry = Entry(entry_frame)
        password_lbl = ttk.Label(entry_frame, text= 'Password')
        password_entry = Entry(entry_frame)

        log_btn1 = ttk.Button(login, text= 'Log In', width= 15, command=lambda: log_in())
        log_btn2 = ttk.Button(login, text= 'Exit', width= 15, command=lambda: root.destroy())

        log_lbl.pack()
        entry_frame.pack()
        user_lbl.grid(column=1, row=1)
        user_entry.grid(column=2, row=1)
        password_lbl.grid(column=1, row=2)
        password_entry.grid(column=2, row=2)
        log_btn1.pack(pady=5)
        log_btn2.pack()

        root.withdraw()
        root.mainloop()

#Application Execution

if __name__ == '__main__':
    db = logic.Logic()
    main = Application(db)