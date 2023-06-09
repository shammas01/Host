


# def post(self, request):
#         form = CustomerRegistration(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_active = False
#             user.save()
            
#             current_site = get_current_site(request)
#             message = render_to_string('user/email_verification.html', {
#                 'user': user,
#                 'domain': current_site.domain,
#                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                 'token': account_activation_token.make_token(user),
#             })
#             mail_subject = 'Activate your account.'
#             to_email = form.cleaned_data.get('email')
#             email = EmailMessage(mail_subject, message, to=[to_email])
#             email.send()
#             messages.success(request, 'An email has been sent to your email address. Please click on the link to verify your account.')
#             return redirect('email_verification_sent')
#         else:
#             messages.warning(request, 'Invalid Input Data')
#             return render(request, 'user/registration.html', locals())
        



# class AccountActivateView(View):
#     def get(self, request, uidb64, token):
#         try:
#             uid = force_str(urlsafe_base64_decode(uidb64))
#             user = User.objects.get(pk=uid)
#         except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#             user = None
        
#         if user is not None and account_activation_token.check_token(user, token):
#             user.is_active = True
#             user.save()
#             messages.success(request,'congratulation! User Activation SuccessFull')
#             return redirect('login')
#         else:
#             messages.warning(request,'Invalid Activation Link')
#             return render(request,'user/activation_failed.html', locals())



# def show_cart(request):
#     user = request.user
#     cart = Cart.objects.filter(user=user)
#     amount = 0
#     for p in cart:
#         value = p.quantity * p.product.discounted_price
#         amount = amount + value
#     totalamount = amount + 40
#     totalitem = 0
#     wishlistcount = 0
#     if request.user.is_authenticated:
#         totalitem = len(Cart.objects.filter(user=request.user))
#         wishlistcount = len(Wishlist.objects.filter(user=request.user))
#     return render(request, 'user/addtocart.html', locals())



#@login_required
# def remove_cart(request):
#     if request.method == "GET":
#         prod_id = request.GET['prod_id']
#         c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
#         c.delete()
#         user = request.user
#         cart = Cart.objects.filter(user=user)
#         amount = 0
#         for p in cart:
#             value = p.quantity * p.product.discounted_price
#             amount = amount + value
#         totalamount = amount + 40
#         data = {
#             'quantity': c.quantity,
#             'amount': amount,
#             'totalamount': totalamount
#         }
#         return  JsonResponse(data)


# CHECKOUT PAGE

<!-- <section class="pricing-section spad">


<div class="container">
    {% if messages %}
       {% for msg in messages %}
       <div class="alert alert-danger" role="alert">
        {{msg}}

       </div>
       {% endfor %}
    {% endif %}
    <div class="row mt-5">
        <div class="col-sm-6">
            <h4 style="color: coral;" >order summery</h4>
            <hr>
            {% for item in cart_items %}
            <div class="card mb-2">
                <div class="card-body">
                    <h5>Product: {{item.product.title}}</h5>
                    <p>Quantity: {{item.quantity}}</p>
                    <p class="fw-bold">Price {{item.product.discounted_price}}</p>
                </div>
            </div>
            {% endfor %}
            <p class="fw-bold">Total Cost + Rs. 40 = {{totalamount}}</p>
            <small style="color: green";>Terms and condition:</small>
        </div>
    <div class="col-sm-4 offset-sm-1">
        <h4 style="color: coral;" >Select Shipping Address </h4>
        <hr>
        <form method="post" id="myform">
            {% csrf_token %}
            {% for ad in add %}
            <div class="card">
                <div class="card-body">
                    <h5>{{ad.name}}</h5>
                    <p>Mobile: {{ad.mobile}}</p>
                    <p>{{ad.locality}} {{ad.city}} {{ad.state}} - {{ad.zipcode}}</p>
                </div>
            </div>
                <div class="form-check mt-2 mb-5">
                    <input class="form-check-input" type="radio" name="custid" id="custadd{{forloop.counter}}" value="{{ad.id}}">
                    <label class="form-check-label fw-bold" for="custadd{{forloop.counter}}" style="color: white;" >
                        Address: {{forloop.counter}}</label>                  
                </div>
            {% endfor %}

         <div class="form-check mb-3">
                <label for="totamount" class="form-check-label" style="color: white;">Total Amount</label>
                <input type="number" class="form-control" name="totamount" value={{totalamount}} readonly>
            
            <div class="text-end">
                <a href="{%url 'showcart'%} " type="button" class="btn btn-danger mt-3 px-5 fw-bold">Back</a>&nbsp&nbsp

                {% comment %} <button type="submit" class="btn btn-warning mt-3 px-5 fw-bold">Continue</button> {% endcomment %}
                <button id="rzp-button1" type="submit" class="btn btn-warning mt-3 px-5 fw-bold">Payment</button>
                  
            </div>   
        </div>

        </form>

    </div>
    </div>
</div>
</section>






<script>
    var options = {
        "key": "rzp_test_pcdquxRlrldDSu", // Enter the Key ID generated from the Dashboard
        "amount": "{{razoramount}}", // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
        "currency": "INR",
        "name": "GYM Products",
        "description": "Purchase Product",
        // "image": "https://example.com/your_logo",
        "order_id": "{{order_id}}", //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
        "handler": function (response){
            console.log("success")
            var form = document.getElementById("myform");
           // alert(response.razorpay_payment_id);
           // alert(response.razorpay_order_id);
           // alert(response.razorpay_signature)
           window.location.href = `http://localhost:8000/paymentdone?order_id=${response.razorpay_order_id}&payment_id=${response.razorpay_payment_id}&cust_id=${form.elements["custid"].value}`
        },
           
        "theme": {"color": "#3399cc"}
        
            
    };

    var rzp1 = new Razorpay(options);
    rzp1.on('payment.failed', function (response){
            // alert(response.error.code);
            alert(response.error.description);
           
    });
    document.getElementById('rzp-button1').onclick = function(e){
        console.log("button click")
        rzp1.open();
        e.preventDefault();
    }
</script>  -->




@login_required(login_url= 'login')
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
        context = {}
    
    totalitem = 0
    wishlistcount = 0
    if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishlistcount = len(Wishlist.objects.filter(user=request.user))

    return render(request, 'user/currentplan.html', context)




@login_required(login_url= 'login')
def cancel_plan(request,plan_id):
    purchase_plan = get_object_or_404(PurchasePlan, id=plan_id, user=request.user)
    plan = purchase_plan.plan

    plan.end_date = timezone.now()
    plan.save() 

    purchase_plan.delete()
    return redirect('currentplan')