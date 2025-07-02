# 🐚 Backdoor (Reverse Shell)

## 🔍 Overview

This project implements a **custom reverse shell** that allows remote control of a target machine through an encrypted TCP connection. The shell connects from the victim machine (client) to the attacker's machine (C2 server) and enables the attacker to run shell commands, navigate directories, and upload/download files using Base64 encoding.

⚠️ This project is for **educational and ethical use only**. It is designed to help learners understand how reverse shells work in penetration testing and red teaming scenarios.

---

## 💡 Features

- 🔁 **Persistent reverse connection** to the C2 server
- 🖥️ **Remote shell command execution** (e.g., `ls`, `whoami`, `cd`)
- 📂 **Directory navigation** (`cd` command with path tracking)
- ⬆️ **File upload/download** via Base64 encoding
- 💥 **Robust error handling** and `try/except` safety
- 🔌 **Automatic reconnection** if server is temporarily down

---

## ⚙️ Technologies Used

- Python 3.x
- `socket` – for client-server communication
- `subprocess` – to execute OS-level commands
- `os`, `base64`, `time` – for file handling, encoding, and reconnection logic



