

from datetime import timezone
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from . models import Plan, PurchasePlan, product, Customer, Cart,Payment,OrderPlaced,Wishlist
from . forms import CustomerRegistration, CustomerProfileForm 
from django.contrib import messages
from django.contrib.auth import logout,login
from django.http import HttpResponse, JsonResponse,HttpResponseBadRequest

from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from django.conf import settings
import razorpay
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator



# Create your views here.

@login_required(login_url= 'login')
def index(request):
    totalitem = 0
    wishlistcount = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishlistcount = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'user/index.html',locals())


@login_required(login_url= 'login')
def service(request):
    totalitem = 0
    wishlistcount = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishlistcount = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'user/service.html',locals())


@login_required(login_url= 'login')
def team(request):
    totalitem = 0
    wishlistcount = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishlistcount = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'user/team.html',locals())


@login_required(login_url= 'login')
def gallery(request):
    totalitem = 0
    wishlistcount = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishlistcount = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'user/gallery.html',locals())


def sample(request):
    return render(request, 'user/sample.html')



@login_required(login_url= 'login')
def about(request):
    totalitem = 0
    wishlistcount = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishlistcount = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'user/about-us.html',locals())

@login_required(login_url= 'login')
def contact(request):
    totalitem = 0
    wishlistcount = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishlistcount = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'user/contact.html',locals())


class CategoryView(View):
    def get(self, request, val):
        totalitem = 0
        wishlistcount = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishlistcount = len(Wishlist.objects.filter(user=request.user))
        Product = product.objects.filter(category=val)
        title = product.objects.filter(category=val).values('title')
        return render(request, 'user/category.html', locals())



class CategoryTitle(View):
    def get(self, request, val):        
        Product = product.objects.filter(title=val)
        title = product.objects.filter(category=Product[0].category).values('title')
        totalitem = 0
        wishlistcount = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishlistcount = len(Wishlist.objects.filter(user=request.user))
        return render(request, 'user/category.html', locals())


@method_decorator(login_required(login_url = 'login'),name='dispatch')
class ProductDetails(View):
    def get(self, request, pk):
        Product = product.objects.get(pk=pk)  
        wishlist = Wishlist.objects.filter(Q(product=Product) & Q(user=request.user))
        totalitem = 0
        wishlistcount = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishlistcount = len(Wishlist.objects.filter(user=request.user))
        return render(request,'user/productdetails.html',locals())

   


class CustemorRegistrationView(View):
    def get(self, request):
        form = CustomerRegistration()
        totalitem = 0
        wishlistcount = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishlistcount = len(Wishlist.objects.filter(user=request.user))
        return render(request, 'user/registration.html', locals())

    

    def post(self, request):
        form = CustomerRegistration(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('user/verify-email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            mail_subject = 'Activate your account.'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            messages.success(request,'An email has been sent to your email address. Please click on the link to verify your account.')
            return redirect('email_verification_sent')
        else:
            messages.warning(request, 'Invalid Input Data')
            return render(request, 'user/registration.html', locals())


def email_done(request):
    return render(request, 'user/email_done.html')


class AccountActivateView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'congratulation! User Activation SuccessFull')
            return redirect('email_done')
        else:
            messages.warning(request, 'Invalid Activation Link')
            return render(request, 'user/activation_failed.html', locals())


class EmailVerificationSentView(View):
    def get(self, request):
        return render(request, 'user/email_verification_sent.html')


class EmailVerificationView(View):
    def get(self, request):
        return render(request, 'user/email_verification_sent.html')


class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'user/login.html', locals())

    def post(self, request):
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome, {user.username}!')
            return redirect('profile')
        else:
            messages.warning(request, 'Invalid username or password.')
            return render(request, 'user/login.html', locals())


@method_decorator(login_required(login_url = 'login'),name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        totalitem = 0
        wishlistcount = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishlistcount = len(Wishlist.objects.filter(user=request.user))
        return render(request, 'user/profile.html', locals())

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']

            reg = Customer(user=user, name=name, locality=locality, mobile=mobile, city=city, state=state,zipcode=zipcode)

            reg.save()
            messages.success(request, 'congratulation! your detail is updated')
        else:
            messages.warning(request, 'Invalid Input')
        return render(request, 'user/profile.html', locals())


@login_required(login_url= 'login')
def address(request):
    add = Customer.objects.filter(user=request.user)
    totalitem = 0
    wishlistcount = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishlistcount = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'user/address.html', locals())


