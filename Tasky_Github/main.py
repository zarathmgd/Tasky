import customtkinter as ctk
from tkinter import messagebox
import database

# Thème
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class TaskyApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configuration de la fenêtre
        self.title("Tasky")
        self.geometry("400x500")
        
        # Initialisation de la BDD
        database.init_bd()
        
        # ID de l'utilisateur connecté
        self.current_user_id = None
        
        # Page de connexion
        self.show_login()

    def clear_screen(self):
        """Efface tout le contenu de la fenêtre pour changer de page."""
        for widget in self.winfo_children():
            widget.destroy()

    # ==========================================
    # PAGE 1 : CONNEXION (LOGIN)
    # ==========================================
    def show_login(self):
        self.clear_screen()
        
        ctk.CTkLabel(self, text="Tasky - Login", font=("Arial", 24, "bold")).pack(pady=40)

        self.entry_pseudo = ctk.CTkEntry(self, placeholder_text="Pseudo")
        self.entry_pseudo.pack(pady=10)

        self.entry_pass = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.entry_pass.pack(pady=10)

        # Bouton Connexion appelle la fonction verify_login
        ctk.CTkButton(self, text="Login", command=self.verify_login).pack(pady=10)
        
        # Bouton Inscription appelle show_register
        ctk.CTkButton(self, text="Sign in", fg_color="transparent", border_width=1, command=self.show_register).pack(pady=10)

    def verify_login(self):
        pseudo = self.entry_pseudo.get()
        password = self.entry_pass.get()
        
        user_id = database.login_check(pseudo, password)
        
        if user_id:
            self.current_user_id = user_id
            self.show_tasks()
        else:
            messagebox.showerror("Error", "pseudo or password wrong.")

    # ==========================================
    # PAGE 2 : INSCRIPTION (SIGNIN)
    # ==========================================
    def show_register(self):
        self.clear_screen()
        
        ctk.CTkLabel(self, text="Tasky - Sign in", font=("Arial", 24, "bold")).pack(pady=40)

        self.entry_new_pseudo = ctk.CTkEntry(self, placeholder_text="Choose a pseudo")
        self.entry_new_pseudo.pack(pady=10)

        self.entry_new_pass = ctk.CTkEntry(self, placeholder_text="Choose a password", show="*")
        self.entry_new_pass.pack(pady=10)

        # Bouton Valider appelle register_user
        ctk.CTkButton(self, text="Confirm", fg_color="green", command=self.register_user).pack(pady=10)
        ctk.CTkButton(self, text="Return", fg_color="transparent", command=self.show_login).pack()

    def register_user(self):
        pseudo = self.entry_new_pseudo.get()
        password = self.entry_new_pass.get()
        
        if pseudo and password:
            success = database.user_signin(pseudo, password)
            if success:
                messagebox.showinfo("Success", "Account created ! Please log in.")
                self.show_login()
            else:
                messagebox.showerror("Error", "This pseudo is already used.")
        else:
            messagebox.showwarning("Warning", "Please fill in all fields.")

    # ==========================================
    # PAGE 3 : LISTE DES TÂCHES
    # ==========================================
    def show_tasks(self):
        self.clear_screen()
        
        ctk.CTkLabel(self, text="Tasky - My Tasks", font=("Arial", 20, "bold")).pack(pady=20)

        # Zone d'ajout 
        self.entry_task = ctk.CTkEntry(self, placeholder_text="New task...")
        self.entry_task.pack(pady=5)
        
        # Appel à add_new_task
        ctk.CTkButton(self, text="Add", command=self.add_new_task).pack(pady=5)
 
        self.scrollter = ctk.CTkScrollableFrame(self, width=300, height=300)
        self.scrollter.pack(pady=20)
        
        self.load_tasks_list()

    def add_new_task(self):
        title = self.entry_task.get()
        if title:
            database.add_task(title, self.current_user_id)
            self.entry_task.delete(0, 'end')
            self.load_tasks_list()

    def load_tasks_list(self):
        # Vider la zone d'affichage
        for widget in self.scrollter.winfo_children():
            widget.destroy()
            
        # Récupèrer les tâches (id, titre, statut)
        tasks = database.get_tasks(self.current_user_id)
        
        for t in tasks:
            task_id = t[0]
            title = t[1]
            status = t[2]
            
            # --- Ligne conteneur ---
            row_frame = ctk.CTkFrame(self.scrollter, fg_color="transparent")
            row_frame.pack(fill="x", pady=5)
            
            # --- Checkbox ---
            chk = ctk.CTkCheckBox(
                row_frame, 
                text=title, 
                command=lambda tid=task_id, st=status: self.toggle_status(tid, st)
            )
            chk.pack(side="left", padx=10)
            if status == 1: chk.select()
                
            # --- Bouton Supprimer (Rouge, à droite) ---
            btn_del = ctk.CTkButton(
                row_frame, 
                text="X", 
                width=30, 
                fg_color="#cc0000", 
                hover_color="#aa0000",
                command=lambda tid=task_id: self.delete_task_action(tid)
            )
            btn_del.pack(side="right", padx=5)

            # --- Bouton Modifier (Bleu, à côté de Supprimer) ---
            btn_edit = ctk.CTkButton(
                row_frame, 
                text="✎",  # Symbole crayon
                width=30, 
                fg_color="#1f6aa5", # Bleu standard
                command=lambda tid=task_id: self.edit_task_action(tid)
            )
            btn_edit.pack(side="right", padx=5)


    # Éditer (Ouvre une pop-up)
    def edit_task_action(self, task_id):
        # Boîte de dialogue
        dialog = ctk.CTkInputDialog(text="New title :", title="Edit task")
        
        # Le programme attend que l'utilisateur clique sur OK
        new_title = dialog.get_input()
        
        # Si l'utilisateur a écrit quelque chose (et pas cliqué sur Annuler)
        if new_title:
            database.update_task_title(task_id, new_title)
            self.load_tasks_list()

    # Changer le statut
    def toggle_status(self, task_id, current_status):
        # Si c'était 0, ça devient 1. Si c'était 1, ça devient 0.
        new_status = 1 if current_status == 0 else 0
        database.update_task_status(task_id, new_status)
        # Recharger la liste pour que l'affichage soit synchro
        self.load_tasks_list()

    # Supprimer
    def delete_task_action(self, task_id):
        database.delete_task(task_id)
        self.load_tasks_list()

if __name__ == "__main__":
    app = TaskyApp()
    app.mainloop()