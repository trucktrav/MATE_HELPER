import tkinter as tk
import DB_Helper.py_safe_eval as safe
import os
from DB_Helper.py_eval_helper import EvalHelp, HeaderHelp


class Selector(tk.Frame):
    """
    Selector class
    input: string name of the group, parent frame of the group, and controller of window
    Creates a label using the input name, two list boxes, on the left is the 'from' and the right is the 'to
    Between the lists are 4 buttons to move the data between the list, move one ('>' or '<') and move all ('>>' or '<<')
    Class also holds the data contained in the list, in two variables. The list variable is modified by add or del
    buttons. On update the list variables set the var lists, which are connected to the visual display.

    """

    def __init__(self, name, l_type, parent, controller, session):
        tk.Frame.__init__(self, master=parent)
        self.frame = tk.Frame(master=self)
        self.frame.pack(side="top", fill="both", expand=True)
        self.name = name
        self.parent = parent
        self.controller = controller
        self.session = session
        # load the database information for the lists
        self.db_from = [item for item in session.query(HeaderHelp)]
        self.list_from = [item.name for item in self.db_from]
        self.db_to = [item for item in session.query(EvalHelp).filter_by(type=name)]
        self.list_to = [item.name for item in self.db_to]
        # set the display list boxes to the database lists
        self.var_from = tk.StringVar(value=self.list_from)
        self.var_to = tk.StringVar(value=self.list_to)

        # create the label
        self.label = tk.Label(master=self.frame, text="{0} Selector".format(name))
        # create the from list
        self.lb_from = ListObject(name="from_list", parent=self.frame, controller=controller, list_data=self.var_from)
        self.lb_from.grid(row=1, column=0, sticky='nsew')
        # create the to list
        self.lb_to = ListObject(name="to_list", parent=self.frame, controller=controller, list_data=self.var_to)
        self.label.grid(row=0, column=0, sticky='nsew')
        # create the buttons
        if l_type == 'selector':
            self.buttons = SelectorButtons(parent=self.frame, controller=self)
            self.lb_to.grid(row=1, column=2, sticky='nsew')
        elif l_type == 'calculator':
            self.lb_from.grid(row=1, column=0, rowspan=2, sticky='nsew')
            self.buttons = SelectorCalculator(parent=self.frame, controller=self)
            self.buttons.grid(row=1, column=2, sticky='nsew')
            self.lb_from.list.config(selectmode=tk.SINGLE)
            self.lb_to.list.bind(sequence='<<ListboxSelect>>', func=self.to_select)
            self.lb_from.list.bind(sequence='<Double-Button-1>', func=self.buttons.use_selection)
            self.lb_to.grid(row=2, column=2, sticky='nsew')
        else:
            print('{0} is not a valid list creator type'.format(type))

        c, r = self.frame.grid_size()
        for i in range(r):
            self.frame.grid_rowconfigure(i, weight=1)
        for j in range(c):
            if j != 1:
                self.frame.grid_columnconfigure(j, weight=1)

    def add_selection(self, method):
        """
        input: method = 'one' or 'all
        output: none
        action: adds the selected or all items to the "to list" and removes from the "from list"
        """
        if method == 'one':
            selection = self.lb_from.list.curselection()
        else:
            selection = [x for x in range(len(self.list_from))]

        for i in selection:
            value = self.lb_from.list.get(i)
            add = EvalHelp(name=value, function=value, display=value, type=self.name)
            session.add(add)
            session.commit()
            self.list_from.remove(value)
            self.list_to.append(value)
        self.var_from.set(self.list_from)
        self.var_to.set(self.list_to)

    def del_selection(self, method):
        """
        input: method = 'one' or 'all
        output: none
        action: removes the selected or all items from the "to list" and puts back on the "from list"
        """
        if method == 'one':
            i = self.lb_to.list.curselection()[0]
            selection = session.query(EvalHelp).filter_by(name=self.list_to[i])
            self.list_to.remove(self.list_to[i])
        else:
            selection = session.query(EvalHelp).filter_by(type=self.name)
            self.list_to = []

        for i in selection:
            session.delete(i)
            self.list_from.append(i.name)

        session.commit()
        self.list_from.sort()
        self.var_from.set(self.list_from)
        self.var_to.set(self.list_to)

    def set_list(self, set_list):
        """
        input: list to display in the listbox
        return: nothing
        Set the from list and clears the to list
        """
        self.list_from = set_list
        self.var_from.set(self.list_from)
        # self.list_to = []
        # self.var_to.set(self.list_to)

    def to_select(self, param):
        print('to_select')
        i = self.lb_to.list.curselection()[0]
        selection = session.query(EvalHelp).filter_by(name=self.list_to[i]).first()
        self.buttons.set_text(selection=selection)


