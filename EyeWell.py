from customtkinter import *
from datetime import datetime
import re
import pygame
import time
from plyer import notification
import os
from PIL import Image, ImageTk
import json
import threading
import sys

delay = 30
# default value of delay
selectedRadioBtn = False
# default value of radioBtn

reMin = "Reminder!"
reMsg = "Time to take a break from screen!"
reMsg_Stripped = reMsg.replace(" ", "")
AllFont = "SF PRO display regular"
fontSize = 15.8


os.chdir(os.path.dirname(os.path.abspath(__file__)))


app = CTk(fg_color="#0f0f0f")
app.title("EyeWell")
app.geometry("560x360")
app.resizable(False, False)
# app.after(201, lambda : app.iconbitmap(r"2330.ico"))
icon_img = Image.open("Final.png")
icon_tk = ImageTk.PhotoImage(icon_img)
# setting icon of the app

app.tk.call("wm", "iconphoto", app._w, icon_tk)
app.iconphoto(False, icon_tk)
app.iconbitmap("Final.ico")
# deactivate_automatic_dpi_awareness()
app.protocol("WM_DELETE_WINDOW", sys.exit)
# if Clicked on exit by main window then it gonna trigger sys.exit()

app_data_dir = os.path.join(os.getenv("APPDATA"), "EyeWell")


# creates/access a dir named 'EyeWell' in the AppData directory
def appDataCreation():
    global app_data_dir
    if not os.path.exists(app_data_dir):
        os.makedirs(app_data_dir)
        # function to create the app data directory


set_window_scaling(1)


user_data_file = os.path.join(app_data_dir, "user_data.json")
# creates a file named 'user_data.json' for retrieving data in the EyeWell directory
file_path = ""


def check_Entry():
    global reMin, entry
    checkEntry = (entry.get()).strip()
    checkEntry2 = checkEntry.replace(" ", "")
    # strips all the entry fields and removes all spaces to check for empty spaces and default reminder Title
    if checkEntry2 == "" or checkEntry2 == reMin:
        DefaultTxt()
        # gonna set the reminder title to default if it's empty or default on strip
        return reMin
    else:
        return entry.get()


def check_Entry2():
    global reMsg, MsgEntry
    checkEntry = (MsgEntry.get()).strip()
    checkEntry2 = checkEntry.replace(" ", "")
    # strips all the entry fields and removes all spaces to check for empty spaces and default reminder message
    if checkEntry2 == "" or checkEntry2 == reMsg_Stripped:
        DefaultTxt2()
        # gonna set the reminder message to default if it's empty or default on strip
        return reMsg
    else:
        return MsgEntry.get()


def DefaultTxt():
    entry.delete(0, END)
    entry.insert(0, reMin)
    # defaulting the entry field to the default reminder message(reMin)


def DefaultTxt2():
    global reMsg
    MsgEntry.delete(0, END)
    MsgEntry.insert(0, reMsg)
    # defaulting the MsgEntry field to the default reminder message(reMsg)


def switch_callback():
    global entry, label3
    state = TitSwitch.get()
    # gonna get state of TitSwitch(title switch)
    if state == True:
        disabledEntry()
        # disables the entry of First Entry(title field/entry) if switch is checked
    else:
        enabledEntry()
        # enables the entry of First Entry(title field/entry) if switch is unchecked
    return


def disabledEntry():
    global entry, label3
    check_Entry()
    # checks the entry of Title field/entry
    entry.configure(state="disabled", text_color="grey", placeholder_text=reMin)
    label3.configure(text_color="grey")


def enabledEntry():
    global entry, label3
    entry.configure(state="normal", text_color="white")
    label3.configure(text_color="White")


def disabledEntry2():
    global MsgEntry, customMsg
    check_Entry2()
    # checks the entry of reminder message field/entry
    MsgEntry.configure(state="disabled", text_color="grey", placeholder_text=reMin)
    customMsg.configure(text_color="grey")


def enabledEntry2():
    global MsgEntry, customMsg
    MsgEntry.configure(state="normal", text_color="white")
    customMsg.configure(text_color="White")


