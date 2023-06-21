

from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from . forms import MyPasswordChangeForm,MySetPasswordForm,MyPasswordResetForm
from . views import EmailVerificationSentView,EmailVerificationView,LoginView,AccountActivateView
from django.contrib import admin


urlpatterns = [
    
    path('',views.index,name='index'),
    path('service/',views.service),
    path('team/',views.team),
    # path('class/',views.class_d),
    path('about/',views.about ,name='about'),
    path('contact/',views.contact ,name='contact'),
    path('sample/',views.sample),
    path('gallery/',views.gallery,name='gallery'),

    path("category/<slug:val>",views.CategoryView.as_view(),name="category"),
    path('categorytitle/<val>',views.CategoryTitle.as_view(),name='categorytitle'),
    path("productdetails/<int:pk>",views.ProductDetails.as_view(),name="productdetails"),
    path('profile/',views.ProfileView.as_view(),name='profile'),
    path('address/',views.address,name='address'),
    path('updateaddress/<int:pk>',views.UpdateAddress.as_view(),name='updateaddress'),
    
    #login authentication
    path('registration/',views.CustemorRegistrationView.as_view(), name='registration'),
    # path('accounts/login',auth_view.LoginView.as_view(template_name = 'user/login.html',authentication_form=LoginForm),name='login'),
    path('accounts/login/',LoginView.as_view() ,name='login'),
    path('profile/',views.ProfileView.as_view(), name='profile'),
    path('address/',views.ProfileView.as_view(), name='address'),

    #password changing
    path('passwordchange/',auth_view.PasswordChangeView.as_view(template_name='user/changepassword.html',form_class=MyPasswordChangeForm,success_url='/passwordcahangedone'),name='passwordchange'),

    path('passwordcahangedone/',auth_view.PasswordChangeDoneView.as_view(template_name='user/passwordcahangedone.html'),name='passwordcahangedone'),
    
    # PasswordReset
    path('password-reset/',auth_view.PasswordResetView.as_view(template_name='user/password_reset.html',form_class=MyPasswordResetForm) , name='password_reset'),
    path('password-reset/done/',auth_view.PasswordResetDoneView.as_view(template_name='user/password_reset_done.html') , name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_view.PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html',form_class=MySetPasswordForm) , name='password_reset_confirm'),
    path('password-reset-complete/',auth_view.PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html') , name='password_reset_complete'),

    path('logout/',views.logout_view,name='logout_view'),

    path('sample/',views.sample),


    # new >>>>>>>>>>>>>>>
    
    path('email-verification-sent/',EmailVerificationView.as_view(), name='email_verification_sent'),
    path('verify-email/<str:username>/<str:token>/', EmailVerificationSentView.as_view(), name='email_verification_sent_view'),
    path('activate/<uidb64>/<token>/',AccountActivateView.as_view(),name="activate"),
    path('email_done/',views.email_done,name='email_done'),

    # ADD TO CART
    path('add-to-cart/',views.add_to_cart,name='add-to-cart'),
    path('cart/',views.show_cart,name='showcart'),
    path('checkout/',views.checkout.as_view(),name='checkout'),
    path('paymentdone/',views.payment_done,name='paymentdone'),
    path('orders/',views.orders,name='orders'),
    path('search/',views.search,name='search'),
    
    

    #ajax-myscripts(folder in static)
    path('pluscart/',views.plus_cart),
    path('minuscart/',views.minus_cart),
    path("removecart/",views.remove_cart),
    path("pluswishlist/",views.plus_wishlist),
    path("minuswishlist/",views.minus_wishlist),
    path('wishlistcount/', views.wishlist_count, name='wishlist_count'),
    path('wishlist/',views.wishlist,name='wishlist'),

    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>  23-05-23  <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    path('calculate_bmi/',views.calculate_bmi,name="calculate_bmi"),
    path('bmi/',views.bmi,name="bmi"),

    

    path('timetable/',views.time_table,name="timetable"),
    path('class/',views.our_class,name="ourclass"),
    

    #<<<<<<<<<<<<< plan selection (25-05-23) >>>>>>>>>>>>>>>>>>>
    path('plan/',views.plan,name="plan"),
    path('plan_detail/<int:plan_id>/', views.plan_detail, name='plan_detail'),
    path('planpaymentdone/',views.plan_payment_done,name="planpaymentdone"),
    path('currentplan/',views.current_plan,name='currentplan'),
    path('cancel-plan/<int:plan_id>/', views.cancel_plan, name='cancel_plan'),
    
    

] +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header = "GYM Admin"
admin.site.site_title = "GYM Admin"
admin.site.site_index_title = "Welcome to GYM"