def load_and_process(path_to_rawdata):
    """
    Loads and processes data.
    
    Loads rawdata using Pandas library and Process data by removing unwanted columns,
    Dealing with Missing Values, aggregating values,and wrangling the dataframe. Only
    Works for Airbnb raw dataset found raw directory or in the 
    website: http://insideairbnb.com/get-the-data.html
    
    Parameters
    ----------
    path_to_rawdata : directory path to the raw .csv file
        The raw dataset to be processed.
    
    Returns
    -------
    df
        a Pandas dataframe with processed data
        
    Examples
    --------
    >>>load_and_process("<pathtorawfile>")
    pandas.core.frame.DataFrame
    
    """
        
    import pandas as pd
    import numpy as np
    # Method chain 1: Load Data; Wrangle Columns; Clean Data
    df1 =pd.read_csv(path_to_rawdata)
    df1 = (df1
          .loc[:,['name','room_type','price','accommodates','minimum_nights','number_of_reviews','review_scores_rating','review_scores_cleanliness','review_scores_checkin','review_scores_communication','review_scores_location']]         
          .dropna(axis='rows',how='any')
          .reset_index(drop=True)
          )

    # Method chain 2: Lets Process the Data! 
    labels_acc = ['1','2','3','4','5','6-10','10+']
    bins_acc = [1,2,3,4,5,6,10,13]
    N_max = df1['number_of_reviews'].max()
    df1 = (df1
           .assign(tenants=lambda x: pd.cut(x.accommodates,bins=bins_acc,labels=labels_acc,include_lowest=True))
           .assign(Price=lambda x: pd.to_numeric(df1['price'].str.split('$').str.get(1),errors='coerce'))
           .assign(Experience_Rating=lambda x: df1['review_scores_rating']*0.1)
           .assign(Overall_Rating=lambda x: (df1['review_scores_rating']*0.1) + df1['review_scores_cleanliness'] + df1['review_scores_checkin']+df1['review_scores_communication']+df1['review_scores_location'])
           .drop(columns=['accommodates','price','review_scores_rating'])
          )
    df2 = df1.assign(Bayesian_Rating=lambda x: ((N_max*df1['Overall_Rating'].mean()) + (df1['number_of_reviews']*df1['Overall_Rating']))/(N_max+df1['number_of_reviews']))

    # Method Chain 3: Rearrange and Rename all the columns
    df = (df2
           .reindex(columns=[              
                         'name',
                         'room_type',
                         'minimum_nights',
                         'Price',
                         'tenants',
                         'number_of_reviews',
                         'Experience_Rating',
                         'review_scores_cleanliness',
                         'review_scores_checkin',
                         'review_scores_communication',
                         'review_scores_location',
                         'Overall_Rating',
                         'Bayesian_Rating'
                           ]
                      )
           .rename(columns={
                         'name':'Name',
                         'room_type':'Room Type',
                         'Price':'Price per Night ($)',
                         'minimum_nights':'Days of Stay',
                         'tenants':'# of tenants',
                         'number_of_reviews':'Total Reviews',
                         'Experience_Rating':'Experience Rating',
                         'review_scores_cleanliness':'Cleanliness Rating',
                         'review_scores_checkin':'Checkin Rating',
                         'review_scores_communication':'Communication Rating',
                         'review_scores_location':'Location Rating',
                         'Overall_Rating':'Overall Rating',
                         'Bayesian_Rating':'Bayesian Rating'
                           }           
                  )   
            )

    return(df)

def Ranker(df,top,xsize,color,title):
    """
    Takes in a dataframe and plots a bargraph that shows the
    Name, ranks, bayesian rating, and price of airbnbs.
    
    Takes in a dataframe with names, price, bayesian rating for their column index.
    Plots a bargraph using Seaborn and Matplotlib libraries; Names on the y axis and price
    on the x axis. Ranking and Bayesian Ratings are placed within each bar of the name and
    the price at the tip of the bars.
    
    Parameters
    ----------
    df : pandas.core.frame.DataFrame
        the Dataframe that includes names, price, bayesian rating for their column index.
    
    top : int
        Truncates the Dataframe to a certain number of rows
        
    xsize : tuple
        Sets the x axis ticker size
    
    color : str
        color for the sns.bargraph
        
    title : str
        Sets the title for which price range the graph is for
    
    Returns
    -------
    plt.show()
        Plots the bargraph for top <#> airbnbs in a certain price range
        
    Examples
    --------
    >>>Ranker(df=<dataframe>,top=20,xsize=(0,100),color='Greens','<100')
    Plots a bargraph showing the top 20 Airbnbs '<100' dollars as well as their ranking, 
    ratings, and price 
    
    """
    
    
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    plt.figure(figsize=(10,top*0.5))
    plt.xlim(xsize)
    plot = sns.barplot(data=df,y='Name',x='Price per Night ($)',color=color)
    sns.despine()
    plt.bar_label(plot.containers[0],labels=df['Price per Night ($)'].round(2))
    i=0
    bars = range(1,top+1)
    for p in plot.patches:
        plot.annotate("Rank #"+str(bars[i])+" | Rating:"+str(df['Bayesian Rating'][i].round(3)),
                   (xsize[0]+5,p.get_y()+0.5)
                   )
        i = i+1
    plot.set(title=f"Top {top} Airbnbs '{title}' dollars", ylabel=" ")
    return(plt.show())