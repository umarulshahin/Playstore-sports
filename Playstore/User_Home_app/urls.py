from django.urls import path
from . import views

urlpatterns = [
    path('',views.Dashbord,name="Dashbord"),
    
    path('all_product/',views.All_Product,name="all_product"),
    
    path('view_product/<int:id>',views.View_Product,name="view_product"),
    
    path('user_profile/',views.User_Profile,name="user_profile"),
    
    path('edit_profile/<int:id>',views.Edit_Profile,name="edit_profile"),
    
    path('addresses/',views.Addresses,name="addresses"),
    
    path('add_address/',views.Add_Address,name="add_address"),
    
    path('delete_address/<int:id>',views.Delete_Address,name="delete_address"),
    
    path('edit_address/',views.Edit_Address,name="edit_address"),
    
    path('add-to-cart',views.Add_to_Cart,name="add_to_cart"),
    
    path('cart/',views.User_Cart,name="user_cart"),
    
    path('update-quantity/',views.update_quantity_view, name="update_quantity"),
    
    path('delete_cart/<int:product_id>/', views.Delete_Cart, name="delete_cart"),
    
    path('checkout/',views.Checkout,name="checkout"),
    
    path('edit_checkout_address/',views.Checkout_Edit_Address, name="edit_checkout_address"),
    
    path('checkout_add_address/',views.Checkout_Add_Address, name="checkout_add_address"),
    
    path('user_order',views.User_Order,name='user_order'),
    
    path('confirmation',views.Confirmation,name='confirmation'),
    
    path('my_order/',views.My_Order,name="my_order"),
    
    path('order_details/<int:id>',views.Order_Details,name="order_details"),
    
    path('cancellation/<int:id>',views.Cancellation,name="cancellation"),
    
    path('pay_with_upi',views.Pay_With_Upi,name="pay_with_upi"),
    
    path('new_password/',views.New_Password,name="new_password"),
    
    path('orders_bill<int:id>',views.Orders_Bill,name="orders_bill"),
    
    path('suggestions/', views.Suggestions, name="suggestions"),  
    
    path('add_wishlist/',views.Add_Wishlist,name="add_wishlist"),
    
    path('user_wishlist/',views.User_Wishlist,name="user_wishlist"),
    
    path('remove_wishlist/<int:id>',views.Remove_Wishlist,name="remove_wishlist"),
    
    path('my_wallet/',views.My_Wallet,name="my_wallet"),
    
    path("wallet_upi/",views.Wallet_upi,name="wallet_upi"),
    
    path("wallet_recharge/",views.wallet_Recharge,name="wallet_recharge"),
    
    path("return/<int:id>",views.Return,name="return"),
    
      

    
    

]
