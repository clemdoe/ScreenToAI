import tkinter as tk
from PIL import ImageGrab

# Configuration de la fenêtre de sélection
class ScreenshotTool:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-alpha', 0.3)
        self.root.attributes('-topmost', True)
        
        self.canvas = tk.Canvas(self.root, cursor='cross', bg='gray15')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Ajout du bouton close
        self.add_close_button() 
        
        self.start_x = None
        self.start_y = None
        self.rect = None

        # Liaison des événements souris
        self.canvas.bind('<ButtonPress-1>', self.on_press)
        self.canvas.bind('<B1-Motion>', self.on_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_release)
    
    def cancel_capture(self, event):
        self.root.destroy()
        print("Capture annulée")

    def add_close_button(self):
        # Création du bouton rond
        screen_width = self.root.winfo_screenwidth()
        size = 40
        x = screen_width//2 - size//2
        y = 20
        
        # Cercle de fond
        self.canvas.create_oval(
            x, y, x, y,
            fill='#555555', outline='#777777', width=2,
            tags='close_btn',
        )
        
        # Croix blanche
        pad = 12
        self.canvas.create_line(
            x+pad, y+pad, x+size-pad, y+size-pad,
            fill='white', width=2, tags='close_btn'
        )
        self.canvas.create_line(
            x+size-pad, y+pad, x+pad, y+size-pad,
            fill='white', width=2, tags='close_btn'
        )
        
        # Interaction
        self.canvas.tag_bind('close_btn', '<Button-1>', self.cancel_capture)

    def on_press(self, event):
        # Point de départ
        self.start_x = event.x
        self.start_y = event.y
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, 
            self.start_x, self.start_y, 
            outline= 'grey',
            fill= 'grey',
            width=4)

    def on_drag(self, event):
        # Redimensionnement du rectangle pendant le drag
        if self.rect:
            self.canvas.coords(
                self.rect, 
                self.start_x, self.start_y, 
                event.x, event.y)

    def on_release(self, event):
        # Capture de la zone sélectionnée
        x1 = min(self.start_x, event.x)
        y1 = min(self.start_y, event.y)
        x2 = max(self.start_x, event.x)
        y2 = max(self.start_y, event.y)
        
        self.root.destroy()
        self.screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        #self.screenshot.save('capture.png')
        print("Capture sauvegardée sous capture.png")

# Lancement de l'application
if __name__ == '__main__':
    app = ScreenshotTool()
    app.root.mainloop()
    #app.screenshot.show()