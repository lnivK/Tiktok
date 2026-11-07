# app.py
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox
from comment import run_comment_client
from gift import run_gift_client

class TikTokApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Modular TikTok Live Dashboard")
        self.root.geometry("900x500")

        self.total_gifts = 0
        self.total_diamonds = 0

        # Simple UI setup
        top_frame = tk.Frame(root, pady=10)
        top_frame.pack(fill=tk.X, padx=10)

        tk.Label(top_frame, text="Username:", font=("Arial", 10, "bold")).pack(side=tk.LEFT)
        self.username_entry = tk.Entry(top_frame, font=("Arial", 10), width=20)
        self.username_entry.pack(side=tk.LEFT, padx=5)

        self.connect_btn = tk.Button(top_frame, text="Start Tracking", bg="green", fg="white", command=self.start_app)
        self.connect_btn.pack(side=tk.LEFT, padx=10)

        # Text display boxes
        body_frame = tk.Frame(root)
        body_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.comment_box = scrolledtext.ScrolledText(body_frame, width=50, bg="#1e1e1e", fg="#00ffcc")
        self.comment_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        self.gift_box = scrolledtext.ScrolledText(body_frame, width=50, bg="#1e1e1e", fg="#ff99ff")
        self.gift_box.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

    def log_comment(self, text):
        self.comment_box.insert(tk.END, text + "\n")
        self.comment_box.see(tk.END)

    def log_gift(self, text):
        self.gift_box.insert(tk.END, text + "\n")
        self.gift_box.see(tk.END)

    def update_stats(self, gift_count, diamond_count):
        self.total_gifts += gift_count
        self.total_diamonds += diamond_count
        print(f"Stats Updated -> Gifts: {self.total_gifts}, Diamonds: {self.total_diamonds}")

    def start_app(self):
        target = self.username_entry.get().strip()
        if not target:
            messagebox.showerror("Error", "Enter a username!")
            return

        # Run comment script in background thread
        threading.Thread(
            target=lambda: run_comment_client(target, lambda msg: self.root.after(0, lambda: self.log_comment(msg))),
            daemon=True
        ).start()

        # Run gift script in background thread
        threading.Thread(
            target=lambda: run_gift_client(
                target, 
                lambda msg: self.root.after(0, lambda: self.log_gift(msg)),
                lambda g, d: self.root.after(0, lambda: self.update_stats(g, d))
            ),
            daemon=True
        ).start()

        self.connect_btn.config(state=tk.DISABLED, text="Running...")

if __name__ == "__main__":
    root = tk.Tk()
    app = TikTokApp(root)
    root.mainloop()