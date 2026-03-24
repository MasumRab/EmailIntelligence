import re
with open("src/backend/python_backend/category_routes.py", "r") as f:
    text = f.read()

text = text.replace('return CategoryResponse(**new_category.data)',
                    'print("DATA REC:", new_category.data)\n        return CategoryResponse(**new_category.data)')

with open("src/backend/python_backend/category_routes.py", "w") as f:
    f.write(text)