@method_decorator(login_required(login_url = 'login'),name='dispatch')
class UpdateAddress(View):
    def get(self, request, pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        totalitem = 0
        wishlistcount = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishlistcount = len(Wishlist.objects.filter(user=request.user))
        return render(request, 'user/updateaddress.html', locals())


    def post(self, request, pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request, 'Congradulation! Details Are Successfully Updated')
        else:
            messages.warning(request, 'Invalid Input')
        return redirect('address')



def logout_view(request):
    logout(request)
    request.session.flush()
    messages.success(request, 'You have been logged out successfully.')
    return redirect('index')



def my_view(request):
    request.session['my_key'] = 'my_value'


def my_view(request):
    response = HttpResponse('Hello, world!')
    response.set_cookie('my_cookie', 'my_value')
    return response


@login_required(login_url='login')
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    Product = get_object_or_404(product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=user, product=Product)

    if not created:
        # If the cart item already exists, increase the quantity by 1
        cart_item.quantity += 1
        cart_item.save()

    return redirect("/cart")
    


@login_required(login_url='login')
def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount = amount + 40
    totalitem = 0
    wishlistcount = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishlistcount = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'user/addtocart.html', locals())





class checkout(View):
    def get(self, request):
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items=Cart.objects.filter(user=user)
        totalitem = 0
        wishlistcount = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishlistcount = len(Wishlist.objects.filter(user=request.user))
        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount = famount + value
        totalamount = famount + 40
        razoramount = int(totalamount * 100)
        razorpay_key = settings.RAZOR_KEY_ID
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        data = {"amount":razoramount,"currency":"INR","receipt":"order_rcptid_12"}
        payment_response = client.order.create(data=data)
        print(payment_response)
        order_id = payment_response['id']
        order_status = payment_response['status']
        if order_status == 'created':
            payment = Payment(
                user=user,
                amount=totalamount,
                razorpay_order_id=order_id,
                razorpay_payment_status=order_status
            )
            payment.save()
        return render(request, 'user/checkout.html', locals())






def payment_done(request):
    
    try:
        order_id = request.GET.get('order_id')
        payment_id = request.GET.get('payment_id')
        cust_id = request.GET.get('cust_id')

        user = request.user
        customer = get_object_or_404(Customer, id=cust_id)
        payment = get_object_or_404(Payment, razorpay_order_id=order_id)

        payment.paid = True
        payment.razorpay_payment_id = payment_id
        payment.save()

        cart = Cart.objects.filter(user=user)
        for c in cart:
            OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity, payment=payment).save()
            c.delete()

        return redirect("orders")
    except (Customer.DoesNotExist, Payment.DoesNotExist):
        return redirect("index")
    except Exception as e:      
        print(str(e))
        return redirect("index")
     



@login_required(login_url='login')
def orders(request):
    order_placed = OrderPlaced.objects.filter(user=request.user)

    totalitem = 0
    wishlistcount = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishlistcount = len(Wishlist.objects.filter(user=request.user))

    return render(request, 'user/orders.html',locals())


# cart plus, minus and remove button functions
@login_required(login_url= 'login')
def plus_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)


@login_required(login_url= 'login')
def minus_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        if c.quantity >= 2:
           c.quantity -= 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)




@login_required(login_url= 'login')
def remove_cart(request):
    if request.method == "GET":
        prod_id = request.GET.get('prod_id')
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        
        user = request.user
        cart = Cart.objects.filter(user=user)
        
        if cart.exists():
            amount = 0
            for p in cart:
                value = p.quantity * p.product.discounted_price
                amount += value
            totalamount = amount + 40
            
            data = {
                'quantity': c.quantity,
                'amount': amount,
                'totalamount': totalamount
            }
        else:
            data = {'refresh': True}
        
        return JsonResponse(data)


@login_required(login_url='login')  
def plus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        Product = product.objects.get(id=prod_id)
        user = request.user
        # Check if the product already exists in the user's wishlist
        if not Wishlist.objects.filter(user=user, product=Product).exists():
            Wishlist(user=user, product=Product).save()
        data = {
            'message': "Wishlist Added Successfully",
        }
        return JsonResponse(data)


@login_required(login_url='login')
def minus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        Product = product.objects.get(id=prod_id)
        user = request.user
        Wishlist.objects.filter(user=user,product=Product).delete()
        data={
            'message':"Wishlist Remove Successfully",
        }
        return JsonResponse(data)


def wishlist_count(request):
    count = 0
    if request.user.is_authenticated:
        count = len(Wishlist.objects.filter(user=request.user))
    data = {
        'count': count,
    }
    return JsonResponse(data)


def search(request):
    query = request.GET['search']
    totalitem = 0
    wishlistcount = 0
    if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishlistcount = len(Wishlist.objects.filter(user=request.user))
    Product = product.objects.filter(Q(title__icontains=query))
    return render(request,"user/search.html",locals())