def switch_callback2():
    global MsgEntry
    state = MsgSwitch.get()

    if state == True:
        disabledEntry2()
        # disables the entry of reminder message field if the switch is checked
    else:
        enabledEntry2()
        # enables the entry of reminder message field if the switch is unchecked
    return


def charlimit(*args):
    global entry_var
    # basically a character limiter function to tackle error of exceeding the character limit
    if len(entry_var.get()) > 64:
        entry_var.set(entry_var.get()[:64])
        # gonna stop the user from entering more than 64 characters
        # by limiting the input to 64


def charlimit1(*args):
    # same as charlimit()
    global MsgEntry_var
    if len(MsgEntry_var.get()) > 64:
        MsgEntry_var.set(MsgEntry_var.get()[:64])


def KeepCallBack():
    global KeepSwitch
    global keepSwitchState
    keepSwitchState = KeepSwitch.get()
    if keepSwitchState == True:
        disabled()
        disabled_Op()
        # gonna disable the time range function and label if KeepSwitch is checked
        return True
    else:
        enabled()
        enabled_Op()
        # gonna enable the time range function and label if KeepSwitch is unchecked
        return False


def slider_callback(Val):
    global delayRem
    delayRem = int(Val)
    label1.configure(text=f"Remind me, every {delayRem} minutes")
    return Val


def finalTitle():
    if TitSwitch.get() == True:
        return reMin
    else:
        if check_Entry() != False:
            return entry.get()
        else:
            return None


def finalMsg():
    if MsgSwitch.get() == True:
        return reMsg
    else:
        if check_Entry2() != False:
            return MsgEntry.get()
        else:
            return reMsg


def browse_file():
    try:
        file_path = filedialog.askopenfilename(
            title="Select an Audio File",
            filetypes=[("Audio Files", "*.wav *.mp3 *.ogg")],
        )
        # gonna trigger file dialog box which gonna import the location of audio file
        if file_path:
            if os.path.isfile(file_path):
                return file_path
            else:
                AudLabelFail()
        else:
            return None
    except Exception as e:
        return None


checkFile = False


def finalFile():
    global file_path, checkFile, BtnCheck
    BtnCheck = False
    toggle_icon()
    file_path = browse_file()  # Use your `browse_file()` function

    if not file_path and selectedRadioBtn == True:
        AudLabelFail()
        # error_label.place(x=425, y=y_4-2)
        return None
    else:
        # Clear the error label if a valid file is selected
        if selectedRadioBtn == True:
            AudLabelSuccess()
            return file_path
        else:
            return None


def AudLabelSuccess():
    global checkFile
    file_label.configure(text="Audio File\nSelected!")
    # if audio imports successfully it would show this text
    error_label.configure(text="")
    activeVol()
    # gonna unhide the custom volume slider and play button
    playNewAudio(file_path)
    # gonna start playing audio from file_path location
    checkFile = True
    # gonna update checkFile variable to tackle the issue of multiple file selection


def AudLabelFail():
    global checkFile
    NoAudio()
    error_label.configure(text="*No valid file selected.\nPlease try again.")
    # if audio didn't imports after fileSelection popup dialogbox it would show this text
    file_label.configure(text="")
    checkFile = False


def AudLabelClear():
    error_label.configure(text="")
    file_label.configure(text="")
    unActiveVol()


def HideBtn():
    global selectedRadioBtn
    Btn.place_forget()
    selectedRadioBtn = False
    AudLabelClear()


def unHideBtn():
    global selectedRadioBtn
    Btn.place(x=378, y=y_4 - 1)
    selectedRadioBtn = True


def timeFor():
    fromTime = UserSelection1()
    fromFormat = UserSelection2()
    toTime = UserSelection3()
    toFormat = UserSelection4()

    final_from = f"{fromTime} {fromFormat}"
    final_to = f"{toTime} {toFormat}"
    # converts the time 'from' and 'to' TO actual usable time format
    return final_from, final_to
    # returns the value of 'from' and 'to' time in usable format


