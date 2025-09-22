# Automated CFU Counter with Raspberry Pi and Computer Vision (YOLOv8n)

This repository contains the source code for an automated system that detects and counts Colony Forming Units (CFUs) on agar plates in real-time using a Raspberry Pi and YOLOv8n model.

## ✨ Features
- Raspberry Pi + Pi Camera for image acquisition
- Real-time detection with YOLOv8
- GUI built using Kivy
- Affordable and portable alternative to commercial colony counters

## 📂 Files
- `cfu_counter.py` – Main application code
- `requirements.txt` – Python dependencies

## ⚙️ Installation
Clone the repository and install dependencies:

```bash
git clone https://github.com/frederickkofilumor/Automated-CFU-Counter.git
cd Automated-CFU-Counter
pip install -r requirements.txt

## 🔗 Model Weights
The trained YOLOv8nano model (`best.pt`) is not included in this repository due to file size limits.  

📥 [Click here to download best.pt](https://drive.google.com/uc?export=download&id=1EkHKVDeS7vP0EJ1gxVQTxy_D7bljV1st)

Once downloaded, place `best.pt` in the project folder (same directory as `cfu_counter.py`).
