import logic
from tkinter import *
from tkinter import ttk, messagebox
import tkinter.font as tkfont

# Application Layer
class Application():
    #Initialize with business layer parameter
    def __init__(self, logic: logic.Logic):
        self.logic = logic

        server_list = ['', 'PostgreSQL']
        db_list = ['', 'IN450DB']

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
            server = selected_server.get()
            db = selected_db.get()
            user = user_entry.get()
            password = password_entry.get()
            return server, db, user, password
        
        #Checks credentials against the database and returns an error if incorrect
        def log_in():
            server, db, user, password = login_fetch()
            try:
                logic.login_check(server, db, user, password)
                login.withdraw()
                root.deiconify()
            except:
                messagebox.showinfo(f"Database {db} Login Error", "Incorrect username or password.")
                user_entry.delete(0, END)
                password_entry.delete(0, END)

        #Drops main window and returns login window / Clears entry fields
        def log_out():
            root.withdraw()
            login.deiconify()
            selected_server.set('')
            selected_db.set('')
            output_win.delete('1.0', END)
            user_entry.delete(0, END)
            password_entry.delete(0, END)

    #Root Window
        root = Tk()
        root.title('PostgreSQL Data Access Application')
        root.geometry('500x500')

        style = ttk.Style()
        style.configure('TMenubutton', background='white')

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

        exit_frame = Frame(root)
        out_btn = ttk.Button(exit_frame, text= 'Log Off', width= 15, command= lambda: log_out())
        exit_btn = ttk.Button(exit_frame, text= 'Exit', width= 15, command= lambda: root.destroy())

        lbl.pack(padx=10, pady=10, anchor= 'w')
        btn_frame.pack(pady=10)
        btn1.grid(column=1, row=1)
        btn2.grid(column=2, row=1)
        btn3.grid(column=3, row=1)
        btn4.grid(column=4, row=1)
        win_frame.pack(fill=X, pady=10)
        scroll_y.pack(side= RIGHT, fill= Y)
        output_win.pack()
        exit_frame.pack()
        out_btn.grid(column=1, row=1)
        exit_btn.grid(column=2, row=1)

    #Login Window
        login = Toplevel()
        login.geometry('500x175')
        log_lbl = ttk.Label(login, text= 'Data Access Login', justify= 'center')

        # Entry Frame
        entry_frame = Frame(login)
        server_lbl = ttk.Label(entry_frame, text= 'Server')
        selected_server = StringVar()
        server_select = ttk.OptionMenu(entry_frame, selected_server, *server_list)
        server_select.config(width=15)
        selected_db = StringVar()
        db_lbl = ttk.Label(entry_frame, text= 'Database')
        db_select = ttk.OptionMenu(entry_frame, selected_db, *db_list)
        db_select.config(width=15)
        user_lbl = ttk.Label(entry_frame, text= 'Username')
        user_entry = Entry(entry_frame)
        password_lbl = ttk.Label(entry_frame, text= 'Password')
        password_entry = Entry(entry_frame, show='*')

        log_btn1 = ttk.Button(login, text= 'Log In', width= 15, command=lambda: log_in())
        log_btn2 = ttk.Button(login, text= 'Exit', width= 15, command=lambda: root.destroy())

        log_lbl.pack()
        entry_frame.pack()
        server_lbl.grid(column=1, row=1, padx=5)
        server_select.grid(column=2, row=1, pady=2)
        db_lbl.grid(column=1, row=2, padx=5)
        db_select.grid(column=2, row=2, pady=2)
        user_lbl.grid(column=1, row=3, padx=5)
        user_entry.grid(column=2, row=3)
        password_lbl.grid(column=1, row=4, padx=5)
        password_entry.grid(column=2, row=4)
        log_btn1.pack(pady=5)
        log_btn2.pack()

        root.withdraw()
        root.mainloop()

#Application Execution

if __name__ == '__main__':
    db = logic.Logic()
    main = Application(db)