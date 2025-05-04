import sys
import mss
from PIL import Image
from PyQt6.QtCore import Qt, QRect, pyqtSignal, QEventLoop
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
import google.generativeai as genai
from screen import ScreenshotTool
from tkinter import simpledialog
import tkinter as tk

class ScreenshotAnalyzer:
    def __init__(self):
        # Configurer Gemini
        GOOGLE_API_KEY = "AIzaSyDqGvFHQXwDFh82rYuSuookusjmv3Gs9Rc"
        genai.configure(api_key=GOOGLE_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.5-flash-preview-04-17')
        
        # Outil de capture existant
        self.capture_tool = ScreenshotTool()
    
    def analyze_screenshot(self):
        # Demander un commentaire
        comment = simpledialog.askstring("Analyse", "Entrez votre commentaire:")
        
        # Charger l'image
        img = self.capture_tool.screenshot
        
        # Préparer le prompt combiné
        prompt = f"L'utilisateur a envoyé cette capture d'écran avec ce commentaire : '{comment}'. Analyse l'image et réponds de manière utile."
        
        # Envoyer à Gemini
        response = self.model.generate_content([prompt, img])
        
        # Afficher le résultat
        print(response.text)
        result_window = tk.Toplevel()
        result_window.title("Résultat de l'analyse")
        tk.Label(result_window, text=response.text, wraplength=600).pack(padx=20, pady=20)
        

""" # Lancement de l'application
if __name__ == '__main__':
    app = ScreenshotTool()
    app.root.mainloop()
    #app.screenshot.show() """

if __name__ == '__main__':
    analyzer = ScreenshotAnalyzer()
    analyzer.capture_tool.root.mainloop()
    analyzer.analyze_screenshot()


""" if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # 1. Sélection de la région
    selected_rect = process_selection()
    
    # 2. Capture de la région
    img = capture_region(selected_rect)
    
    # 3. Requête à Gemini
    response = model.generate_content(["Analyse cette image:", img])
    
    # 4. Affichage des résultats
    overlay = Overlay()
    overlay.label.setText(response.text)
    overlay.resize(400, 300)
    overlay.show()
    
    sys.exit(app.exec()) """