def TimeSlot():
    TimeSlot = []
    for i in range(1, 13):
        time = f"{i}:00"
        TimeSlot.append(time)
        # easy way to add time range in option
    return TimeSlot


def InitAudio():
    global file_path
    pygame.mixer.init()
    # initializes the pygame mixer module for further playmusic on command
    if file_path:
        FinalAud = pygame.mixer.Sound(file_path)
        return FinalAud


def playAudio():
    FinalAud = InitAudio()
    pygame.mixer.music.stop()
    FinalAud.set_volume((slider2.get()) * 0.01)
    if FinalAud:
        FinalAud.play()
    else:
        return False


def playNewAudio(file_path):
    global BtnCheck, trigg
    pygame.mixer.music.stop()
    # stopping the old audio file
    pygame.mixer.music.load(file_path)
    BtnCheck = False
    # basically pause button when imported new audio file
    toggle_icon()
    trigg = False
    # so the trigg var in button can have chance to run again


def NoAudio():
    global BtnCheck
    pygame.mixer.music.stop()
    unActiveVol()
    # gonna stop the music and hide the control volume slider and play btn


def is_time_between():
    start_time, end_time = timeFor()
    # gonna retrieve values from timeFor() function which is basically dropdown options's values in hour and mins
    current_time = datetime.now().strftime("%I:%M %p")
    current_time_real = datetime.strptime(current_time, "%I:%M %p")

    start_time_real = datetime.strptime(start_time, "%I:%M %p")
    end_time_real = datetime.strptime(end_time, "%I:%M %p")

    if end_time_real < start_time_real:
        return (
            current_time_real >= start_time_real or current_time_real <= end_time_real
        )
    else:
        return start_time_real <= current_time_real <= end_time_real


shiftY = 12


def mainY(Y, shiftY):
    Y -= shiftY
    return Y
    # to shift the all the buttons and elements up just by single cmd


def Label1():
    global y_1
    y_1 = 21
    # LABEL 1
    global label1, slider
    y_1 = mainY(y_1, shiftY) + 2
    # y_1 is main y level value for all elements in Label1()
    # SAME IN OTHER LABELS TOO
    # SLIDER

    slider = CTkSlider(master=app, from_=5, to=60, command=slider_callback)
    slider.configure(width=270, number_of_steps=11)
    slider.set(25)
    slider.place(x=243, y=y_1 + 7)
    label1 = CTkLabel(
        app,
        text=f"Remind me, every {int(slider.get())} minutes",
        font=(AllFont, 16.5),
        width=100,
    )
    label1.place(x=20, y=y_1)
    return label1


def Label2():
    global y_2
    y_2 = 55
    # LABEL 2
    global TitSwitch
    y_2 = mainY(y_2, shiftY)
    label2 = CTkLabel(
        app, text="Use Default Title For Notification: ", font=(AllFont, fontSize)
    )
    label2.place(x=20, y=y_2)
    # TITLE SWITCH
    TitSwitch = CTkSwitch(
        master=app, text="", command=switch_callback, switch_width=43, switch_height=20
    )
    TitSwitch.select()
    TitSwitch.place(x=257, y=y_2 + 3)


