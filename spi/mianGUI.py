# -*- coding: cp1256 -*-
#https://docstore.mik.ua/orelly/other/python2/1.9.htm
from fits import CalculateSPI,gamma_cdf,dateparse
import os
import warnings
warnings.filterwarnings("ignore")
from SPIgraph import SPIgraph

try:
    import Tkinter as tk
    import tkMessageBox as message
    import  tkFileDialog as filedialog
    import ttk
except:
    import tkinter as tk
    from tkinter import filedialog
    from tkinter import ttk
    from tkinter import messagebox as message
try:
    import pandas as pd
    
    import matplotlib
    import matplotlib.pyplot as plt
    matplotlib.use("TkAgg")
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
    from matplotlib.figure import Figure
except ImportError:
    print("Install pylab  and pandas")
    message.showerror("""Error","Please check you have installed PanDas and MatPlotLib  and outputs
Please go  http://www.lfd.uci.edu/~gohlke/pythonlibs""")
   
##class Plot:
##    def __init__(self, master, data):
##        self.df = pd.DataFrame(data=data[1],index=data[0])
##        # Create a container
##        self.frame = tk.Frame(master)
##        self.fig = Figure(figsize=(7,2))
##        self.ax = self.fig.add_subplot(111)
##        self.line = self.df.plot(ax=self.ax)
##        self.canvas = FigureCanvasTkAgg(self.fig,master=master)
##        self.canvas.draw()
##        self.canvas.get_tk_widget().pack(side='top', fill='both')#, expand=1)
##        self.frame.pack()
##        #self.ax.cla()

##    def update(self, data):
##        """Updates the plot with new data"""
##
##        self.x = data.index
##        self.y = data.values
##
##        self.line[0].set_xdata(self.x)
##        self.line[0].set_ydata(self.y)
##
##        self.canvas.draw()
##        self.frame.pack()

        
        
##        canvas.get_tk_widget().grid(row=3)#side=tk.BOTTOM, fill=tk.BOTH, expand=True
##        toolbar = NavigationToolbar2TkAgg(canvas, self)
##        toolbar.update()
##        canvas._tkcanvas.pack()#side=tk.TOP, fill=tk.BOTH, expand=True
##        
        
class SPItab(tk.Frame):#,tk.Menu):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, background="white")
##        self.add_command(label='Exit', command=root.destroy)
        
        self.parent = parent
        menubar = tk.Menu(root)
        menubar.add_command(label="File")
        menubar.add_command(label="Quit", command=root.quit())
        root.config(menu=menubar)
