# app.py
import threading
import os
import sys
import time
import tkinter as tk
from tkinter import messagebox, scrolledtext
from comment import run_comment_client
from gift import run_gift_client
from viewer import viewer
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class TikTokApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TikTok Live Dashboard | Created by lnivK")
        self.root.geometry("620x780")
        self.root.resizable(False, False)
        
        try:
            self.root.iconbitmap(resource_path("web.ico"))
        except Exception:
            pass

        self.total_gifts = 0
        self.total_diamonds = 0
        self.total_likes = 0
        self.is_running = False
        self.session_id = 0

        # ==========================================
        # TOP FRAME: Target Username, Connect & Disconnect
        # ==========================================
        top_frame = tk.Frame(root, pady=6)
        top_frame.pack(fill=tk.X, padx=10)

        tk.Label(top_frame, text="TARGET:", font=("Arial", 9, "bold")).pack(side=tk.LEFT)
        self.username_entry = tk.Entry(top_frame, font=("Arial", 9), width=15)
        self.username_entry.pack(side=tk.LEFT, padx=5)

        self.connect_btn = tk.Button(top_frame, text="Connect", bg="green", fg="white", font=("Arial", 8, "bold"), command=self.start_app)
        self.connect_btn.pack(side=tk.LEFT, padx=3)

        self.disconnect_btn = tk.Button(top_frame, text="Disconnect", bg="red", fg="white", font=("Arial", 8, "bold"), state=tk.DISABLED, command=self.stop_app)
        self.disconnect_btn.pack(side=tk.LEFT, padx=3)

        # ==========================================
        # STATS ROW: Single Row (Side-by-Side Cards)
        # ==========================================
        stats_main_frame = tk.Frame(root, padx=10, pady=4)
        stats_main_frame.pack(fill=tk.X)

        def create_row_stat_card(parent, title_text, text_color):
            card = tk.Frame(parent, bd=1, relief=tk.SOLID, pady=6, padx=8)
            card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2)
            
            lbl_title = tk.Label(card, text=title_text, font=("Arial", 9, "bold"))
            lbl_title.pack(side=tk.LEFT)
            
            lbl_value = tk.Label(card, text="0", font=("Consolas", 10, "bold"), fg=text_color)
            lbl_value.pack(side=tk.RIGHT)
            
            return lbl_value

        self.viewer_count_label = create_row_stat_card(stats_main_frame, "viewer:", "#008866")
        self.like_count_label = create_row_stat_card(stats_main_frame, "likes:", "#006699")
        self.total_gift_label = create_row_stat_card(stats_main_frame, "diamond:", "#990099")

        # ==========================================
        # MIDDLE ROW: Top Viewers Vertical Box
        # ==========================================
        top_viewers_frame = tk.Frame(root, padx=10, pady=4)
        top_viewers_frame.pack(fill=tk.X)

        top_container = tk.LabelFrame(top_viewers_frame, text=" top viewers ", font=("Arial", 9, "bold"), fg="#00ccff")
        top_container.pack(fill=tk.X)

        # ScrolledText box so it can list many viewers vertically with scroll support
        self.top_viewers_box = scrolledtext.ScrolledText(top_container, height=6, bg="#1e1e1e", fg="#00ccff", font=("Consolas", 9))
        self.top_viewers_box.pack(fill=tk.BOTH, expand=True)

        # ==========================================
        # BOTTOM ROW: Chat & Gift Feeds (Side-by-Side)
        # ==========================================
        bottom_frame = tk.Frame(root)
        bottom_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(5, 5))

        # Chat Box (Left)
        chat_container = tk.LabelFrame(bottom_frame, text=" chat ", font=("Arial", 9, "bold"), fg="#00aa88")
        chat_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 3))
        
        self.comment_box = scrolledtext.ScrolledText(chat_container, height=12, width=24, bg="#1e1e1e", fg="#00ffcc", font=("Consolas", 9))
        self.comment_box.pack(fill=tk.BOTH, expand=True)

        # Gift Box (Right)
        gift_container = tk.LabelFrame(bottom_frame, text=" gift feed ", font=("Arial", 9, "bold"), fg="#aa00aa")
        gift_container.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(3, 0))
        
        self.gift_box = scrolledtext.ScrolledText(gift_container, height=12, width=24, bg="#1e1e1e", fg="#ff99ff", font=("Consolas", 9))
        self.gift_box.pack(fill=tk.BOTH, expand=True)

        # ==========================================
        # FOOTER FRAME: Bottom Status & Credit Bar
        # ==========================================
        footer_frame = tk.Frame(root, bd=1, relief=tk.SUNKEN, pady=3)
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.footer_label = tk.Label(footer_frame, text="Status: Disconnected", font=("Arial", 8), fg="#666666")
        self.footer_label.pack(side=tk.LEFT, padx=10)

        credit_label = tk.Label(footer_frame, text="Created by lnivK with AI", font=("Arial", 8, "italic"), fg="#888888")
        credit_label.pack(side=tk.RIGHT, padx=10)

    def safe_log_comment(self, session, text):
        if session == self.session_id and self.is_running:
            self.comment_box.insert(tk.END, text + "\n")
            self.comment_box.see(tk.END)

    def safe_log_gift(self, session, text):
        if session == self.session_id and self.is_running:
            self.gift_box.insert(tk.END, text + "\n")
            self.gift_box.see(tk.END)

    def safe_update_viewer_count(self, session, count):
        if session == self.session_id and self.is_running:
            self.viewer_count_label.config(text=str(count))

    def safe_update_likes(self, session, like_count):
        if session == self.session_id and self.is_running:
            self.total_likes += like_count
            self.like_count_label.config(text=str(self.total_likes))

    def safe_update_stats(self, session, gift_count, diamond_count):
        if session == self.session_id and self.is_running:
            self.total_gifts += gift_count
            self.total_diamonds += diamond_count
            self.total_gift_label.config(text=str(self.total_diamonds))

    def safe_update_top_viewers(self, session, names):
        if session == self.session_id and self.is_running:
            self.top_viewers_box.delete("1.0", tk.END)
            if names:
                for idx, name in enumerate(names, start=1):
                    self.top_viewers_box.insert(tk.END, f"{idx}. {name}\n")
            else:
                self.top_viewers_box.insert(tk.END, "No top viewers listed yet\n")
            self.top_viewers_box.see(tk.END)

    def start_app(self):
        target = self.username_entry.get().strip()
        if not target:
            messagebox.showerror("Error", "Enter a target username!")
            return

        self.session_id += 1
        current_session = self.session_id

        self.is_running = True
        self.total_gifts = 0
        self.total_diamonds = 0
        self.total_likes = 0
        
        self.viewer_count_label.config(text="...")
        self.like_count_label.config(text="0")
        self.total_gift_label.config(text="0")
        
        self.top_viewers_box.delete("1.0", tk.END)
        self.top_viewers_box.insert(tk.END, "Connecting...\n")
        
        self.comment_box.delete("1.0", tk.END)
        self.gift_box.delete("1.0", tk.END)

        self.connect_btn.config(state=tk.DISABLED)
        self.disconnect_btn.config(state=tk.NORMAL)
        self.username_entry.config(state=tk.DISABLED)
        
        self.footer_label.config(text=f"Status: Connected to @{target}", fg="#008800")

        # 1. Comment stream thread
        threading.Thread(
            target=lambda: run_comment_client(target, lambda msg: self.root.after(0, lambda: self.safe_log_comment(current_session, msg))),
            daemon=True
        ).start()
        time.sleep(1)

        # 2. Gift stream thread
        threading.Thread(
            target=lambda: run_gift_client(
                target, 
                lambda msg: self.root.after(0, lambda: self.safe_log_gift(current_session, msg)),
                lambda g, d: self.root.after(0, lambda: self.safe_update_stats(current_session, g, d))
            ),
            daemon=True
        ).start()
        time.sleep(1)

        # 3. Viewer, Likes & Top Viewers stream thread
        threading.Thread(
            target=lambda: viewer(
                target, 
                lambda count: self.root.after(0, lambda: self.safe_update_viewer_count(current_session, count)),
                lambda likes: self.root.after(0, lambda: self.safe_update_likes(current_session, likes)),
                lambda names: self.root.after(0, lambda: self.safe_update_top_viewers(current_session, names))
            ),
            daemon=True
        ).start()

    def stop_app(self):
        self.is_running = False
        self.session_id += 1

        self.connect_btn.config(state=tk.NORMAL)
        self.disconnect_btn.config(state=tk.DISABLED)
        self.username_entry.config(state=tk.NORMAL)
        
        self.viewer_count_label.config(text="0")
        self.like_count_label.config(text="0")
        self.total_gift_label.config(text="0")
        
        self.top_viewers_box.delete("1.0", tk.END)
        self.top_viewers_box.insert(tk.END, "Disconnected\n")
        
        self.comment_box.insert(tk.END, "--- Disconnected ---\n")
        self.gift_box.insert(tk.END, "--- Disconnected ---\n")
        
        self.footer_label.config(text="Status: Disconnected", fg="#666666")

if __name__ == "__main__":
    root = tk.Tk()
    app = TikTokApp(root)
    root.mainloop()