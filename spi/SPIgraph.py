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

import pandas as pd

def autolabel(ax, xpos='center'):
    """
    Attach a text label above each bar in *rects*, displaying its height.

    *xpos* indicates which side to place the text w.r.t. the center of
    the bar. It can be one of the following {'center', 'right', 'left'}.
    
    """
    totals = []

    # find the values and append to list
    for i in ax.patches:
        totals.append(i.get_width())

    # set individual bar lables using above list
    total = sum(totals)

    # set individual bar lables using above list
    for i in ax.patches:
        # get_width pulls left or right; get_y pushes up or down
        ax.text(i.get_width()+.3, i.get_y()+.1, \
                str(round((i.get_width()/total)*100, 2))+'%\n n= '+str(total), fontsize=7,
    color='dimgrey')
##    xpos = xpos.lower()  # normalize the case of the parameter
##    ha = {'center': 'center', 'right': 'left', 'left': 'right'}
##    offset = {'center': 0.5, 'right': 0.57, 'left': 0.43}  # x_txt = x + w*off
##
##    for rect in rects:
##        height = rect.get_height()
##        ax.text(rect.get_x() + rect.get_width()*offset[xpos], 1.01*height,
##                '{}'.format(height), ha=ha[xpos], va='bottom')

        
SPIclasses=pd.DataFrame(data=['SPI ≤ -2', '-2 < SPI ≤ -1.5', '-1.5 < SPI ≤ -1', '-1 < SPI ≤ 1',
       '1 < SPI ≤ 1.5', '1.5 < SPI ≤ 2', 'SPI ≥ 2'],
             index=['Extremely dry', 'Severely dry', 'Moderately dry', 'Near normal',
       'Moderately wet', 'Severely wet', 'Extremely wet'],
                        columns=["Class"])


def reclass (spi):
    if spi <= -2:
        return "Extremely dry";
    elif -2 < spi <=-1.5:
        return "Severely dry";
    elif -1.5 < spi <=-1:
        return "Moderately dry";
    elif -1 < spi <= 1:
        return "Near normal"
    elif 1 < spi <= 1.5:
        return "Moderately wet"
    elif 1.5 < spi <= 2:
        return "Severely wet"
    elif spi >= 2:
        return "Extremely wet"
                 

class SPIgraph(tk.Frame):
    def __init__(self, parent,dataframe=None):#, controller):
        tk.Frame.__init__(self, parent)

    
        self.note = ttk.Notebook(parent)
        self.tab1 = ttk.Frame(self.note)
        self.tab2 = ttk.Frame(self.note)
        self.tab3= ttk.Frame(self.note)
        self.df=dataframe
##        
        self.parent = parent
        #self.df=dataframe
        self.parent.title("SPI Plot")
        self.style = ttk.Style()
        self.style.theme_use("default")
        
        self.pack(fill=tk.BOTH, expand=2)
        self.intial()
    def intial(self):
        
        
        self.note.add(self.tab1, text = "SPI graph")#,image=scheduledimage, compound=TOP)
        
        #self.note.pack()
        
        label = tk.Label(self.tab1, text="Graph Page!")
        label.grid(row=1)#,pady=3,padx=3)
        exit_btn=tk.Button(self.tab1,text='Go back to main page',command=self.close,
                        activebackground='grey',activeforeground='#AB78F1',
                        bg='#58F0AB',highlightcolor='red',padx='10px',pady='3px')
        exit_btn.grid(row=2,  column=2)
        import matplotlib.pyplot as plt
        from matplotlib.figure import Figure
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg



##        fig = Figure(figsize=(7,5), dpi=200)
        fig = plt.figure()
        num=int("%i11"%len(self.df.columns))
        i=0
        ax=[]
        for col in self.df.columns:
            ax1 = fig.add_subplot(num+i)
            ax.append(ax1)
          
            spi_pos=self.df[col].clip(lower=0).to_frame(col)            
            spi_neg=self.df[col].clip(upper=0).to_frame(col)
##            print(spi)
            self.df[col].plot(ax=ax[i], color="black")
            plt.fill_between(spi_neg.index,spi_neg[col].values,color="r")
            plt.fill_between(spi_pos.index,spi_pos[col].values,color="b")
            ax1.legend(loc='right', bbox_to_anchor=(1.15, 0.9), shadow=True, fontsize=10)

            i+=1

