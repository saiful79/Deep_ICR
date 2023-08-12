
from enum import unique


def main(class_list):
    for i in class_list:
        print(i)
    print(len(class_list))

def class_list_function():
    Extra_add = [" ",'±']
    # Extra_add = ['ং','ঃ','়']
    PUNCHATION =Extra_add+['।','!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', ' ', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']
    NUMBER = ["0","1","2","3","4","5","6","7","8","9"]
    unique_character = ['1', '0', ':', '5', '7', 'L', 'T', 'R', 'F', '2', '3', '4', '/', '9', '8', '"', '.', '-', ',', 'P', 'w', 'v', 'u', 't', 's', 'r', 'A', 'U', 'O', '6', 'M', '(', ')', 'J', '‘', '&', ']', '[', 'z', 'B', ' ', 'H', 'E', 'I', 'N', '%', '#', 'K', 'X', 'p', 'o', 'n', 'm', 'k', 'j', 'i', '}', 'Z', 'Y', 'W', 'V', 'G', 'D', 'C', 'c', 'b', 'a', '`', '_', '$', 'e', 'l', '>', '<', '’', '\\', 'S']
    ALPAHBET = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    PUNCTUATION = ['।','!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', ' ', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']
    small_ALPAHBET = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v","w","x", "y", "x"]
    character_list = NUMBER+ALPAHBET+PUNCTUATION+small_ALPAHBET+unique_character
    GET_ALL_CLASSES = []
    for i in character_list:
         if i not in GET_ALL_CLASSES:
            GET_ALL_CLASSES.append(i)
    return GET_ALL_CLASSES

if __name__=="__main__":
    all_list_cls= class_list_function()
    main(all_list_cls)


