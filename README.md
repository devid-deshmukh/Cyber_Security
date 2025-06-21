# Cyber-Security

Final Project of **IBM Edunet Cybersecurity Internship**

## 📌 Project Title

**Steganography – Hiding Text Under Image**

## 📝 Overview

This project was developed as part of the IBM Edunet Foundation Cybersecurity internship (6 weeks). The goal is to build a steganography system that securely hides encrypted text messages within digital images. The tool ensures hidden data remains undetectable to unauthorized users while maintaining image quality.

---

## 📂 Repository Name

**Cyber-Security**

### 📄 Files in the Repository

- `encryption.py` — Script for encoding secret messages into images
- `decryption.py` — Script for decoding hidden messages from images
- `Cyber-Security-Steganography.pptx` — PowerPoint presentation detailing the project
- `encryptedImage.jpg` — Sample encrypted image with a hidden message

---

## ⚙️ System Requirements

- **OS**: Windows 10 or later
- **Processor**: Dual-core or higher
- **RAM**: At least 4GB
- **Python**: 3.9 or newer

---

## 📚 Libraries Used

- `Tkinter` — GUI (built-in with Python)
- `Pillow` — Image handling
- `PyCryptodome` — AES-EAX encryption/decryption
- `Numpy` — Pixel data handling
- `OpenCV` _(optional)_ — Edge detection
- `Base64` — Encoding and decoding

---

## ⚡ How to Use

### Encryption

1️⃣ Ensure `encryption.py` is in the same directory as your input image.  
2️⃣ Run:

````bash
python encryption.py
3️⃣ Enter your secret message and password when prompted.
4️⃣ The tool generates encryptedImage.jpg with the hidden message.

Decryption
1️⃣ Ensure decryption.py is in the same directory as your encrypted image.
2️⃣ Run:
python decryption.py
3️⃣ Enter your password when prompted.
4️⃣ The tool displays the hidden message if the password is correct.

🚀 Deployment
Developed in Python using Tkinter, Pillow, PyCryptodome

Standalone desktop tool

Supports PNG, JPEG, BMP, GIF

📚 References
Pillow Documentation

PyCryptodome

Johnson & Jajodia (1998). Exploring Steganography: Seeing the Unseen

Daemen & Rijmen (2001). The Design of AES

Fridrich (2009). Steganography in Digital Images

## 📥 Cloning the Repository

To clone this repository to your local machine, run:

```bash
git clone https://github.com/devid-deshmukh/Cyber_Security.git
cd Cyber_Security


````
