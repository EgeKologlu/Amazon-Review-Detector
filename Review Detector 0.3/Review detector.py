from selenium import webdriver
import time
import os
driver = webdriver.Chrome()


Path_of_main = os.path.realpath(__file__)
Path_of_database= Path_of_main.replace("Review.py",R"DATABASE")
Path_to_asins =Path_of_main.replace("Review.py",R"ASINs")
Path_of_newreviews = Path_of_main.replace("Review.py",R"New Reviews")
ASIN_list = open(Path_to_asins +r"\\"+ "ASINs.txt").readlines()

class ASINs_Review:
    def __init__(self,reviews,name,stars):
        self.name = name
        self.reviews = reviews
        self.stars = stars

date = time.localtime(time.time())
hour = int(time.strftime("%H"))
minute = int(time.strftime("%M"))

name = "%d_%d_%d_%d_%d.txt"%(date[1],date[2],date[0],hour,minute)
name_new = "New reviews %d_%d_%d_%d_%d.txt"%(date[1],date[2],date[0],hour,minute)
Name_of_lasttxt = os.listdir(Path_of_database)[-1]
fle = open(Path_of_database+r"\\"+Name_of_lasttxt, "r")
file = open((Path_of_database+r"\\"+name),'w+')

New_Reviews = open(Path_of_newreviews+r"\\"+ name_new,"w+")

for ASIN,line in zip(ASIN_list,fle):
    driver.get(
        "https://www.amazon.com/product-reviews/" + ASIN + "/ref=cm_cr_othr_d_btm?ie=UTF8&reviewerType=all_reviews&sortBy=recent#R2OYJFRLIO5YER")
    if not driver.find_elements_by_css_selector("span[data-hook='review-date']") == []:
        reviewws = driver.find_elements_by_css_selector("span[data-hook='review-date']")
        starss = driver.find_elements_by_css_selector('i[data-hook="review-star-rating"]')
        staars = list(map(lambda x: x.get_attribute("innerText"), starss))
        stars = list(map(lambda x: x.replace(".0 out of 5 stars"," star"), staars))
        reviews = list(map(lambda x: x.text, reviewws))

    else:
        reviews =["no review yet"]
    ASIN = ASINs_Review(reviews,ASIN,stars)
    linne = line.rstrip()
    old_review=linne.split("Last review ")[-1]
    new_review=ASIN.reviews[0]
    if old_review == new_review:
        pass
    else:
        print("New " + ASIN.stars[0]+  " review on " + "https://www.amazon.com/product-reviews/" + (ASIN.name).rstrip() + "/ref=cm_cr_othr_d_btm?ie=UTF8&reviewerType=all_reviews&sortBy=recent#R2OYJFRLIO5YER")
        New_Reviews.write("New " + ASIN.stars[0]+  " review: " + "https://www.amazon.com/product-reviews/" + (ASIN.name).rstrip() + "/ref=cm_cr_othr_d_btm?ie=UTF8&reviewerType=all_reviews&sortBy=recent#R2OYJFRLIO5YER\n")

    file.write( (ASIN.name).rstrip() + ":" + "Last review " + ASIN.reviews[0] + "\n")

print("-------------------")
print("       DONE")
print("-------------------")
file.close()
fle.close()
New_Reviews.close()
driver.close()

