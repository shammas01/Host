
$('.plus-cart').click(function(){
    var id=$(this).attr("pid").toString();
    var eml=(this.parentNode.children[2])
    console.log("pid =",id)

    $.ajax({
        type:"GET",
        url:"/pluscart",
        data:{
            prod_id:id
        },
        success:function(data){
            console.log("data =" ,data)
            eml.innerText = data.quantity
            document.getElementById("amount").innerText=data.amount
            document.getElementById("totalamount").innerText=data.totalamount
        }
    })
})



$('.minus-cart').click(function(){
    var id=$(this).attr("pid").toString();
    var eml=(this.parentNode.children[2])
    console.log("pid =",id)

    $.ajax({
        type:"GET",
        url:"/minuscart",
        data:{
            prod_id:id
        },
        success:function(data){
            console.log("data =" ,data)
            eml.innerText = data.quantity
            document.getElementById("amount").innerText=data.amount
            document.getElementById("totalamount").innerText=data.totalamount
        }
    })
})



$('.remove-cart').click(function() {
  var id = $(this).attr("pid").toString();
  var eml = this;
  console.log("pid =", id);
  console.log("eml =",eml);

  $.ajax({
      type: "GET",
      url: "/removecart",
      data: {
          prod_id: id
      },
      success: function(data) {
          console.log("data =", data);
          if (data.refresh) {
              location.reload(); // Refresh the page
          } else {
              eml.innerText = data.quantity;
              document.getElementById("amount").innerText = data.amount;
              document.getElementById("totalamount").innerText = data.totalamount;
              eml.parentNode.parentNode.parentNode.parentNode.remove();
          }
      }
  });
});






$(document).on('click', '.plus-wishlist', function() {
    var button = $(this);
    var productId = button.attr("pid");

    $.ajax({
        type: "GET",
        url: "/pluswishlist",
        data: {
            prod_id: productId
        },
        success: function(data) {
            button.removeClass('plus-wishlist').addClass('minus-wishlist');
            button.html('<i class="fa-solid fa-heart fa-xl" style="color: #ffffff;"></i>');
            updateWishlistCount();
        }
    });
});




$(document).on('click', '.minus-wishlist', function() {
    var button = $(this);
    var productId = button.attr("pid");

    $.ajax({
        type: "GET",
        url: "/minuswishlist",
        data: {
            prod_id: productId
        },
        success: function(data) {
            button.removeClass('minus-wishlist').addClass('plus-wishlist');
            button.html('<i class="fa-solid fa-heart-circle-plus fa-xl" style="color: #ffffff;"></i>');
            updateWishlistCount();
        }
    });
});

function updateWishlistCount() {
    $.ajax({
        type: "GET",
        url: "/wishlistcount",
        success: function(data) {
            $('#wishlist-count').text(data.count);
        }
    });
}






$(document).ready(function() {
    // Form submission event handler
    $('#bmiForm').submit(function(event) {
      event.preventDefault(); // Prevent form submission
  
      // Get form data
      var height = $('#heightInput').val();
      var weight = $('#weightInput').val();
      var age = $('#ageInput').val();
      var sex = $('#sexInput').val();
  
      // Send AJAX request
      $.ajax({
        type: 'POST',
        url: '/calculate_bmi/',  // URL to your backend view
        data: {
          'height': height,
          'weight': weight,
          'age': age,
          'sex': sex
        },
        headers: {
          'X-CSRFToken': getCookie('csrftoken') // Include the CSRF token in the request headers
        },
        success: function(response) {
          // Display result in the popup
          showResultPopup(response);
        },
        error: function(xhr, textStatus, error) {
          console.log(error); // Handle error if necessary
        }
      });
    });
  
    // Close button click event handler
    $('#closeBtn').click(function() {
      hideResultPopup();
    });
  
    // Function to show the result popup
    function showResultPopup(html) {
      $('#resultContent').html(html);
      $('#resultPopup').fadeIn();
    }
  
    // Function to hide the result popup
    function hideResultPopup() {
      $('#resultPopup').fadeOut();
    }
  
    // Function to retrieve the CSRF token from the cookie
    function getCookie(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
          var cookie = jQuery.trim(cookies[i]);
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    }
  });
  
  
  





