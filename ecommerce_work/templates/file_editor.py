def editor():
    file = input("Enter whole file path: ")
    original = input("Enter the text you want to change: ")
    replacement = input("Enter the text replacement: ")

    initial_file = open(file, 'r+')
    text = initial_file.read()
    
    if original in text:
        pending_text = text.replace(original, replacement)
        new_text = open(file, 'w')
        new_text.write(pending_text)
        print(f"{original} was changed to {replacement}")
    else:
        print(f"Could not change {original} because it could not be found")

editor()