class SelectorButtons(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, master=parent)

        self.btn_add_one = tk.Button(master=self, text=">", command=lambda: controller.add_selection('one'))
        self.btn_add_all = tk.Button(master=self, text=">>", command=lambda: controller.add_selection('all'))
        self.btn_del_one = tk.Button(master=self, text="<", command=lambda: controller.del_selection('one'))
        self.btn_del_all = tk.Button(master=self, text="<<", command=lambda: controller.del_selection('all'))

        self.grid(row=1, column=1, sticky='nsew')
        self.btn_add_one.grid(row=0, column=0, sticky='nsew')
        self.btn_add_all.grid(row=1, column=0, sticky='nsew')
        self.btn_del_one.grid(row=2, column=0, sticky='nsew')
        self.btn_del_all.grid(row=3, column=0, sticky='nsew')

    @staticmethod
    def set_text(selection: EvalHelp):
        print('selector do nothing, yet')


class SelectorCalculator(tk.Frame):

    def __init__(self, parent: tk.Frame, controller: Selector):
        tk.Frame.__init__(self, master=parent)
        self.controller = controller
        self.btn_clear = tk.Button(master=self, text="Clear", command=self.clear_selection)
        self.btn_use = tk.Button(master=self, text=">", command=self.use_selection)
        # Name section
        self.frame_name = tk.Frame(master=self)
        self.frame_name.grid_columnconfigure(1, weight=1)
        self.lbl_name = tk.Label(master=self.frame_name, text='Name')
        self.lbl_name.grid(row=0, column=0)
        self.text_name = tk.Entry(master=self.frame_name)
        self.text_name.grid(row=0, column=1, sticky='nsew')
        # function section
        self.frame_function = tk.Frame(master=self)
        self.frame_function.grid_columnconfigure(1, weight=1)
        self.lbl_function = tk.Label(master=self.frame_function, text='Function')
        self.lbl_function.grid(row=0, column=0)
        self.text_function = tk.Entry(master=self.frame_function)
        self.text_function.grid(row=0, column=1, sticky='nsew')
        # display section
        self.frame_display = tk.Frame(master=self)
        self.frame_display.grid_columnconfigure(1, weight=1)
        self.lbl_display = tk.Label(master=self.frame_display, text='Display')
        self.lbl_display.grid(row=0, column=0)
        self.text_display = tk.Entry(master=self.frame_display)
        self.text_display.grid(row=0, column=1, sticky='nsew')
        # buttons
        self.btn_commit = tk.Button(master=self, text=">>", command=self.commit_selection)
        self.btn_del_one = tk.Button(master=self, text="<", command=lambda: controller.del_selection('one'))
        self.btn_del_all = tk.Button(master=self, text="<<", command=lambda: controller.del_selection('all'))
        # grid
        self.grid(row=1, column=1, sticky='nsew')
        self.btn_clear.grid(row=0, column=0, sticky='nsew')
        self.btn_use.grid(row=0, column=1, sticky='nsew')
        self.frame_name.grid(row=1, column=0, columnspan=3, sticky='nsew')
        self.frame_function.grid(row=2, column=0, columnspan=3, sticky='nsew')
        self.frame_display.grid(row=3, column=0, columnspan=3, sticky='nsew')
        self.btn_commit.grid(row=4, column=0, sticky='nsew')
        self.btn_del_one.grid(row=4, column=1, sticky='nsew')
        self.btn_del_all.grid(row=4, column=2, sticky='nsew')

        c, r = self.grid_size()
        for i in range(r - 1):
            self.grid_rowconfigure(i, weight=1)
        for j in range(c):
            self.grid_columnconfigure(j, weight=1)

    def clear_selection(self):
        self.text_function.delete(0, tk.END)
        self.text_display.delete(0, tk.END)
        self.text_name.delete(0, tk.END)

    def use_selection(self, *args):
        print(args)
        selection = self.controller.lb_from.list.curselection()

        for i in selection:
            self.text_function.insert(tk.END, 'run_data[{0}]'.format(self.controller.lb_from.list.get(i)))

    def commit_selection(self):
        display = self.text_display.get()
        function = self.text_function.get()
        name = self.text_name.get()

        if len(display) == 0 or len(function) == 0 or len(name) == 0:
            return
        add = EvalHelp(name=name, function=function, display=display, type='calcs')
        session.add(add)
        session.commit()
        self.controller.list_to.append(display)
        self.controller.var_to.set(self.controller.list_to)
        self.text_function.delete(0, tk.END)
        self.text_display.delete(0, tk.END)
        self.text_name.delete(0, tk.END)

    def set_text(self, selection: EvalHelp):
        self.text_function.delete(0, tk.END)
        self.text_display.delete(0, tk.END)
        self.text_name.delete(0, tk.END)
        self.text_name.insert(index=0, string=selection.name)
        self.text_function.insert(index=0, string=selection.function)
        self.text_display.insert(index=0, string=selection.display)


