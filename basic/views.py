from django.shortcuts import redirect, render
from django.contrib import messages

# from .models import Reccdb
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

from .models import Reccdb


def Homepage(request):
    # if request.method == "GET":
    #     country_arr = [0,0,0,0,0,0]
    #     purpose_arr = [0,0]
    #     adults_arr = [0,0,0]

        
    #     try :
    #         country = request.POST['country']
    #         if country == 'Spain':
    #             country_arr[0] = 1
    #         elif country == 'United Kingdom':
    #             country_arr[1] = 1
    #         elif country == 'Argentina':
    #             country_arr[2] = 1
    #         elif country == "Bolivia":
    #             country_arr[3] = 1
    #         elif country == "Mexico":
    #             country_arr[3] = 1
    #         elif country == "England":
    #             country_arr[3] = 1
           
    #     except :
    #         messages.error(request, 'Fields cant be blank')
    #         return redirect('homepage')
        
    #     try :
    #         purpose = request.POST['purpose']
    #         if purpose == 'Business':
    #             purpose_arr[0] = 1
    #         elif purpose == 'Leisure':
    #             purpose_arr[1] = 1
            
    #     except : 
    #         messages.error(request, "Feld cant be empty")
    #         return redirect('homepage')

        
    #     try:
    #         adults = request.POST['adults']
    #         if adults == 'Solo':
    #             adults_arr[0] = 1
    #         elif adults == 'Double':
    #             adults_arr[1] = 1
    #         elif adults == 'Group':
    #             adults_arr[2] = 1

    #     except:
    #         messages.error(request, "Feld cant be empty")
    #         return redirect('homepage')
        
    #     arr = country_arr + purpose_arr + adults_arr
    #     return arr
        
    return render(request, "index.html")


def About(request):
    # a = Reccdb.objects.filter(business = 1)
    # print(a,"anzilll")
    # for i in a:
    #     print(i.id, "abhijith")
    queryset = Reccdb.objects.all()
    df = pd.DataFrame.from_records(queryset.values())
    print(df,"abhiii")
    return render(request, 'about.html')


def ContactUs(request):
    queryset = Reccdb.objects.all()
    df = pd.DataFrame.from_records(queryset.values())
    processedDF = df[['hotelname', 'uk', 'spain', 'france', 'netherland', 'austria', 'italy', 'business', 'leisure', 'solo', 'couple', 'group']]
    processedDF.set_index('hotelname', inplace=True)

    userDF= pd.DataFrame(index=['user'],columns=['United Kingdom','Spain','France','Netherlands','Austria','Italy',
                                             'Business','Leisure',
                                             'Solo','Couple','Group'])
    userDF.loc['user'] = [0,1,0,0,0,0,0,1,0,1,0]

    # Calculate cosine similarity

    similarityDF = cosine_similarity(processedDF, userDF)
    similarityDF = pd.DataFrame(similarityDF)
    similarityDF['Average_Score'] = 0.0

    # Calculate and add average score to the similarity dataframe
    for index, row in similarityDF.iterrows():
        hotel_name = processedDF.index[index]
        hotelRow = df[df['hotelname'] == hotel_name].head(1)
        # similarityDF.at[index, 'Average_Score'] = hotelRow['average_Score_hotel']

    # Sort the dataframe by similarity and average score
    similarityDF = similarityDF.sort_values(by=[0, 'Average_Score'], ascending=False).head(5)

    # Get recommended hotels
    recc_hotels = []
    for index, row in similarityDF.iterrows():
        hotel_name = processedDF.index[index]
        print(hotel_name)
        hotelRow = df[df['hotelname'] == hotel_name].head(1)
        recc_hotels.append({
            'hotel_name': hotel_name,
            # 'average_score': hotelRow['average_Score_hotel'],
            'similarity_score': row[0]
        })
    return render(request, 'contact.html')




def recommend_hotels(request):
    # Import the CSV data or load it from your data source



    queryset = Reccdb.objects.all()
    df = pd.DataFrame.from_records(queryset.values())
    print(df,"abhiii")
    processedDF = df
    userDF = [0,0,0,0,0,1,0,1,0,1,0]

    # Calculate cosine similarity
    similarityDF = cosine_similarity(processedDF, userDF)
    similarityDF = pd.DataFrame(similarityDF)
    similarityDF['Average_Score'] = 0.0

    # Calculate and add average score to the similarity dataframe
    for index, row in similarityDF.iterrows():
        hotel_name = processedDF.index[index]
        hotelRow = df[df['hotel_name'] == hotel_name].head(1)
        similarityDF.at[index, 'Average_Score'] = hotelRow['average_Score_hotel']

    # Sort the dataframe by similarity and average score
    similarityDF = similarityDF.sort_values(by=[0, 'Average_Score'], ascending=False).head(5)

    # Get recommended hotels
    recc_hotels = []
    for index, row in similarityDF.iterrows():
        hotel_name = processedDF.index[index]
        print(hotel_name)
        hotelRow = df[df['hotel_name'] == hotel_name].head(1)
        recc_hotels.append({
            'hotel_name': hotel_name,
            'average_score': hotelRow['average_Score_hotel'],
            'similarity_score': row[0]
        })



    return render(request, 'recommendation.html', {'recc_hotels': recc_hotels})
