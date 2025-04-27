# 🥷 Naruto Hand Sign Trainer - Real-Time Gesture Recognition

Welcome to the **Naruto Hand Sign Trainer**!  
This project is a full system combining:

- 📚 A **Training Notebook** to prepare and augment a dataset of Naruto hand signs.
- 🖥️ A **Flask WebApp** that detects your hand signs in real-time, teaching you jutsus like Shadow Clone Jutsu, Chidori, and more!

Built with ❤️ using Flask, YOLOv8, Mediapipe, OpenCV, and custom augmentation techniques.

---

## ✨ Features

### 📓 Training Notebook Features

- 📂 Load and process a custom Naruto hand sign dataset.
- 🔄 Data Augmentation (horizontal flipping, scaling, HSV shifts).
- 🏋️ Fine-tune a YOLOv8 model (`best_naruto_signs_7.pt`) for hand sign classification.
- 📈 Train with optimized parameters for small datasets.

### 🖥️ Web Application Features

- 🖐️ Real-time Hand Sign Detection using YOLOv8 and Mediapipe.
- 📚 **Learning Mode**: Follow jutsu sequences step-by-step.
- 🎯 **Mastery Mode**: Perform full jutsus flawlessly to level up.
- 🆓 **Free Practice Mode**: Practice any sign freely.
- ⏱️ **Time Attack Mode**: Complete as many hand signs as you can in 60 seconds.
- 📝 Gesture history saved into `gestures.json`.
- 📈 Mastery tracking saved into `stats.json`.

---

## 📂 Folder Structure

```bash
/app/
  ├── main.py             # Flask app for real-time sign detection
  ├── gestures.json        # Saved detected hand signs
  ├── stats.json           # Jutsu performance tracking
  ├── templates/
  │    ├── menu.html       # Main menu page
  │    ├── index.html      # Live detection page
  │    ├── stats.html      # Statistics page
/notebooks/
  ├── codeitup5-0.ipynb    # Training and Augmentation Notebook
/models/
  ├── best_naruto_signs_7.pt   # Trained YOLO model (not included in repo)
requirements.txt           # Project dependencies
README.md                  # This file!
