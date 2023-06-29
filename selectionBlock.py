class SelectionBlock:
    def __init__(self, name, parent_frame):
        self.block_frame = ttk.Frame(parent_frame)
        self.block_frame.pack(padx=10, pady=10)

        self.name_label = ttk.Label(self.block_frame, text=name)
        self.name_label.pack()

        self.entry = ttk.Entry(self.block_frame)
        self.entry.pack(pady=10)

        self.delete_button = ttk.Button(self.block_frame, text="Удалить", command=self.delete_block)
        self.delete_button.pack()

    def delete_block(self):
        self.block_frame.destroy()

def add_selection_block(self):
    name = self.combobox.get()
    block = SelectionBlock(name, self.combobox_frame)