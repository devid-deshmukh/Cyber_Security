import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
from lsb_utils import lsb_decode
from edge_utils import detect_edges, edge_decode
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
import base64, re, os

def clean_pad_b64(s):
    s = re.sub(r'[^A-Za-z0-9+/=]', '', s)
    return s + ('=' * ((4 - len(s) % 4) % 4))

def extract_and_decrypt():
    img_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")])
    if not img_path:
        return
    pw = pw_entry.get()
    if not pw:
        return messagebox.showerror("Error", "Enter password.")

    img = Image.open(img_path).convert("RGB")
    p1 = lsb_decode(img)
    p2 = edge_decode(img, detect_edges(img_path))
    full = p1 + p2

    if len(full) < 8:
        return messagebox.showerror("Error", "Data is corrupted or too small.")

    length = int(full[:8])
    b64 = full[8:]
    if len(b64) < length:
        return messagebox.showerror("Error", f"Incomplete data: got {len(b64)}/{length}")
    b64 = clean_pad_b64(b64[:length])

    try:
        payload = base64.b64decode(b64)
    except Exception as e:
        return messagebox.showerror("Error", f"Invalid Base64: {e}")

    key = PBKDF2(pw, b'stego_salt', dkLen=32)
    cipher = AES.new(key, AES.MODE_EAX, nonce=payload[:16])
    try:
        plaintext = cipher.decrypt_and_verify(payload[16:-16], payload[-16:])
        messagebox.showinfo("Hidden Message", plaintext.decode())
    except ValueError:
        messagebox.showerror("Error", "MAC failed: wrong password or corrupted data.")
    except Exception as e:
        messagebox.showerror("Error", f"Decryption failed: {repr(e)}")

root = tk.Tk()
root.title("Extract & Decrypt")
tk.Label(root, text="Password:").pack(pady=5)
pw_entry = tk.Entry(root, show="*", width=60); pw_entry.pack(pady=5)
tk.Button(root, text="Extract & Decrypt", command=extract_and_decrypt).pack(pady=15)
root.mainloop()
