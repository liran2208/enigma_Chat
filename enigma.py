from functools import reduce
rotor_one = "ekmflgdqvzntowyhxuspaibrcj"
rotor_two = "ajdksiruxblhwtmcqgznpyfvoe"
rotor_three = "bdfhjlcprtxvznyeiwgakmusqo"
rotor_four = "esovpzjayquirhxlnftgkdcmwb"
rotor_five = "vzbrgityupsdnhlxawmjqofeck"
ref_a = "ejmzalyxvbwfcrquontspikhgd"
ref_b = "yruhqsldpxngokmiebfzcwvjat"
ref_c = "fvpjiaoyedrzxwgctkuqsbnmhl"

day_states = []

def initialize_states(rotors, states):
    """
    :param rotors:
    :param states:
    :return: set the starting settings of the enigma. it sets daily
    """
    global day_states
    day_states = states[:]
    
    rotors_lst = []
    for i in rotors:
        if i == 1:
            rotors_lst.append(rotor_one[:])
        if i == 2:
            rotors_lst.append(rotor_two[:])
        if i == 3:
            rotors_lst.append(rotor_three[:])
        if i == 4:
            rotors_lst.append(rotor_four[:])
        if i == 5:
            rotors_lst.append(rotor_five[:])
        if i == 'a':
            rotors_lst.append(ref_a[:])
        if i == 'b':
            rotors_lst.append(ref_b[:])
        if i == 'c':
            rotors_lst.append(ref_c[:])
    
    for i in range(len(rotors)-1):
        rotors_lst[i] = rotors_lst[i][-states[i]+1:] + rotors_lst[i][:-states[i]+1]
    
    return rotors_lst


def switchLetters(pears, letter):
    """
    :param pears:
    :param letter:
    :return: the string after the action of the plugboard
    """
    for i in range(len(pears)):
        if letter in pears[i]:
            if letter == pears[i][1]:
                return pears[i][0]
            else:
                return pears[i][1]
    return letter


def add_states(states, rotors):
    """
    :param states:
    :param rotors:
    :return: the changed and updated rotors
    the rotor's way of operation is like a clock, that the first rotors is the seconds,
    the second is the minutes and the third is the hours, when the second hand is above
    a certain number,  it resets and the to the seconds hand is added one...
    (same with hours and minutes)
    """
    states[0] += 1
    rotors[0] = change_state(rotors[0], 1)
    for i in range(len(states) - 1):
        if states[i] > 26:
            states[i] -= 26
            states[i + 1] += 1
            rotors[i+1] = change_state(rotors[i + 1], 1)


def change_state(r, state):
    """
    :param r:
    :param state:
    :return: rotated string (r), (state) times
    this functions is used to rotate the rotors of the enigma.
    """
    # changes the state of the rotor once(state), rotates the string 'r' once
    return r[-state:] + r[:-state]


def rotor(rotors, msg, states):
    """
    :param rotors:
    :param msg:
    :param states:
    :return: the string after the action of the rotors.
    """
    output = []
    for i in range(len(msg)):
        if msg[i].isalpha():
            case = msg[i].isupper()
            char = msg[i].lower()
            char = reduce(lambda res, rot: rot[ord(res) - ord("a")], rotors, char.lower())
            char = reduce(lambda res, rot: chr(rot.index(res) + ord("a")), rotors[2::-1], char)
            output.append(char.upper()) if case else output.append(char)
            add_states(states, rotors)
        else:
            output.append(msg[i])
    
    for i in range(len(states)):
        rotors[i] = change_state(rotors[i], 0 - states[i]+1)
    return output


def addOne(msg):
    lst = [char for char in msg]
    new_lst = []
    for i in lst:
        new_lst.append(chr(ord(i) + msg.find(i)))
    return ''.join(new_lst)


def cypher(msg, rotors, plugboard):
    """
    :param msg:
    :param rotors:
    :param plugboard:
    :return: enigma method encryption message
    """
    states = day_states[:]
    lst = [char for char in msg]
    for i in range(len(lst)):
        lst[i] = (switchLetters(plugboard, lst[i]))
    lst = rotor(rotors, lst, states)
    for i in range(len(lst)):
        lst[i] = switchLetters(plugboard, lst[i])
    encrypted = ''.join(lst)
    return encrypted


def main():
# testing the enigma function
    # ---------------insert here your settings------------------------------
    rotors = [1, 4, 5, 'c']
    rotor_settings = [5, 4, 2]
    plugboard = ["ab", "xy", "hj", "po", "mn", "ld", "qw", "fr", "ev", "zs"]
    rotors = initialize_states(rotors, rotor_settings)
    msg = "xjmsr"
    # ---------------------------------------------------------------------

    print ("output: " + cypher(msg, rotors, plugboard))

if __name__ == "__main__":
    main()

