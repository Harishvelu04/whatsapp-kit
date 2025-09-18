import pywhatkit
import datetime
import time
import tkinter as tk
from tkinter import messagebox
import webbrowser  # ✅ Added for opening WhatsApp Web

def log_message(phone_no, message, method):
    with open("sent_messages.txt", "a") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {method} | {phone_no} | {message}\n")

def send_scheduled_message():
    phone_no = phone_entry.get().strip()
    message = msg_entry.get().strip()
    hour = hour_entry.get().strip()
    minute = min_entry.get().strip()

    try:
        if hour and minute:
            send_hour = int(hour)
            send_min = int(minute)
        else:
            now = datetime.datetime.now()
            send_hour = now.hour
            send_min = now.minute + 1
            if send_min >= 60:
                send_hour = (send_hour + (send_min // 60)) % 24
                send_min = send_min % 60

        pywhatkit.sendwhatmsg(phone_no, message, send_hour, send_min)
        log_message(phone_no, message, f"Scheduled {send_hour:02d}:{send_min:02d}")
        messagebox.showinfo("✅ Success", f"Message scheduled for {send_hour:02d}:{send_min:02d}")
    except Exception as e:
        messagebox.showerror("❌ Error", f"Scheduling failed: {e}")

def send_instant_message():
    phone_no = phone_entry.get().strip()
    message = msg_entry.get().strip()

    try:
        pywhatkit.sendwhatmsg_instantly(phone_no, message, wait_time=10, tab_close=True)
        log_message(phone_no, message, "Instant")
        messagebox.showinfo("✅ Success", "Message sent instantly!")
    except Exception as e:
        messagebox.showerror("❌ Error", f"Instant send failed: {e}")

def send_multiple_messages():
    phone_no = phone_entry.get().strip()
    message = msg_entry.get().strip()

    try:
        for i in range(3):
            pywhatkit.sendwhatmsg_instantly(phone_no, f"{message} ({i+1})", wait_time=10, tab_close=True)
            log_message(phone_no, f"{message} ({i+1})", f"Multi {i+1}")
            time.sleep(10)
        messagebox.showinfo("✅ Success", "All messages sent!")
    except Exception as e:
        messagebox.showerror("❌ Error", f"Multiple send failed: {e}")

# ✅ New function to open WhatsApp Web for QR login
def open_whatsapp_web():
    try:
        webbrowser.open("https://web.whatsapp.com")
        messagebox.showinfo("🔓 Scan QR", "WhatsApp Web opened. Please scan the QR code to log in.")
    except Exception as e:
        messagebox.showerror("❌ Error", f"Could not open WhatsApp Web: {e}")

# GUI setup
root = tk.Tk()
root.title("💬 WhatsApp Automation Tool")
root.geometry("450x450")
root.config(bg="#2c3e50")

# Fonts
font_label = ("Helvetica", 12, "bold")
font_entry = ("Helvetica", 12)
font_btn = ("Helvetica", 12, "bold")

# Title
tk.Label(root, text="WhatsApp Automation Tool", font=("Helvetica", 16, "bold"), bg="#34495e", fg="white", pady=10).pack(fill="x")

# Form frame
form_frame = tk.Frame(root, bg="#2c3e50")
form_frame.pack(pady=20)

tk.Label(form_frame, text="Phone (+country code):", font=font_label, bg="#2c3e50", fg="white").grid(row=0, column=0, sticky="e", pady=5, padx=5)
phone_entry = tk.Entry(form_frame, font=font_entry, width=25)
phone_entry.grid(row=0, column=1, pady=5, padx=5)

tk.Label(form_frame, text="Message:", font=font_label, bg="#2c3e50", fg="white").grid(row=1, column=0, sticky="e", pady=5, padx=5)
msg_entry = tk.Entry(form_frame, font=font_entry, width=25)
msg_entry.grid(row=1, column=1, pady=5, padx=5)

tk.Label(form_frame, text="Hour (24h):", font=font_label, bg="#2c3e50", fg="white").grid(row=2, column=0, sticky="e", pady=5, padx=5)
hour_entry = tk.Entry(form_frame, font=font_entry, width=5)
hour_entry.grid(row=2, column=1, sticky="w", pady=5, padx=5)

tk.Label(form_frame, text="Minute:", font=font_label, bg="#2c3e50", fg="white").grid(row=3, column=0, sticky="e", pady=5, padx=5)
min_entry = tk.Entry(form_frame, font=font_entry, width=5)
min_entry.grid(row=3, column=1, sticky="w", pady=5, padx=5)

# Buttons frame
btn_frame = tk.Frame(root, bg="#2c3e50")
btn_frame.pack(pady=10)

btn_style = {
    "font": font_btn,
    "fg": "white",
    "width": 30,
    "padx": 5,
    "pady": 5
}

# ✅ New button for QR login
tk.Button(btn_frame, text="🔓 Login to WhatsApp", bg="#f39c12", command=open_whatsapp_web, **btn_style).pack(pady=5)
tk.Button(btn_frame, text="📌 Schedule (or custom time)", bg="#27ae60", command=send_scheduled_message, **btn_style).pack(pady=5)
tk.Button(btn_frame, text="⚡ Send Instantly", bg="#2980b9", command=send_instant_message, **btn_style).pack(pady=5)
tk.Button(btn_frame, text="🔁 Send 3 Messages (10 sec apart)", bg="#c0392b", command=send_multiple_messages, **btn_style).pack(pady=5)

root.mainloop()
