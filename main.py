import tkinter as tk
import webbrowser
from tkinter import messagebox

# ================= DATABASE =================

from db_manager import (
    create_table,
    register_user,
    login_user,
    update_password,
    get_password
)

create_table()

# ================= CONTENT =================

from content_manager import get_topics, get_resources


# ================= THEME =================

BG_COLOR = "#F4F6F8"
CARD_COLOR = "white"
PRIMARY = "#4A90E2"
SUCCESS = "#50C878"
TEXT = "#333333"
BTN_HOVER = "#357ABD"

FONT_TITLE = ("Segoe UI", 20, "bold")
FONT_TEXT = ("Segoe UI", 11)
FONT_BTN = ("Segoe UI", 11, "bold")


# ================= ROOT =================

root = tk.Tk()
root.title("Python Learning Portal")
root.geometry("900x650")
root.resizable(True, True)
root.configure(bg=BG_COLOR)


# ================= GLOBAL =================

current_user = ""
current_semester = ""


# ================= HELPERS =================

def clear():
    for w in root.winfo_children():
        w.destroy()


def open_link(url):
    webbrowser.open(url)


def create_card():

    clear()

    main = tk.Frame(root, bg=BG_COLOR)
    main.pack(fill="both", expand=True)

    card = tk.Frame(
        main,
        bg=CARD_COLOR,
        padx=170,
        pady=200
    )

    card.place(relx=0.5, rely=0.5, anchor="center")

    return card


def create_button(parent, text, command, color=PRIMARY):

    btn = tk.Button(
        parent,
        text=text,
        font=FONT_BTN,
        bg=color,
        fg="white",
        width=22,
        height=2,
        bd=0,
        cursor="hand2",
        command=command
    )

    btn.bind("<Enter>", lambda e: btn.config(bg=BTN_HOVER))
    btn.bind("<Leave>", lambda e: btn.config(bg=color))

    return btn


# ================= HOME =================

def home_page():

    card = create_card()

    tk.Label(
        card,
        text="Python Learning Portal",
        font=FONT_TITLE,
        bg=CARD_COLOR,
        fg=PRIMARY
    ).pack(pady=20)

    create_button(card, "Login", login_page).pack(pady=10)

    create_button(card, "Register", register_page, SUCCESS).pack(pady=10)


# ================= LOGIN =================

def login_page():

    card = create_card()

    tk.Label(
        card,
        text="Student Login",
        font=FONT_TITLE,
        bg=CARD_COLOR,
        fg=PRIMARY
    ).pack(pady=20)

    tk.Label(card, text="Username", bg=CARD_COLOR, fg=TEXT).pack(anchor="w")

    u_entry = tk.Entry(card, width=30, font=FONT_TEXT)
    u_entry.pack(pady=5)

    tk.Label(card, text="Password", bg=CARD_COLOR, fg=TEXT).pack(anchor="w")

    p_entry = tk.Entry(card, width=30, show="*", font=FONT_TEXT)
    p_entry.pack(pady=5)

    create_button(
        card,
        "Login",
        lambda: do_login(u_entry, p_entry)
    ).pack(pady=15)

    create_button(
        card,
        "Register",
        register_page,
        SUCCESS
    ).pack(pady=5)

    tk.Button(
        card,
        text="Change Password",
        bg=CARD_COLOR,
        fg=PRIMARY,
        bd=0,
        cursor="hand2",
        command=change_password_page
    ).pack(pady=10)


def do_login(u_entry, p_entry):

    global current_user

    u = u_entry.get().strip()
    p = p_entry.get().strip()

    if not u or not p:
        messagebox.showerror("Error", "All fields required")
        return

    result = login_user(u, p)

    if result == "no_user":
        messagebox.showerror("Error", "Username not found")

    elif result == "wrong_pass":
        messagebox.showerror("Error", "Wrong password")

    else:
        current_user = u
        student_dashboard()


# ================= REGISTER =================

def register_page():

    card = create_card()

    tk.Label(
        card,
        text="Student Registration",
        font=FONT_TITLE,
        bg=CARD_COLOR,
        fg=PRIMARY
    ).pack(pady=20)

    tk.Label(card, text="Username", bg=CARD_COLOR).pack()

    u_entry = tk.Entry(card, width=30)
    u_entry.pack(pady=5)

    tk.Label(card, text="Password", bg=CARD_COLOR).pack()

    p_entry = tk.Entry(card, show="*", width=30)
    p_entry.pack(pady=5)

    tk.Label(card, text="Confirm Password", bg=CARD_COLOR).pack()

    c_entry = tk.Entry(card, show="*", width=30)
    c_entry.pack(pady=5)

    create_button(
        card,
        "Register",
        lambda: do_register(u_entry, p_entry, c_entry)
    ).pack(pady=15)

    create_button(
        card,
        "Back",
        home_page,
        "#888"
    ).pack(pady=10)


