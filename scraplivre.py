import requests
import lxml
import time
import csv
import string
import re
from bs4 import BeautifulSoup

urlSite = "http://books.toscrape.com"

data_livre = dict()

default_url = (
    "http://books.toscrape.com/catalogue/slow-states-of-collapse-poems_960/index.html"
)


def get_book_info(url):
    reponse = requests.get(url)

    data_livre["url"] = url

    if reponse.ok:

        soup = BeautifulSoup(reponse.text, "lxml")

        titre = soup.find("title").get_text()
        data_livre["title"] = titre

        soup2 = soup.find("article", "product_page")

        tds = soup2.findAll("td")
        ths = soup2.findAll("th")
        for td, th in zip(tds, ths):
            data_livre[th.text] = td.text

        image = soup2.find("img")
        img_url = (urlSite + soup.img["src"]).replace("../..", "")
        data_livre["img_url"] = img_url

        # rajouter url image et reconstruire image

        description = soup2.find("p", recursive=False)
        # print(description.text)
        data_livre["description"] = description.text

        links = soup.findAll("a")
        category = None
        for u in links:

            if "category" in u["href"] and u.text != "Books":
                category = u.text
                break
        assert category is not None

        ps = soup.findAll("p")
        p_rating = None
        for p in ps:
            if "star-rating" in p["class"]:
                p_rating = p["class"]
                break
        assert p_rating is not None

        letters_to_numbers = {
            "Zero": 0,
            "One": 1,
            "Two": 2,
            "Three": 3,
            "Four": 4,
            "Five": 5,
        }
        rating = letters_to_numbers[p_rating[1]]
        data_livre["rating"] = rating

        data_livre["category"] = category

    return data_livre


headers = [
    "product_page_url",
    "universal_product_code",
    "title",
    "price_including_tax",
    "price_excluding_tax",
    "number_available",
    "product_description",
    "category",
    "review_rating",
    "image_url",
]


def info2csv(info_dict, output_file):
    print("---------------")
    with open(output_file, "w") as handle:
        print("test")
        handle.write(",".join(headers) + "\n")
        url = info_dict["url"]
        universal_product_code = info_dict["UPC"]
        title = info_dict["title"].strip().strip("\n").split("|")[0]
        price_including_tax = info_dict["Price (incl. tax)"].split("£")[1]
        price_excluding_tax = str(
            float(price_including_tax) - float(info_dict["Tax"].split("£")[1])
        )
        try:
            number_available = info_dict["Availability"].split("(")[1].split()[0]
        except IndexError:
            number_available = 0
        product_description = info_dict["description"]
        category = info_dict["category"]
        review_rating = info_dict["rating"]
        img_url = info_dict["img_url"]
        print(img_url)
        line_to_write = (
            ",".join(
                [
                    url,
                    universal_product_code,
                    title,
                    price_including_tax,
                    price_including_tax,
                    number_available,
                    product_description,
                    category,
                    str(review_rating),
                    img_url,
                ]
            )
            + "\n"
        )
        handle.write(line_to_write)


mon_info_dict = get_book_info(default_url)
info2csv(mon_info_dict, "test.csv")


"""
for url in listeCategory
book = fonction(url)
ecritureCsv

fonction main : fonction qui va organiser les autres fonctions


product=dict()

product["product_name"] = "L'amie prodigieuse"

def get_book(url):
    request
    article
    mettre les infos dans products
    return product

def csv_writer():
    modules csv avec fonction spéciale dico dictwriter

   ''' 
   """
