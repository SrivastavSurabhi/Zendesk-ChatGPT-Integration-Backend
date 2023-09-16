user_id= ""
list = window.location.href.split('&')
let token= list[list.length - 1 ].split('token=')[1]

$(window).on('load', function() {
    user_id= window.location.href.split('&')[0].split('=')[1]
    usersPricingInfo(user_id)
})

$(document).ready(function(){
    href = window.location.href
    $('#v-pills-invoices-tab').click(function(){
        cust_id = window.location.href.split('&')[0].split('=')[1]
        initializeInvoiceDataTable(cust_id)
    })

    $('.planCheck').click(function(){
        $('.card').removeClass('card-active')
        $(this).closest('.card').addClass('card-active')
    })
    
    $('.plan-interval-tab').click(function(){
        $('.planCheck').prop('checked',false)
    })

    $('.make-payment').on('click', function(){
        if ($('.planCheck:checked').length>0){
            $('.make-payment').parent().children('p').remove()
            checkedPlan = $('.planCheck:checked').val();
            period = $('.plan-interval-tab.active').attr('id')
            data = {}
            if (checkedPlan == 'professionalPlan' && period == 'month') {
                pricePlan = 'Professional Plan'
                interval = 'month'
            }
            else if (checkedPlan == 'professionalPlan' && period == 'year') {
                pricePlan = 'Professional Plan'
                interval = 'year'
            }
            else if(checkedPlan == 'growthPlan' && period == 'month'){
                pricePlan = 'Growth Plan'
                interval = 'month'
            }
            else if(checkedPlan == 'growthPlan' && period == 'year'){
                pricePlan = 'Growth Plan'
                interval = 'year'
            }
            data['pricePlan'] = pricePlan
            data['interval']= interval
            cust_id = window.location.href.split('&')[0].split('=')[1]
            $.ajax({
                method:"POST",
                url: '/billing/create-checkout-session/?user_id='+cust_id ,
                headers: {Authorization: "Bearer "+token},
                processData: false,
                contentType: false, 
                data:JSON.stringify(data),
                success:function(data) {  
                    console.log(data)
                    window.location.href= data['checkout_session']
                },
                error: function() {
                    console.log("error")
                }

            })
        }
        else{
            if($('.make-payment').parent().children('p').length == 0){
                $('.make-payment').parent().prepend(`<p style="color:red">Please check atleast one check to continue.</p>`)
            }  
        }
    })

    $(document).on('click','.view_invoice',function(){
        invoice_id = $(this).attr('id')
        $.ajax({
            method:"GET",
            url: '/billing/invoice-detail/?invoice_id='+invoice_id ,
            headers: {Authorization: "Bearer "+ token},
            processData: false,
            contentType: false, 
            success:function(data) {  
                window.location.href=data['pdf_url']
            },
            error: function() {
                console.log("error")
            }

        })
    })

    $(document).on('click','.confirm-cancel', function(){
        user_id = window.location.href.split('&')[0].split('=')[1]
        $.ajax({
            method:"GET",
            url: '/billing/cancel-plan/?user_id='+user_id ,
            headers: {Authorization: "Bearer "+ token},
            processData: false,
            contentType: false, 
            beforeSend: function() { 
                console.log("Before send")
            },
            complete: function() {
                console.log("Complete")
            },
            success:function(data) {  
                if(data['success']){
                    $('#confirmation_popup').modal('hide');
                    $('.cancel_plan_div button').prop('disabled',true);
                }
                else{
                    alert("Something went wrong please try again.")
                }
                
            },
            error: function() {
                console.log("error")
            }

        })
    })
})


// function getWordWandAPIToken(){
//     console.log(user_id)
//     if(token == undefined || token == "")
//     {
//         token = getJWTtoken(user_id);
//     }
//     return token;
// }

// function getJWTtoken(user_id){
//     $.ajax({
//         url:  '/get_jwt_token_by_id/',
//         data: { "user_id":user_id},
//         beforeSend: function() { 
//             console.log("before send")
//         },
//         complete: function() {
//             console.log("complete")     
//         },
//         success:function(data) {  
//             console.log("data",data)
//             token = data['token']
//         },
//         error: function() {
//             console.log("error")
//         }
//     })
//     return token
// }

function initializeInvoiceDataTable(user_id)
{
    if ($.fn.DataTable.isDataTable('#invoices-table')) {
        // Destroy existing DataTable instance
        TaskTable.destroy();
    }
    var FinalTableOptions = {
        searching: true,
        processing: true,
        serverSide: true,
        stateSave: false,
        responsive: true,
        pagination:true,
        order: [[ 0, "desc" ]],
        oLanguage: {
           sZeroRecords: "No data found",
           sProcessing: '<i class="fa fa-spinner fa-spin fa-3x fa-fw"></i><span class="sr-only">Loading...</span>'
        },    
        columns: [
            {
                data: null,
                render: function(data, type, full, meta) {
                    return meta.row + meta.settings._iDisplayStart + 1;
                }                   
            },
            {
                data: 'plan_name',
                searchable: true,
            },
            {
                data: 'start_date',
                searchable: true,
            },
            {
                data: 'end_date',
                searchable: true,
            },
            {
                data: 'status',
                searchable: true,
            },
            {
                data: 'invoice_id',
                render: function(data, type, full, meta) {
                    html =`<button class="btn btn-primary view_invoice" id="${data}">Download Invoice</button>`
                    return html;
                }  
            },
       
        ],
        ajax: {
            "url":"/billing/invoices/?user_id="+user_id,
            "headers": {Authorization: "Bearer "+token},

        }
    }
    // Merge Table options With constant data
    TaskTable = $('#invoices-table').DataTable(FinalTableOptions);
}

function usersPricingInfo(user_id){
    $.ajax({
        method:"GET",
        url: '/billing/user_info?user_id='+user_id ,
        headers: {Authorization: "Bearer "+ token},
        processData: false,
        contentType: false, 
        success:function(data) {  
           console.log(data)
           if(data['context']['error']){
            alert(data['context']['error'])
           }
           else{
           console.log(data['subscription_list'])
           result = data['context']
           email = result['user_email']
           $('.logged-in-user').text(result['user_email'])
           $('.make-payment').attr('disabled',false)
           if(result['subscription'] == 'active'){
            $('.cancel_plan_div button').prop('disabled', false)
            $('.user_plan_title').text(result['active_plan'])
           }
           else if(result['subscription'] == 'canceled'){
            $('.cancel_plan_div button').prop('disabled', true)
            $('.user_plan_title').text(result['active_plan'])
           }
           else if(result['subscription'] == 'inactive'){
            $('.cancel_plan_div button').prop('disabled', true)
            $('.user_plan_title').text(result['active_plan'])
           }
           else if(result['subscription'] == 'No Plan'){
            $('.cancel_plan_div button').prop('disabled', true)
            $('.user_plan_title').text(result['active_plan'])
           }
        }
        },
        error: function() {
            console.log("error")
        }

    })
}
