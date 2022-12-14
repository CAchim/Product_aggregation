

class Product:

    def __init__(self, p_name, p_desc, p_price, p_currency,
            p_rating_value, p_review_count, p_best_rating, p_worst_rating) -> None:
        """
        Initialize a new Product. a prodicut is represented by it's attributes
        which are specidied in the constructor parameters.

        Args:
            param1 (str): name of the product
            param2 (str): description of the prodcut
            param3 (str): price of the product
            param4 (str): currency that is used for the product price
            param5 (str): average value for rating
            param6 (str): total number of the reviews
            param7 (str): highest rating value from the total
            param8 (str): lowest rating value from the total
        """
        self.name = p_name
        self.description = p_desc
        self.price = p_price
        self.currency = p_currency
        self.rating_value = p_rating_value
        self.review_count = p_review_count
        self.best_rating = p_best_rating
        self.worst_rating = p_worst_rating
