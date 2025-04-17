$(document).ready(function() {
    alertify.set('notifier', 'position', 'top-right');
    alertify.set('notifier', 'delay', 5);
    function showNotification(type, message) {
        var icon = '';
        if (type === 'success') {
            icon = '✔';  // Checkmark for success
        } 
        else if (type === 'error') {
            icon = '';  // 
        }
        else if(type=='other'){
            icon='';
        }
        alertify.notify(icon + ' ' + message, type, 5);
    }

    $('.addToCartbtn').click(function (e) { 
        e.preventDefault();
        
        var product_uid = $(this).closest('.product_data').find('.prod_uid').val(); 
        var product_qty = $(this).closest('.product_data').find('.qty-input').val(); 
        var token = $('input[name=csrfmiddlewaretoken]').val(); // CSRF token

        $.ajax({
            type: "POST",
            url: "/addtocart/",  
            data: {
                'product_uid': product_uid,
                'product_qty': product_qty,
                csrfmiddlewaretoken: token
            },
            success: function (response) {
                console.log(response);
                if (response.message) {
                    if (response.status === 'success') {
                        showNotification('success', response.message);
                    } else {
                        showNotification('error', response.message);
                    }
                }
            }
        });
    });

    $('.addToWishlistbtn').click(function (e) { 
        e.preventDefault();
        
        var product_uid = $(this).closest('.product_data').find('.prod_uid').val(); 
        var token = $('input[name=csrfmiddlewaretoken]').val(); // CSRF token

        $.ajax({
            type: "POST",
            url: "/addtowishlist/",  
            data: {
                'product_uid': product_uid,
                csrfmiddlewaretoken: token
            },
            success: function (response) {
                console.log(response);
                
            },
        });
    });

    
    $('.updatewishlist').click(function (e) {
        e.preventDefault();
    
        var product_uid = $(this).closest('.product_data').find('.prod_uid').val();
        var token = $('input[name=csrfmiddlewaretoken]').val(); 
        var icon = $(this).find('i'); 
    
        $.ajax({
            type: "POST",
            url: "/updatewishlist/",  
            data: {
                'product_uid': product_uid,
                csrfmiddlewaretoken: token
            },
            success: function (response) {
                console.log(response);

                //item added to cart
                if (response.status === 'added') {
                    icon.removeClass('fa-heart-o').addClass('fa-heart'); 
                    icon.css('color', 'red'); 
                    //showNotification('success', 'Added to wishlist');
                }
                //item removed on reclicking
                else if (response.status === 'removed') {
                    icon.removeClass('fa-heart').addClass('fa-heart-o'); 
                    icon.css('color', ''); 
                    //showNotification('success', 'Removed from wishlist');
                }
            },
        });
    });
    
        // Check wishlist status when the page loads to apply red color to the heart icon for items already in the wishlist
    $('.product_data').each(function () {
        var product_uid = $(this).find('.prod_uid').val();
        var icon = $(this).find('.updatewishlist i'); // Get the heart icon for this product

        $.ajax({
            type: "GET",
            url: "/checkwishlist/",  
            data: {
                'product_uid': product_uid
            },
            success: function (response) {
                if (response.in_wishlist) {
                    icon.removeClass('fa-heart-o').addClass('fa-heart'); // Change to filled heart
                    icon.css('color', 'red'); // Set the heart to red
                }
            }
        });
    });

    $('.changeQuantity').click(function (e) { 
        e.preventDefault();
        
        var product_uid = $(this).closest('.product_data').find('.prod_uid').val(); 
        var product_qty = $(this).closest('.product_data').find('.qty-input').val(); 
        var token = $('input[name=csrfmiddlewaretoken]').val(); // CSRF token
        $.ajax({
            type: "POST",
            url: "/updatecart/",  
            data: {
                'product_uid': product_uid,
                'product_qty': product_qty,
                csrfmiddlewaretoken: token
            },
            success: function (response) {
                console.log(response);
            }
        });
    });

    // for deleting item from cart
    $('.delete-cart-item').click(function (e) { 
        e.preventDefault();

        var product_uid = $(this).closest('.product_data').find('.prod_uid').val(); 
        var product_qty = $(this).closest('.product_data').find('.qty-input').val();
        var token = $('input[name=csrfmiddlewaretoken]').val(); // CSRF token

        $.ajax({
            type: "POST",
            url: "/deletecartitem/",
            data: {
                'product_uid': product_uid,
                'product_qty': product_qty,
                 csrfmiddlewaretoken: token
            },
            success: function (response) {
                console.log(response);
                sessionStorage.setItem('notificationType', 'success');
                sessionStorage.setItem('notificationMessage', 'Removed from cart');
                // $('.cart_data').load(location.href + " .cart_data");
                location.reload();
            }
        });
    });

    // for deleting item from wishlist
    $('.delete-wishlist-item').click(function (e) { 
        e.preventDefault();

        var product_uid = $(this).closest('.product_data').find('.prod_uid').val(); 
        var token = $('input[name=csrfmiddlewaretoken]').val(); // CSRF token

        $.ajax({
            type: "POST",
            url: "/deletewishlistitem/",
            data: {
                'product_uid': product_uid,
                 csrfmiddlewaretoken: token
            },
            success: function (response) {
                console.log(response);
                sessionStorage.setItem('notificationType', 'success');
                sessionStorage.setItem('notificationMessage', 'Removed from wishlist');
                location.reload();
                // $('.wishlist_data').load(location.href + " .wishlist_data");
                // showNotification('success','Removed from wishlist');
            }
        });
    });

    //addtocart from wishlist and remove from there
    $('.addToCartbtnr').click(function (e) { 
        e.preventDefault();
        var product_uid = $(this).closest('.product_data').find('.prod_uid').val(); 
        var product_qty = $(this).closest('.product_data').find('.qty-input').val(); 
        var token = $('input[name=csrfmiddlewaretoken]').val(); // CSRF token

        $.ajax({
            type: "POST",
            url: "/addtocartr/",  
            data: {
                'product_uid': product_uid,
                'product_qty': product_qty,
                csrfmiddlewaretoken: token
            },
            success: function (response) {
                console.log(response);
                if (response && response.message && response.status) {
                    if (response.status === 'success') {
                        sessionStorage.setItem('notificationType', 'success');
                        sessionStorage.setItem('notificationMessage', response.message);
                    }
                }
                location.reload(); 
            }
            
        });
    });

    //add all to cart from wishlist
    $('.addAllToCartbtn').click(function (e) {
        e.preventDefault();
    
        var token = $('input[name=csrfmiddlewaretoken]').val(); // 
        var product_qty = 1;
    
        $.ajax({
            type: "POST",
            url: "/addtocartfromwishlist/", 
            data: {
                'product_qty': product_qty,
                csrfmiddlewaretoken: token
            },
            success: function (response) {
                console.log(response);
                if (response.message) {
                    if (response.status === 'success') {
                        sessionStorage.setItem('notificationType', 'success');
                        sessionStorage.setItem('notificationMessage', response.message);
                    } 
                }
                // if (response.out_of_stock) {
                //     alert("The following items were out of stock: " + response.out_of_stock.join(", "));
                // }
                location.reload(); 
            },
        });
    });

    //for placing order
    // $('.purch').click(function (e) {
    //     e.preventDefault();
    //     e.stopPropagation(); 
    //     const fname = $('#fname').val();
    //     const lname = $('#lname').val();
    //     const contact = $('#contact').val();
    //     const district = $('#district').val();
    //     const city = $('#city').val();
    //     const street = $('#street').val();
    //     const paymentMode = $('input[name=payment_mode]:checked').val();

    //     if (!fname || !lname || !contact || !district || !city || !street) {
    //         showNotification('error', 'Please fill all the fields');
    //         return; 
    //     }
    //     if (!paymentMode) {
    //         showNotification('error', "Please select a payment method");
    //         return  
    //     }
    //     const formData = {
    //         fname: $('#fname').val(),
    //         lname: $('#lname').val(),
    //         email: $('#email').val(),
    //         contact: $('#contact').val(),
    //         district: $('#district').val(),
    //         city: $('#city').val(),
    //         street: $('#street').val(),
    //         payment_mode: $('input[name=payment_mode]:checked').val(),
    //         total_price: $('input[name=total_price]').val(),
    //         csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
    //     };
    
    //     $.ajax({
    //         type: 'POST',
    //         url: "/placeorder/", 
    //         data: formData,
    //         success: function (response) {
    //             console.log(response);
    //             if (response.message) {
    //                 // Only show the notification once
    //                 if (response.status === 'success') {
    //                     showNotification('success', response.message);
    //                 } else if (response.status === 'error') {
    //                     showNotification('error', response.message);
    //                 }
    //             }
    //         },
    //         error: function (xhr, status, error) {
    //             // Handle error response
    //             showNotification('error', `An error occurred: ${xhr.responseText || error}`);
    //         }
    //     });
    // });
    $('.purch').click(function (e) {
        e.preventDefault();
        e.stopPropagation(); 
    
        const fname = $('#fname').val();
        const lname = $('#lname').val();
        const contact = $('#contact').val();
        const country = $('#country').val();
        const city = $('#city').val();
        const street = $('#street').val();
        const paymentMode = $('input[name=payment_mode]:checked').val();
        
        if (!fname || !lname || !contact || !country || !city || !street) {
            showNotification('error', 'Please fill all the fields');
            return; 
        }
        if (!paymentMode) {
            showNotification('error', "Please select a payment method");
            return;  
        }
    
        const formData = {
            fname: fname,
            lname: lname,
            email: $('#email').val(),
            contact: contact,
            country: country,
            city: city,
            street: street,
            payment_mode: paymentMode,
            total_price: $('input[name=total_price]').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        };
    
        // Sending data via AJAX (POST)
        $.ajax({
            type: 'POST',
            url: "/placeorder/",  // Your URL
            data: formData,
            success: function (response) {
                if (paymentMode === "paypal" && response.billing_page_url) {
                    // Redirect to PayPal for payment
                    const form = $('<form method="POST" action="' + response.billing_page_url + '" target="_blank">');
                    form.append('<input type="hidden" name="csrfmiddlewaretoken" value="' + formData.csrfmiddlewaretoken + '">');
                    form.append('<input type="hidden" name="fname" value="' + formData.fname + '">');
                    form.append('<input type="hidden" name="lname" value="' + formData.lname + '">');
                    form.append('<input type="hidden" name="email" value="' + formData.email + '">');
                    form.append('<input type="hidden" name="contact" value="' + formData.contact + '">');
                    form.append('<input type="hidden" name="country" value="' + formData.country + '">');
                    form.append('<input type="hidden" name="city" value="' + formData.city + '">');
                    form.append('<input type="hidden" name="street" value="' + formData.street + '">');
                    form.append('<input type="hidden" name="payment_mode" value="' + formData.payment_mode + '">');
                    form.append('<input type="hidden" name="total_price" value="' + formData.total_price + '">');
                    
                    $('body').append(form);
                    form.submit();  // Submit the form to PayPal in a new tab
                    console.log("Data being sent to billing page:", formData);
                } else if (paymentMode === "COD" && response.success_page_url) {
                    window.location.href = response.success_page_url;
                } else {
                    showNotification('error', 'Unexpected error occurred. Please try again.');
                }
            },
            error: function (xhr, status, error) {
                showNotification('error', `An error occurred: ${xhr.responseText || error}`);
            }
        });
    });
   
    var notificationType = sessionStorage.getItem('notificationType');
    var notificationMessage = sessionStorage.getItem('notificationMessage');

    if (notificationType && notificationMessage) {
        // Show the notification
        showNotification(notificationType, notificationMessage);
        // Clear the stored notification
        sessionStorage.removeItem('notificationType');
        sessionStorage.removeItem('notificationMessage');
    }
    
});




    


