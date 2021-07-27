def load_and_process(path_to_rawdata):
    # Method chain 1: load data; truncating column; deal with missing data
    df1 = pd.read_csv(path_to_rawdata)
    ls_col = df1.columns
    ls_want = ['name',
               'room_type',
               'price',
               'accommodates',
               'minimum_nights',
               'number_of_reviews',
               'review_scores_rating',
               'review_scores_cleanliness',
               'review_scores_checkin',
               'review_scores_communication',
               'review_scores_location'
              ]
    ls_not_want = list(df1.drop(columns = ls_want).columns) ## invert drop function to keep the columns we need/want
    df1 = df1.drop(columns = ls_not_want).dropna(axis='rows',how='any').reset_index(drop=True) #data frame with wanted columns and dealt missing data

    
    # Method chain 2: Reformatting values into groups; rearranging renaming columns
    df2 = df1.copy()
    
    labels_acc = ['1','2','3','4','5','6-10','10+']
    bins_acc = [1,2,3,4,5,6,10,13]
    df2['accommodates'] = pd.cut(x=df1['accommodates'],bins=bins_acc,labels=labels_acc,include_lowest=True)

    ## maybe segregate the min and max nights
    labels_nights = ['day(s)','week(s)','month(s)']
    bins_nights = [1,7,30,365]
    df2['minimum_nights'] = pd.cut(x=df1['minimum_nights'],bins=bins_nights,labels=labels_nights,include_lowest=True)

    ## still have to convert the price into an object
    labels_price = ['<$100','$100-$199','$200-$299','$300-$399','$400-$500','$500+']
    bins_price =[1,100,200,300,400,500,1000]
    x = pd.to_numeric(df1['price'].str.split('$').str.get(1),errors='coerce') # <---maybe list comprhension this?
    df2['price'] = pd.cut(x=x,bins=bins_price,labels=labels_price,include_lowest=True)

    ## truncate the review_scores_rating to /10 int instead of /100
    df2['review_scores_rating'] = (df1['review_scores_rating']*0.1)//1
    
    rearrange = [
     'name',
     'room_type',
     'price',
     'minimum_nights',
     'accommodates',
     'number_of_reviews',
     'review_scores_rating',
     'review_scores_cleanliness',
     'review_scores_checkin',
     'review_scores_communication',
     'review_scores_location']
    df2 = df2.reindex(columns=rearrange)

    rename = {
     'name':'Name',
     'room_type':'Room Type',
     'price':'Price',
     'minimum_nights':'Length of Stay',
     'accommodates':'# of tenants',
     'number_of_reviews':'Total Reviews',
     'review_scores_rating':'Experience Rating',
     'review_scores_cleanliness':'Cleanliness Rating',
     'review_scores_checkin':'Checkin Rating',
     'review_scores_communication':'Communication Rating',
     'review_scores_location':'Location Rating'
    }
    df = df2.rename(columns=rename)
        
    return df
