   path("shop/", views.shop,name="shop"),
    path("productdetail/<int:id>", views.product_detail, name="product_detail"),
    path("shop/<str:cat>", views.product_category, name="product_category"),
]