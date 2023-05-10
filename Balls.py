# Import selenium and webdriver modules
import time
from selenium import webdriver
import csv
from itertools import product


# Create an instance of Chrome webdriver
driver = webdriver.Chrome()

# Navigate to the webpage
driver.get("https://www.taylormadegolf.com/taylormade-drivers/?lang=en_US")
data = []
# Array with links lo do Web Scrapping
pages = [
    {
        'category': "Balls/TP5-TP5X",
        'url': "https://www.taylormadegolf.com/taylormade-balls-TP5-TP5x/?lang=en_US"
    },
    # {
    #     'category': "Balls/TP5X-PIX",
    #     'url': "https://www.taylormadegolf.com/tp5-pix/?lang=en_US"
    # },
    # {
    #     'category': "Balls/Tour Response",
    #     'url': "https://www.taylormadegolf.com/tour-response-golf-balls/?lang=en_US"
    # },
    # {
    #     'category': "Balls/Soft Response",
    #     'url': "https://www.taylormadegolf.com/soft-response-golf-balls/?lang=en_US"
    # },
    {
        'category': "Balls/Kalea",
        'url': "https://www.taylormadegolf.com/taylormade-balls-kalea/?lang=en_US"
    },
    {
        'category': "Balls/Online Exclusive Soft Balls",
        'url': "https://www.taylormadegolf.com/taylormade-online-exclusive-balls/?lang=en_US"
    }

]

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
        links = links + [productUnit.find_element("tag name", "a").get_attribute("href")]

    for link in links:
        print(link)
        driver.get(link)
        try:
            image = driver.find_element("class name", "img-fluid").get_attribute("src")
            name = driver.find_element("id", "product-name").text.strip()   
            price = float(driver.find_element(
               "class name", "value").get_attribute("content"))
            print(price)
            specialPrice = price*0.9
            sku = driver.find_element("class name", "product-id").text.strip()    
        except:
            name = "No aplica"
            price = "No aplica"
            specialPrice = "No aplica"
            sku = "No aplica"
            image = "No aplica"
            data=data+[]

        # Select HAND values
        try:
            select = driver.find_element("id", "Hand-1")
            options = select.find_elements("tag name", "option")
            hand = []
            for option in options:
             if (len(hand) <= 2):
                if (option.text.strip() != "Select Hand"):
                      hand = hand+[option.text.strip()]
            print(hand)
        except:
            hand = []

        # Select SHAFT values
        try:
            select = driver.find_element("id", "Shaft-1")
            options = select.find_elements("tag name", "option")
            shaft = []
            for option in options:
              if (len(shaft) <= 2):
                if (option.text.strip() != "Select Shaft"):
                      shaft = shaft+[option.text.strip()]
            print(shaft)
        except:
            shaft = []

        # Select LOFT values
        try:
            select = driver.find_element("id", "Akeneo_Loft-1")
            options = select.find_elements("tag name", "option")
            loft = []
            for option in options:
                if(len(loft) <= 2):
                    if (option.text.strip() != "Select Loft"):
                        loft = loft+[option.text.strip().replace("°", "")]
            print(loft)
        except:
            try:
                select = driver.find_element("id", "Iron Type-1")
                options = select.find_elements("tag name", "option")
                loft = []
                for option in options:
                    if(len(loft) <= 2):
                        if (option.text.strip() != "Select Loft"):
                            loft = loft+[option.text.strip().replace("°", "")]
                print(loft)
            except:
                loft = []
        
        # Select FLEX values
        try:
            select = driver.find_element("id", "Akeneo_Flex-1")
            options = select.find_elements("tag name", "option")
            flex = []
            for option in options: 
                if (len(flex) <= 2):
                    if (option.text.strip() != "Select Flex"):
                        flex = flex+[option.text.strip()]
            print(flex)
        except:
            flex = []


        data = data+[{'Product Name': name, 
                      'Price (TaylorMade Price Book) USD': price, 
                      'SKU': sku, 
                      'Category': page['category'],
                      'Price (VIP Pricing)': specialPrice, 
                      'Entitlement': 'All Access for TaylorMade AURA', 
                      'Product isActive': 'TRUE', 
                      'Media Standard Url 1': image,
                      'Media Listing URL' : image,
                      'Variation AttributeSet':'Ball_Combinations'
                      }]


        count = 1;
        for i, j, k, l in product(hand, shaft, loft, flex):
            if count <= 2:
                data = data+[{'Product Name': name, 
                          'Price (TaylorMade Price Book) USD': price, 
                          'SKU': sku + str(count),
                          'Price (VIP Pricing)': specialPrice, 
                          'Variation Attribute Name 1': 'Color__c',
                          'Variation Attribute Value 1': i,
                          'Entitlement': 'All Access for TaylorMade AURA', 
                          'Product isActive': 'TRUE', 
                          'Variation Parent (StockKeepingUnit)': sku
                          }]
            count = count + 1
            print(i, j, k, l)

        print(name, price, image, sku, specialPrice)
# Write the data to a CSV file
csvfile = open('/Users/harold/Documents/balls.csv', 'w', newline='')
fieldnames = ['Product Name', 
              'Price (TaylorMade Price Book) USD', 
              'Price (VIP Pricing)', 
              'SKU', 
              'Category', 
              'Variation AttributeSet',
              'Variation Attribute Name 1',
              'Variation Attribute Value 1', 
              'Entitlement', 
              'Product isActive', 
              'Variation Parent (StockKeepingUnit)', 
              'Media Standard Url 1',
              'Media Listing URL'
              ]
writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
writer.writeheader()
writer.writerows(data)
# Close the file
csvfile.close()
# Close the driver
driver.close()