##        frame_main = tk.Frame(self)
##        frame_main.grid(sticky='n')
        self.nb=ttk.Notebook(self)
        
        self.page1=ttk.Frame(self.nb)
        #self.page2=ttk.Frame(self.nb)
        self.parent.title("SPI")
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.centreWindow()
        self.pack(fill=tk.BOTH, expand=2)   
        self.initialize()
    def initialize(self):
        self.nb.add(self.page1,text="SPI")
        
        lblInput = tk.Label(self.page1,text="Input",
                              anchor="w",fg="white",bg="black",width=10,relief=tk.RIDGE)
        lblInput.grid(row=0,column=0,sticky='W')
        self.inFile = tk.StringVar()#
       # okayCommand = self.register(self.okX)
        self.entryInFile = tk.Entry(self.page1,width=30,textvariable=self.inFile )
        self.entryInFile.grid (row=0, column=1)
        #
        colored_btn = ttk.Button(self.page1,text="Brouse", style="C.TButton",command=self.OnButtonClick)
        colored_btn.grid (row=0, column=2)
        quit_btn=tk.Button(self.page1,text='Close',command=self.close
                           ,highlightcolor='red',padx='10px',pady='3px')
        quit_btn.grid(row=0, column=4)
        
        

        self.entryInFile.grid (row=0, column=1)
        lblDisturbition= tk.Label(self.page1,text="Disturbution",
                              anchor="w",fg="white",bg="black",relief=tk.RIDGE)
        lblDisturbition.grid(row=1,column=0,sticky='W')
        self.disturbution = tk.StringVar()
        self.countryCombo = ttk.Combobox(self.page1, textvariable=self.disturbution)
        self.countryCombo['values'] = ('Gamma', 'Pearson3', '')
        self.countryCombo.current(0)
        #self.countryCombo.bind("<<ComboboxSelected>>", self.newCountry)
        self.countryCombo.grid(row=1, column=1, padx=5, pady=5, ipady=2, sticky="W")
        lblScale= tk.Label(self.page1,text="Time Scale",
                              anchor="w",fg="white",bg="black",width=10,relief=tk.RIDGE,)
        lblScale.grid(row=2,column=0,sticky='W') 
        k=1
        self.scales=[1,3,6,9,12,24]
        self.chk={}
        self.chk2={}
        self.inScale = tk.StringVar()#
        for scale in self.scales:
            #print (scale,k)
            self.chk["var%i"%scale] = tk.StringVar()
            self.chk[str(scale)]= tk.Checkbutton(self.page1, text="%i"%scale, variable=self.chk["var%i"%scale],
                                                 command=self.addtolist,
                               onvalue="%i"%scale, offvalue="")
            self.chk[str(scale)].grid(row=2,column=k)
           
            self.chk[str(scale)].invoke()
            self.chk[str(scale)].select()
            #print(help(self.chk[str(scale)]))
            #self.chk["var%i"%scale].set(1)
            k+=1
       # okayCommand = self.register(self.okX)
        self.entryScale= tk.Entry(self.page1,textvariable=self.inScale)
        self.entryScale.grid (row=3, column=1)
        self.entryScale.bind("<Return>", self.evaluate) 
        lblFreq= tk.Label(self.page1,text="Frequency",
                              anchor="w",fg="white",bg="black",width=10,relief=tk.RIDGE,)
        lblFreq.grid(row=4,column=0,sticky='W')
        self.freq = tk.IntVar()
        
        self.freqName=["Weakly","8 Daily", "16 Daily", "Monthly"]
        c=0
        for fq in self.freqName:
            rdbtm=tk.Radiobutton(self.page1,
                        text=fq,
                        #padx= 5, 
                        variable=self.freq, 
                        value=c, command=self.ShowChoice)
            rdbtm.grid(row=4,column=c+2,sticky='W')
            c+=1
        self.freq.set(3)
        
        lblOutput = tk.Label(self.page1,text="Output",
                              anchor="w",fg="white",bg="black",width=10)
        lblOutput.grid(row=5,column=0,sticky='W')
        self.outFile = tk.StringVar()#
       # okayCommand = self.register(self.okX)
        self.entryOutFile = tk.Entry(self.page1,textvariable=self.outFile )
        self.entryOutFile.grid (row=5, column=1)
        self.inFile.set(u"فايل ورودي" )
        btn2 = ttk.Button(self.page1,text="Save Output", style="C.TButton",
                          command=self.outButtonClick)
        
        btn2.grid (row=5, column=2)
        btn3 = ttk.Button(self.page1,text="Run", style="C.TButton",command=self.Run)
        
        btn3.grid (row=6, column=2)
##        lblPolt = tk.Label(self.page1,text="Plot")#,command=self.Run)
##        lblPolt.grid (row=7, column=0)
        self.var1 = tk.StringVar()
        btnPolt = ttk.Button(self.page1,text="Plot", style="C.TButton", command=self.plot)#,font=tk.LARGE_FONT)#,command=self.Run)
        btnPolt.grid (row=8, column=1,pady=10,padx=10)
        btnGraph = ttk.Button(self.page1, text="Graph Page",command=self.show_graph )
        btnGraph.grid (row=8, column=3,pady=10,padx=10)
                            #command=lambda: controller.show_frame(SPIgraph))
            
        
