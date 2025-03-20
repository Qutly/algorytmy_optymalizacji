import random


class Item:
    def __init__(self, id, value, weight):
        self.id = id
        self.value = value
        self.weight = weight

    def __str__(self):
        return f"Id: {self.id}, Value: {self.value}, Weight: {self.weight}\n"


class Problem:
    def __init__(self, n, seed, external_items=None):
        self.items = external_items if external_items else []
        if external_items is None:
            random.seed(seed)
            self.items_number = n
            for i in range(n):
                value = random.randint(1, 10)
                weight = random.randint(1, 10)
                self.items.append(Item(i + 1, value, weight))
            else:
                self.items_number = len(self.items)

    def __str__(self):
        return "\n".join(str(item) for item in self.items).strip()

    def solve(self, capacity):
        sorted_items = sorted(self.items, key=lambda x: x.value / x.weight, reverse=True)

        items_id = []
        value_sum = 0
        weight_sum = 0

        for item in sorted_items:
            if weight_sum + item.weight <= capacity:
                weight_sum += item.weight
                value_sum += item.value
                items_id.append(item.id)

        return Result(items_id, value_sum, weight_sum)


class Result:
    def __init__(self, items_id, value_sum, weight_sum):
        self.items_id = items_id
        self.value_sum = value_sum
        self.weight_sum = weight_sum

    def __str__(self):
        return (f"Items in backpack: {', '.join(map(str, self.items_id))}\n"
                f"Total value: {self.value_sum}\n"
                f"Total weight: {self.weight_sum}")


if __name__ == "__main__":
    n = int(input("Enter the number of items: "))
    seed = int(input("Enter the seed: "))

    problem = Problem(n, seed)
    print(problem)

    backpack_capacity = int(input("Enter the backpack capacity: "))

    result = problem.solve(backpack_capacity)
    print(result)
