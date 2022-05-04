from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import cv2 as cv
import SystemControl

is_on = False
show_frame = True
testing_mode = False
cap = None
root1 = None


def main():
    # declare the root
    root = Tk()
    root.title('Hand Gesture Recognition System')
    root.geometry("900x700")

    # declare the style
    style = ttk.Style()
    style.theme_create("MyStyle", parent="classic", settings={
        "TFrame": {"configure": {"background": '#d9d9d9'}},
        "TNotebook": {"configure": {"tabmargins": [0, 0, 0, 0]}},
        "TNotebook.Tab": {"configure": {"padding": [10, 10]},
                          "map": {"background": [("selected", '#f0f0f0')]}}})
    style.theme_use("MyStyle")

    # declare Notebook in the root
    tabControl = ttk.Notebook(root)
    tabControl.pack(expand=True, fill="both")

    # add Tab bar into the Notebook
    tab1 = ttk.Frame(tabControl)
    tab1.pack(fill=BOTH, expand=True)

    tab2 = ttk.Frame(tabControl)
    tab2.pack(fill=BOTH, expand=True)

    tab3 = ttk.Frame(tabControl)
    tab3.pack(fill=BOTH, expand=True)

    tabControl.add(tab1, text='Home')
    tabControl.add(tab2, text='Gesture Guideline')
    tabControl.add(tab3, text='About')

    # declare a scroll bar for the second tab
    canvas_tab2 = Canvas(tab2, bg='#d9d9d9')
    scroll = Scrollbar(tab2, command=canvas_tab2.yview)
    canvas_tab2.config(yscrollcommand=scroll.set, scrollregion=(0, 0, 0, 11300))
    canvas_tab2.pack(side=LEFT, fill=BOTH, expand=True)
    scroll.pack(side=RIGHT, fill=Y)
    frame_tab2 = Frame(canvas_tab2, bg='#d9d9d9')
    canvas_tab2.create_window(0, 0, window=frame_tab2, anchor='nw')

    # Tab 1
    title = Label(tab1, text='Hand Gesture Recognition System', font=("Arial", 18), bg='#d9d9d9')
    title.grid(row=0, column=1, columnspan=2, padx=250, pady=(130, 0))

    empty_label = Label(tab1, text='', font=("Arial", 18), bg='#d9d9d9')
    empty_label.grid(row=1, column=1, columnspan=2, pady=20)

    def test_mode():
        global testing_mode, show_frame
        if checkbutton2.get() == 1:
            button1['state'] = 'disabled'
            button1.select()
            show_frame = True
            testing_mode = True
        else:
            button1['state'] = 'normal'
            testing_mode = False

    def check_value():
        global show_frame
        if checkbutton1.get() == 1:
            show_frame = True
        else:
            show_frame = False

    # Define our switch function
    def switch():
        global is_on, cap, root1
        if not is_on:
            on_button.config(image=on)
            is_on = True
            print(show_frame)
            print(testing_mode)
            SystemControl.start(root, show_frame, testing_mode)
        else:
            cap = SystemControl.cap
            root1 = SystemControl.root1
            on_button.config(image=off)
            is_on = False
            cap.release()
            cv.destroyAllWindows()
            root1.destroy()

    start = Label(tab1, text='Click to Start', font=("Arial", 15), bg='#d9d9d9')
    start.grid(row=2, column=1, sticky=E, padx=(0, 10))

    # Define Images
    on = ImageTk.PhotoImage(Image.open("resource/on.png").resize((100, 100)))
    off = ImageTk.PhotoImage(Image.open("resource/off.png").resize((100, 100)))

    # Create A Button for turning on/off the recognition system
    on_button = Button(tab1, image=off, bd=0, command=switch, borderwidth=0, highlightthickness=0, bg='#d9d9d9')
    on_button.grid(row=3, column=1, sticky=E, padx=(0, 15), pady=(10, 0))

    settings = Label(tab1, text='Settings', font=("Arial", 15), bg='#d9d9d9')
    settings.grid(row=2, column=2, sticky=W, padx=(45, 0))

    # Create checkbutton for the settings of the recognition system
    checkbutton1 = IntVar()
    button1 = Checkbutton(tab1, text="Show Webcam Frame",
                          variable=checkbutton1,
                          onvalue=1,
                          offvalue=0,
                          bg='#d9d9d9',
                          command=check_value)
    button1.select()
    button1.grid(row=3, column=2, sticky=NW, padx=(20, 0), pady=(35, 0))

    checkbutton2 = IntVar()
    button2 = Checkbutton(tab1, text="Recognition Mode Only",
                          variable=checkbutton2,
                          onvalue=1,
                          offvalue=0,
                          bg='#d9d9d9',
                          command=test_mode)
    button2.grid(row=3, column=2, sticky=NW, padx=(20, 0), pady=(65, 0))

    # Tab 2
    r0c0 = Entry(frame_tab2, font=("Arial", 10), bg='#d9d9d9', fg='black', justify='center', width=27)
    r0c0.grid(row=0, column=0)
    r0c0.insert(END, "Function")
    r0c0.config(state=DISABLED)
    r0c1 = Entry(frame_tab2, font=("Arial", 10), bg='#d9d9d9', fg='black', justify='center', width=43)
    r0c1.grid(row=0, column=1)
    r0c1.insert(END, "Hand Gesture (Right Hand)")
    r0c1.config(state=DISABLED)
    r0c2 = Entry(frame_tab2, font=("Arial", 10), bg='#d9d9d9', fg='black', justify='center', width=53)
    r0c2.grid(row=0, column=2)
    r0c2.insert(END, "Description")
    r0c2.config(state=DISABLED)

    label_list = ['Mouse Pointer', 'Left Click', 'Right Click', 'Stop', 'A', 'B', 'C', 'D', 'E', 'F',
                  'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W',
                  'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'Up', 'Down', 'Left',
                  'Right', 'Space', 'Backspace', 'Enter', 'Caps Lock']

    for i in label_list:
        row = label_list.index(i)+1
        c0 = Label(frame_tab2, text=i, font=("Arial", 10), bg='#d9d9d9', fg='black')
        c0.grid(row=row, column=0)
        img_name = 'resource/' + i + '.jpg'
        image = Image.open(img_name).resize((230, 230))
        image = ImageTk.PhotoImage(image)
        c2 = Label(frame_tab2, image=image)
        c2.image = image
        c2.grid(row=row, column=1)

    textPointer = "Function: \n" \
                  "This gesture is responsible for mouse cursor moving. " \
                  "Use this gesture if you want to move the cursor of " \
                  "the computer mouse.\n\n" \
                  "Gesture: \n" \
                  "1. Hold your hand in a fist and palm facing outward.\n" \
                  "2. Place your index finger up and point at top left " \
                  "side."
    r1c2 = Label(frame_tab2, text=textPointer, font=("Arial", 10), bg='#d9d9d9', fg='black', justify='left',
                 anchor='w', width=39, wraplength=300)
    r1c2.grid(row=1, column=2)

    textLeftClick = "Function: \n" \
                    "This gesture is responsible for mouse left click. " \
                    "Use this gesture if you want to perform a left click " \
                    "function.\n\n" \
                    "Gesture: \n" \
                    "1. Hold your hand in a fist and palm facing outward.\n" \
                    "2. Place your index and middle fingers straight up " \
                    "and stick together.\n" \
                    "3. Rotate your hand 90 degrees counterclockwise to " \
                    "make your index and middle fingers point to the left."
    r2c2 = Label(frame_tab2, text=textLeftClick, font=("Arial", 10), bg='#d9d9d9', fg='black', justify='left',
                 anchor='w', width=39, wraplength=300)
    r2c2.grid(row=2, column=2)

    textRightClick = "Function: \n" \
                     "This gesture is responsible for mouse right click. " \
                     "Use this gesture if you want to perform a right " \
                     "click function.\n\n" \
                     "Gesture: \n" \
                     "1. Hold your hand in a fist and palm facing outward.\n" \
                     "2. Place your index, middle and ring fingers " \
                     "straight up and stick together.\n" \
                     "3. Rotate your hand 90 degrees counterclockwise to " \
                     "make your index, middle and ring fingers point to " \
                     "the left."
    r3c2 = Label(frame_tab2, text=textRightClick, font=("Arial", 10), bg='#d9d9d9', fg='black', justify='left',
                 anchor='w', width=39, wraplength=300)
    r3c2.grid(row=3, column=2)

    textStop = "Function: \n" \
               "This gesture is a “stop” sign. Use this gesture if " \
               "you want the computer to stop performing any " \
               "commands and functions controlled by any gestures " \
               "or if you do not want the computer to perform any " \
               "commands and functions.\n\n" \
               "Gesture: \n" \
               "1. Hold your hand open and palm facing outward."
    r4c2 = Label(frame_tab2, text=textStop, font=("Arial", 10), bg='#d9d9d9', fg='black', justify='left', anchor='w',
                 width=39, wraplength=300)
    r4c2.grid(row=4, column=2)

    textA = "Function: \n" \
            "This gesture is responsible for the letter ‘A’ key. " \
            "Use this gesture if you want to type letter ‘A’.\n\n" \
            "Gesture: \n" \
            "1. Hold your hand in a fist and palm face outward.\n" \
            "2. Place the index, middle, ring, little fingers straight " \
            "down without bend them inward.\n" \
            "3. The thumb finger faces up and sticks to the side of " \
            "the index finger."
    r5c2 = Label(frame_tab2, text=textA, font=("Arial", 10), bg='#d9d9d9', fg='black', justify='left', anchor='w',
                 width=39, wraplength=300)
    r5c2.grid(row=5, column=2)

    textB = "Function: \n" \
            "This gesture is responsible for the letter ‘B’ key. " \
            "Use this gesture if you want to type letter ‘B’.\n\n" \
            "Gesture: \n" \
            "1. Hold your hand open with palm facing outward.\n" \
            "2. All 4 fingers except the thumb standing straight and " \
            "sticking together.\n" \
            "3. Tuck your thumb into your palm."
    r6c2 = Label(frame_tab2, text=textB, font=("Arial", 10), bg='#d9d9d9', fg='black', justify='left', anchor='w',
                 width=39, wraplength=300)
    r6c2.grid(row=6, column=2)

    textC = "Function: \n" \
            "This gesture is responsible for the letter ‘C’ key. " \
            "Use this gesture if you want to type letter ‘C’.\n\n" \
            "Gesture: \n" \
            "1. Curve your hand like the letter 'C' with the top 4 " \
            "fingers hold together forming the top curve and the " \
            "thumb forming the bottom curve.\n" \
            "2. Your palm faces to your left."
    r7c2 = Label(frame_tab2, text=textC, font=("Arial", 10), bg='#d9d9d9', fg='black', justify='left', anchor='w',
                 width=39, wraplength=300)
    r7c2.grid(row=7, column=2)

    textD = "Function: \n" \
            "This gesture is responsible for the letter ‘D’ key. " \
            "Use this gesture if you want to type letter ‘D’.\n\n" \
            "Gesture: \n" \
            "1. Curve your middle, ring, and little fingers together " \
            "and touch them to your thumb to make a circle.\n" \
            "2. Place your index finger up straight.\n" \
            "3. Your palm faces to the left.\n" \
            "4. The space of the circle must be shown."
    r8c2 = Label(frame_tab2, text=textD, font=("Arial", 10), bg='#d9d9d9', fg='black', justify='left', anchor='w',
                 width=39, wraplength=300)
    r8c2.grid(row=8, column=2)

    textE = "Function: \n" \
            "This gesture is responsible for the letter ‘E’ key. " \
            "Use this gesture if you want to type letter ‘E’.\n\n" \
            "Gesture: \n" \
            "1. Hold your hand with your top 4 " \
            "fingers touching each other and bending down, and palm faces outward.\n" \
            "2. Bend your thumb into your palm and touch the " \
            "tips of the fingers above."
    r9c2 = Label(frame_tab2, text=textE, font=("Arial", 10), bg='#d9d9d9', fg='black', justify='left', anchor='w',
                 width=39, wraplength=300)
    r9c2.grid(row=9, column=2)

    textF = "Function: \n" \
            "This gesture is responsible for the letter ‘F’ key. " \
            "Use this gesture if you want to type letter ‘F’.\n\n" \
            "Gesture: \n" \
            "1. Hold your hand with your index finger and thumb " \
            "touching each other to form a circle, and palm face " \
            "outward.\n" \
            "2. Hold the other 3 fingers straight up and apart.\n" \
            "3. The space of the circle must be shown."
    r10c2 = Label(frame_tab2, text=textF, font=("Arial", 10), bg='#d9d9d9', fg='black', justify='left', anchor='w',
                  width=39, wraplength=300)
    r10c2.grid(row=10, column=2)

    textG = "Function: \n" \
            "This gesture is responsible for the letter ‘G’ key. " \
            "Use this gesture if you want to type letter ‘G’.\n\n" \
            "Gesture: \n" \
            "1. Hold your hand in a fist, with knuckles lined up " \
            "vertically and palm facing inward.\n" \
            "2. Keep your middle, ring, and little fingers curled " \
            "in, while your index finger and thumb stick out " \
            "parallel to each other."
    r11c2 = Label(frame_tab2, text=textG, font=("Arial", 10), bg='#d9d9d9', fg='black', justify='left', anchor='w',
                  width=39, wraplength=300)
    r11c2.grid(row=11, column=2)

    textH = "Function: \n" \
            "This gesture is responsible for the letter ‘H’ key. " \
            "Use this gesture if you want to type letter ‘H’.\n\n" \
            "Gesture: \n" \
            "1. Hold your hand horizontally, palm facing inward.\n" \
            "2. Place your index and middle fingers straight out " \
            "together and stack horizontally, index at the top.\n" \
            "3. The rest of the fingers and thumb are curled in."
    r12c2 = Label(frame_tab2, text=textH, font=("Arial", 10), bg='#d9d9d9', fg='black', justify='left', anchor='w',
                  width=39, wraplength=300)
    r12c2.grid(row=12, column=2)

    textI = "Function: \n" \
            "This gesture is responsible for the letter ‘I’ key. " \
            "Use this gesture if you want to type letter ‘I’.\n\n" \
            "Gesture: \n" \
            "1. Hold your hand in a fist and palm facing outward.\n" \
            "2. Place only your little finger up straight."
    r13c2 = Label(frame_tab2, text=textI, font=("Arial", 10), bg='#d9d9d9', fg='black', justify='left', anchor='w',
                  width=39, wraplength=300)
    r13c2.grid(row=13, column=2)

    textJ = "Function: \n" \
            "This gesture is responsible for the letter ‘J’ key. " \
            "Use this gesture if you want to type letter ‘J’.\n\n" \
            "Gesture: \n" \
            "1. Hold your hand open and palm facing outward.\n" \
            "2. Bend your index, middle, ring fingers straight " \
            "down, while your thumb and little finger stay up and " \
            "expand outward.\n" \
            "3. Rotate your hand 90 degrees counterclockwise to " \
            "make your thumb points to the left, the thumb is " \
            "slightly bent."
    r14c2 = Label(frame_tab2, text=textJ, font=("Arial", 10), bg='#d9d9d9', fg='black', justify='left', anchor='w',
                  width=39, wraplength=300)
    r14c2.grid(row=14, column=2)

    textK = "Function: \n" \
            "This gesture is responsible for the letter ‘K’ key. " \
            "Use this gesture if you want to type letter ‘K’.\n\n" \
            "Gesture: \n" \
            "1. Hold your index and middle fingers in a 'V' shape " \
            "and palm facing inward.\n" \
            "2. Rotate your hand 45 degrees counterclockwise.\n" \
            "3. Place your thumb between your index and middle " \
            "fingers.\n" \
            "4. The two remaining fingers are curled in and " \
            "touching your palm."
    r15c2 = Label(frame_tab2, text=textK, font=("Arial", 10), bg='#d9d9d9', fg='black', justify='left', anchor='w',
                  width=39, wraplength=300)
    r15c2.grid(row=15, column=2)

    textL = "Function: \n" \
            "This gesture is responsible for the letter ‘L’ key. " \
            "Use this gesture if you want to type letter ‘L’.\n\n" \
            "Gesture: \n" \
            "1. Hold your hand in a fist and palm facing outward.\n" \
            "2. Put your thumb and index fingers straight out, " \
            "index points up and thumb points left."
    r16c2 = Label(frame_tab2, text=textL, font=("Arial", 10), bg='#d9d9d9', fg='black', justify='left', anchor='w',
                  width=39, wraplength=300)
    r16c2.grid(row=16, column=2)

    textM = "Function: \n" \
            "This gesture is responsible for the letter ‘M’ key. " \
            "Use this gesture if you want to type letter ‘M’.\n\n" \
            "Gesture: \n" \
            "1. Hold your hand and palm facing outward, with " \
            "your index, middle, ring, and little fingers curled " \
            "into your palm.\n" \
            "2. Tuck your thumb between your ring and little " \
            "fingers.\n" \
            "3. Show your thumb out as much as possible."
    r17c2 = Label(frame_tab2, text=textM, font=("Arial", 10), bg='#d9d9d9', fg='black', justify='left', anchor='w',
                  width=39, wraplength=300)
    r17c2.grid(row=17, column=2)

    textN = "Function: \n" \
            "This gesture is responsible for the letter ‘N’ key. " \
            "Use this gesture if you want to type letter ‘N’.\n\n" \
            "Gesture: \n" \
            "1. Hold your hand and palm facing outward, with " \
            "your index, middle, ring, and little fingers curled " \
            "into your palm.\n" \
            "2. Tuck your thumb between your middle and ring " \
            "fingers.\n" \
            "3. Show your thumb out as much as possible."
    r18c2 = Label(frame_tab2, text=textN, font=("Arial", 10), bg='#d9d9d9', fg='black', justify='left', anchor='w',
                  width=39, wraplength=300)
    r18c2.grid(row=18, column=2)

    textO = "Function: \n" \
            "This gesture is responsible for the letter ‘O’ key. " \
            "Use this gesture if you want to type letter ‘O’.\n\n" \
            "Gesture: \n" \
            "1. Curve your hand like the letter ‘O’ with the top " \
            "4 fingers hold together forming the top curve and " \
            "the thumb forming the bottom curve.\n" \
            "2. Touch the top curve to the bottom curve to form " \
            "a circle.\n" \
            "3. The palm faces to the left."
    r19c2 = Label(frame_tab2, text=textO, font=("Arial", 10), bg='#d9d9d9', fg='black', justify='left', anchor='w',
                  width=39, wraplength=300)
    r19c2.grid(row=19, column=2)

    textP = "Function: \n" \
            "This gesture is responsible for the letter ‘P’ key. " \
            "Use this gesture if you want to type letter ‘P’.\n\n" \
            "Gesture: \n" \
            "1. Hold your hand in a fist and palm faces downward.\n" \
            "2. Place your index finger outward and middle finger " \
            "downward.\n" \
            "3. Place your thumb between the index and middle " \
            "fingers."
    r20c2 = Label(frame_tab2, text=textP, font=("Arial", 10), bg='#d9d9d9', fg='black', justify='left', anchor='w',
                  width=39, wraplength=300)
    r20c2.grid(row=20, column=2)

    textQ = "Function: \n" \
            "This gesture is responsible for the letter ‘Q’ key. " \
            "Use this gesture if you want to type letter ‘Q’.\n\n" \
            "Gesture: \n" \
            "1. Hold your hand in a fist and palm faces downward.\n" \
            "2. Stick your index finger and thumb out parallel to " \
            "each other and point downward, while keep your " \
            "middle, ring, and little fingers curled in."
    r21c2 = Label(frame_tab2, text=textQ, font=("Arial", 10), bg='#d9d9d9', fg='black', justify='left', anchor='w',
                  width=39, wraplength=300)
    r21c2.grid(row=21, column=2)

    textR = "Function: \n" \
            "This gesture is responsible for the letter ‘R’ key. " \
            "Use this gesture if you want to type letter ‘R’.\n\n" \
            "Gesture: \n" \
            "1. Hold your hand in a fist and palm faces outward.\n" \
            "2. Place your index and middle fingers up and " \
            "cross them."
    r22c2 = Label(frame_tab2, text=textR, font=("Arial", 10), bg='#d9d9d9', fg='black', justify='left', anchor='w',
                  width=39, wraplength=300)
    r22c2.grid(row=22, column=2)

    textS = "Function: \n" \
            "This gesture is responsible for the letter ‘S’ key. " \
            "Use this gesture if you want to type letter ‘S’.\n\n" \
            "Gesture: \n" \
            "1. Hold your hand in a fist and palm facing outward, " \
            "with all fingers curled into your palm."
    r23c2 = Label(frame_tab2, text=textS, font=("Arial", 10), bg='#d9d9d9', fg='black', justify='left', anchor='w',
                  width=39, wraplength=300)
    r23c2.grid(row=23, column=2)

    textT = "Function: \n" \
            "This gesture is responsible for the letter ‘T’ key. " \
            "Use this gesture if you want to type letter ‘T’.\n\n" \
            "Gesture: \n" \
            "1. Hold your hand and palm facing outward, with " \
            "your index, middle, ring, and little fingers curled " \
            "into your palm.\n" \
            "2. Tuck your thumb between your index and middle " \
            "fingers.\n" \
            "3. Show your thumb out as much as possible."
    r24c2 = Label(frame_tab2, text=textT, font=("Arial", 10), bg='#d9d9d9', fg='black', justify='left', anchor='w',
                  width=39, wraplength=300)
    r24c2.grid(row=24, column=2)

    textU = "Function: \n" \
            "This gesture is responsible for the letter ‘U’ key. " \
            "Use this gesture if you want to type letter ‘U’.\n\n" \
            "Gesture: \n" \
            "1. Hold your hand in a fist and palm facing outward.\n" \
            "2. Place your index and middle fingers straight up " \
            "and stick together."
    r25c2 = Label(frame_tab2, text=textU, font=("Arial", 10), bg='#d9d9d9', fg='black', justify='left', anchor='w',
                  width=39, wraplength=300)
    r25c2.grid(row=25, column=2)

    textV = "Function: \n" \
            "This gesture is responsible for the letter ‘V’ key. " \
            "Use this gesture if you want to type letter ‘V’.\n\n" \
            "Gesture: \n" \
            "1. Hold your hand in a fist and palm facing outward.\n" \
            "2. Place your index and middle fingers up and apart " \
            "to form a ‘V’ shape."
    r26c2 = Label(frame_tab2, text=textV, font=("Arial", 10), bg='#d9d9d9', fg='black', justify='left', anchor='w',
                  width=39, wraplength=300)
    r26c2.grid(row=26, column=2)

    textW = "Function: \n" \
            "This gesture is responsible for the letter ‘W’ key. " \
            "Use this gesture if you want to type letter ‘W’.\n\n" \
            "Gesture: \n" \
            "1. Hold your hand in a fist and palm facing outward.\n" \
            "2. Put your index, middle, and ring fingers out and " \
            "point straight up and apart to form a ‘W’ shape."
    r27c2 = Label(frame_tab2, text=textW, font=("Arial", 10), bg='#d9d9d9', fg='black', justify='left', anchor='w',
                  width=39, wraplength=300)
    r27c2.grid(row=27, column=2)

    textX = "Function: \n" \
            "This gesture is responsible for the letter ‘X’ key. " \
            "Use this gesture if you want to type letter ‘X’.\n\n" \
            "Gesture: \n" \
            "1. Hold your hand in a fist and palm facing the " \
            "left side.\n" \
            "2. Stick out your index finger and bend it into " \
            "a hook."
    r28c2 = Label(frame_tab2, text=textX, font=("Arial", 10), bg='#d9d9d9', fg='black', justify='left', anchor='w',
                  width=39, wraplength=300)
    r28c2.grid(row=28, column=2)

    textY = "Function: \n" \
            "This gesture is responsible for the letter ‘Y’ key. " \
            "Use this gesture if you want to type letter ‘Y’.\n\n" \
            "Gesture: \n" \
            "1. Hold your hand open and palm facing outward.\n" \
            "2. Bend your index, middle, ring fingers straight " \
            "down, while your thumb and little finger stay up and " \
            "expand outward."
    r29c2 = Label(frame_tab2, text=textY, font=("Arial", 10), bg='#d9d9d9', fg='black', justify='left', anchor='w',
                  width=39, wraplength=300)
    r29c2.grid(row=29, column=2)

    textZ = "Function: \n" \
            "This gesture is responsible for the letter ‘Z’ key. " \
            "Use this gesture if you want to type letter ‘Z’.\n\n" \
            "Gesture: \n" \
            "1. Hold your hand in a fist and palm facing outward.\n" \
            "2. Place your index and little fingers straight up."
    r30c2 = Label(frame_tab2, text=textZ, font=("Arial", 10), bg='#d9d9d9', fg='black', justify='left', anchor='w',
                  width=39, wraplength=300)
    r30c2.grid(row=30, column=2)

    text0 = "Function: \n" \
            "This gesture is responsible for the number ‘0’ key. " \
            "Use this gesture if you want to type number ‘0’.\n\n" \
            "Gesture: \n" \
            "1. Hold your hand open and palm faces to the left.\n" \
            "2. Stick your index, middle, ring and little fingers " \
            "together and bend down 90 degrees, keep them a " \
            "little curve.\n" \
            "3. Place and touch your thumb under the 4 fingers."
    r31c2 = Label(frame_tab2, text=text0, font=("Arial", 10), bg='#d9d9d9', fg='black', justify='left', anchor='w',
                  width=39, wraplength=300)
    r31c2.grid(row=31, column=2)

    text1 = "Function: \n" \
            "This gesture is responsible for the number ‘1’ key. " \
            "Use this gesture if you want to type number ‘1’.\n\n" \
            "Gesture: \n" \
            "1. Hold your hand in a fist and palm facing inward.\n" \
            "2. Place your index finger straight up."
    r32c2 = Label(frame_tab2, text=text1, font=("Arial", 10), bg='#d9d9d9', fg='black', justify='left', anchor='w',
                  width=39, wraplength=300)
    r32c2.grid(row=32, column=2)

    text2 = "Function: \n" \
            "This gesture is responsible for the number ‘2’ key. " \
            "Use this gesture if you want to type number ‘2’.\n\n" \
            "Gesture: \n" \
            "1. Hold your hand in a fist and palm facing inward.\n" \
            "2. Place your index and middle fingers straight up."
    r33c2 = Label(frame_tab2, text=text2, font=("Arial", 10), bg='#d9d9d9', fg='black', justify='left', anchor='w',
                  width=39, wraplength=300)
    r33c2.grid(row=33, column=2)

    text3 = "Function: \n" \
            "This gesture is responsible for the number ‘3’ key. " \
            "Use this gesture if you want to type number ‘3’.\n\n" \
            "Gesture: \n" \
            "1. Hold your hand in a fist and palm facing inward.\n" \
            "2. Take your thumb, index and middle fingers out."
    r34c2 = Label(frame_tab2, text=text3, font=("Arial", 10), bg='#d9d9d9', fg='black', justify='left', anchor='w',
                  width=39, wraplength=300)
    r34c2.grid(row=34, column=2)

    text4 = "Function: \n" \
            "This gesture is responsible for the number ‘4’ key. " \
            "Use this gesture if you want to type number ‘4’.\n\n" \
            "Gesture: \n" \
            "1. Hold your hand in a fist and palm facing inward.\n" \
            "2. Place your index, middle, ring, and little " \
            "fingers straight up."
    r35c2 = Label(frame_tab2, text=text4, font=("Arial", 10), bg='#d9d9d9', fg='black', justify='left', anchor='w',
                  width=39, wraplength=300)
    r35c2.grid(row=35, column=2)

    text5 = "Function: \n" \
            "This gesture is responsible for the number ‘5’ key. " \
            "Use this gesture if you want to type number ‘5’.\n\n" \
            "Gesture: \n" \
            "1. Hold your hand open and palm facing inward."
    r36c2 = Label(frame_tab2, text=text5, font=("Arial", 10), bg='#d9d9d9', fg='black', justify='left', anchor='w',
                  width=39, wraplength=300)
    r36c2.grid(row=36, column=2)

    text6 = "Function: \n" \
            "This gesture is responsible for the number ‘6’ key. " \
            "Use this gesture if you want to type number ‘6’.\n\n" \
            "Gesture: \n" \
            "1. Hold your hand open and palm facing inward.\n" \
            "2. Bend your index, middle, ring fingers straight " \
            "down, while your thumb and little finger stay up " \
            "and expand outward."
    r37c2 = Label(frame_tab2, text=text6, font=("Arial", 10), bg='#d9d9d9', fg='black', justify='left', anchor='w',
                  width=39, wraplength=300)
    r37c2.grid(row=37, column=2)

    text7 = "Function: \n" \
            "This gesture is responsible for the number ‘7’ key. " \
            "Use this gesture if you want to type number ‘7’.\n\n" \
            "Gesture: \n" \
            "1. Hold your hand open and palm facing outward.\n" \
            "2. Touch your thumb and ring finger together, the " \
            "ring finger lays flat without any bend (slightly " \
            "curved is acceptable).\n" \
            "3. Index, middle, and little fingers stay straight up."
    r38c2 = Label(frame_tab2, text=text7, font=("Arial", 10), bg='#d9d9d9', fg='black', justify='left', anchor='w',
                  width=39, wraplength=300)
    r38c2.grid(row=38, column=2)

    text8 = "Function: \n" \
            "This gesture is responsible for the number ‘8’ key. " \
            "Use this gesture if you want to type number ‘8’.\n\n" \
            "Gesture: \n" \
            "1. Hold your hand open and palm facing outward.\n" \
            "2. Touch your thumb and middle finger together, " \
            "the middle finger lays flat without any bend " \
            "(slightly curved is acceptable).\n" \
            "3. Index, ring and little fingers stay straight up."
    r39c2 = Label(frame_tab2, text=text8, font=("Arial", 10), bg='#d9d9d9', fg='black', justify='left', anchor='w',
                  width=39, wraplength=300)
    r39c2.grid(row=39, column=2)

    text9 = "Function: \n" \
            "This gesture is responsible for the number ‘9’ key. " \
            "Use this gesture if you want to type number ‘9’.\n\n" \
            "Gesture: \n" \
            "1. Hold your hand open and palm facing outward.\n" \
            "2. Touch your thumb and index finger together " \
            "and face to the front, the index finger lays flat " \
            "without any bend (slightly curved is acceptable).\n" \
            "3. Middle, ring and little fingers stay straight up."
    r40c2 = Label(frame_tab2, text=text9, font=("Arial", 10), bg='#d9d9d9', fg='black', justify='left', anchor='w',
                  width=39, wraplength=300)
    r40c2.grid(row=40, column=2)

    textUp = "Function: \n" \
             "This gesture is responsible for the keyboard’s " \
             "up-arrow key. Use this gesture if you want to move " \
             "the cursor into a up direction.\n\n" \
             "Gesture: \n" \
             "1. Hold your hand into a thumb up gesture and palm " \
             "facing inward.\n" \
             "2. The thumb points upward and the other 4 fingers " \
             "are curled in."
    r41c2 = Label(frame_tab2, text=textUp, font=("Arial", 10), bg='#d9d9d9', fg='black', justify='left', anchor='w',
                  width=39, wraplength=300)
    r41c2.grid(row=41, column=2)

    textDown = "Function: \n" \
               "This gesture is responsible for the keyboard’s " \
               "down-arrow key. Use this gesture if you want to move " \
               "the cursor into a down direction.\n\n" \
               "Gesture: \n" \
               "1. Hold your hand into a thumb up gesture where the " \
               "thumb points upward.\n" \
               "2. Invert your hand to make your palm facing outward " \
               "and your thumb pointing downward."
    r42c2 = Label(frame_tab2, text=textDown, font=("Arial", 10), bg='#d9d9d9', fg='black', justify='left', anchor='w',
                  width=39, wraplength=300)
    r42c2.grid(row=42, column=2)

    textLeft = "Function: \n" \
               "This gesture is responsible for the keyboard’s " \
               "left-arrow key. Use this gesture if you want to move " \
               "the cursor into a left direction.\n\n" \
               "Gesture: \n" \
               "1. Hold your hand in a fist and palm facing outward.\n" \
               "2. Stick out your thumb and point to the left side."
    r43c2 = Label(frame_tab2, text=textLeft, font=("Arial", 10), bg='#d9d9d9', fg='black', justify='left', anchor='w',
                  width=39, wraplength=300)
    r43c2.grid(row=43, column=2)

    textRight = "Function: \n" \
                "This gesture is responsible for the keyboard’s " \
                "right-arrow key. Use this gesture if you want to " \
                "move the cursor into a right direction.\n\n" \
                "Gesture: \n" \
                "1. Hold your hand into a thumb up gesture where " \
                "the thumb points upward and palm facing inward.\n" \
                "2. Rotate your hand 90 degrees clockwise to make " \
                "your thumb pointing to the right."
    r44c2 = Label(frame_tab2, text=textRight, font=("Arial", 10), bg='#d9d9d9', fg='black', justify='left', anchor='w',
                  width=39, wraplength=300)
    r44c2.grid(row=44, column=2)

    textSpace = "Function: \n" \
                "This gesture is responsible for the keyboard’s " \
                "space bar. Use this gesture if the space bar is " \
                "needed or you want to put a space into something " \
                "while typing.\n\n" \
                "Gesture: \n" \
                "1. Hold your hand in a fist, with knuckles lined up " \
                "vertically and palm facing inward.\n" \
                "2. Place your thumb out straight and point upward.\n" \
                "3. Place your index finger out straight and point to " \
                "the left.\n" \
                "4. Keep your middle, ring and little fingers curled in."
    r45c2 = Label(frame_tab2, text=textSpace, font=("Arial", 10), bg='#d9d9d9', fg='black', justify='left', anchor='w',
                  width=39, wraplength=300)
    r45c2.grid(row=45, column=2)

    textBackspace = "Function: \n" \
                    "This gesture is responsible for the keyboard’s " \
                    "backspace key. Use this gesture if you want to " \
                    "delete any character.\n\n" \
                    "Gesture: \n" \
                    "1. Hold your hand in a fist, with knuckles lined up " \
                    "vertically and palm facing inward.\n" \
                    "2. Place your thumb out straight and point upward.\n" \
                    "3. Place your index and middle fingers out straight " \
                    "and point to the left.\n" \
                    "4. Keep your ring and little fingers curled in."
    r46c2 = Label(frame_tab2, text=textBackspace, font=("Arial", 10), bg='#d9d9d9', fg='black', justify='left',
                  anchor='w', width=39, wraplength=300)
    r46c2.grid(row=46, column=2)

    textEnter = "Function: \n" \
                "This gesture is responsible for the keyboard’s " \
                "enter key. Use this gesture if you want to add " \
                "next line or return control to a running program.\n\n" \
                "Gesture: \n" \
                "1. Hold your hand in a fist, with knuckles lined up " \
                "vertically and palm facing outward.\n" \
                "2. Place your thumb out straight and point upward.\n" \
                "3. Place your index and middle fingers out straight " \
                "and point to the right.\n" \
                "4. Keep your ring and little fingers curled in."
    r47c2 = Label(frame_tab2, text=textEnter, font=("Arial", 10), bg='#d9d9d9', fg='black', justify='left', anchor='w',
                  width=39, wraplength=300)
    r47c2.grid(row=47, column=2)

    textCapsLock = "Function: \n" \
                   "This gesture is responsible for the keyboard’s " \
                   "caps lock key. Use this gesture if you want to turn " \
                   "on/off the caps lock key.\n\n" \
                   "Gesture: \n" \
                   "1. Hold your hand in a fist, with knuckles lined up " \
                   "vertically and palm facing outward.\n" \
                   "2. Place your thumb up straight.\n" \
                   "3. Place your index finger out straight and point to " \
                   "the right.\n" \
                   "4. Keep your middle, ring and little fingers curled in."
    r48c2 = Label(frame_tab2, text=textCapsLock, font=("Arial", 10), bg='#d9d9d9', fg='black', justify='left',
                  anchor='w', width=39, wraplength=300)
    r48c2.grid(row=48, column=2)

    # Tab 3
    title_tab3 = Label(tab3, text='About', font=("Arial", 18), bg='#d9d9d9', justify='left')
    title_tab3.pack(pady=(15, 0), padx=(15, 0), anchor='w')

    textTab3 = "Hand Gesture Recognition System is a system that allows users to use hand gestures to control and" \
               " interact with the computer without external devices. The main goal of this project is to build a " \
               "direct and natural intuitive Human Computer Interaction (HCI) that does not rely on traditional input" \
               " devices such as Mouse and Keyboard. The traditional human-computer interaction system has created a " \
               "gap between human and computer, and is gradually inapplicable in some fields. I hope to build a new " \
               "HCI system that can bridge the gap between human and computer and can also be applied to any field. " \
               "This project requires a webcam to function. The functions that the system can perform are limited. " \
               "The gestures for all functions have also been provided. See the Gesture Guideline page for " \
               "more information."
    content_tab3 = Label(tab3, text=textTab3, font=("Arial", 10), bg='#d9d9d9', justify='left', wraplength=500)
    content_tab3.pack(pady=(15, 0), padx=(15, 0), anchor='w')

    root.mainloop()


if __name__ == '__main__':
    main()
