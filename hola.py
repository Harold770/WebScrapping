# Import selenium and webdriver modules
import time
from selenium import webdriver
import csv
from itertools import product


# Create an instance of Chrome webdriver
driver = webdriver.Chrome()

# Array with links lo do Web Scrapping
pages = [
    {
        'category': "Clubs/Drivers",
        'url': "https://www.taylormadegolf.com/taylormade-drivers/?lang=en_US"
    },
    {
        'category': "Clubs/Fairway Woods",
        'url': "https://www.taylormadegolf.com/taylormade-fairways/?lang=en_US"
    },
    {
        'category': "Clubs/Hybrids",
        'url': "https://www.taylormadegolf.com/taylormade-rescues/?lang=en_US"
    },
    {
        'category': "Clubs/Irons",
        'url': "https://www.taylormadegolf.com/taylormade-irons/?lang=en_US"
    },
    {
        'category': "Clubs/Wedges",
        'url': "https://www.taylormadegolf.com/taylormade-wedges/?lang=en_US"
    },
    {
        'category': "Clubs/Putters",
        'url': "https://www.taylormadegolf.com/taylormade-putters/?lang=en_US"
    }

]

# Navigate to the webpage

driver.get("https://www.taylormadegolf.com/taylormade-drivers/?lang=en_US")
data = []


time.sleep(20)


for page in pages:
    time.sleep(5)
    driver.get(page['url'])
    links = []
    links.clear()
    # Find all elements with class="product"
    product_elements = driver.find_elements("class name", "product")

    # Loop through each product and extract the link
    for productUnit in product_elements:
        links = links + \
            [productUnit.find_element("tag name", "a").get_attribute("href")]

    for link in links:
        print(link)
        driver.get(link)

        try:
            image = driver.find_element(
                "class name", "img-fluid").get_attribute("src")
        except:
            image = "No image"

        try:
            name = driver.find_element("id", "product-name").text.strip()
        except:
            name = "No name"

        try:
            price = float(driver.find_element(
               "class name", "value").get_attribute("content"))
            print(price)
            specialPrice = price*0.9
        except:
            price = "No price"
            specialPrice= "No special price"

        try:
            sku = driver.find_element("class name", "product-id").text.strip()
        except:
            sku = "Not Found"

        # Select HAND values
        try:
            select = driver.find_element("id", "Hand-1")
            options = select.find_elements("tag name", "option")
            hand = []
            for option in options:
             if (option.text.strip() != "Select Hand"):
                  hand = hand+[option.text.strip()]
            print(hand)
        except:
            hand = ["NA"]

        # Select SHAFT values
        try:
            select = driver.find_element("id", "Shaft-1")
            options = select.find_elements("tag name", "option")
            shaft = []
            for option in options:
              if (option.text.strip() != "Select Shaft"):
                  shaft = shaft+[option.text.strip()]
            print(shaft)
        except:
            shaft = ["NA"]

        # Select LOFT values
        try:
            select = driver.find_element("id", "Akeneo_Loft-1")
            options = select.find_elements("tag name", "option")
            loft = []
            for option in options:
                if (option.text.strip() != "Select Loft"):
                    loft = loft+[option.text.strip().replace("°", "")]
            print(loft)
        except:
            try:
                select = driver.find_element("id", "Iron Type-1")
                options = select.find_elements("tag name", "option")
                loft = []
                for option in options:
                    if (option.text.strip() != "Select Loft"):
                        loft = loft+[option.text.strip().replace("°", "")]
                print(loft)
            except:
                loft = ["NA"]
        
        # Select FLEX values
        try:
            select = driver.find_element("id", "Akeneo_Flex-1")
            options = select.find_elements("tag name", "option")
            flex = []
            for option in options:
               if (option.text.strip() != "Select Flex"):
                   flex = flex+[option.text.strip()]
            print(flex)
        except:
            flex = ["NA"]

        data = data+[{'Name': name, 
                      'Price (TaylorMade Price Book) USD': price, 
                      'SKU': sku, 
                      'Category': page['category'],
                      'Price (VIP Pricing)': specialPrice, 
                      'Entitlement': 'View All', 
                      'ProductIsActive': 'TRUE', 
                      'Image': image,
                      'Variation AttributeSet':'Club_Combinations'
                      }]



        for i, j, k, l in product(hand, shaft, loft, flex):
            data = data+[{'Name': name, 
                          'Price (TaylorMade Price Book) USD': price, 
                          'SKU': sku,
                          'Price (VIP Pricing)': specialPrice, 
                          'Variation Attribute Name 1': 'Hand__c',
                          'Hand': i, 
                          'Variation Attribute Name 2': 'Shaft__c',
                          'Shaft': j,
                          'Variation Attribute Name 3': 'Loft__c',
                          'Loft': k, 
                          'Variation Attribute Name 4': 'Flex__c',
                          'Flex': l, 
                          'Entitlement': 'View All', 
                          'ProductIsActive': 'TRUE', 
                          'Variation Parent (StockKeepingUnit)': sku, 
                          'Image': image
                          }]
            print(i, j, k, l)

        print(name, price, image, sku, specialPrice)
# Write the data to a CSV file
csvfile = open('/Users/harold/Documents/names.csv', 'w', newline='')
fieldnames = ['Name', 
              'Price (TaylorMade Price Book) USD', 
              'Price (VIP Pricing)', 
              'SKU', 
              'Category', 
              'Variation AttributeSet',
              'Variation Attribute Name 1',
              'Hand', 
              'Variation Attribute Name 2',
              'Shaft', 
              'Variation Attribute Name 3',
              'Loft',
              'Variation Attribute Name 4',
              'Flex', 
              'Entitlement', 
              'ProductIsActive', 
              'Variation Parent (StockKeepingUnit)', 
              'Image'
              ]
writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
writer.writeheader()
writer.writerows(data)
# Close the file
csvfile.close()
# Close the driver
driver.close()
