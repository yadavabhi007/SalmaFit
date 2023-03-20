from django.urls import path, include
# from rest_framework import routers
from . import views

# router = routers.DefaultRouter()
# router.register()

urlpatterns = [
    # path('', include(router.urls)),
    path('countrycode/', views.CountryCodeView.as_view(), name='countrycode'),
    path('email/', views.EmailVerificationView.as_view(), name='email'),
    path('emailverify/', views.VerifyEmailView.as_view(), name='emailverify'),
    path('register/', views.UserRegistration.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('phoneverify/', views.PhoneVerificationView.as_view(), name='phoneverify'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('deactivate/', views.UserProfileDeactivateView.as_view(), name='deactivate'),
    path('changepassword/', views.UserChangePasswordView.as_view(), name='changepassword'),
    path('resetpassword/', views.ResetPassword.as_view(), name='resetpassword'),
    path('send-reset-password-email/', views.SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', views.UserPasswordResetView.as_view(), name='reset-password'),
    path('logout/', views.UserLogoutView.as_view(), name ='logout'),
    path('product/', views.ProductsView.as_view(), name='product'),
    path('addproduct/', views.ProductsAddView.as_view(), name='addproduct'),
    path('recentproducts/', views.RecentProductsView.as_view(), name='recentproducts'),
    path('pendingproducts/', views.PendingProductsView.as_view(), name='pendingproducts'),
    path('editproduct/', views.EditProductsView.as_view(), name='editproducts'),
    path('rejectedproducts/', views.RejectedProductsView.as_view(), name='rejectedproducts'),
    path('approvedproducts/', views.ApprovedProductsView.as_view(), name='approvedproducts'),
    path('occasionallyproducts/', views.OccasionallyProductsView.as_view(), name='occasionallyproducts'),
    path('rejectedwhiledietingproducts/', views.RejectedWhileDietingProductsView.as_view(), name='rejectedwhiledietingproducts'),
    path('notifications/', views.NotificationsView.as_view(), name='notifications'),
    path('notification/', views.NotificationRemoveView.as_view(), name='notification'),
]