class Utility(object):

    @staticmethod
    def next_item(collection, item):
        """
        Returns the item after item
        Returns None if item isn't in collection
        """

        if item in collection:

            if item == collection[-1]:

                return collection[0]
            
            else:

                return collection[collection.index(item) + 1]

        else:

            return None

    @staticmethod
    def previous_item(collection, item):
        """
        Returns the item before item
        Returns None if item isn't in collection
        """

        if item in collection:

            if item == collection[0]:

                return collection[-1]

            else:

                return collection[collection.index(item) - 1]

        else:

            return None
