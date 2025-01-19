import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Per caricare immagini in formati diversi da .png

countMoves = 0
countMaxMoves = 10
fruit = None
points = 0  
image_path = "trophy.png"
# Funzione per gestire il movimento del personaggio
def move_character(event):
    global countMoves
    if event.keysym == 'Up':    # Freccia su
        canvas.move(player, 0, -10)
    elif event.keysym == 'Down':  # Freccia giù
        canvas.move(player, 0, 10)
    elif event.keysym == 'Left':  # Freccia sinistra
        canvas.move(player, -10, 0)
    elif event.keysym == 'Right':  # Freccia destra
        canvas.move(player, 10, 0)

    countMoves += 1
    checkPos()

def showWinning():
    custom_window = tk.Toplevel(window)
    custom_window.title("Congratulazioni!")
    custom_window.geometry("200x200")
    try:
                trophy_image = Image.open(image_path)
                img_resized = trophy_image.resize((100, 100))
                trophy_photo = ImageTk.PhotoImage(img_resized)
    except:
                messagebox.showerror("Errore", "Immagine non trovata.")
                return
    
    trophy_label = tk.Label(custom_window, image=trophy_photo)
    trophy_label.image = trophy_photo  # Necessario per mantenere una reference all'immagine
    trophy_label.pack(pady=20)

    # Crea una label per il messaggio
    message_label = tk.Label(custom_window, text="Hai vinto! Congratulazioni!", font=("Arial", 14))
    message_label.pack(pady=10)

    # Aggiungi un bottone per chiudere la finestra
    close_button = tk.Button(custom_window, text="Chiudi", command=custom_window.destroy)
    close_button.pack(pady=10)
    
# Funzione per controllare la posizione e generare il frutto
def checkPos():
    global countMoves, fruit, points

    # Controlla se il numero di mosse ha raggiunto il limite
    if countMoves == countMaxMoves:
        countMoves = 0  # Resetta il contatore delle mosse

        # Posizione del giocatore
        player_coords = canvas.coords(player)
        player_x = (player_coords[0] + player_coords[2]) // 2
        player_y = (player_coords[1] + player_coords[3]) // 2

        # Genera un frutto vicino alla posizione del giocatore
        xSprite = random.randint(max(20, player_x - 100), min(580, player_x + 100))
        ySprite = random.randint(max(20, player_y - 100), min(580, player_y + 100))

        # Rimuovi il frutto precedente se esiste
        if fruit:
            canvas.delete(fruit)

        # Crea un nuovo frutto (cerchio rosso)
        fruit = canvas.create_oval(
            xSprite - 10, ySprite - 10, xSprite + 10, ySprite + 10, fill="red"
        )

    # Controlla se il giocatore ha raggiunto il frutto
    if fruit:
        player_coords = canvas.coords(player)
        fruit_coords = canvas.coords(fruit)
        if (
            player_coords[2] >= fruit_coords[0] and  # Lato destro giocatore 
            player_coords[0] <= fruit_coords[2] and  # Lato sinistro giocatore 
            player_coords[3] >= fruit_coords[1] and  # Parte inferiore giocatore parte superiore del frutto
            player_coords[1] <= fruit_coords[3]      # Parte superiore giocatore la parte inferiore del frutto
        ):
            points += 1
            points_label.config(text=f"Punteggio: {points}")
            showWinning()
            #messagebox.showinfo("Hai vinto!", f"Hai raggiunto il frutto! Punteggio: {points}")
            canvas.delete(fruit)

window = tk.Tk()
window.title("Gioco 2D - SpriteMoving")
window.geometry("600x600")
points_label = tk.Label(window, text=f"Punteggio: {points}", font=("Arial", 14), bg="lightblue")
points_label.pack()
canvas = tk.Canvas(window, width=600, height=600, bg="lightblue")
canvas.pack()
x, y = 300, 300 
player = canvas.create_rectangle(x - 20, y - 20, x + 20, y + 20, fill="green")


window.bind("<Up>", move_character)
window.bind("<Down>", move_character)
window.bind("<Left>", move_character)
window.bind("<Right>", move_character)

# Avvia il loop della finestra
window.mainloop()