#>>>>>>>>>>>>>>>>>>>.23-05-23 <<<<<<<<<<<<<<<<<<<
@login_required(login_url= 'login')
def bmi(request):
    totalitem = 0
    wishlistcount = 0
    if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishlistcount = len(Wishlist.objects.filter(user=request.user))
    return render(request,'user/bmi.html',locals())


def calculate_bmi(request):
    if request.method == 'POST':
        height = float(request.POST.get('height'))
        weight = float(request.POST.get('weight'))
        age = int(request.POST.get('age'))
        sex = request.POST.get('sex')

        # Perform BMI calculation and determine the result
        bmi = weight / ((height/100) ** 2)

        # Determine the BMI category based on the calculated value
        if bmi < 18.5:
            category = ' - You are Underweight'
        elif 18.5 <= bmi <= 24.9:
            category = ' - You are Healthy'
        elif 25.0 <= bmi <= 29.9:
            category = ' - You are Overweight'
        else:
            category = ' - You are Obese'

        # Prepare the result HTML
        result_html = f'''
            <table id="resultTable">
                <tbody>
                    <tr>
                        <td class="point">{bmi:.1f}</td>
                        <td>{category}</td>
                    </tr>
                </tbody>
            </table>
        '''

        return HttpResponse(result_html)
    else:
        return HttpResponseBadRequest("Invalid request method.")




@login_required(login_url= 'login')
def time_table(request):
    totalitem = 0
    wishlistcount = 0
    if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishlistcount = len(Wishlist.objects.filter(user=request.user))
    return render(request,'user/class-timetable.html',locals())

@login_required(login_url= 'login')
def our_class(request):
    totalitem = 0
    wishlistcount = 0
    if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishlistcount = len(Wishlist.objects.filter(user=request.user))
    return render(request,'user/class-details.html',locals())


#<<<<<<<<<<<<< plan selection (25-05-23) >>>>>>>>>>>>>>>>>>>

@login_required(login_url='login')
def plan(request):
    plans = Plan.objects.all()

    totalitem = 0
    wishlistcount = 0
    if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishlistcount = len(Wishlist.objects.filter(user=request.user))
    return render(request,'user/plan.html',locals())



@login_required(login_url= 'login')
def plan_detail(request,plan_id):
    plan = Plan.objects.get(id = plan_id)
    user = request.user
    existing_plan = PurchasePlan.objects.filter(user=user).exists()
    razoramount = int(plan.price * 100)

    totalitem = 0
    wishlistcount = 0
    if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishlistcount = len(Wishlist.objects.filter(user=request.user))
    razorpay_key = settings.RAZOR_KEY_ID        
    return render(request,'user/plan_detail.html',locals())




def plan_payment_done(request):
    if request.method == 'POST':
        plan_id = request.POST.get('plan_id')
        amount = request.POST.get('amount')
        user = request.user
        plan = Plan.objects.get(id=plan_id)
        purchase = PurchasePlan(user=user, plan=plan)
        purchase.save()

        return redirect("currentplan")
    else:
        return redirect('plan')




@login_required(login_url='login')
def cancel_plan(request, plan_id):
    purchase_plan = get_object_or_404(PurchasePlan, id=plan_id, user=request.user)
    plan = purchase_plan.plan

    if plan.end_date and plan.end_date < timezone.now():
        plan.end_date = timezone.now()
        plan.save()

    purchase_plan.delete()
    return redirect('plan')
 


@login_required(login_url='login')
def current_plan(request):
    user = request.user

    try:
        purchase_plan = PurchasePlan.objects.select_related('plan').get(user=user)
        plan = purchase_plan.plan

        if plan.end_date and plan.end_date < timezone.now():
            plan.end_date = timezone.now()
            plan.save()
            purchase_plan.delete()
            plan = None

        if not plan:
            raise PurchasePlan.DoesNotExist

        start_date = timezone.now()
        end_date = start_date + timedelta(days=plan.duration * 30)
        plan.start_date = start_date
        plan.end_date = end_date
        plan.save()

        context = {
            'plan': plan,
            'cancel_plan_id': purchase_plan.id
        }
    except PurchasePlan.DoesNotExist:
        plan = None
        context = {}

    totalitem = 0
    wishlistcount = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishlistcount = len(Wishlist.objects.filter(user=request.user))

    return render(request, 'user/currentplan.html', context)







@login_required(login_url= 'login')
def wishlist(request):
    user = request.user
   
    Product = Wishlist.objects.filter(user=user)


    totalitem = 0
    wishlistcount = 0
    if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishlistcount = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'user/wishlist.html',locals())