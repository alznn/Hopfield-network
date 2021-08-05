from tkinter import *
from tkinter import ttk
from kernal import getGUI
class skin():
    def __init__(self):
        Label(window, text='Origin picture', font=('Arial', 14)).place(x=30, y=0)
        Label(window, text='Recall picture', font=('Arial', 14)).place(x=30, y=300)
        self.org_canvas = Canvas(window, width=350, height=250)
        self.img = PhotoImage(file='')
        self.imgArea = self.org_canvas.create_image(0, 0, anchor=NW, image=self.img)
        self.org_canvas.place(x=30, y=30, anchor='nw')

        self.result_canvas = Canvas(window, width=350, height=280)
        self.result_img = PhotoImage(file='')
        self.result_imgArea = self.result_canvas.create_image(0, 0, anchor=NW, image=self.result_img)
        self.result_canvas.place(x=30, y=330, anchor='nw')

        Label(window, text='Origin picture - add Noise', font=('Arial', 14)).place(x=400, y=0)
        Label(window, text='Recall picture - add Noise', font=('Arial', 14)).place(x=400, y=300)
        self.norg_canvas = Canvas(window, width=350, height=250)
        self.oimg = PhotoImage(file='')
        self.noimgArea = self.norg_canvas.create_image(0, 0, anchor=NW, image=self.oimg)
        self.norg_canvas.place(x=400, y=30, anchor='nw')

        self.nresult_canvas = Canvas(window, width=350, height=280)
        self.nresult_img = PhotoImage(file='')
        self.nresult_imgArea = self.nresult_canvas.create_image(0, 0, anchor=NW, image=self.nresult_img)
        self.nresult_canvas.place(x=400, y=330, anchor='nw')

        # self.labelTop = Label(window, text="選擇資料集", font=('Arial', 12)).place(x=600, y=400)
        # self.labelTop.place(x=10, y=5)

        Label(window, text='是否加入雜訊:', font=('Arial', 12)).place(x=800, y=10)
        self.isNoise = ttk.Combobox(window,
                                values=["是","否"], font=('Arial', 12))
        self.isNoise.place(x=800, y=30)
        self.isNoise.current(0)

        Label(window, text='雜訊機率 :', font=('Arial', 12)).place(x=800, y=65)
        Label(window, text='[0,1] 之間，預設學習率為 0.25', font=('Arial', 10)).place(x=875, y=65)
        noise_rate = StringVar()
        noise_rate.set('0.25')
        entry_noise_rate = Entry(window, textvariable=noise_rate, font=('Arial', 12))
        entry_noise_rate.place(x=800, y=95)

        Label(window, text='選擇資料集:', font=('Arial', 12)).place(x=800, y=125)
        self.dataset = ttk.Combobox(window,
                                values=["Basic","Bonus"], font=('Arial', 12))
        self.dataset.place(x=800, y=145)
        self.dataset.current(0)
        self.dataset.bind("<<ComboboxSelected>>", self.get_pattern)

        self.pattern_comboExample = ttk.Combobox(window,
                                                 values=[], font=('Arial', 12))

        self.btn_train = Button(window, text='train', command=lambda:train_model()).place(x=800, y=450)
        self.but_showImg = Button(window, text=" show result ", command=lambda:change())
        self.but_showImg.place(x=900, y=450)

        def change():
            # pass
            self.org_canvas.itemconfig(self.noimgArea, image="")
            self.result_canvas.itemconfig(self.noimgArea, image="")
            self.norg_canvas.itemconfig(self.noimgArea, image="")
            self.nresult_canvas.itemconfig(self.noimgArea, image="")

            isNoise_signal = str(self.isNoise.get())
            noise_rate = str(entry_noise_rate.get())
            print("isNoise_signal:",isNoise_signal)
            print("noise_rate: ",noise_rate)
            import os
            current = os.getcwd()
            # file_dir = current + '\\Hopfield_dataset\\'
            file_dir = current + '\\'
            print(self.pattern_comboExample.get())
            data = str(self.pattern_comboExample.get()).split("：")
            print(data)
            file_name = file_dir + data[0] + '_origin' + data[1] + '.png'
            file_org = resize(file_name)
            print(file_org)
            self.img = PhotoImage(file='' + file_org)
            self.org_canvas.itemconfig(self.imgArea, image=self.img)
            if isNoise_signal== "是":
                print("get in if ")
                file_name = file_dir + data[0] + '_noise' + noise_rate + '_' + data[1] + '.png'
                print(file_name)
                nfile_org = resize(file_name)
                self.oimg = PhotoImage(file='' + nfile_org)
                self.norg_canvas.itemconfig(self.noimgArea, image=self.oimg)
                #
                reset_file_name = file_dir + data[0] + '_noise'+noise_rate+'_recall' + data[1] + '.png'
                print(reset_file_name)
                nfile_recall = resize(reset_file_name)
                self.nresult_img = PhotoImage(file=nfile_recall)
                self.nresult_canvas.itemconfig(self.nresult_imgArea, image=self.nresult_img)
            #
            else:
                reset_file_name = file_dir + data[0] + '_recall' + data[1] + '.png'
                file_recall = resize(reset_file_name)
                print(file_recall)
                self.result_img = PhotoImage(file=file_recall)
                self.result_canvas.itemconfig(self.result_imgArea, image=self.result_img)
                print("change done")

        def train_model():
            if str(self.isNoise.get()) == '是': isNoise_signal=True
            else: isNoise_signal = False

            # noise_rate = round(float(entry_noise_rate.get()),2)
            noise_rate = format(float(entry_noise_rate.get()),'.2f')
            data = str(self.pattern_comboExample.get()).split("：")
            # getGUI(flag, isNoise, assign_pattern, rate)
            print(str(data[0]),isNoise_signal,int(data[1]),noise_rate)
            getGUI(str(data[0]),isNoise_signal,int(data[1]),noise_rate)

        def resize(file_name):
            from PIL import Image
            #type+"_"+file+".png")
            im = Image.open(file_name)
            # print(im.size)
            nim = im.resize((320, 240), Image.BILINEAR)
            nim.save(file_name)
            #
            im = Image.open(file_name)
            # print(im.size)
            nim = im.resize((320,240), Image.BILINEAR)
            nim.save(file_name)
            return file_name

    def get_pattern(self,event):
        # choose_dataset = str(self.choose_dataset.get())
        Label(window, text='選擇輸入矩陣:', font=('Arial', 12)).place(x=800, y=185)
        if str(self.dataset.get()) == "Basic":
            self.pattern_comboExample = ttk.Combobox(window,
                                                     values=["Basic：0", "Basic：1",
                                                             "Basic：2"], font=('Arial', 12))
            self.pattern_comboExample.place(x=800, y=210)
            self.pattern_comboExample.current(0)
        elif str(self.dataset.get()) == "Bonus":
            self.pattern_comboExample = ttk.Combobox(window,
                                                     values=["Bonus：0", "Bonus：1",
                                                             "Bonus：2", "Bonus：3", "Bonus：4",
                                                             "Bonus：5", "Bonus：6", "Bonus：7", "Bonus：8"
                                                         , "Bonus：9", "Bonus：10", "Bonus：11", "Bonus：12"
                                                         , "Bonus：13", "Bonus：14"], font=('Arial', 12))
            self.pattern_comboExample.place(x=800, y=210)
            self.pattern_comboExample.current(0)

# 第1步，例項化object，建立視窗window
window = Tk()
# 第2步，給視窗的視覺化起名字
window.title('My Window')
# 第3步，設定視窗的大小(長 * 寬)
window.geometry('1200x1200')  # 這裡的乘是小x
# 第4步，載入 wellcome image
app = skin()
window.mainloop()