def Label3():
    global entry, label3, MsgEntry, MsgSwitch, customMsg, y_3, entry_var, MsgEntry_var
    y_3 = 93
    y_3 = mainY(y_3, shiftY)
    # LABEL 3
    label3 = CTkLabel(app, text="Custom Title: ", font=(AllFont, 16), text_color="grey")
    label3.place(x=20, y=y_3 - 4.5)

    # CUSTOM TITLE TEXT INPUT
    entry_var = StringVar()
    entry_var.trace_add("write", charlimit)

    entry = CTkEntry(
        master=app,
        textvariable=entry_var,
        placeholder_text=reMin,
        width=425,
        corner_radius=4,
        fg_color=("White", "Black"),
        height=32,
        border_color="Black",
        font=(AllFont, 14),
    )
    entry.place(x=118, y=y_3 - 4)
    entry.insert(0, reMin)
    entry.configure(text_color="grey")
    entry.configure(state="disabled")

    MsgLabel = CTkLabel(
        app, text="Default Message For Notification: ", font=(AllFont, fontSize)
    )
    MsgLabel.place(x=20, y=y_3 + 35)
    MsgEntry_var = StringVar()

    MsgSwitch = CTkSwitch(
        master=app, text="", command=switch_callback2, switch_width=43, switch_height=20
    )
    MsgSwitch.select()
    MsgSwitch.place(x=260, y=y_3 + 38)

    # LABEL Msg
    customMsg = CTkLabel(
        app, text="Custom Message: ", font=(AllFont, 15.5), text_color="grey"
    )
    customMsg.place(x=20, y=y_3 + 72)
    # BASICALLY placing customMsg label at the same position as the entry
    # TEXT INPUT
    MsgEntry = CTkEntry(
        master=app,
        textvariable=MsgEntry_var,
        placeholder_text=reMsg,
        width=395,
        corner_radius=4,
        fg_color=("White", "Black"),
        height=30,
        border_color="Black",
        font=(AllFont, 14),
    )
    MsgEntry.place(x=150, y=y_3 + 72)
    MsgEntry.insert(0, reMsg)
    MsgEntry.configure(text_color="grey")
    MsgEntry.configure(state="disabled")

    return entry_var, MsgEntry_var


def Label4():
    global BtnWdth, BtnHeigth, y_4, select_option
    BtnWdth = 20
    BtnHeigth = 10
    y_4 = 206
    y_4 = mainY(y_4, shiftY)
    global label4
    global sound_label, Btn, None_Var
    global error_label, file_label
    Btn = CTkButton(
        app,
        text="Choose..",
        command=finalFile,
        corner_radius=5,
        font=(AllFont, fontSize),
        width=BtnWdth,
        height=BtnHeigth,
    )

    label4 = CTkLabel(app, text="Play Sound: ", font=(AllFont, fontSize))
    label4.place(x=20, y=y_4 - 3)

    select_option = StringVar(value="None")

    None_Var = CTkRadioButton(
        app,
        text="None",
        command=HideBtn,
        font=(AllFont, fontSize),
        variable=select_option,
        value="None",
    )
    None_Var.place(x=125, y=y_4)

    Custom_var = CTkRadioButton(
        app,
        text="Custom",
        font=(AllFont, fontSize),
        command=unHideBtn,
        variable=select_option,
        value="Custom",
    )
    Custom_var.place(x=278, y=y_4)
    error_label = CTkLabel(app, text="", font=(AllFont, 10), text_color="grey")
    error_label.place(x=455, y=y_4 - 2)
    file_label = CTkLabel(app, text="", font=(AllFont, 11), text_color="grey")
    file_label.place(x=458, y=y_4 - 3)


def Label5():
    global y_5
    y_5 = 239
    y_5 = mainY(y_5, shiftY)
    global KeepSwitch
    label5 = CTkLabel(app, text="Keep It Running(Always):", font=(AllFont, fontSize))
    label5.place(x=20, y=y_5)
    KeepSwitch = CTkSwitch(
        master=app, text="", command=KeepCallBack, switch_width=43, switch_height=20
    )
    KeepSwitch.select()
    KeepSwitch.place(x=200, y=y_5 + 4)


def UserSelection1():
    selectedVal = fromdropDown1.get()
    # gonna get userselection from fromdropDown1
    return selectedVal


def UserSelection2():
    selectedVal = fromdropDown2.get()
    # gonna get userselection from fromdropDown2
    return selectedVal


def UserSelection3():
    selectedVal = toDropDown1.get()
    # gonna get userselection from toDropDown1
    return selectedVal


def UserSelection4():
    selectedVal = toDropDown2.get()
    # gonna get userselection from toDropDown2
    return selectedVal


