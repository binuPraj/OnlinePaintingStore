from .models import Category

def category_context(request):
    categories = Category.objects.all()  # Fetch all categories
    """ subcategories = Sub_category.objects.all()  # Fetch all subcategories """
    context = {
        'categories': categories,  
        #'subcategories': subcategories, 
    }
    return context

