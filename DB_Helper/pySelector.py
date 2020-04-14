import tkinter as tk


class Selector(tk.Frame):
    """
    Selector class
    input: string name of the group, parent frame of the group, and controller of window
    Creates a label using the input name, two list boxes, on the left is the 'from' and the right is the 'to
    Between the lists are 4 buttons to move the data between the list, move one ('>' or '<') and move all ('>>' or '<<')
    Class also holds the data contained in the list, in two variables. The list variable is modified by add or del
    buttons. On update the list variables set the var lists, which are connected to the visual display.

    """
    def __init__(self, name, parent, controller):
        tk.Frame.__init__(self, master=parent)
        self.frame = tk.Frame(master=self)
        self.frame.pack(side="top", fill="both", expand=True)
        # self.frame.grid_rowconfigure(0, weight=1)
        # self.frame.grid_columnconfigure(0, weight=1)
        self.name = name
        self.parent = parent
        self.controller = controller
        self.list_from = []
        self.list_to = []
        self.var_from = tk.StringVar(value=[])
        self.var_to = tk.StringVar(value=[])

        # create the label
        self.label = tk.Label(master=self.frame, text="{0} Selector".format(name))
        # create the from list
        self.lb_from = ListObject(name="from_list", parent=self.frame, controller=controller, list_data=self.var_from)
        # create the to list
        self.lb_to = ListObject(name="to_list", parent=self.frame, controller=controller, list_data=self.var_to)
        # create the buttons
        self.button_frame = tk.Frame(master=self.frame)
        self.btn_add_one = tk.Button(master=self.button_frame, text=">", command=lambda: self.add_selection('one'))
        self.btn_add_all = tk.Button(master=self.button_frame, text=">>", command=lambda: self.add_selection('all'))
        self.btn_del_one = tk.Button(master=self.button_frame, text="<", command=lambda: self.del_selection('one'))
        self.btn_del_all = tk.Button(master=self.button_frame, text="<<", command=lambda: self.del_selection('all'))

        self.label.grid(row=0, column=0, sticky='nsew')
        self.lb_from.grid(row=1, column=0, sticky='nsew')
        self.button_frame.grid(row=1, column=1, sticky='nsew')
        self.btn_add_one.grid(row=0, column=0, sticky='nsew')
        self.btn_add_all.grid(row=1, column=0, sticky='nsew')
        self.btn_del_one.grid(row=2, column=0, sticky='nsew')
        self.btn_del_all.grid(row=3, column=0, sticky='nsew')
        self.lb_to.grid(row=1, column=2, sticky='nsew')
        # self.frame.grid_columnconfigure(2, weight=2)

        r, c = self.frame.grid_size()
        for i in range(r):
            self.frame.grid_rowconfigure(i, weight=1)
        for j in range(c):
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
            selection = self.lb_to.list.curselection()
        else:
            selection = [x for x in range(len(self.list_to))]

        for i in selection:
            value = self.lb_to.list.get(i)
            self.list_to.remove(value)
            self.list_from.append(value)
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
        self.list_to = []
        self.var_to.set(self.list_to)


class ListObject(tk.Frame):
    """
    ListObject class
    input: string name of the group, parent frame of the group, controller of window, and list data
    Creates a list using the input data, along with horizontal(x) and vertical(y) scroll bars
    Does not store the data
    """
    def __init__(self, name, parent, controller, list_data):
        tk.Frame.__init__(self, master=parent)

        self.name = name
        self.parent = parent
        self.controller = controller

        # create the scroll bars
        self.xscroll = tk.Scrollbar(master=self, orient=tk.HORIZONTAL)
        self.yscroll = tk.Scrollbar(master=self, orient=tk.VERTICAL)
        # create the list box
        self.list = tk.Listbox(master=self, selectmode=tk.EXTENDED,  listvariable=list_data,
                               yscrollcommand=self.yscroll.set, xscrollcommand=self.xscroll.set)
        # config the scroll bars
        self.yscroll.config(command=self.list.yview)
        self.xscroll.config(command=self.list.xview)

        # now pack everything
        self.list.grid(row=0, column=0, sticky='nsew')
        self.list.grid_columnconfigure(0, weight=1)
        # self.xscroll.pack(side=tk.BOTTOM, fill=tk.X, expand=True)
        # self.list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # self.yscroll.pack(side=tk.LEFT, fill=tk.Y, expand=True)


class ListApp(tk.Tk):
    """
    ListApp class
    input: none
    Create the window app, three Selectors, for Intermediates, Attributes, and Calculation lists
    Also create the 'execute' button, which returns the various "To" lists
    """
    def __init__(self):
        super().__init__()
        window = super()
        window.title('MATE Helper')
        window.geometry('800x800')

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.names = ['intermediates', 'attributes', 'calcs']
        self.lists = {}
        for name in self.names:
            self.lists[name] = Selector(name=name, parent=self.container, controller=self)
            self.lists[name].grid(row=self.names.index(name), column=0, sticky='nsew')

        # self.inter_list =
        # self.attr_list = Selector("attributes", parent=self.container, controller=self)
        # self.attr_list.grid(row=1, column=0, sticky='nsew')
        # self.calc_list = Selector("calcs", parent=self.container, controller=self)
        # self.calc_list.grid(row=2, column=0, sticky='nsew')
        self.exec = tk.Button(master=self.container, text="Build Data", command=lambda: self.execute())
        self.exec.grid(row=len(self.names), column=0, sticky='nsew')
        self.container.grid_columnconfigure(0, weight=1)

        r, c = self.container.grid_size()
        for i in range(r):
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


if __name__ == "__main__":
    app = ListApp()
    data = {}
    data['intermediates'] = list(map(lambda x: x, range(20)))
    data['attributes'] = list(map(lambda x: x ** 2, range(20)))
    data['calcs'] = list(map(lambda x: x ** 3, range(20)))
    app.set_data(list_data=data)
    app.mainloop()
    print('done')
