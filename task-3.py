import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os


class ContactManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Manager")

        # Setting the style for the main window
        self.root.configure(bg="#f0f0f0")

        self.contacts = self.load_contacts()

        self.frame = tk.Frame(root, bg="#f0f0f0")
        self.frame.pack(pady=10)

        self.listbox = tk.Listbox(self.frame, width=50, height=15, font=("Arial", 12), bg="#ffffff", fg="#000000", bd=1,
                                  relief="solid")
        self.listbox.pack(side=tk.LEFT, padx=10)
        self.update_listbox()

        self.scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=self.scrollbar.set)

        self.add_button = tk.Button(root, text="Add Contact", command=self.add_contact, font=("Arial", 12),
                                    bg="#4CAF50", fg="#ffffff", bd=0, relief="solid", padx=10, pady=5)
        self.add_button.pack(pady=5)

        self.edit_button = tk.Button(root, text="Edit Contact", command=self.edit_contact, font=("Arial", 12),
                                     bg="#FFC107", fg="#ffffff", bd=0, relief="solid", padx=10, pady=5)
        self.edit_button.pack(pady=5)

        self.delete_button = tk.Button(root, text="Delete Contact", command=self.delete_contact, font=("Arial", 12),
                                       bg="#F44336", fg="#ffffff", bd=0, relief="solid", padx=10, pady=5)
        self.delete_button.pack(pady=5)

    def load_contacts(self):
        if os.path.exists("contacts.json"):
            with open("contacts.json", "r") as file:
                return json.load(file)
        return []

    def save_contacts(self):
        with open("contacts.json", "w") as file:
            json.dump(self.contacts, file)

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for contact in self.contacts:
            self.listbox.insert(tk.END, contact['name'])

    def validate_phone(self, phone):
        return phone.isdigit() and len(phone) == 10

    def validate_email(self, email):
        return "@" in email

    def add_contact(self):
        name = simpledialog.askstring("Input", "Enter Name:", parent=self.root)
        if name:
            phone = simpledialog.askstring("Input", "Enter Phone Number:", parent=self.root)
            if not self.validate_phone(phone):
                messagebox.showerror("Error", "Phone number must be 10 digits.", parent=self.root)
                return

            email = simpledialog.askstring("Input", "Enter Email Address:", parent=self.root)
            if not self.validate_email(email):
                messagebox.showerror("Error", "Email must contain '@' symbol.", parent=self.root)
                return

            self.contacts.append({"name": name, "phone": phone, "email": email})
            self.save_contacts()
            self.update_listbox()

    def edit_contact(self):
        selected_index = self.listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Warning", "No contact selected!", parent=self.root)
            return

        index = selected_index[0]
        contact = self.contacts[index]

        new_name = simpledialog.askstring("Input", "Edit Name:", initialvalue=contact['name'], parent=self.root)
        new_phone = simpledialog.askstring("Input", "Edit Phone Number:", initialvalue=contact['phone'],
                                           parent=self.root)
        if not self.validate_phone(new_phone):
            messagebox.showerror("Error", "Phone number must be 10 digits.", parent=self.root)
            return

        new_email = simpledialog.askstring("Input", "Edit Email Address:", initialvalue=contact['email'],
                                           parent=self.root)
        if not self.validate_email(new_email):
            messagebox.showerror("Error", "Email must contain '@' symbol.", parent=self.root)
            return

        self.contacts[index] = {"name": new_name, "phone": new_phone, "email": new_email}
        self.save_contacts()
        self.update_listbox()

    def delete_contact(self):
        selected_index = self.listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Warning", "No contact selected!", parent=self.root)
            return

        index = selected_index[0]
        del self.contacts[index]
        self.save_contacts()
        self.update_listbox()


if __name__ == "__main__":
    root = tk.Tk()
    app = ContactManager(root)
    root.mainloop()