def Label6():
    global TimeSlot, fromdropDown1, fromdropDown2, toDropDown1, toDropDown2, label6, y_6, label7
    TimeSlot = TimeSlot()
    y_6 = 277
    y_6 = mainY(y_6, shiftY)
    fromdropDown1 = CTkOptionMenu(
        app,
        values=TimeSlot,
        width=70,
        corner_radius=4,
        fg_color="black",
        button_color="black",
        button_hover_color="grey",
        font=(AllFont, fontSize),
        state="disabled",
        command=lambda _: UserSelection1(),
    )
    fromdropDown1.place(x=135, y=y_6)
    # placing the dropdown menu
    fromdropDown2 = CTkOptionMenu(
        app,
        values=["AM", "PM"],
        width=30,
        corner_radius=4,
        fg_color="black",
        button_color="black",
        button_hover_color="grey",
        font=(AllFont, fontSize),
        state="disabled",
        command=lambda _: UserSelection2(),
    )
    fromdropDown2.place(x=210, y=y_6)

    toDropDown1 = CTkOptionMenu(
        app,
        values=TimeSlot,
        width=70,
        corner_radius=4,
        fg_color="black",
        button_color="black",
        button_hover_color="grey",
        font=(AllFont, fontSize),
        state="disabled",
        command=lambda _: UserSelection3(),
    )
    toDropDown1.place(x=307, y=y_6)

    toDropDown2 = CTkOptionMenu(
        app,
        values=["AM", "PM"],
        width=30,
        corner_radius=4,
        fg_color="black",
        button_color="black",
        button_hover_color="grey",
        font=(AllFont, fontSize),
        state="disabled",
        command=lambda _: UserSelection4(),
    )
    toDropDown2.place(x=379, y=y_6)
    label6 = CTkLabel(
        app, text="Custom Time: ", font=(AllFont, fontSize), text_color=("grey", "grey")
    )
    label6.place(x=18, y=y_6)
    label7 = CTkLabel(app, text="to", font=(AllFont, 16), text_color=("grey", "grey"))
    label7.place(x=280, y=y_6)
    disabled()
    # it's disabled by default tho


def enabled():
    global label6, label7
    label6.configure(text_color="white")
    label7.configure(text_color="white")


def disabled():
    global label6, label7
    label6.configure(text_color="grey")
    label7.configure(text_color="grey")


def disabled_Op():
    fromdropDown1.configure(state="disabled")
    fromdropDown2.configure(state="disabled")
    toDropDown1.configure(state="disabled")
    toDropDown2.configure(state="disabled")


def enabled_Op():
    fromdropDown1.configure(state="enabled")
    fromdropDown2.configure(state="enabled")
    toDropDown1.configure(state="enabled")
    toDropDown2.configure(state="enabled")


FinalAud1 = InitAudio()


def PlayAudioLoop():
    global FinalAud1, music
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.set_volume((slider2.get()) * 0.01)
    # gonna adjust the volume by multiplying slider's value * 0.01 to get actual percentage of volume
    if file_path:
        pygame.mixer.music.play(-1)
        # gonna play in loop
    else:
        return


def Preview():
    global BtnCheck

    if not BtnCheck:
        playAudio()
        # if pausebutton is not active, play audio
    pass


def slider2_call(Var):
    # Main 'Var' in parameter is value given by slider
    global ValOfSlider2
    ValOfSlider2 = int(Var)
    pygame.mixer.music.set_volume(ValOfSlider2 * 0.01)
    label8.configure(text=f"{ValOfSlider2}%")
    return ValOfSlider2


BtnCheck = True  # to get the button to work like toggle command
trigg = False  # temprorary thing just make sure the condition works only 1 time


def toggle_icon():
    global BtnCheck, trigg
    if BtnCheck:
        if not trigg:
            PlayAudioLoop()
            trigg = True
            button.configure(
                text="⏸",
                fg_color=SaveBtn._fg_color,
                font=(AllFont, 14.6),
                height=26,
                width=27,
            )
            BtnCheck = False
        if file_path:
            pygame.mixer.music.unpause()
            button.configure(
                text="⏸",
                fg_color=SaveBtn._fg_color,
                font=(AllFont, 14.6),
                height=26,
                width=27,
            )
            BtnCheck = False
            return False
    else:
        if file_path:
            pygame.mixer.music.pause()
        button.configure(
            text="▶", fg_color="green", font=(AllFont, 18), height=23, width=27
        )
        BtnCheck = True
        return True


