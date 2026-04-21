class Hair:
    def __init__(self, length, color, type):
        self.length = length
        self.color = color
        self.type = type

    def __str__(self):
        return f"Pelo {self.length}, color {self.color}, tipo {self.type}"

class Eyes:
    def __init__(self, color, type):
        self.color = color
        self.type = type
    
    def __str__(self):
        return f"Ojos {self.type}, color {self.color}"

class Head:
    def __init__(self, hair, eyes):
        self.hair = hair
        self.eyes = eyes

    def __str__(self):
        return f"Cabeza: \n     {str(self.hair)} \n     {str(self.eyes)}"

class Torso:
    def __init__(self, head, right_arm, left_arm):
        self.head = head
        self.right_arm = right_arm
        self.left_arm = left_arm

    def __str__(self):
        return f"  {str(self.head)} \n   Brazos: \n     {str(self.right_arm)} \n     {str(self.left_arm)}"

class Hand:
    def __init__(self, side):
        self.side = side

    def __str__(self):
        return f"Mano {self.side}"

class Arm:
    def __init__(self, hand):
        self.hand = hand

    def __str__(self):
        return f"Brazo de la {str(self.hand)}"

class Leg:
    def __init__(self, feet):
        self.feet = feet

    def __str__(self):
        return f"Pierna del {str(self.feet)}"

class feet:
    def __init__(self, side):
        self.side = side

    def __str__(self):
        return f"Pie {self.side}"

class Human():
    def __init__(self, torso, right_leg, left_leg):
        self.torso = torso
        self.right_leg = right_leg
        self.left_leg = left_leg

    def __str__(self):
        return f"Características Físicas de la Persona \n\n Torso: \n {str(self.torso)} \n\n Piernas: \n   {str(self.right_leg)} \n   {str(self.left_leg)}"

def main():
    right_feet = feet("Derecho")
    right_leg = Leg(right_feet)
    left_feet = feet("Izquierdo")
    left_leg = Leg(left_feet)

    right_hand = Hand("Derecha")
    right_arm = Arm(right_hand)
    left_hand = Hand("Izquierda")
    left_arm = Arm(left_hand)

    hair = Hair("Corto","Negro","Rizado") 
    eyes = Eyes("Verdes","Redondos")

    head = Head(hair, eyes)

    torso = Torso(head, right_arm, left_arm)

    human = Human(torso, right_leg, left_leg)

    print(str(human))


if __name__ == "__main__":
    main()