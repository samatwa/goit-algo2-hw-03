import csv
import timeit
from BTrees.OOBTree import OOBTree

# Додавання до OOBTree (індексуємо по Price)
def add_item_to_tree (tree: OOBTree, item: dict) -> None:
    price = item['Price']
    if price not in tree:
        tree[price] = []
    tree[price].append(item)

# Додавання до dict
def add_item_to_dict(dct: dict, item: dict) -> None:
    dct[item['ID']] = item

# Запит до OOBTree (ефективний діапазон)
def range_query_tree (tree: OOBTree, min_price: float, max_price: float) -> list:
    result = []
    for items in tree.items(min_price, max_price):
        result.extend(items)
    return result

# Запит до dict (повільний лінійний пошук)
def range_query_dict(dct: dict, min_price: float, max_price: float) -> list:
    return [item for item in dct.values() if min_price <= item['Price'] <= max_price]

# Основна логіка
tree_price_indexed = OOBTree()
dictionary = {}

# Завантаження CSV
with open('generated_items_data.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        item = {
            'ID': int(row['ID']),
            'Name': row['Name'],
            'Category': row['Category'],
            'Price': float(row['Price'])
        }
        add_item_to_tree(tree_price_indexed, item)
        add_item_to_dict(dictionary, item)

# Параметри запиту
price_min = 50.0
price_max = 100.0

# Вимірювання часу виконання
tree_time = timeit.timeit(lambda: range_query_tree (tree_price_indexed, price_min, price_max), number=100)
dict_time = timeit.timeit(lambda: range_query_dict(dictionary, price_min, price_max), number=100)

print("Результати виконання 100 діапазонних запитів:")
print(f"Total range_query time for OOBTree: {tree_time:.6f} seconds")
print(f"Total range_query time for Dict:    {dict_time:.6f} seconds")

# Порівняння
if tree_time < dict_time:
    improvement = ((dict_time - tree_time) / dict_time) * 100
    print(f"OOBTree швидше на {improvement:.2f}%")
else:
    improvement = ((tree_time - dict_time) / tree_time) * 100
    print(f"Dict швидше на {improvement:.2f}%")