def activeVol():
    if selectedRadioBtn:
        slider2.place(x=270, y=235)
        label8.place(x=517, y=230)
        button.place(x=515, y=192)
        # if selectedRadioBtn(checking if audio file is loaded) is true then this menu would work


def unActiveVol():
    slider2.place_forget()
    label8.place_forget()
    button.place_forget()
    # basically hiding all these slider2,label8,button


def Label7():
    global slider2, label8, button

    slider2 = CTkSlider(master=app, from_=0, to=100, command=slider2_call)
    slider2.configure(width=246, number_of_steps=101)
    label8 = CTkLabel(app, text=f"{int(slider2.get())}%", font=(AllFont, 17))
    button = CTkButton(
        master=app,
        text="▶",
        font=(AllFont, 18),
        command=toggle_icon,
        width=31,
        height=23,
        corner_radius=3.4,
        fg_color="green",
    )


def SaveData():
    global data
    if not os.path.exists(app_data_dir):
        print(app_data_dir)
        os.makedirs(app_data_dir)
    data = {
        "entry": entry.get(),
        "MsgEntry": MsgEntry.get(),
        "Slider": slider.get(),
        "TitSwitch": TitSwitch.get(),
        "MsgSwitch": MsgSwitch.get(),
        "KeepSwitch": KeepSwitch.get(),
        "radioBtn": checkAud(),
        "filepath": file_path,
        "FromMenu1": UserSelection1(),
        "FromMenu2": UserSelection2(),
        "ToMenu1": UserSelection3(),
        "ToMenu2": UserSelection4(),
        "Volume": slider2.get(),
    }
    # basically saving the data in user_data.json in the app_data_dir
    finalData = json.dumps(data)
    # dumping the data into the json file
    print(user_data_file)
    with open(user_data_file, "w") as f:
        f.write(finalData)
        # writing the data
    return data


def LoadData():
    global selectedRadioBtn, file_path, entry, MsgEntry, slider, KeepSwitch, select_option, fromdropDown1, fromdropDown2, toDropDown1, toDropDown2, file_pathAAH

    def SwitchFunc(SwitchInDict, SwitchInVar):
        if data.get(SwitchInDict) == True:
            SwitchInVar.select()
            # gonna select the switch if it is True in the data
            # just by input of the switch name from json and the variable name
            return True
        else:
            SwitchInVar.deselect()
            return False

    if os.path.isfile(user_data_file):
        with open(user_data_file, "r") as f:
            data = json.load(f)
            SwitchFunc("MsgSwitch", MsgSwitch)
            SwitchFunc("TitSwitch", TitSwitch)
            SwitchFunc("KeepSwitch", KeepSwitch)
            # retrieving the data from the json file
            if SwitchFunc("TitSwitch", TitSwitch) == False:
                if data.get("entry") == "" or data.get("entry") == reMin:
                    disabledEntry()
                    TitSwitch.select()
                    # if text in entry is empty or at default
                else:
                    enabledEntry()
            if SwitchFunc("MsgSwitch", MsgSwitch) == False:
                if data.get("MsgEntry") == "" or data.get("MsgEntry") == reMsg:
                    disabledEntry2()
                    MsgSwitch.select()
                    # if text in Msgentry is empty or at default
                else:
                    enabledEntry2()

            if data.get("radio") == "None" or data.get("radio") == "null":
                select_option.set("None")
            else:
                select_option.set("Custom")
                selectedRadioBtn = True
                unHideBtn()
            if data.get("filepath") != "":
                file_path = data.get("filepath")
                unHideBtn()
                AudLabelSuccess()
            if SwitchFunc("KeepSwitch", KeepSwitch) == False:
                enabled()
                enabled_Op()
                # gonna enable the menu and custom label if the keepSwitch is off otherwise by default it's on
            entry.delete(0, END)
            MsgEntry.delete(0, END)
            # gonna delete default texts from entry fields
            entry.insert(0, data.get("entry"))
            MsgEntry.insert(0, (data.get("MsgEntry")))
            # gonna insert the data from the json file into the entry fields
            slider.set((data.get("Slider")))
            slider2.set((data.get("Volume")))
            label1.configure(text=f"Remind me, every {int(slider.get())} minutes")
            label8.configure(text=f"{int(slider2.get())}%")
            # changing the labels according to value of sliders loaded from json file
            fromdropDown1.set(data.get("FromMenu1"))
            fromdropDown2.set(data.get("FromMenu2"))
            toDropDown1.set(data.get("ToMenu1"))
            toDropDown2.set(data.get("ToMenu2"))
            # gonna set the values of dropdown menus according to the data from the json file
    else:
        return False


