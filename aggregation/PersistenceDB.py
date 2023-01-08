from rdflib import Graph, Literal, URIRef, Namespace, RDF
from Product import Product
from rdflib.plugins.sparql import prepareQuery
from rdflib.namespace import XSD
import datetime
import os
import __main__


class PersistenceDB:
    """
    The PersistenceDB class is intended to manage a small ttl database file which
    stores the schema.org format of products as RDF.

    The class is used to write data in the database file but also read from the file.

    The reading is done with the help of some functions that use SPARQL querys in order
    to get the desired info from the database file
    """
    def __init__(self, db_name: str):
        """
        initialize a new object if the PersistenceDB class

        Args:
            param1 (str): name of the ttl database file which will be initialized
        """
        self.schema = Namespace("http://schema.org/")        
        self.graph = Graph()
        self.graph.bind("schema", self.schema)
        self.project_path = os.path.dirname(__main__.__file__)
        self.database = f'{self.project_path}\{"database_files"}\{db_name}'


    def write_to_databse(self, product: Product) -> None:
        """
        This function is used to write the builded rdf object in the ttl database
        file. it appends the serialized rdf object to the file without removing
        the old data, this way it can behave as a database with a history of the data
        that has been inserted

        Args:
            param1 (Product object): this parameter represents a Product object that
                                     contains all the info about a product obtained
                                     from a json_ld at a previous step

        Return:
            None
        """
        self.graph.remove((None, None, None))
        self.build_product_as_rdf(product)

        with open(self.database, 'ab') as f:
            f.write(self.graph.serialize(format='turtle').encode())


    def _read_database_file(self):
        """
        This method is marked as a private function and it is used to
        update the graph object with the newst content of the database file
        before each query is executed

        Return:
            a graph object with the content of the database file
        """
        db_content = self.graph.parse(self.database, format='turtle')
        return db_content


    def check_if_product_exists(self, keyword: str) -> bool:
        """
        This method is used to check if a specific product exists in the database
        file.

        Args:
            param1 (str): this param represents an item that will be 
                          searched  in the database

        Return:
            True if the product exists, False otherwise
        """
        self.graph = self._read_database_file()

        query = f"""
        PREFIX schema: <http://schema.org/>
        ASK {{
            ?product a schema:Product .
            ?product schema:name "{keyword}" .
        }}
        """

        results = self.graph.query(query)
        return results.askAnswer
    

    def get_products_by_name_and_price(self, keyword: str, criteria: str, price: int, order: str):
        """
        Extracts the products that contain the keyword you insert.
        The products will contain the price which can be filtered by the lowest
        or highest price and also they can be sorted ascending or descending.
        Thsi function will build a SPARQL query that will extract the products based on
        the user inputs
        Args:
            param1 (str): keyword that will be used to search the products you want
            param2 (str): this param is used to filter the products by price
                          Posible values: >, <, >=, <=
            param3 (int): the price amount to get the products from the database
            param4 (str): this param will help you to filter the products by their price
                          ascending or descending
                          Posible values: ASC, DESC  
        Return; JSON object with the products found
        """
        self.graph = self._read_database_file()

        query_string = f"""
        PREFIX schema: <http://schema.org/>

        SELECT *
        WHERE {{
          ?product a schema:Product .
          ?product schema:name ?name .
          ?product schema:description ?description .
          ?product schema:price ?price .
          ?product schema:currency ?currency .
          FILTER(regex(?name, "{keyword}", "i") && ?price {criteria} {price})
        }}
        ORDER BY {order}(?price)
        """
        data = {}
        data['items'] = []
        query = prepareQuery(query_string)
        results = self.graph.query(query)

        for row in results:
            data['items'].append({
                "name": row.name.value,
                "description": row.description.value,
                "price": row.price.value,
                "currency": row.currency.value
            })

        return data


    def get_products_by_name_and_ratings(self, keyword: str, criteria: str, rating: int, order: str):
        """
        Extracts the products that contain the keyword you insert.
        The products will contain all the info about aproduct which can be filtered by the lowest
        or highest rating value and also they can be sorted ascending or descending.
        Thsi function will build a SPARQL query that will extract the products based on
        the user inputs
        Args:
            param1 (str): keyword that will be used to search the products you want
            param2 (str): this param is used to filter the products by price
                          Posible values: >, <, >=, <=
            param3 (int): the rating value of the desired products
            param4 (str): this param will help you to filter the products by their price
                          ascending or descending
                          Posible values: ASC, DESC  
        Return; JSON object with the products found
        """
        self.graph = self._read_database_file()

        query_string = f"""
        PREFIX schema: <http://schema.org/>

        SELECT *
        WHERE {{
          ?product a schema:Product .
          ?product schema:name ?name .
          ?product schema:description ?description .
          ?product schema:price ?price .
          ?product schema:currency ?currency .
          ?product schema:rating_value ?rating_value .
          ?product schema:review_count ?review_count .
          ?product schema:best_rating ?best_rating .
          ?product schema:worst_rating ?worst_rating .
          FILTER(regex(?name, "{keyword}", "i") && ?rating_value {criteria} {rating})
        }}
        ORDER BY {order}(?rating_value)
        """
        data = {}
        data['items'] = []
        query = prepareQuery(query_string)
        results = self.graph.query(query)

        for row in results:
            data['items'].append({
                "name": row.name.value,
                "description": row.description.value,
                "price": row.price.value,
                "currency": row.currency.value,
                "rating_value": row.rating_value.value,
                "review_count": row.review_count.value,
                "best_rating": row.best_rating.value,
                "worst_rating": row.worst_rating.value
            })

        return data    


    def get_date_time_formated(self) -> str:
        """
        This method is used to get the date and time that will be used to identify
        when a specific product was inserted in the database file

        Return:
            Literal with the date and time formated
        """
        now = datetime.datetime.now()
        return Literal(now.isoformat(), datatype=XSD.dateTime)


    def build_product_as_rdf(self, product: Product) -> None:
        """
        Creates a product from the Product object that will be formated as RDF
        with all the info in it. This function will be called after when the crated
        object will be written in the database ttl file

        Args:
            param1 (Product object): this parameter represents a Product object that
                                     contains all the info about a product obtained
                                     from a json_ld at a previous step

        Return:
            None
        """
        product_url = URIRef(product.product_url)
        self.graph.add((product_url, RDF.type, self.schema.Product))
        self.graph.add((product_url, self.schema.name, Literal(product.name)))
        self.graph.add((product_url, self.schema.description, Literal(product.description)))
        self.graph.add((product_url, self.schema.price, Literal(float(product.price), datatype=XSD.integer)))
        self.graph.add((product_url, self.schema.currency, Literal(product.currency)))
        self.graph.add((product_url, self.schema.rating_value, Literal(float(product.rating_value), datatype=XSD.integer)))
        self.graph.add((product_url, self.schema.review_count, Literal(product.review_count)))
        self.graph.add((product_url, self.schema.best_rating, Literal(product.best_rating)))
        self.graph.add((product_url, self.schema.worst_rating, Literal(product.worst_rating)))
        self.graph.add((product_url, self.schema.dateCreated , self.get_date_time_formated()))
    