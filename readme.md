# Concurrent File Server with Web Dashboard

## Overview
This project implements a **Concurrent File Server** using **Python Socket Programming**, **Threading**, and a **Flask-based Web Dashboard**. It serves multiple clients simultaneously by spawning a separate thread for each incoming file request. The Web Dashboard provides real-time information about connected clients, active threads, available files, and server logs.

---

## Features
- **Multi-threaded Concurrent File Server**
- **TCP Connection-Oriented Communication**
- **1000-byte chunk transfer with 200ms delay**
- **Real-time Web Dashboard (Flask)**
- **Active Threads Counter**
- **Connected Clients Monitor**
- **File List Viewer**
- **Download Request Monitoring**
- **Clean Modular Professional Folder Structure**

---

## Folder Structure (Professional)
```
project/
 ├── app/
 │    ├── server/
 │    │      └── file_server.py
 │    ├── web/
 │    │      ├── routes.py
 │    │      ├── templates/
 │    │      │      └── dashboard.html
 │    │      └── static/
 │    │             ├── style.css
 │    └── utils/
 │           └── logger.py
 ├── files/        # Folder containing downloadable files
 ├── run.py        # Starts both server & web dashboard
 └── README.md
```

---

## Working Mechanism
### **1. Client–Server Architecture**
The client sends the **filename** to the server via a TCP connection. The server accepts the request and spawns a **dedicated thread** for that specific client.

### **2. Thread Responsibilities**
Each server thread handles exactly one job:
1. Open the requested file
2. Read in 1000-byte chunks
3. Send each chunk through the socket
4. Sleep for **200 milliseconds** after each flush

### **3. Why 1000-Byte Chunks?**
- Optimizes network transfer
- Avoids overloading buffer
- Ensures smooth real-time transmission

### **4. Why 200ms Delay?**
- Simulates real-world rate-limited servers
- Helps analyze throughput
- Demonstrates controlled streaming

### **5. Web Dashboard**
The Flask dashboard displays:
- Active threads
- Live logs
- Available files
- Connected clients

---

## Technologies Used
### **Backend**
- Python 3.x
- Flask
- Socket
- Threading

### **Frontend**
- HTML5
- CSS3
- Bootstrap (optional for UI enhancement)
- AJAX for real-time logs

---

## How to Run
### **1. Install Requirements**
```
pip install flask
```

### **2. Start the System**
```
python run.py
```

### **3. Open Dashboard**
```
http://127.0.0.1:5000
```

---

## Conclusion
This professionally structured project demonstrates:
- Real concurrent processing
- Thread-based parallelism
- Clean separation of concerns
- Web-based monitoring system

It is ideal for:
- Computer Networks assignments
- Practical demonstration of client-server models
- Showcasing multithreading concepts

---

