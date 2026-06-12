# 📱 Wireless Barcode Scanner

**Turn your smartphone into a wireless barcode reader with instant PC integration!**

A powerful, open-source utility that transforms your Android or iPhone into a wireless barcode/QR code scanner. Scanned codes are instantly sent directly to any active application on your Windows PC—Excel spreadsheets, web browsers, text editors, and more.

---

## ✨ Features

- **🔄 Real-time Barcode Scanning**: Instantly capture barcodes and QR codes from your mobile device
- **💻 Direct PC Integration**: Codes are automatically inputted into active applications (Excel, browsers, etc.)
- **🔒 Secure Local Network**: Works on your local Wi-Fi—no cloud dependency, maximum privacy
- **🎯 Zero Configuration**: Simple setup, no complex installations
- **📵 No Ads, No Tracking**: Completely free and open-source
- **🌐 Cross-Browser Compatible**: Works with Chrome, Firefox, and other modern browsers
- **⚡ Fast & Responsive**: Low-latency real-time scanning

---

## 🛠️ System Requirements

### **Windows PC (Data Receiver)**
- **OS**: Windows 10 or Windows 11
- **Network**: Active Wi-Fi connection
- **Internet**: Active internet connection required
- **Python**: Python 3.7+ (required for running from source)

### **Smartphone (Data Sender)**
- **OS**: Android or iOS
- **Camera**: Working front or rear camera
- **Network**: Wi-Fi capability (must connect to same network as PC)
- **Browser**: Google Chrome or other modern web browser (Chrome recommended)

---

## 📦 Installation & Setup

### **Step 1️⃣: Download the PC Application**

1. Visit the [Releases](https://github.com/wgwohan/BarCode_Scanner/releases) section of this repository
2. Download the latest `gui_server.exe` file
3. Save it in a folder of your choice on your Windows PC

### **Step 2️⃣: Run the PC Software**

1. **Ensure your PC and mobile device are on the same local network** before proceeding
2. Double-click the `gui_server.exe` file
3. A **Windows Defender Firewall alert** may appear:
   - ✅ Check the box: "Private networks, such as my home or work network"
   - ✅ Click "Allow access"
4. The application window will open showing your **PC's IP address** (e.g., `192.168.1.100`)

📌 **Keep this window open while scanning!**

### **Step 3️⃣: Connect Mobile Device to Same Network**

If your PC and smartphone are already on the same Wi-Fi network, skip this step.

**Option A: Using Existing Wi-Fi**
- Connect your smartphone to the same Wi-Fi network as your PC

**Option B: Using Mobile Hotspot**
1. Open **Settings** → **Mobile Hotspot** on your Windows PC
2. Set a custom network name and password
3. Connect your phone to this hotspot

---

## 🚀 Using the Scanner

### **Method A: Using Chrome Flags (Recommended)**

This method allows direct camera access from your browser.

1. **On your smartphone**, open Google Chrome
2. Open a new tab and navigate to: `chrome://flags`
3. Search for **"Insecure origins treated as secure"**
4. Enable this flag
5. Enter your Windows PC IP address with port: `http://YOUR_PC_IP:8000`
   - Example: `http://192.168.1.100:8000`
6. Tap **"Relaunch"** to restart Chrome
7. Navigate to your PC's IP address in the address bar
8. The barcode scanner interface will load

### **Method B: Using Mobile HTML File (Alternative)**

1. Download the `scanner.html` file from the [Releases](https://github.com/wgwohan/BarCode_Scanner/releases)
2. Save it to your smartphone's local storage
3. Open the file using your file manager
4. Select **Google Chrome** to open it
5. Continue with the steps below

---

## 📖 How to Scan

1. **Enter PC IP Address**
   - Tap the "Change IP" button
   - Enter the IP address shown in your PC's application window
   - Status indicator should turn **green** showing "Connected to PC"

2. **Request Camera Permissions**
   - Tap "Request Camera Permissions"
   - Select "Allow while visiting the site" when prompted

3. **Start Scanning**
   - Your camera will activate
   - Align the barcode/QR code with the targeting reticle on your screen
   - The code will be automatically scanned and sent to your PC

4. **View Results**
   - Scanned codes instantly appear in your active PC application
   - Results are logged in the "Recent Scans" section

5. **Stop Scanning**
   - Tap "Stop Scanning" when finished

---

## ⚙️ Technical Details

### **Architecture**
- **Frontend**: HTML5 + JavaScript (QR code library: `html5-qrcode`)
- **Backend**: Python with WebSockets
- **Communication**: WebSocket protocol for real-time data transfer
- **Servers**: 
  - HTTP Server (Port 8000): Serves the web interface
  - WebSocket Server (Port 8765): Handles barcode data transmission

### **Key Components**
- `gui_server.py`: Main Python server application
- `gui_server.exe`: Compiled Windows executable
- `barcode_server.html`: Web interface for mobile scanning

---

## 🔧 Running from Source

If you prefer to run from source code:

### **Requirements**
```
Python 3.7+
websockets
pyautogui
```

### **Installation**
```bash
pip install websockets pyautogui
```

### **Run**
```bash
python gui_server.py
```

---

## ⚠️ Troubleshooting

### **Connection Failed**
- ❌ Check if PC and phone are on the **same network**
- ❌ Verify the **IP address** is correct
- ❌ Ensure the PC application window is still open
- ❌ Try disabling Windows Firewall temporarily (Windows Firewall may block the connection)

### **Camera Not Working**
- ❌ Ensure you've enabled the Chrome flag (Method A only)
- ❌ Grant camera permissions when prompted
- ❌ Try using a different browser if Chrome doesn't work
- ❌ Restart the browser and try again

### **Codes Not Being Typed**
- ❌ Ensure cursor is in an active text field on your PC
- ❌ Check that the status indicator shows "Connected"
- ❌ Try clicking in the target application first

### **Windows Firewall Alert**
- ✅ Click "Allow access" and select "Private networks"
- ✅ If blocked, add the application to Windows Firewall exceptions

---

## 📝 Notes

- **Beta Version**: This is an open-source beta application. Occasional bugs may occur. Your feedback helps us improve!
- **Local Network Only**: The application works only on your local Wi-Fi network (no internet transmission)
- **Windows Only**: PC software currently supports Windows 10 and 11
- **Mobile Flexibility**: Mobile app works on any smartphone with a modern web browser

---

## 📞 Support & Feedback

This is a **completely free, open-source utility** with:
- ✅ Zero advertisements
- ✅ Zero hidden restrictions
- ✅ Zero tracking

We'd love to hear from you! Please share:
- 🐛 Bug reports
- 💡 Feature suggestions
- ✨ General feedback

**Contact via WhatsApp**: [+94771599229](https://wa.me/+94771599229)

---

## 📜 License

This project is open-source and free to use. Feel free to fork, modify, and distribute!

---

## 👨‍💻 Developer

**Developed by Wohan**

Visit: [GitHub Profile](https://github.com/wgwohan)

---

## 🙏 Acknowledgments

Special thanks to:
- `html5-qrcode` library for QR code scanning
- Python `websockets` library for real-time communication
- All users who provide valuable feedback

---

**Happy Scanning! 📱✨**
