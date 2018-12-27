
try:
    import numpy as np
    import lmoments as lm
    from scipy import stats
    ma=np.ma
    import scipy.stats.distributions as ssd
except ImportError:
    print("Install lmoments  and scipy")
    




def pearsonfit(data):
    data=np.array(data)
    nozero=len(data.nonzero()[0])
    pze=1-float(nozero)/len(data)
    #print pze
    #data2=ma.masked_values(data.values, 0)

    para=lm.pelpe3(lm.samlmu(data[data!=0],3))



    p3= np.array([lm.cdfpe3(i,para) for i in  data])


    p3=stats.norm.ppf(p3)
    #p3=stats.norm.ppf(pze+(1-pze)*lm.cdfnor(p3,[0,1]))
    return p3




def gamma_cdf(aseries):  
    """
    Returns the CDF values for aseries.
    
    -Parameters
    aseries : TimeSeries
        Annual series of data (one column per period)
    """
    # Mask the months for which no precipitations were recorded
    
    # Get the proportion of 0 precipitation for each period (MM/WW)
    nozero=np.count_nonzero(aseries) 
    zero=len(aseries)-nozero
    pzero=float(zero)/len(aseries)
##    print pzero,zero
    aseries_ = ma.masked_values(aseries, 0.0)
    # Mask outside the reference period
    #aseries_._mask |= condition._data
    mean_rain = aseries_.mean(axis=0)
    #print mean_rain
    aleph = np.ma.log(mean_rain) - np.ma.log(aseries_).mean(axis=0) 
    alpha = (1. + ma.sqrt(1.+4./3*aleph)) / (4.*aleph)

    beta = mean_rain/alpha
##    print alpha, beta
    # Get the Gamma CDF (per month)
    cdf = pzero + (1.-pzero) * ssd.gamma.cdf(aseries,alpha,scale=beta)
    pn=stats.norm.ppf(cdf.astype(float))
    pn[np.where(pn<-4)[0]]=-4
    
    
    return pn



def gammafit(Data):
    data=np.array(Data)
    index1=np.where(data==0)[0]
    index2=np.where(data!=0)[0]
    pze=float(len(index1))/len(data)
    print (pze)
    if pze>=(1/16.):
        indx=np.where(data==0)[0]
        data[indx[0]]=0.001

        
##    nozero=len(data.nonzero()[0])
##    pze=1-float(nozero)/len(data)
    
    #print pze
    #data2=ma.masked_values(data.values, 0)

 
    para=lm.pelgam(lm.samlmu(data[data!=0],2))

    #global pze
    print (para,pze)
    print (data)
    
    gam= np.array([lm.cdfgam(i,para) for i in data])
    #gam[index1]=0
    
    #global cdf
    
    

##    gam[index2]=np.ma.array(gam)
    
    
    gam=stats.norm.ppf(gam.astype(float))
    
    
    cdf= np.zeros(shape=len(gam))#([pze+(1-pze)*lm.cdfnor(i,[0,1]) for i in gam])
    cdf[index1]=pze
    cdf[index2]=np.array([pze+(1-pze)*lm.cdfnor(i,[0,1]) for i in gam[index2]])
    print (cdf)
    
   
##    print para
    pn=stats.norm.ppf(cdf.astype(float))
    pn[np.where(pn<-4)[0]]=-4
    del data
    return pn
def glo(data):
    """Generalized Logistic Generalized Logistic distribution function."""
    para=lm.pelglo(lm.samlmu(data,4))
##    print para

    p3= np.array([lm.cdfglo(i,para) for i in  data])
    
    p3=stats.norm.ppf(p3.astype(float))
    pn=stats.norm.ppf(lm.cdfnor(p3,[0,1]))
    return pn
def gamma3(data):
    para=stats.gamma._fitstart(data)
    a,loc,scale=para
    cdf=stats.gamma.cdf(data,a,loc=loc,scale=scale)
    ppf=stats.norm.ppf(cdf)
    return ppf
    
##    shape,loc,scale=stats.fisk.fit(data)
##    cdf=stats.fisk.cdf(data,shape,loc=loc,scale=scale)
##    spi=stats.norm.ppf(cdf.astype(float))
##    return spi

if __name__ =="__main__":
##    data=[123,34,4,654,37,78,0,0,0]
##    data=np.array(data)
####    print pearsonfit(data)
##    spi= glo(data)
    pass
import pandas as pd
dateparse = lambda x: pd.datetime.strptime(x, u'%Y-%m-%d') if "-" in x else pd.datetime.strptime(x, u'%d/%m/%Y')
##ins="weatherData/GONBADEG.csv"
def CalculateSPI(scales,ins,outs,rainColumn,Freq,cdf=gamma_cdf):
    
##    writer_spi = pd.ExcelWriter(r"C:\Python27\Lib\site-packages\PyQt4\far_spi16.xlsx")
    mydata=pd.read_csv(ins ,index_col=0,
                      date_parser=dateparse,parse_dates=True)
    
##    dataf=r"C:\Python27\Lib\site-packages\PyQt4\far_test11.xlsx"
##    data=pd.read_excel(dataf)
    
    k=0
    for scale in scales:
        rain=mydata[rainColumn]
        print (scale)
        if scale>1:
            rain=rain.rolling(scale, min_periods=scale).sum()
            
            rain.dropna(inplace=True)
            rain=rain.to_frame("Rain%i"%scale)
        else:
            rain=rain.to_frame("Rain%i"%scale)
            
        if Freq=="Monthly":
            rain['Rank']=rain.index.month
        
    ##    groupYear=rain.groupby(data.index.year)
    ##    df=groupYear[["PRCP"]].resample('16D').sum()
    ##    df=df.reset_index().drop('level_0', axis=1)
    ##    df.index=df['level_1']
    ##    df['Rank']=df.index.dayofyear/16+1
    ##    df['Rank']=df.index.month#/16+1
        w=max(rain['Rank'])
        j=0
        for i in range(w):
            dfw=rain[["Rain%i"%scale]][rain["Rank"]==i+1]
            data=dfw.values.astype(float).flatten()
            spi=cdf(data)
            spi=pd.DataFrame(data=spi,index=dfw.index,columns=["SPI%i"%scale])              
            if j==0:
                SPI=spi
                j+=1
            else:
                SPI=pd.concat([SPI,spi],axis=0)
        SPI=SPI.sort_index()
        if k==0:
            SPI_final=SPI
            k+=1
        else:
##            SPI_final=pd.concat([SPI_final,SPI],axis=0)
            SPI_final=SPI_final.join(SPI, how='outer')
            #SPI_final=pd.concat([SPI_final,SPI],axis=1)
        
    SPI_final.to_csv(outs )
        
    
    

##    data=np.array([  9. ,   0. ,  13.6,   6.8,   5.3,  39. ,   4.7,   0. ,  10.9,
##         0. ,   0.4,   8.9,   1.8,   0. ,  22.6,  23.9,   8.5,  24. ,
##        13.3,  27.4,   9.1,  19.5,   9.6,   0.3])
##    data=data.reshape(-1,2)
##    spi=gammafit(data[:,1])
##    
        
        
    
    
##    print spi
##    shape,loc,scale=stats.fisk.fit(data)
##    cdf=stats.fisk.cdf(data,shape,loc=loc,scale=scale)
##    p3=stats.norm.ppf(cdf)
##    pn=stats.norm.ppf(stats.norm.cdf(p3,[0,1]))
##    print pn
    
    

    
    



