from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginate_objects(objs, items_per_page, page):

    paginator = Paginator(objs, items_per_page)

    try:
        objs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        objs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        objs = paginator.page(paginator.num_pages)

    return objs