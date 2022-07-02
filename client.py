import threading
import socket
import time
from tkinter import *
from tkinter import font
from tkinter import ttk
import sys


FORMAT = 'utf-8'


class GUI:
    def __init__(self):
        self.gui_running = True
        self.Window = Tk()
        self.Window.protocol('WM_DELETE_WINDOW', self.killer)
        self.Window.withdraw()
        self.Window.bind('<Return>', lambda send: self.sendButton(self.entryMsg.get()))
        self.network = Toplevel()
        self.network.protocol('WM_DELETE_WINDOW', self.killer)
        self.network.title('Select Network')
        self.network.resizable(width=False, height=False)
        self.network.configure(width=400, height=300)
        self.pls = Label(self.network, text='Network Details', justify=CENTER, font='Helvetica 12')
        self.pls.place(relheight=0.15, relx=0.2, rely=0.07)
        self.labelName = Label(self.network, text='IP/PORT: ', font='Helvetica 12')
        self.labelName.place(relheight=0.2, relx=0.1, rely=0.2)
        self.entryName = Entry(self.network, font='Helvetica 14')
        self.entryName.place(relwidth=0.4, relheight=0.12, relx=0.35, rely=0.2)
        self.entryName.focus()
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.client.connect((HOST, PORT))
        self.go = Button(self.network, text='CONTINUE', font='Helvetica 14 bold',
                         command=lambda: self.goAhead(self.entryName.get()))
        self.go.place(relx=0.4, rely=0.55)
        self.Window.mainloop()

    def goAhead(self, info):
        self.network.destroy()
        self.layout()
        self.client.connect((info.split('/')[0], int(info.split('/')[1])))
        rcv = threading.Thread(target=self.receive)
        rcv.start()

    def layout(self):
        self.Window.deiconify()
        self.Window.title("The Ballers Chat")
        self.Window.resizable(width=False,
                              height=False)
        self.Window.configure(width=800,
                              height=550,
                              bg="#17202A")
        self.labelHead = Label(self.Window,
                               bg="#17202A",
                               fg="#EAECEE",
                               text='THE BALLERS CHATROOM',
                               font="Helvetica 13 bold",
                               pady=5)
        self.labelHead.place(relwidth=1)
        self.line = Label(self.Window,
                          width=450,
                          bg="#ABB2B9")

        self.line.place(relwidth=1,
                        rely=0.07,
                        relheight=0.012)

        self.textCons = Text(self.Window,
                             width=20,
                             height=2,
                             bg="#17202A",
                             fg="#EAECEE",
                             font="Helvetica 14",
                             padx=5,
                             pady=5)
        self.textCons.place(relheight=0.745,
                            relwidth=1,
                            rely=0.08)

        self.labelBottom = Label(self.Window,
                                 bg="#ABB2B9",
                                 height=80)

        self.labelBottom.place(relwidth=1,
                               rely=0.825)

        self.entryMsg = Entry(self.labelBottom,
                              bg="#2C3E50",
                              fg="#EAECEE",
                              font="Helvetica 13")

        # place the given widget
        # into the gui window
        self.entryMsg.place(relwidth=0.74,
                            relheight=0.06,
                            rely=0.008,
                            relx=0.011)

        self.entryMsg.focus()

        # create a Send Button
        self.buttonMsg = Button(self.labelBottom,
                                text="Send",
                                font="Helvetica 10 bold",
                                width=20,
                                bg="#ABB2B9",
                                command=lambda: self.sendButton(self.entryMsg.get()))

        self.buttonMsg.place(relx=0.77,
                             rely=0.008,
                             relheight=0.06,
                             relwidth=0.22)

        self.textCons.config(cursor="arrow")

        # create a scroll bar
        scrollbar = Scrollbar(self.textCons)

        # place the scroll bar
        # into the gui window
        scrollbar.place(relheight=1,
                        relx=0.974)

        scrollbar.config(command=self.textCons.yview)

        self.textCons.config(state=DISABLED)

        # function to basically start the thread for sending messages

    def sendButton(self, msg):
        self.textCons.config(state=DISABLED)
        self.msg = msg
        self.entryMsg.delete(0, END)
        snd = threading.Thread(target=self.sendMessage)
        snd.start()

        # function to receive messages

    def receive(self):
        while True:
            try:
                message = self.client.recv(1024).decode(FORMAT)

                # if the messages from the server is NAME send the client's name
                if message == '/quit':
                    self.client.close()
                    self.textCons.config(state=NORMAL)
                    self.textCons.insert(END,
                                         '<<YOU HAVE DISCONNECTED>>' + "\n\n")
                    self.textCons.config(state=DISABLED)
                    self.textCons.see(END)
                    break
                else:
                    # insert messages to text box
                    self.textCons.config(state=NORMAL)
                    self.textCons.insert(END,
                                         message + "\n\n")

                    self.textCons.config(state=DISABLED)
                    self.textCons.see(END)
            except:
                # an error will be printed on the command line or console if there's an error
                if self.gui_running:
                    print("An error occurred!")
                    self.client.close()
                    self.gui_running = False
                    self.Window.destroy()
                    self.killer()
                else:
                    sys.exit()

        # function to send messages

    def sendMessage(self):
        self.textCons.config(state=DISABLED)
        while True:
            message = self.msg
            self.client.send(message.encode(FORMAT))
            break
            # if message == '/quit':
            #     self.client.close()
            # else:
            #     break

    def killer(self):
        self.gui_running = False
        self.Window.destroy()
        self.client.close()
        sys.exit()


# create a GUI class object
g = GUI()
