from main.main.models import Product, Size, Category

category = Category.objects.create(title="Одежда")

category_another = Category()
category_another.title = "Обувь"
category_another.save()

product = Product.objects.create(title="Свитшот", weight=00, sku="1211212", category=Category.objects.get(id=2),
                                 size=Size.objects.get(id=3), quantity=1, price=1500.01)
product = Product.objects.create(title="Туфли", weight=0.56, sku="112233.122", category=Category.objects.get(id=3),
                                 size=Size.objects.get(id=4), quantity=1, price=1200.01)

for category_item in Category.objects.all():
    products = Product.objects.filter(category=category_item.id)
    for product_item in products:
        print("Товар: {} в категории {} ".format(product_item.title, category_item))
