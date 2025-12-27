import os
import time
import random
import json

# Helferfunktionen
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

SAVE_FILE = "plant_save.json"

# ASCII-Stages für die Pflanze
PLANT_STAGES = [
    ["   .   "],
    ["   |   ",
     "   |   "],
    ["   |   ",
     "  /|\\  "],
    ["   |   ",
     "  /|\\  ",
     "   |   "],
    ["   |   ",
     "  /|\\  ",
     "  / \\  "]
]

BEE = "🐝"
FLOWER = "🌸"

FUN_EVENTS = [
    "Eine freche Biene stiehlt Nektar! 😹",
    "Dein Pflänzchen macht einen kleinen Freudentanz! 💃",
    "Ein Schmetterling landet auf den Blättern! 🦋",
    "Die Sonne blinzelt schelmisch! 🌞",
    "Eine Schnecke macht ein Nickerchen auf deinem Pflänzchen. 🐌"
]

class Plant:
    def __init__(self, name, health=5, size=0):
        self.name = name
        self.health = health
        self.size = size

    def water(self):
        print(f"\n💧 Du gießt {self.name}!")
        self.health += 1
        self.grow()
        time.sleep(1)

    def give_sun(self):
        print(f"\n☀️ Du gibst {self.name} Sonne!")
        self.health += 1
        self.grow()
        time.sleep(1)

    def grow(self):
        if self.health > 5 and self.size < len(PLANT_STAGES) - 1:
            self.size += 1
            self.health = 5
            print(f"🌿 {self.name} wächst! Größe: {self.size + 1}")
        self.display()

    def display(self):
        clear()
        print(f"💚 {self.name} – Gesundheit: {self.health}, Größe: {self.size + 1}")
        # Pflanze zeichnen
        for line in PLANT_STAGES[self.size]:
            print(line)
        # Blumen und Bienen zufällig
        flowers = " ".join([FLOWER for _ in range(random.randint(1,3))])
        bees = " ".join([BEE for _ in range(random.randint(1,3))])
        print(flowers)
        print(bees)

    def wilt(self):
        self.health -= 1
        if self.health <= 0:
            print(f"😢 Oh nein! {self.name} ist verwelkt!")
            return True
        return False

    def save(self):
        data = {
            "name": self.name,
            "health": self.health,
            "size": self.size
        }
        with open(SAVE_FILE, "w") as f:
            json.dump(data, f)
        print("💾 Fortschritt gespeichert!")

    @staticmethod
    def load():
        try:
            with open(SAVE_FILE, "r") as f:
                data = json.load(f)
                print("📂 Spielstand geladen!")
                return Plant(data["name"], data["health"], data["size"])
        except FileNotFoundError:
            return None

def random_event(plant):
    if random.random() < 0.5:
        event = random.choice(FUN_EVENTS)
        print(f"\n🎉 Zufallsevent: {event}")
        # Manchmal heilt das Event die Pflanze oder sie wächst ein Stück
        if "Biene" in event or "Schmetterling" in event:
            plant.health += 1
        if "Freudentanz" in event:
            plant.grow()
        time.sleep(2)

def mini_game(plant):
    print("\n🕹️ Mini-Spiel: Fange die Biene!")
    print("Drücke Enter so schnell wie möglich, um die Biene zu fangen!")
    input("Bereit? Los! ⏱️ ")
    reaction = random.random()
    if reaction > 0.5:
        print(f"🎉 Super! {plant.name} bekommt extra Nektar!")
        plant.health += 2
        plant.grow()
    else:
        print(f"😅 Oh nein, die Biene entwischt!")
    time.sleep(1)

def main():
    clear()
    print("🌸🐝 Willkommen zu Bienen, Blümchen & Spaß! 🐝🌸")
    plant = Plant.load()
    if not plant:
        name = input("Wie soll dein Pflänzchen heißen? ")
        plant = Plant(name)
    plant.display()

    while True:
        print("\nWas möchtest du tun?")
        print("1. Gießen 💧")
        print("2. Sonne geben ☀️")
        print("3. Mini-Spiel 🕹️")
        print("4. Fortschritt speichern 💾")
        print("5. Spiel beenden ❌")
        choice = input("Deine Wahl: ")

        if choice == "1":
            plant.water()
        elif choice == "2":
            plant.give_sun()
        elif choice == "3":
            mini_game(plant)
        elif choice == "4":
            plant.save()
        elif choice == "5":
            print("Spiel beendet. Bis bald! 👋")
            break
        else:
            print("Ungültige Eingabe!")
            time.sleep(1)

        random_event(plant)

        # Zufällig verwelken
        if random.random() < 0.1:
            if plant.wilt():
                print("💀 Spiel vorbei!")
                break

        time.sleep(1)

if __name__ == "__main__":
    main()
