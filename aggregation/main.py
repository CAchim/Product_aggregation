import DataExtraction
from PersistenceDB import PersistenceDB

"""
Demo usege for the O1
"""

# Initialize a list with different products from different websites
items = [
    "https://www.quickmobile.ro/telefoane-si-accesorii/telefoane-mobile/apple-iphone-13-pro-dual-sim-esim-1tb-5g-albastru-sierra-blue-59103",
    "https://www.emag.ro/telefon-mobil-apple-iphone-13-128gb-5g-blue-mlpk3rm-a/pd/DCFCMXMBM/?X-Search-Id=4acaa8e84a306cfe8055&X-Product-Id=8667454&X-Search-Page=1&X-Search-Position=0&X-Section=search&X-MB=0&X-Search-Action=view",
    "https://www.pcgarage.ro/monitoare-led/dell/gaming-s2522hg-245-inch-1-ms-negru-g-sync-compatible-freesync-premium-240-hz/?pssrc=ps&psaf=P5R&pscc=ca2b7424b2b0125866546eaa6d3f226e&utm_source=pricy.ro&utm_medium=profitshare&utm_campaign=profitshare_P5R&utm_content=link",
    "https://www.evomag.ro/monitoare-monitoare-led/dell-monitor-gaming-ips-led-dell-24.5-s2522hg-full-hd-1920-x-1080-hdmi-displayport-pivot-240-hz-1-ms-negru-3818364.html?utm_source=2parale&utm_medium=quicklink&utm_campaign=bb3110552&2pau=bb3110552&2ptt=quicklink&2ptu=d4f678b43&2prp=hyHiARx5gf6WerX4FbjlkeTozgL55it9f7mjqzl4DAvJlq9krlFjCAYts-JGPmEg_kWZ9f2dfkjUdQhSUvd7zQ2UpPTYCcVFTeSVrItpgJltsrpQsZeYMHNA-hMlQmPM9nzhST3uzpDtsUNADUaXbvQ0q9qunUX4Sc9ZB1s8iAQ&2pdlst="
]
# Instantiate a new object of DataExtraction class that takes the previous list
# of items as a parameter
data_extraction = DataExtraction.DataExtraction(items)

# Call the get_products_info function to get the info about each product
# in the list. This function returns a list of product objects
products = data_extraction.get_products_info()

# Iterate through each object in the list and output the content
# for product in products:
#     str = f'#name : {product.product_url}\n\n'\
#           f'#name : {product.name}\n\n'\
#           f'#description : {product.description}\n\n' \
#           f'#price : {product.price}\n'\
#           f'#currency : {product.currency}\n'\
#           f'#rating value : {product.rating_value}\n'\
#           f'#review count : {product.review_count}\n'\
#           f'#best rating : {product.best_rating}\n'\
#           f'#worst rating : {product.worst_rating}\n'
#     print(str)
#     print("----------------------------------")

# Demo usage for O2 and O3 combined
db = PersistenceDB("example.ttl")

for product in products:
    db.write_to_databse(product)

print(db.get_products_by_name_and_price("iphone", ">", 3000, "ASC"))
print("------------------------------------")
print(db.get_products_by_name_and_ratings("monitor", ">", 2, "DESC"))
