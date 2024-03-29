import tkinter as tk
from random import randint
#import time

class tree:
    child = []
    field = []
    points = 0
    bankPoints = 0
    eval = None
    depth = 0

class Game:
    def __init__(self, root, length):
        self.root = root
        self.length = length
        self.sequence = [randint(1, 4) for _ in range(length)]  # Ģenerē skaitļu virkni
        self.tree = tree()
        self.tree.field = self.fieldCalc
        self.currentNode = self.tree
        self.generateTree(self.tree)
        self.points = 0
        self.bank_points = 0
        self.turn_number = 0
        self.selected_index = None

        self.label = tk.Label(root, text=f"Skaitļu virkne: {self.sequence}")
        self.label.pack()

        self.points_label = tk.Label(root, text=f"Tavi punkti: {self.points}")
        self.points_label.pack()

        self.bank_points_label = tk.Label(root, text=f"Bankas punkti: {self.bank_points}")
        self.bank_points_label.pack()

        self.turn_label = tk.Label(root, text = f"Gājiens: {self.turn_number}")
        self.turn_label.pack()

        self.last_CPU_move_label = tk.Label(root, text = f"Pēdējais CPU gājiens:")
        self.last_CPU_move_label.pack()

        self.number_buttons = []
        for index, number in enumerate(self.sequence):
            button = tk.Button(root, text=str(number), command=lambda i=index: self.select_number(i))
            button.pack(side="left")
            self.number_buttons.append(button)

        self.add_button = tk.Button(root, text="Pievienot punktus", command=self.add_to_points)
        self.add_button.pack(side="left")

        self.split_button = tk.Button(root, text="Sadala", command=self.split_number)
        self.split_button.pack(side="right")
        

    def select_number(self, index):
        if self.selected_index is not None:
            self.number_buttons[self.selected_index].config(relief=tk.RAISED)
        self.selected_index = index
        self.number_buttons[index].config(relief=tk.SUNKEN)

    def add_to_points(self):
        if self.selected_index is not None:
            selected_number = self.sequence.pop(self.selected_index)
            self.points += selected_number
            self.number_buttons[self.selected_index].destroy()
            self.number_buttons.pop(self.selected_index)
            self.turn_number += 1
            self.update_display()

    def split_number(self):
        if self.selected_index is not None:
            selected_number = self.sequence[self.selected_index]
            if selected_number == 2:
                self.bank_points += 1
                self.sequence[self.selected_index] = 1
                self.sequence.insert(self.selected_index + 1, 1)
                self.turn_number += 1
            elif selected_number == 4:
                self.points += 2
                #self.bank_points += 1
                self.sequence[self.selected_index] = 2
                self.sequence.insert(self.selected_index + 1, 2)
                self.turn_number += 1
            self.update_display()

    def check_winner(self):
        if not self.sequence:
            #total_points = self.points + self.bank_points
            if self.points % 2 == 0 and self.bank_points % 2 == 0:
                winner = "Pirmais spēlētājs"
            elif self.points % 2 == 1 and self.bank_points % 2 == 1:
                winner = "Otrais spēlētājs (CPU)"
            else:
                winner = "Neizšķirts"
            self.label.config(text=f"Spēle beigusies! Uzvar: {winner}")

    def update_display(self):
        self.label.config(text=f"Skaitļu virkne: {self.sequence}")
        self.points_label.config(text=f"Tavi punkti: {self.points}")
        self.bank_points_label.config(text=f"Bankas punkti: {self.bank_points}")
        self.selected_index = None

        for button in self.number_buttons:
            button.destroy()
        self.number_buttons = []
        for index, number in enumerate(self.sequence):
            button = tk.Button(self.root, text=str(number), command=lambda i=index: self.select_number(i))
            button.pack(side="left")
            self.number_buttons.append(button)
        
        self.check_winner()
        if self.sequence:
            self.select_player_turn()

    def cpu_turn(self):
        if len(self.sequence) > 1:
            choice = randint(1,len(self.sequence)-1)
        else:
            choice = 0
        #time.sleep(0.3)
        self.select_number(choice)
        #time.sleep(0.3)
        selected_number = self.sequence[self.selected_index]
        
        if selected_number == 2 or selected_number == 4:
            doSplit = randint(1,2)
            if doSplit == 1:
                self.last_CPU_move_label.config(text=f"Pēdējais CPU gājiens: split_number:{selected_number}")
                self.split_number()
            else:
                self.last_CPU_move_label.config(text=f"Pēdējais CPU gājiens: add_to_points:{selected_number}")
                self.add_to_points()
        else:
            self.last_CPU_move_label.config(text=f"Pēdējais CPU gājiens: add_to_points:{selected_number}")
            self.add_to_points()
        #time.sleep(0.3)

    def select_player_turn(self):
        if self.turn_number % 2 == 0:
            self.turn_label.config(text=f"Gājiens: {self.turn_number} (Spēlētājs)")
        else:
            self.turn_label.config(text=f"Gājiens: {self.turn_number} (CPU)")
            self.cpu_turn()

    def fieldCalc(self):
        count = [0,0,0,0]
        for number in self.currentNode.field:
            match number:
                case 1:
                    count[0] = count[0]+1
                    break
                case 2:
                    count[1] = count[1]+1
                    break
                case 3:
                    count[2] = count[2]+1
                    break
                case 4:
                    count[3] = count[3]+1
                    break
        return count
    
    # TODO: koka ģenerēšana. Pašlaik liekas diezgan sadirsta
    # var neuztvert par nopietnu un pārakstīt ja rodas ideja
    def generateTree(node):
        count = node.field
        for index, number in enumerate(count):
            match index:
                case 0: # izvelas 1 pievieno punktiem
                    if number == 0: 
                        break
                    else:   # depth+1, ciparu_sk - 1,  punktu_sk + 1
                        newChild = node
                        newChild.depth = node.depth +1
                        newChild.points = node.points + index+1
                        newCount = count
                        newCount[index] = newCount[index]-1
                        newChild.field = newCount
                        node.child.append(newChild) # pievieno jaunu lapu kokam

                case 1: # izvelas 2 pievieno punktiem vai sadala
                    if number == 0: 
                        break
                    else:   # depth+1, ciparu2_sk - 1,  punktu_sk + 2
                        newChild = node
                        newChild.depth = node.depth +1
                        newChild.points = node.points + index+1
                        newCount = count
                        newCount[index] = newCount[index]-1
                        newChild.field = newCount
                        node.child.append(newChild) # pievieno jaunu lapu kokam
                        # 2 sadala
                        # depth+1, ciparu2_sk - 1, ciparu1_sk + 2  bankas_punktu_sk + 1
                        newChild2 = node
                        newChild2.depth = node.depth +1
                        newChild2.bankPoints = node.bankPoints + 1
                        newCount2 = count
                        newCount2[index] = newCount[index]-1
                        newCount2[0] = newCount2[0]+2
                        newChild2.field = newCount
                        node.child.append(newChild2) # pievieno jaunu lapu kokam

                case 2: # izvelas 3 pievieno punktiem
                    if number == 0: 
                        break
                    else:   # depth+1, ciparu3_sk - 1,  punktu_sk + 3
                        newChild = node
                        newChild.depth = node.depth +1
                        newChild.points = node.points + index+1
                        newCount = count
                        newCount[index] = newCount[index]-1
                        newChild.field = newCount
                        node.child.append(newChild) # pievieno jaunu lapu kokam

                case 3: # izvelas 4 pievieno punktiem
                    if number == 0: 
                        break
                    else:   # depth+1, ciparu4_sk - 1,  punktu_sk + 4
                        newChild = node
                        newChild.depth = node.depth +1
                        newChild.points = node.points + index+1
                        newCount = count
                        newCount[index] = newCount[index]-1
                        newChild.field = newCount
                        node.child.append(newChild) # pievieno jaunu lapu kokam
                        # 4 sadala
                        # depth+1, ciparu4_sk - 1, ciparu2_sk + 2
                        newChild2 = node
                        newChild2.depth = node.depth +1
                        newCount2 = count
                        newCount2[index] = newCount[index]-1
                        newCount2[1] = newCount2[1]+2
                        newChild2.field = newCount
                        node.child.append(newChild2) # pievieno jaunu lapu kokam


    def minMax(self):       # position, depth, maximisingPlayer
        print("minMax")

    # TODO: alphaBeta funkcija
    def alphaBeta(self):    # position, depth, maximisingPlayer, alpha, beta
        print("alphaBeta")
        # valueFunction izsauks no šejienes

    def valueFunction(self):
        print("valueFunction")
            
def main():
    length = randint(4, 7)  # Ģenerē skaitļu virknes garumu
    root = tk.Tk()
    root.title("Spēle ar skaitļu virkni")

    game = Game(root, length)

    root.mainloop()

if __name__ == "__main__":
    main()