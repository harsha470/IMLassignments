from bs4 import BeautifulSoup
import requests
import pandas as pd
national_url='https://www.goibibo.com/sitemap-https/hotel-cities.xml'
international_url='https://www.goibibo.com/sitemap-https/international_hotel_cities.xml'
website_url='https://www.goibibo.com'
urls=[national_url,international_url]
#
filename="Data.csv"
f=open(filename,'w',encoding='utf-8')
headers="Hotel Name,City,Country,Rating,Price,Amenities,Review-1,Review-2"
f.write(headers+"\n")
for base_url in urls:
    xmlurl=requests.get(base_url)
    #print(xmlurl.status_code)
    xmlsoup=BeautifulSoup(xmlurl.content,'lxml')
    hotels_list=xmlsoup.find_all('url')
    for site in hotels_list:
        #print(site.loc.text)
        hotels_website=requests.get(site.loc.text,'lxml')
        hotel_soup=BeautifulSoup(hotels_website.content,'lxml')
        cards=hotel_soup.find_all('div',{'class':'HotelCardstyles__OuterWrapperDiv-sc-1s80tyk-0 eXWmAQ'})
        #print(cards)
        for card in cards:
            get_url=card.findAll("div",{"class":"HotelCardstyles__HotelNameWrapperDiv-sc-1s80tyk-11 jkwhbV"})
            hotel_url=website_url+get_url[0].a['href']
            #print(hotel_url)
            hotel_url_req=requests.get(hotel_url)
            hotelsoup=BeautifulSoup(hotel_url_req.content,'lxml')
            hotel_name=hotelsoup.find('h3',{'class':'dwebCommonstyles__SectionHeader-sc-112ty3f-5 HotelName__HotelNameText-sc-1bfbuq5-0 hMoKY'}).text
            city=hotelsoup.find_all('span',itemprop='name')
            lisd=[]
            for x in city[0:4]:
                lisd.append(x.text)
                
                if len(lisd)<=3:
                    hotel_country='NaN'
                    
                else:
                    a=lisd[3]
                    b=lisd[2]
                    
                    hotel_country=b[11:]
                
            hotel_city=(hotel_soup.find('h1',{'class':'SRPstyles__SeoSrpPageTitle-sc-19ucfhx-5 jGKNlG'}).text.split())[-1]
            hotel_rating=hotelsoup.find('span',itemprop='ratingValue')
            if hotel_rating!=None:
                hotel_rating=hotel_rating.text
            else:
                hotel_rating='NaN'
            #print(hotel_rating)
            
            hotel_price=card.find('p',{'class':'HotelCardstyles__CurrentPrice-sc-1s80tyk-26 ckALLt'})
            if hotel_price!=None:
                hotel_price=hotel_price.text
            else:
                hotel_price='NaN'
            
            #print(hotel_name,hotel_rating,hotel_price)

            f.write(hotel_name+",")
            f.write(hotel_city+",")
            f.write(hotel_country+",")
            f.write(hotel_rating+",")
            f.write(hotel_price+",")
            hotel_ammenities=[]
            x=card.find_all('p',attrs={'AmenitiesListstyles__TextWrapper-sc-19dqtu1-7 kQzGvm'})
            for a in x:
                #hotel_ammenities.append(a.text)
                try:
                    f.write(a.text)
                except:
                    f.write(' '+',')
            
            reviews=hotelsoup.findAll("div",{"class":"Layouts__Column-sc-1yzlivq-1 UserReviewstyles__UserReviewWrapperDiv-sc-1y05l7z-3 koJpKV"})
            if len(reviews)>=2:
                f.write(","+ reviews[0].text.split("\n",1)[0].split(",",1)[0])
                f.write(","+ reviews[1].text.split("\n",1)[0].split(",",1)[0])
            if len(reviews)==1:
                f.write(","+ reviews[0].text.split("\n",1)[0].split(",",1)[0])
                f.write(","+" ")
            if len(reviews)==0:
                f.write(","+" ")
                f.write(","+" ")
            f.write("\n")
            

            
            #reviews=page_soup.findAll("div",{"class":"Layouts__Column-sc-1yzlivq-1 UserReviewstyles__UserReviewWrapperDiv-sc-1y05l7z-3 koJpKV"})
            #data={'Name':[hotel_name],'City':[hotel_city],'Country':[hotel_country],'Rating':[hotel_rating],'Cost':[hotel_price],'Amenities':[hotel_ammenities]}
            #print(data)
#df=pd.DataFrame(data)
#df.to_csv('Data')
f.close()