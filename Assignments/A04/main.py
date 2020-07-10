import tkinter as tk
import os
import json

fpath = "player-info.json"

# GUI window is a subclass of the basic tkinter Frame object
class MainFrame(tk.Frame):
    def __init__(self, master):
        # Call superclass constructor
        tk.Frame.__init__(self, master)
        # Place frame into main window
        self.grid()        
        if os.path.isfile(fpath):
            infile = open(fpath, "r")
            data = infile.read()
            infile.close
        else:
            print("Error: File doesn't exist!")

        playerInfo = json.loads(data)
        title = "Player: " + playerInfo["screen_name"]
        
        i = 0
        for info1, info2 in playerInfo.items():
            if info1 != "screen_name":
                finalInfor1 = info1.ljust(20)
                finalInfor2 = tk.Label(self, text= finalInfor1)
                finalInfor2.grid(sticky = tk.W, row=i, column=0)
                
                finalInfor1 = ":   " + str(info2).strip("[]")
                finalInfor1 = finalInfor1.replace("'","")
                
                finalInfor2 = tk.Label(self, text= finalInfor1)
                finalInfor2.grid(sticky = tk.W, row=i, column=20)
                
                i+=1

# Spawn window
if __name__ == "__main__":
    if os.path.isfile(fpath):
        infile = open(fpath, "r")
        data = infile.read()
        infile.close
    else:
        print("Error: File doesn't exist!")
    playerInfo = json.loads(data)
    title = "Player: " + playerInfo["screen_name"] 
    # Create main window object
    root = tk.Tk()
    # Set title of window
    root.title(f"{title}")
    # Instantiate HelloWorldFrame object
    display = MainFrame(root)
    # Start GUI
    display.mainloop()

