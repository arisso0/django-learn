def get_catalog_filter(data: dict) -> tuple:
    """
    Получить фильтр для каталога из словаря
    :param data: набор фильтров из request
    """
    free_d = False if data.get("filter[freeDelivery]") == "false" else True
    available = False if data.get("filter[available]") == "false" else True

    query_lookups = {
        "price__gte": data.get("filter[minPrice]"),
        "price__lte": data.get("filter[maxPrice]"),
        "free_delivery": free_d,
        "category__id": int(data.get("category")),
    }
    if available:
        query_lookups.update({"count_product__gt": 0})

    name = data.get("filter[name]")
    if name and name != "any":
        query_lookups.update({"name__icontains": name})

    order_by = "created"
    match data.get("sort"):
        case "rating":
            order_by = "rating"
        case "price":
            order_by = "price"
        case "reviews":
            order_by = "reviews_count"
        case "date":
            order_by = "created"
    if data.get("sortType") == "dec":
        order_by = f"-{order_by}"

    return query_lookups, order_by
