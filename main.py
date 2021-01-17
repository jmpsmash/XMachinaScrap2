# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import requests, re
from bs4 import BeautifulSoup
from enum import Enum

class Vendors(Enum):
    PartsConnexion = 1
    PartsExpress = 2
    Madisound = 3

class ProductType(Enum):
    Capacitor = 1
    Inductor  = 2
    Resistor  = 3

class ProductRange(Enum):
    ClarityCap_ESA_CSA_250V =1
    ClarityCap_CMR_MR_400V =2
    Solen_HeptaLitz_14AWG =103
    Solen_HeptaLitz_12AWG =104


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


class Capacitor:
    def __init__(self, name, price, value, href):
        self.name = name
        self.price = re.sub("USD \$", "", price)
        self.value = value
        self.href  = href
        pass
    def ExtractMoreInfo(self):
        if self.href:
            print("PCCap %s has href %s, scraping more info" %(self.name, self.href))
            soup = BeautifulSoup(requests.get(href).content, "html.parser")
 #           self.description =
    def __str__(self):
        return ("%suF\t%s\t%s" % (self.value, self.price, self.name))

class Inductor:
    def __init__(self, name, price, href):
        self.name = name
        self.price = re.sub("USD\$", "", price)
        self.href = href
        self.dcr  = 0.0
        pass

    def ExtractMoreInfo(self):
        if self.href:
            print("PCInductor %s has href %s, scraping more info" % (self.name, self.href))
            soup = BeautifulSoup(requests.get(href).content, "html.parser")
#            self.description =


class ProductList:
    def __init__(self, vendor, type, description, url):
        self.vendor = vendor
        self.type   = type
        self.url    = url
        self.description = description
        self.product_list = []

    def Scrape(self):
        soup = BeautifulSoup(requests.get(self.url).content, "html.parser")

        if self.vendor == Vendors.PartsConnexion:
            self.ProcessVendorPC(soup)
        elif self.vendor == Vendors.PartsExpress:
            self.ProcessVendorPE(soup)
        else:
            print ("Unknown vendor %s" %(self.vendor))
        return self

    def ProcessVendorPC(self, soup):
        title_soup = soup.find("div", {"id": "toparea"})
        title_text = title_soup.find("h1")
        print(title_text.text)

        all_products = soup.find_all("div", {"class": "prodbasics"})
        for product in all_products:
            print ("START")
            prod_name = product.find("a", {"class": "prodname"})
            if (prod_name):
                print("found product %s" % (prod_name.text))
            else:
                print("FAILED\n")
            prod_price = product.find("span", {"class": "saleprice"}).text

            if (prod_price):
                print("found price %s\n" % (prod_price))
            else:
                print("FAILED price")

            if (self.type == ProductType.Capacitor):
                print ("name is: " + prod_name.text)
                prod_value = re.search("([0-9\.]+)u[fF]", prod_name.text)
                if prod_value:
                    prod_value = prod_value.group(1)
                    self.product_list.append(Capacitor(prod_name.text, prod_price, prod_value, ""))
                else:
                    print ("BAD: " + prod_name.text)

            print ("END")

        for prod in self.product_list:
            print ("found %s Capacitor %s %s" %(prod.value, prod.name, prod.price))

        print("found %d products\n" % (len(all_products)))

    def DumpToFile(self):
        filename = str(self.vendor).split(".")[1] + "_" + re.sub("[/ ]", "_", self.description) + ".txt"

        print  ("Dumping to file %s" %(filename))

        f = open(filename, "w")
        f.write ("C\tPrice\tDesc\n")
        for prod in self.product_list:
            f.write(str(prod) + "\n")
        f.close()

        # Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

    print (str(Vendors.PartsConnexion).split(".")[1])

    product_list = [
        ProductList(Vendors.PartsConnexion, ProductType.Capacitor, "Clarity ESA/CSA 250V", "https://www.partsconnexion.com/capacitors-film-claritycap-csa-esa-250vdc-series.html").Scrape(),
        ProductList(Vendors.PartsConnexion, ProductType.Capacitor, "Clarity CMR/MR 400V", "https://www.partsconnexion.com/capacitors-film-claritycap-cmr-mr-400vdc-series.html").Scrape(),
        ProductList(Vendors.PartsConnexion, ProductType.Inductor, "Solen Litz 14AWG", "https://www.partsconnexion.com/solen-hepta-litz-14-awg-inductors.html")
        # PC, Inductor, Solen Litz 12AWG
        # PC, Inductor, Mundorf CFC16
        # PC, Inductor, Mundorf CFC14
        # PC, Inductor, Mundorf CFC12
        # PE, Cap, Jantzen Superior Z
        # PE, Cap, Jantzen Crosscap
        # PE, Cap, Jantzen Silver
        # PE, Cap, Solen
        # PE, Cap, Dayton DMPC
        # PE, Cap, Dayton Standard
        # PE, Cap, Dayton PMPC
        # PE, Cap, Audyn Cap Plus
        # PE, Cap, Audyn Q4
        # PE, Inductor, Dayton 14AWG
        # PE, Inductor, Dayton 18AWG
        # PE, Inductor, Dayton 20AWG
        # PE, Inductor, ERSE 14AWG
        # PE, Inductor, ERSE 18AWG
        # PE, Inductor, Jantzen 15AWG Litz Wax
        # PE, Inductor, Jantzen 15AWG Wire
        # PE, Inductor, Jantzen 18AWG Wire
        # PE, Inductor, Jantzen 20AWG Wire


    ]

    product_list[0].DumpToFile()
    product_list[1].DumpToFile()