# START
def Save_():
    global delay, CusTit, CusMsg, logic_thread, status
    check_Entry()
    check_Entry2()
    SaveData()
    CusTit = finalTitle()
    CusMsg = finalMsg()
    delay = int(slider.get())
    logic_thread = threading.Thread(target=logic, daemon=True)
    status = True
    logic_thread.start()
    return delay, CusTit, CusMsg


def Checker_Msg(Message):
    newMsg = Message.strip()
    if newMsg != "":
        return True
    else:
        return False


def finalMessage(Message):
    if Checker_Msg(Message):
        return Message
    else:
        return "Time to take a break from screen!"
    # default message if msg is empty


def Reminder(Title, Message):
    notification.notify(
        title=Title,
        message=finalMessage(Message),
        app_name="EyeWell",
        timeout=10,  # Duration in seconds
    )


def main(CusTit, CusMsg):

    Title = CusTit
    Message = CusMsg
    Reminder(Title, Message)


def MainLoop(CusTit, CusMsg, delay):
    if checkAud() == True:
        playAudio()
    main(CusTit, CusMsg)
    for i in range(delay):
        time.sleep(60)
        # if delay(in mains ofc) is 1, it will run 1 time, if 2, 2 times, etc
        # good conversion right? lol


def checkAud():
    global file_path
    # i made two vars 'selectedRadioBtn' and 'checkFile' because of radio buttons,
    # if 'none'(name of radio btn) is selected then it should return selectedRadioBtn= false
    if selectedRadioBtn == True and checkFile == True:
        return True
    elif selectedRadioBtn == True and checkFile == False:
        file_path = ""
        return False
    elif selectedRadioBtn == False and checkFile == True:
        file_path = ""
        return False
    else:
        return False


def CloseBtn():
    CloseBtn = CTkButton(
        app,
        text="CLOSE",
        text_color="White",
        hover_color="grey",
        width=55,
        height=23,
        font=("SF Pro Display", 13.5),
        cursor="hand2",
        border_color=("White", "White"),
        command=sys.exit,
        # sys.exit exits the program
        corner_radius=3,
    )
    CloseBtn.place(x=16, y=315)


def SaveBtn():
    global SaveBtn
    SaveBtn = CTkButton(
        app,
        text="SAVE",
        text_color="White",
        hover_color="grey",
        width=55,
        height=23,
        font=("SF Pro Display", 13.7),
        cursor="hand2",
        border_color=("White", "White"),
        command=Save_,
        corner_radius=3,
    )
    SaveBtn.place(x=484, y=315)


logic_thread = None
status = True
if True:
    Label1()
    Label2()
    Label3()
    Label4()
    Label5()
    Label6()
    Label7()
    SaveBtn()
    CloseBtn()
    LoadData()

    def logic():
        global status, delay, CusTit, CusMsg
        CusTit = finalTitle()
        CusMsg = finalMsg()
        delay = int(slider.get())
        keepRun = KeepCallBack()
        if keepRun:
            while status:
                while True:
                    MainLoop(CusMsg, CusTit, delay)
        elif keepRun == False and is_time_between() == True:
            while status:
                while True:
                    MainLoop(CusMsg, CusTit, delay)
        else:
            pass
        status = True

    app.mainloop()
    logic()