##        rightFrame = tk.Frame(self.page1, width=50, height = 6)
##        rightFrame.grid(row=9, column=0, padx=10, pady=5)
        self.entry3= tk.Text(self.page1,padx=5, pady=5
                             , height=5, bg='white')
        
        self.entry3.grid(row=9, column=0,rowspan=5,columnspan=8,
                          ipady=2,padx=5, pady=5,sticky=tk.W+tk.E)

        ### Creates a sunken frame to plot the current spectrum ###
        self.frame = ttk.Frame(self.page1, relief='sunken', borderwidth=2, width=self.winfo_width(), height=50)
        self.frame.grid(row=20, column=0, rowspan=7,columnspan=7,sticky=tk.W+tk.E)
        self.fig = Figure(figsize=(9, 2), dpi=100)
        self.fig.subplots_adjust(left=0.1, right=0.8)
        self.ax1 = self.fig.add_subplot(1, 1, 1)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        canvas_plot = self.canvas.get_tk_widget()
        canvas_plot.grid(row=0,  column=0, rowspan=10, columnspan=4, sticky=tk.W+tk.E+tk.N+tk.S)

        #
        self.nb.grid()
    
    func=[1,3,6,9,12,24]
    def close(self):
        self.parent.destroy()
        
    def show_graph(self):
        root2 = tk.Tk()
        df=pd.read_csv(self.outFile.get(),index_col=0,
                      date_parser=dateparse,parse_dates=True)
        app2 = SPIgraph(root2,df)
        root2.mainloop()
        
        #frame.tkraise()
    def plot(self):
        
        self.ax1.clear()
        out=self.outFile.get()
        print (out)
        if os.path.isfile(out):
            
            df=pd.read_csv(out,index_col=0,
                      date_parser=dateparse,parse_dates=True)
            print (df.head())
            df.plot(ax=self.ax1)
            n=len(df.columns)
            print(n)
            fig = plt.figure()
            ax=[]
            num=int("%i11"%n)
            i=0
            for col in df.columns:
                ax1 = fig.add_subplot(num+i)
                ax.append(ax1)
                df[col].to_frame(col).plot(ax=ax[i])
                plt.legend()
                i+=1           
            fig.savefig(out[:-3]+"png")
            self.dataframe=df
            

        self.canvas.draw()

            
    def centreWindow(self):
        w = 800
        h = 600
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
        x = (sw - w)/4
        y = (sh - h)/10
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def checkbuttom2(self):
        pass
        #print (self.entryScale.get())
    
    def addtolist(self):
        for chk in self.chk2:
            self.chk2[chk].grid_remove()
        i=0
        scales=[]
        for var in self.chk:
            if "var" in var:
                #print (var,i)
                no=var.replace("var","")
                if self.chk[var].get():
                    #self.chk2["chk%i"%int(no)] .grid (row=7, column=i+2)
                    scales.append(int(no))
                    i+=1
            scales=list(set(scales))
            scales.sort()
            self.inScale.set(",".join([str(i) for i in scales]))
        #d=self.entryScale.get()
        a=0
        
        for item in scales:
            self.chk2["chk%i"%int(a+1)] = tk.Checkbutton(self.page1,padx=5,text=item,
                                                      onvalue=int(item), offvalue=""  ,variable=self.chk["var%s"%item]
                                                        )
            self.chk2["chk%i"%int(a+1)] .grid (row=7, column=a+1)
            a+=1         
            
    def OnButtonClick(self):
        self.filename = filedialog.askopenfilename(initialdir = "/",title = "Select file",
                                                  filetypes = (("CSV files","*.csv"),("all files","*.*")))
        self.entry3.insert(tk.END,"You Selected the file %s\n"% self.filename )
        data=pd.read_csv(self.filename)
        self.columns=data.columns
        self.entry3.insert(tk.END, "Columns: "+",".join(self.columns)+"\n")
        self.col=tk.StringVar()
        self.cols = tk.OptionMenu(self.page1, self.col, *self.columns)
        self.col.set(self.columns[1])
        self.cols.grid(row=0,padx=20,column=3,sticky='W')
        self.inFile.set(self.filename)
        out=os.path.dirname(self.filename)+"/"+"SPI_"+os.path.basename(self.filename).split(".")[0]
        self.outFile.set(out+".csv")   
        
    def outButtonClick(self):
        self.outfilename = filedialog.asksaveasfilename(initialdir = "/",title = "Select Output file",
                                                  filetypes = (("CSV files","*.csv"),("all files","*.*")))
        self.outFile.set(self.outfilename+".csv")
        self.entry3.insert(tk.END,"Your output data  are  the file %s\n"%self.outfilename+".csv" )
        
    def checkBar(self,picks):
        c=1
        self.scales=[]
        for pick in picks:
            var = tk.IntVar()
            chk = tk.Checkbutton(self.page1, text=pick, variable=var)
            chk.grid(row=2,column=c)
            c+=1
            self.scales.append(var)
    def scale(self):
        return map((lambda var: var.get()), self.vars)
    def ShowChoice(self):
        #print(self.freqName[self.freq.get()])
        return self.freq.get()
    def evaluate(event):
        scales=map(int,self.inScale.get().split(","))
        print (scales)
        
    def Run(self):
        scales=map(int,self.inScale.get().split(","))
        #print (scales)
        disturbution=self.disturbution.get()
        if disturbution =="Gamma":
            cdf=gamma_cdf
        else:
            print("is not implemented")
        #print(self.filename,self.outFile, self.col.get())
        #print (self.freq.get())
        try:
            CalculateSPI(scales,self.filename,self.outFile.get(),self.col.get(),self.freqName[self.freq.get()],cdf=cdf)
        except:
            message.showerror("Error","Please check inputs and outputs")        

if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(width=tk.FALSE, height=tk.FALSE)
    app = SPItab(root)
    root.mainloop()
    
            


    
