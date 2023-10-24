import tkinter as tk
from tkinter import ttk
import sqlite3


# Класс главного окна
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.tree = None
        self.init_main()
        self.db = db
        self.view_records()

    # инициализация виджетов
    def init_main(self):
        toolbar = tk.Frame(bg='#d7d7d7', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # кнопка добавления
        btn_add = tk.Button(toolbar, text='Добавить', bg='#d7d7d7', relief=tk.RIDGE,
                            bd=3, command=self.open_child)
        btn_add.pack(side=tk.LEFT)
        # кнопка изменения
        btn_upd = tk.Button(toolbar, text='Изменить', bg='#d7d7d7',
                            bd=3, command=self.open_update_child, relief=tk.RIDGE)
        btn_upd.pack(side=tk.LEFT)
        # кнопка удаления
        btn_del = tk.Button(toolbar, text='Удалить', bg='#d7d7d7',
                            bd=3, command=self.delete_records, relief=tk.RIDGE)
        btn_del.pack(side=tk.LEFT)
        # кнопка поиска
        btn_search = tk.Button(toolbar, text='Поиск', bg='#d7d7d7',
                               bd=3, command=self.open_search, relief=tk.RIDGE)
        btn_search.pack(side=tk.LEFT)
        # кнопка обновления
        btn_refrech = tk.Button(toolbar, text='Обновление', bg='#d7d7d7',
                                bd=3, command=self.view_records, relief=tk.RIDGE)
        btn_refrech.pack(side=tk.LEFT)
        self.tree = ttk.Treeview(self, columns=('id', 'name', 'phone', 'email', 'salary'),
                                 height=17, show='headings')
        self.tree.column('id', width=45, anchor=tk.CENTER)
        self.tree.column('name', width=200, anchor=tk.CENTER)
        self.tree.column('phone', width=150, anchor=tk.CENTER)
        self.tree.column('email', width=150, anchor=tk.CENTER)
        self.tree.column('salary', width=100, anchor=tk.CENTER)
        self.tree.heading('id', text='ID')
        self.tree.heading('name', text='ФИО')
        self.tree.heading('phone', text='Телефон')
        self.tree.heading('email', text='E-mail')
        self.tree.heading('salary', text='Зарплата')

        self.tree.pack(side=tk.LEFT)
        # добавление Scrollbar
        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

    # метод добавления данных
    def records(self, name, phone, email, salary):
        self.db.insert_data(name, phone, email, salary)
        self.view_records()

    # отображение данных в окне программы
    def view_records(self):
        self.db.cur.execute('SELECT * FROM users')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=i) for i in self.db.cur.fetchall()]

    # метод поиска данных
    def search_records(self, name):
        self.db.cur.execute('SELECT * FROM users WHERE name LIKE ?',
                            ('%' + name + '%',))
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=i) for i in self.db.cur.fetchall()]

    # метод изменения данных
    def update_record(self, name, phone, email, salary):
        id = self.tree.set(self.tree.selection()[0], '#1')
        self.db.cur.execute('''
            UPDATE users 
            SET name = ?, phone = ?, email = ?, salary = ?
            WHERE id = ?
        ''', (name, phone, email, salary, id))
        self.db.conn.commit()
        self.view_records()

    # удаление выделенных строк
    def delete_records(self):
        for row in self.tree.selection():
            self.db.cur.execute('DELETE FROM users WHERE id = ?',
                                (self.tree.set(row, '#1'),))
        self.db.conn.commit()
        self.view_records()

    # вызов дочернего окна для добавления данных
    def open_child(self):
        Child()

    # вызов дочернего окна для обновления данных
    def open_update_child(self):
        Update()

    # вызов дочернего окна для поиска
    def open_search(self):
        Search()


# класс дочернего окна
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.btn_add = None
        self.entry_salary = None
        self.entry_email = None
        self.entry_phone = None
        self.entry_name = None
        self.init_child()
        self.view = app

    # инициализация виджетов дочернего окна
    def init_child(self):
        self.title('Добавление контакта')
        self.geometry('400x200')
        self.resizable(False, False)
        self.grab_set()  # перехватываем все события
        self.focus_set()  # перехватываем фокус
        label_name = tk.Label(self, text='ФИО')
        label_name.place(x=50, y=50)
        label_phone = tk.Label(self, text='Телефон')
        label_phone.place(x=50, y=80)
        label_email = tk.Label(self, text='Почта')
        label_email.place(x=50, y=110)
        label_salary = tk.Label(self, text='Зарплата')
        label_salary.place(x=50, y=140)

        self.entry_name = tk.Entry(self)
        self.entry_name.place(x=200, y=50)
        self.entry_phone = tk.Entry(self)
        self.entry_phone.place(x=200, y=80)
        self.entry_email = tk.Entry(self)
        self.entry_email.place(x=200, y=110)
        self.entry_salary = tk.Entry(self)
        self.entry_zarplata.place(x=200, y=140)
        btn_cancel = tk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=200, y=170)
        self.btn_add = tk.Button(self, text='Добавить')
        self.btn_add.bind('<Button-1>', lambda ev: self.view.records(self.entry_name.get(),
                                                                     self.entry_phone.get(),
                                                                     self.entry_email.get(),
                                                                     self.entry_salary.get()))
        self.btn_add.place(x=265, y=170)


