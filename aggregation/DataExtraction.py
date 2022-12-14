import typing
import extruct
import requests
from Product import Product
from w3lib.html import get_base_url


class DataExtraction:
    def __init__(self, list_of_items: typing.List[str]) -> None:
        """
        Initialize a new DataExtraction class. It also initialize the headers
        that will be used with the requests library and the syntaxes used
        to extract the Schema.org from the products

        Args:
            param1 (List[str]): list of URLs to different products on different
                                shopping sites.
        """
        self.urls = list_of_items
        self.syntaxes = ['json-ld','opengraph','microdata','rdfa']
        self.missing_info = "-"
        self.headers = {
                        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0",
                        "Accept-Language": "en-US, en;q=0.5"
                       }


    def extract_metadata(self, url) -> typing.Dict:
        """
        Extracts the medatada from a website. The metadata contains the
        Schema.org data about the product. This method will look for syntaxes
        defined in the self.syntaxes variable from the constructor

        Args:
            param1 (str): URL to the desired product

        Return: dictionary with the metadata content

        Raise a Value error in case the request fails
        """
        try:
            r = requests.get(url, headers=self.headers)
        except Exception:
            raise ValueError(f'Requested URL {url} is not correct. Make sure that you entered a valid URL')

        base_url = get_base_url(r.text, r.url)
        metadata = extruct.extract(r.text, 
                               base_url=base_url,
                               uniform=True,
                               syntaxes=self.syntaxes)                                  
        return metadata


    def get_product_info_as_jsonld(self, metadata_dict, 
                                    target_key, target_value) -> typing.Dict:
        """
        Extracts the info about a product in a json ld format.
        it searches for a key with a specific value  in the metadata and gets 
        that information.

        Args:
            param1 (Dict): metadata that will be used to search the product type
            param2 (str): key that will be searched in the metadata json.
            param3 (str): value of the key thwt will be searched for

        Return: dictionary with the Product info
        """  
        for key in metadata_dict:
            if len(metadata_dict[key]) > 0:
                for item in metadata_dict[key]:
                    if item[target_key] == target_value:
                        return item


    def extract_offer_from_jsonld(self, json_dict) -> typing.Dict:
        """
        Searches for the offers category in the received JSON string with
        the Product info.

        Args:
            param1 (Dict): dictionary that will contain the Product info

        Return: dict with the required fields if succedded, a dict with the
                missing value for each key in it if something went wrong
        """
        dict = {"price": "", "curency": ""}
        try:
            offers = json_dict.get("offers")
            dict["price"] = offers.get("price")
            dict["curency"] = offers.get("priceCurrency")
            return dict
        except:
            for key in dict:
                dict[key] = self.missing_info

            return dict


    def extract_ratings_from_jsonld(self, json_dict) -> typing.Dict: 
        """
        Searches for the rating category in the received JSON string with
        the Product info.

        Args:
            param1 (Dict): dictionary that will contain the Product info

        Return: dict with the required fields if succedded, a dict with the
                missing value for each key in it if something went wrong
        """       
        dict = {"ratingValue": "", "reviewCount": "", "bestRating": "", "worstRating": ""}

        try:
            ratings = json_dict.get("aggregateRating")
            dict["ratingValue"] = ratings.get("ratingValue")
            dict["reviewCount"] = ratings.get("reviewCount")
            dict["bestRating"]  = ratings.get("bestRating")
            dict["worstRating"] = ratings.get("worstRating")
            return dict
        except:
            for key in dict:
                dict[key] = self.missing_info

            return dict


    def get_products_info(self) -> typing.List[Product]:
        """
        This is the main function that will parse and extract all the info
        from each URL in the list of URLs required by the user.
        This method will search for the offers, the ratings and also the name
        and the description of the product

        Return: list of Product objects that contain the info for each product
                as a whole.
        """
        products = [] 

        for item in self.urls:
            metadata = self.extract_metadata(item)
            product_info = self.get_product_info_as_jsonld(metadata, "@type", "Product")

            offer = self.extract_offer_from_jsonld(product_info)
            ratings = self.extract_ratings_from_jsonld(product_info)

            products.append(Product(product_info.get("name"), 
                                    product_info.get("description"), 
                                    offer.get("price"), 
                                    offer.get("curency"),
                                    ratings.get("ratingValue"),
                                    ratings.get("reviewCount"),
                                    ratings.get("bestRating"),
                                    ratings.get("worstRating")))

        return products