from django.db import models


class Catalog(models.Model):
    name = models.CharField("Название", max_length=2000)
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name="Родительская категория",
    )
    image = models.ImageField("Изображение", upload_to="media/")

    updated = models.DateTimeField("Обновлено", auto_now=True)
    created = models.DateTimeField("Создано", auto_now_add=True)

    def __str__(self):
        return self.name

    def get_subcategories(self):
        res = []
        subcategories = Catalog.objects.filter(parent=self)
        if subcategories:
            for i in subcategories:
                res.append(
                    {
                        "id": i.id,
                        "title": i.name,
                        "image": {
                            "src": i.image.url,
                            "alt": i.image.name,
                        },
                    },
                )
        return res

    def get_image(self):
        return {
            "src": self.image.url,
            "alt": self.image.name,
        }

    class Meta:
        verbose_name = "Категория каталога"
        verbose_name_plural = "Категории каталога"


class Tag(models.Model):
    name = models.CharField("Название", max_length=2000)
    category = models.ManyToManyField(Catalog, verbose_name="Категория")

    updated = models.DateTimeField("Обновлено", auto_now=True)
    created = models.DateTimeField("Создано", auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"


class Product(models.Model):
    category = models.ForeignKey(Catalog, on_delete=models.CASCADE, verbose_name="Категория")
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    name = models.CharField("Название", max_length=2000)
    short_description = models.TextField("Короткое описание", null=True, blank=True)
    full_description = models.TextField("Полное описание", null=True, blank=True)
    free_delivery = models.BooleanField("Бесплатная доставка", default=False)
    count_product = models.PositiveIntegerField("Количество на складе")
    is_active = models.BooleanField("Активно", default=True)
    tags = models.ManyToManyField(Tag, null=True, blank=True, verbose_name="Теги")
    is_limited = models.BooleanField("Лимитированное", default=False)

    updated = models.DateTimeField("Обновлено", auto_now=True)
    created = models.DateTimeField("Создано", auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def reviews_count(self):
        reviews = Review.objects.filter(product=self)
        return reviews.count()

    @property
    def rating(self):
        rates = list(Review.objects.filter(product=self).values_list("rate", flat=True))
        if rates:
            return round(sum(rates) / len(rates), 2)
        else:
            return 0

    def get_tags(self):
        res = []
        tags = self.tags.all()
        for tag in tags:
            res.append({"id": tag.pk, "name": tag.name})
        return res

    def get_images(self):
        res = []
        images = Image.objects.filter(product=self)
        if images:
            for i in images:
                res.append({"src": i.src.url, "alt": i.src.name})
        return res

    def get_reviews(self):
        reviews = Review.objects.filter(product=self)
        res = []
        if reviews:
            for i in reviews:
                res.append(
                    {
                        "author": i.author,
                        "email": i.email,
                        "text": i.text,
                        "rate": i.rate,
                        "date": i.created,
                    },
                )
        return res

    def get_specifications(self):
        specs = SpecificationProduct.objects.filter(product=self)
        res = []
        if specs:
            for i in specs:
                res.append({"name": i.specification.name, "value": i.value})
        return res

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class Specification(models.Model):
    name = models.CharField("Название", max_length=2000)

    updated = models.DateTimeField("Обновлено", auto_now=True)
    created = models.DateTimeField("Создано", auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Справочник характеристик"
        verbose_name_plural = "Справочник характеристик"


class SpecificationProduct(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="spec_product",
        verbose_name="Товар",
    )
    specification = models.ForeignKey(
        Specification,
        on_delete=models.CASCADE,
        related_name="spec_spec",
        verbose_name="Характеристика",
    )
    value = models.CharField("Значение", max_length=100)

    updated = models.DateTimeField("Обновлено", auto_now=True)
    created = models.DateTimeField("Создано", auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} : {self.specification.name}"

    class Meta:
        verbose_name = "Характеристика товара"
        verbose_name_plural = "Характеристики товара"


class Review(models.Model):
    author = models.CharField("Автор", max_length=2000)
    email = models.EmailField("Email", max_length=200)
    text = models.CharField("Текст отзыва", max_length=2000)
    rate = models.PositiveSmallIntegerField("Оценка")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")

    updated = models.DateTimeField("Обновлено", auto_now=True)
    created = models.DateTimeField("Создано", auto_now_add=True)

    def __str__(self):
        return f"{self.author}: {self.product.name}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    src = models.ImageField()


# region -- Sales and Banners --


class Banner(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")

    updated = models.DateTimeField("Обновлено", auto_now=True)
    created = models.DateTimeField("Создано", auto_now_add=True)

    def __str__(self):
        return f"{self.product.name}"

    class Meta:
        verbose_name = "Товар на баннере главной страницы"
        verbose_name_plural = "Товары на баннере главной страницы"


class Sales(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    sale_price = models.FloatField("Цена товара по скидке")
    date_from = models.DateField("Дата начала действия акционной цены")
    date_to = models.DateField("Дата окончания действия акционной цены")

    updated = models.DateTimeField("Обновлено", auto_now=True)
    created = models.DateTimeField("Создано", auto_now_add=True)

    def __str__(self):
        return f"{self.product.name}"

    def valid_date_from(self):
        return self.date_from.strftime("%d.%m")

    def valid_date_to(self):
        return self.date_to.strftime("%d.%m")

    class Meta:
        verbose_name = "Товар на распродаже"
        verbose_name_plural = "Товары на распродаже"


# endregion