# класс дочернего окна для изменения данных
class Update(Child):
    def __init__(self):
        super().__init__()
        self.btn_upd = None
        self.init_update()
        self.db = db
        self.default_data()

    # инициализация окна
    def init_update(self):
        self.title('Изменение контакта')
        self.btn_add.destroy()
        self.btn_upd = tk.Button(self, text='Изменить')
        self.btn_upd.bind('<Button-1>', lambda ev: self.view.update_record(self.entry_name.get(),
                                                                           self.entry_phone.get(),
                                                                           self.entry_email.get(),
                                                                           self.entry_zarplata.get()))
        self.btn_upd.bind('<Button-1>', lambda ev: self.destroy(), add='+')
        self.btn_upd.place(x=265, y=170)

    # заполнение окна редактирования данными для изменения
    def default_data(self):
        id = self.view.tree.set(self.view.tree.selection()[0], '#1')
        self.db.cur.execute('SELECT * from users WHERE id = ?', (id,))
        row = self.db.cur.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_phone.insert(0, row[2])
        self.entry_email.insert(0, row[3])
        self.entry_zarplata.insert(0, row[4])


# класс окна для поиска
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.entry_name = None
        self.btn_add = None
        self.init_child()
        self.view = app

    # инициализация виджетов дочернего окна
    def init_child(self):
        self.title('Поиск контакта')
        self.geometry('300x100')
        self.resizable(False, False)
        self.grab_set()  # перехватываем все события
        self.focus_set()  # перехватываем фокус
        label_name = tk.Label(self, text='ФИО')
        label_name.place(x=30, y=30)

        self.entry_name = tk.Entry(self)
        self.entry_name.place(x=130, y=30)
        btn_cancel = tk.Button(self, text='Закрыть',
                               command=self.destroy)
        btn_cancel.place(x=150, y=70)
        self.btn_add = tk.Button(self, text='Найти')
        self.btn_add.bind('<Button-1>', lambda ev: self.view.search_records(self.entry_name.get()))
        self.btn_add.bind('<Button-1>', lambda ev: self.destroy(), add='+')
        self.btn_add.place(x=225, y=70)


# класс базы данных
class Db:
    def __init__(self):
        self.conn = sqlite3.connect('Employers.db')
        self.cur = self.conn.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        phone TEXT,
                        email TEXT,
                        salary INTEGER
                    )''')
        self.conn.commit()
        self.default_data()  # заполнение базы тестовыми данными (убрать при первом запуске в случаи если 2 раз не
        # запускается)

    #  добавление информации в базу данных
    def insert_data(self, name, phone, email, salary):
        self.cur.execute('''
                INSERT INTO users (name, phone, email, salary)
                VALUES (?, ?, ?, ?)''', (name, phone, email, salary))
        self.conn.commit()

    #  заполнение базы тестовыми данными
    def default_data(self):
        usr = [
            (1, "Иванов Иван Иванович", "+7(111)111-11-11", "ivan@mail.ru", 100000),
            (2, "Петров Петр Петрович", "+7(222)222-22-22", "petr@gmail.com", 80000),
            (3, "Михайлов Михаил Михайлович", "+7(333)333-33-3", "mikhail@yahoo.com", 60000),
            (4, "Егоров Егор Егорович", "+7(444)444-44-44", "egor@outlook.com", 40000),
            (5, "Дмитриев Дмитрий Дмитриевич", "+7(555)555-55-55", "dmitriy@yandex.ru", 20000)
        ]
        query_insert = '''
        INSERT INTO users (id, name, phone, email, salary)
        VALUES (?, ?, ?, ?, ?)
        '''
        self.cur.executemany(query_insert, usr)
        self.conn.commit()


# при запуске программы
if __name__ == '__main__':
    root = tk.Tk()
    db = Db()
    app = Main(root)
    app.pack()
    root.title('Список сотрудников')
    root.geometry('665x450')
    root.resizable(False, False)
    root.mainloop()