#plt.show()
        self.frame=ttk.Frame(self.tab1)
        self.frame.grid(row=2,sticky=tk.W+tk.E)
        
        canvas = FigureCanvasTkAgg(fig,  self.frame)
        canvas.draw()
        canvas = canvas.get_tk_widget()
        canvas.grid(row=1,  column=0, rowspan=10, columnspan=4, sticky=tk.W+tk.E+tk.N+tk.S)

            
        f=[]
        
        for col in self.df.columns:
            tab=ttk.Frame(self.note )
            f.append(tab)
            self.note.add(tab, text=col)
            df2=self.df[col].to_frame(col)
            df2.dropna(inplace=True)
            #print (df2.head())
            import statsmodels.api as sm
            decomposition = sm.tsa.seasonal_decompose(df2, model='additive')
            fig2 = decomposition.plot()
            plt.figure(figsize=(15,5))
            self.frame=ttk.Frame(tab)
            self.frame.grid(row=2,sticky=tk.W+tk.E)
            canvas = FigureCanvasTkAgg(fig2,  self.frame)
            canvas.draw()
            canvas = canvas.get_tk_widget()
            canvas.grid(row=1,  column=0, rowspan=10, columnspan=4, sticky=tk.W+tk.E+tk.N+tk.S)
        self.tab2=ttk.Frame(self.note )
        self.note.add(self.tab2, text="Frequency")
        fig2 = plt.figure()
        num=int("%i11"%len(self.df.columns))
        i=0
        ax=[]
        for col in self.df.columns:
            ax2= fig2.add_subplot(num+i)
            ax.append(ax2)
            SPI=self.df[col].to_frame(col)
            SPI.dropna(inplace=True)
            print(SPI.head())
            SPI["Class"]=SPI[col].apply(reclass)
            SPIgroup=SPI.groupby(by="Class")
            count=SPIgroup.count()
            d=SPIclasses.join(count)
            print(d.head())                
            plt.style.use('ggplot')
            color_palette_list = ['#009ACD', '#ADD8E6', '#63D1F4', '#0EBFE9',   
                              '#C1F0F6', '#0099CC','#909090']
            d.plot(kind='barh', figsize=(12,7),
                                                color=color_palette_list, fontsize=6,ax=ax[i])
            #plt.set_title('Amount Frequency of %s'%col)
            ax2.set_xlabel('Frequency')
            ax2.set_ylabel('Classes')
##            rects = fig2.patches
            autolabel(ax2, "left")
            i+=1
        self.frame1=ttk.Frame(self.tab2)
        self.frame1.grid(row=2,sticky=tk.W+tk.E)
        
        canvas = FigureCanvasTkAgg(fig2,  self.frame1)
        canvas.draw()
        canvas = canvas.get_tk_widget()
        canvas.grid(row=1,  column=0, rowspan=10, columnspan=4, sticky=tk.W+tk.E+tk.N+tk.S)           
            
        
##            
            #print(self.note[col])
##        tab_names = []
##        for i in self.note.tabs():
##            print (i)
##            tab_names.append(self.note.tab(i, "text"))
##        print (tab_names)   
##            
####            
####            plt.show()
##
##            
##                  
        #fig.savefig(out[:-3]+"png")
            
##        a = f.add_subplot(111)
##        a.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])

        self.note.pack()
        

    def close(self):
        self.parent.destroy()
if __name__ == "__main__":
    import pandas as pd
    from fits import dateparse
    #df=pd.DataFrame(data=[2,3,4,5],columns=["x"])
    file="F:/myDOC/project/report/idle/weatherData/SPI_GONBADEG.csv"
    df=pd.read_csv(file,index_col=0,
                      date_parser=dateparse,parse_dates=True)
    root = tk.Tk()
    root.resizable(width=tk.FALSE, height=tk.FALSE)
    app = SPIgraph(root,df)
    root.mainloop()
    
    label="SPI1"
    
    SPI=df[label]
    SPI=SPI.to_frame(label)
    
    SPI.dropna(inplace=True)
    SPI["Class"]=SPI[label].apply(reclass)
    SPIgroup=SPI.groupby(by="Class")
    count=SPIgroup.count()
    d=SPIclasses.join(count)

    
    plt.style.use('ggplot')
    color_palette_list = ['#009ACD', '#ADD8E6', '#63D1F4', '#0EBFE9',   
                      '#C1F0F6', '#0099CC','#909090']
    
    ax = d.plot(kind='barh', figsize=(12,7),
                                        color=color_palette_list, fontsize=10)
    ax.set_title('Amount Frequency of %s'%label)
    ax.set_xlabel('Frequency')
    ax.set_ylabel('Classes')
    rects = ax.patches
    autolabel(rects, "left")
    
    



    plt.show()

        

        



            
            
        
    
##    for i in SPI.values:
##        print (i)
    
        
    

    