class ListObject(tk.Frame):
    """
    ListObject class
    input: string name of the group, parent frame of the group, controller of window, and list data
    Creates a list using the input data, along with horizontal(x) and vertical(y) scroll bars
    Does not store the data
    """

    def __init__(self, name: str, parent: tk.Frame, controller: tk.Frame, list_data: tk.StringVar):
        """

        @type name: str
        """
        tk.Frame.__init__(self, master=parent)

        self.name = name
        self.parent = parent
        self.controller = controller

        # create the scroll bars
        self.xscroll = tk.Scrollbar(master=self, orient=tk.HORIZONTAL)
        self.yscroll = tk.Scrollbar(master=self, orient=tk.VERTICAL)
        # create the list box
        self.list = tk.Listbox(master=self, selectmode=tk.EXTENDED, listvariable=list_data,
                               yscrollcommand=self.yscroll.set, xscrollcommand=self.xscroll.set)
        # self.list.bind(sequence='<<ListboxSelect>>', func=self.box_selected)
        # config the scroll bars
        self.yscroll.config(command=self.list.yview)
        self.xscroll.config(command=self.list.xview)

        # now pack everything
        self.xscroll.pack(side=tk.BOTTOM, fill=tk.X, expand=False)
        self.list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.yscroll.pack(side=tk.LEFT, fill=tk.Y, expand=False)

    @staticmethod
    def box_selected(event):
        print('list selected')


class ListApp(tk.Tk):
    """
    ListApp class
    input: dict that contains the name and type of list to create, types include 'selector' and 'calculator'
    Create the window app, three Selectors, for Intermediates, Attributes, and Calculation lists
    Also create the 'execute' button, which returns the various "To" lists
    """

    def __init__(self, create_list, session):
        super().__init__()
        self.session = session
        window = super()
        window.title('MATE Helper')
        window.geometry('800x800')
        window.protocol(name="WM_DELETE_WINDOW", func=self.on_delete)
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.names = create_list
        self.lists = {}
        index = 0
        for name, l_type in self.names.items():
            self.lists[name] = Selector(name=name, l_type=l_type, parent=self.container, controller=self, session=session)
            self.lists[name].grid(row=index, column=0, sticky='nsew')
            index += 1

        self.exec = tk.Button(master=self.container, text="Build Data", command=lambda: self.execute())
        self.exec.grid(row=len(self.names), column=0, sticky='nsew')

        c, r = self.container.grid_size()
        for i in range(r - 1):
            self.container.grid_rowconfigure(i, weight=1)
        for j in range(c):
            self.container.grid_columnconfigure(j, weight=1)

    def set_data(self, list_data):
        """
        input: dict with three entries, intermediate, attributes, calcs, each entry contains a list to display
        return: nothing
        """
        for name in self.names:
            self.lists[name].set_list(list_data[name])

    def execute(self):
        print("exec")
        self.destroy()

    def on_delete(self):
        """capture tne on delete message from windows to save the data

        Args: none


        Returns: nothing

        """
        # for key, value in self.lists.items():
        #     self.lists[key].list_to.save_data()
        self.session.close()
        self.destroy()


import sqlalchemy
from sqlalchemy.orm import sessionmaker


if __name__ == "__main__":
    create = {'intermediates': 'selector', 'attributes': 'selector', 'calcs': 'calculator'}
    db = os.path.abspath(os.path.dirname(__file__)) + '\\metrics_database.db'
    engine = sqlalchemy.create_engine('sqlite:///{0}'.format(db))
    Session = sessionmaker(bind=engine)
    session = Session()
    app = ListApp(create_list=create, session=session)
    data = {}
    data['intermediates'] = list(map(lambda x: x, range(20)))
    data['attributes'] = list(map(lambda x: x ** 2, range(20)))
    data['calcs'] = list(map(lambda x: x ** 3, range(20)))
    # app.set_data(list_data=data)
    app.mainloop()
    print('done')