def do_register(u_entry, p_entry, c_entry):

    u = u_entry.get().strip()
    p = p_entry.get().strip()
    c = c_entry.get().strip()

    if not u or not p or not c:
        messagebox.showerror("Error", "All fields required")
        return

    if p != c:
        messagebox.showerror("Error", "Passwords do not match")
        return

    if register_user(u, p):
        messagebox.showinfo("Success", "Registration Successful")
        login_page()
    else:
        messagebox.showerror("Error", "Username already exists")


# ================= PASSWORD =================

def change_password_page():

    card = create_card()

    tk.Label(
        card,
        text="Change Password",
        font=FONT_TITLE,
        bg=CARD_COLOR,
        fg=PRIMARY
    ).pack(pady=20)

    tk.Label(card, text="Username", bg=CARD_COLOR).pack()

    u_entry = tk.Entry(card, width=30)
    u_entry.pack(pady=5)

    tk.Label(card, text="Old Password", bg=CARD_COLOR).pack()

    old_p = tk.Entry(card, show="*", width=30)
    old_p.pack(pady=5)

    tk.Label(card, text="New Password", bg=CARD_COLOR).pack()

    new_p = tk.Entry(card, show="*", width=30)
    new_p.pack(pady=5)

    create_button(
        card,
        "Update Password",
        lambda: do_update(u_entry, old_p, new_p),
        "#FF9800"
    ).pack(pady=15)

    create_button(
        card,
        "Back",
        login_page,
        "#888"
    ).pack(pady=10)


def do_update(u_entry, old_p, new_p):

    u = u_entry.get().strip()
    old = old_p.get().strip()
    new = new_p.get().strip()

    result = login_user(u, old)

    if result != "success":
        messagebox.showerror("Error", "Invalid credentials")
        return

    update_password(u, new)

    messagebox.showinfo("Success", "Password Updated")
    login_page()


# ================= DASHBOARD =================

def student_dashboard():

    card = create_card()

    tk.Label(
        card,
        text=f"Welcome, {current_user}",
        font=FONT_TITLE,
        bg=CARD_COLOR,
        fg=PRIMARY
    ).pack(pady=20)

    create_button(
        card,
        "Semester 1",
        lambda: show_topics("Semester 1")
    ).pack(pady=10)

    create_button(
        card,
        "Semester 2",
        lambda: show_topics("Semester 2")
    ).pack(pady=10)

    create_button(
        card,
        "Logout",
        home_page,
        "#e74c3c"
    ).pack(pady=30)


# ================= TOPICS =================

def show_topics(semester):

    global current_semester
    current_semester = semester

    card = create_card()

    tk.Label(
        card,
        text=semester,
        font=FONT_TITLE,
        bg=CARD_COLOR,
        fg=PRIMARY
    ).pack(pady=10)

    main_frame = tk.Frame(card, bg=CARD_COLOR)
    main_frame.pack(fill="both", expand=True, pady=10)

    canvas = tk.Canvas(main_frame, bg=CARD_COLOR, highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    scroll_frame = tk.Frame(canvas, bg=CARD_COLOR)

    window = canvas.create_window((0, 0), window=scroll_frame, anchor="n")

    canvas.bind("<Configure>", lambda e: canvas.itemconfig(window, width=e.width))

    scroll_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.bind_all(
        "<MouseWheel>",
        lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units")
    )

    for t in get_topics(semester):

        tk.Button(
            scroll_frame,
            text=t,
            width=35,
            height=2,
            bg=SUCCESS,
            fg="white",
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 13, "bold"),
            command=lambda x=t: show_resources(x)
        ).pack(pady=6)

    create_button(
        card,
        "Back",
        student_dashboard,
        "#888"
    ).pack(pady=15)


# ================= RESOURCES =================

def show_resources(topic):

    card = create_card()

    tk.Label(
        card,
        text=topic,
        font=FONT_TITLE,
        bg=CARD_COLOR,
        fg=PRIMARY,
        wraplength=500
    ).pack(pady=10)

    websites, youtube = get_resources(topic)

    # ----------- WEBSITE SECTION -----------

    if websites:

        tk.Label(
            card,
            text="🌐 Website Links",
            font=("Segoe UI", 14, "bold"),
            bg=CARD_COLOR,
            fg=TEXT
        ).pack(pady=(10, 5))

        for link in websites:

            tk.Button(
                card,
                text=link,
                bg=PRIMARY,
                fg="white",
                wraplength=450,
                bd=0,
                cursor="hand2",
                font=FONT_TEXT,
                command=lambda l=link: open_link(l)
            ).pack(pady=3)

    # ----------- YOUTUBE SECTION -----------

    if youtube:

        tk.Label(
            card,
            text="▶ YouTube Videos",
            font=("Segoe UI", 14, "bold"),
            bg=CARD_COLOR,
            fg=TEXT
        ).pack(pady=(15, 5))

        for link in youtube:

            tk.Button(
                card,
                text=link,
                bg="#E53935",
                fg="white",
                wraplength=450,
                bd=0,
                cursor="hand2",
                font=FONT_TEXT,
                command=lambda l=link: open_link(l)
            ).pack(pady=3)

    # Back Button
    create_button(
        card,
        "Back",
        lambda: show_topics(current_semester),
        "#888"
    ).pack(pady=20)


# ================= START =================

home_page()

root.mainloop()

