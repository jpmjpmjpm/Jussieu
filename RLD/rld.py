"""
RLD Class for:
- Representing data
- Performing statistics on it

"""

import numpy as np


class Rld:
    def __init__(self, data_file):
        # Number of items in the data file
        self.items_count = 0
        with open(data_file) as fp:
            context, gains = [], []
            for item in fp:
                self.items_count += 1
                _, i_context, i_gains = item.split(":")

                context.append([float(y) for y in i_context.split(";")])
                gains.append([float(y) for y in i_gains.split(";")])

        # Matrices of themes and number of ad clicks
        self.context, self.gains = np.array(context), np.array(gains)

    # Having a __str__ method is always good to analyze the class!
    def __str__(self):
        return (f"Count of items: {self.items_count}\n"
                f"Sample of context:\n{self.context}\n"
                f"Sample of gains:\n{self.gains}")

    # Return the i-th item context
    def item_context(self, item_index):
        return self.context[item_index]

    # Return the i-th item gains
    def item_gains(self, item_index):
        return self.gains[item_index]

    """
    Return a regret list with one regret by item based on a valuation function.
    The valuation function is defined as
    def valuation_item(context, gains):
        return valuation_item
    It takes as arguments the context and gains of a given item
    Interesting: we pass a function as an argument of a function!
    """

    def regret_list(self, valuation):
        return [valuation(self.item_context(i), self.item_gains(i)) for i in range(self.items_count)]


def main():
    data = Rld('CTR.txt')
    print(data)

    print(f"Context of last item:\n {data.item_context(data.items_count - 1)}\n"
          f"Gains of last item:\n {data.item_gains(data.items_count - 1)}\n")

    # Random strategy evaluation. Valuation for an item is equal to max of gains minus a random gain.
    def strategy_random(context, gains):
        return np.amax(gains) - np.random.choice(gains)

    random_regret_list = data.regret_list(strategy_random)
    print(f"Random regret list: {random_regret_list}\n")

    # Optimal strategy.
    def strategy_optimal(context, gains):
        chosen = np.amax(gains)
        best = np.amax(gains)
        return best - chosen

    optimal_regret_list = data.regret_list(strategy_optimal)
    print(f"Optimal regret list: {optimal_regret_list}\n")


if __name__ == '__main__':
    main()
