import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
from lsb_utils import lsb_encode
from edge_utils import detect_edges, edge_embed
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
import base64, os

def encrypt_and_embed():
    img_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")])
    if not img_path:
        return
    msg, pw = msg_entry.get(), pw_entry.get()
    if not msg or not pw:
        return messagebox.showerror("Error", "Enter both message and password.")

    img = Image.open(img_path).convert("RGB")
    key = PBKDF2(pw, b'stego_salt', dkLen=32)
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(msg.encode())
    payload = cipher.nonce + ciphertext + tag
    b64 = base64.b64encode(payload).decode()
    length_header = f"{len(b64):08d}"
    full = length_header + b64

    mid = len(full) // 2
    part1, part2 = full[:mid], full[mid:]

    img2 = lsb_encode(img, part1)
    stego = edge_embed(img2, part2, detect_edges(img_path))
    out = os.path.splitext(os.path.basename(img_path))[0] + "_stego.png"
    stego.save(out)
    messagebox.showinfo("Success", f"Stego image saved as:\n{out}")

root = tk.Tk()
root.title("Encrypt & Embed")
tk.Label(root, text="Secret Message:").pack()
msg_entry = tk.Entry(root, width=60); msg_entry.pack(pady=5)
tk.Label(root, text="Password:").pack()
pw_entry = tk.Entry(root, show="*", width=60); pw_entry.pack(pady=5)
tk.Button(root, text="Encrypt & Embed", command=encrypt_and_embed).pack(pady=15)
root.mainloop()
