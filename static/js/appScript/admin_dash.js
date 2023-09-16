$(document).ready(function(){
    initializePlanTable()
    let unsavedChanges = false;
    let unsavedInternalFormChanges = false
    
    $('#v-pills-home-tab').click(function(e){
        if ((unsavedChanges)  ||  (unsavedInternalFormChanges)){
            const shouldContinue = confirm("You have unsaved changes. Are you sure you want to leave?");
            if (!shouldContinue) {
                e.preventDefault();
            }
            else{   
                if(unsavedInternalFormChanges){
                    unsavedInternalFormChanges = false
                }
                else{
                    unsavedChanges= false 
                }
                showhideTabs('#v-pills-home','#v-pills-home-tab')                                                                                                                         
                TaskTable1.draw()
            }
        }
        else{
            showhideTabs('#v-pills-home','#v-pills-home-tab')
            TaskTable1.draw()
        }
    })
    $('#v-pills-profile-tab').click(function(e){
        if ((unsavedChanges)  ||  (unsavedInternalFormChanges)){
            const shouldContinue = confirm("You have unsaved changes. Are you sure you want to leave?");
            if (!shouldContinue) {
                e.preventDefault();
            }                                                                               
            else{
                if(unsavedInternalFormChanges){
                    unsavedInternalFormChanges = false
                }
                else{
                    unsavedChanges= false 
                }
                showhideTabs('#v-pills-accounts','#v-pills-profile-tab')                                                                                                                          
                $('.accounts-list-table').removeClass('d-none')
                $('.configure-form').addClass('d-none')
                initializeAllAccountOwnersDataTable()
            }
        }
        else{
            showhideTabs('#v-pills-accounts','#v-pills-profile-tab')
            $('.accounts-list-table').removeClass('d-none')
            $('.configure-form').addClass('d-none')
            initializeAllAccountOwnersDataTable()
        }
    })

    $('#v-pills-settings-tab').click(function(e){
        if ((unsavedChanges)  ||  (unsavedInternalFormChanges)){
            const shouldContinue = confirm("You have unsaved changes. Are you sure you want to leave?");
            if (!shouldContinue) {
                e.preventDefault();
            }
            else{
                if(unsavedInternalFormChanges){
                    unsavedInternalFormChanges = false
                }
                else{
                    unsavedChanges= false 
                }
                showhideTabs('#v-pills-settings','#v-pills-settings-tab')                                                                                                                             
                getAdminSettingsInfo()
            }
        }
        else{
            showhideTabs('#v-pills-settings','#v-pills-settings-tab')                                                                                                                                 
            getAdminSettingsInfo()
        }
    })
    
    const form = $('#main_settings_form');
    const form2 = $('#configurations_by_user');

    // Add event listener to detect changes in the input fields
    form.on('input', function () {
        unsavedChanges = true;
    });

    // Add event listener to detect changes in the input fields
    form2.on('input', function () {
        unsavedInternalFormChanges = true;
    });

    // Add event listener to detect when user is navigating away
    // $(window).on('beforeunload', function (e) {
    //     if (unsavedChanges) {
    //         e.preventDefault();
    //         e.returnValue = ''; // Modern browsers require this to show a custom message
    //     }
    //     if (unsavedInternalFormChanges) {
    //         e.preventDefault();
    //         e.returnValue = ''; // Modern browsers require this to show a custom message
    //     }
    // });

    var agent_role = []
    var cust_sentiment = []
    var agent_tone = []
    var chat_lang = []
    var chat_yni_tone = []
    $('#submit_config').click(function(){
        unsavedChanges= false
        agent_role.length = 0
        cust_sentiment.length = 0
        agent_tone.length = 0
        $.each( $('.agent-role input'), function(index, item){
            agent_role.push({'id':$(this).attr('data-id'),'ui_wording': $(this).val(),'api_wording':$('.api-role-group input[data-id="'+ $(this).attr('data-id')+'"]').val()});
        })
        $.each( $('.cust-sentiment input'), function(index, item){
            cust_sentiment.push({'id':$(this).attr('data-id'),'ui_wording': $(this).val(),'api_wording':$('.api-sentiment-group input[data-id="'+ $(this).attr('data-id')+'"]').val()});
        })
        $.each( $('.agent-tone input'), function(index, item){
            agent_tone.push({'id':$(this).attr('data-id'),'ui_wording': $(this).val(),'api_wording':$('.api-tone-group input[data-id="'+ $(this).attr('data-id')+'"]').val()});
        })
        $.each( $('.reply-language input'), function(index, item){
            chat_lang.push({'id':$(this).attr('data-id'),'ui_wording': $(this).val(),'api_wording':$('.api-language-group input[data-id="'+ $(this).attr('data-id')+'"]').val()});
        })
        $.each( $('.reply-yni-tone input'), function(index, item){
            chat_yni_tone.push({'id':$(this).attr('data-id'),'ui_wording': $(this).val(),'api_wording':$('.api-yni-tone-group input[data-id="'+ $(this).attr('data-id')+'"]').val()});
        })
        context = {'user_id':0,'role':agent_role,'sentiment':cust_sentiment,'tone':agent_tone, 'language':chat_lang, 'yni_tone':chat_yni_tone}
        updateConfiguration(context)
    })

    $(document).on('click','button.view_user_btn', function(){
        $('.accounts-list-table').addClass('d-none')
        $('.configure-form').removeClass('d-none')
        user_id = $(this).attr('id')
        getUserInfo(user_id)
        initializeProjectDataTable('admin',user_id)
    })

    var user_agent_role = []
    var user_cust_sentiment = []
    var user_agent_tone = []
    var user_chat_lang = []
    var user_chat_yni_tone = []
    var configurations = {}
    $(document).on('click','button.submit-user-config', function(){
        unsavedInternalFormChanges= false 
        user_agent_role.length = 0
        user_cust_sentiment.length = 0
        user_agent_tone.length = 0
        user_chat_lang.length = 0
        user_chat_yni_tone.length = 0
        $.each( $('.user-agent-role input'), function(index, item){
            user_agent_role.push({'id':$(this).attr('data-id'),'ui_wording': $(this).val(),'api_wording':$('.user-api-role-group input[data-id="'+ $(this).attr('data-id')+'"]').val()});
        })
        $.each( $('.user-cust-sentiment input'), function(index, item){
            user_cust_sentiment.push({'id':$(this).attr('data-id'),'ui_wording': $(this).val(),'api_wording':$('.user-api-sentiment-group input[data-id="'+ $(this).attr('data-id')+'"]').val()});
        })
        $.each( $('.user-agent-tone input'), function(index, item){
            user_agent_tone.push({'id':$(this).attr('data-id'),'ui_wording': $(this).val(),'api_wording':$('.user-api-tone-group input[data-id="'+ $(this).attr('data-id')+'"]').val()});
        })
        $.each( $('.user-language input'), function(index, item){
            user_chat_lang.push({'id':$(this).attr('data-id'),'ui_wording': $(this).val(),'api_wording':$('.user-api-language-group input[data-id="'+ $(this).attr('data-id')+'"]').val()});
        })
        $.each( $('.user-yni-tone input'), function(index, item){
            user_chat_yni_tone.push({'id':$(this).attr('data-id'),'ui_wording': $(this).val(),'api_wording':$('.user-api-yni-tone-group input[data-id="'+ $(this).attr('data-id')+'"]').val()});
        })
        configurations['role']=$('#role').val();
        configurations['sentiment']=$('#sentiment').val();
        configurations['tone']=$('#tone').val();
        configurations['language']=$('#language').val();
        configurations['yni_tone']=$('#yni_tone').val();
        context = {'user_id':$('.configure-form').attr('id'),'role':user_agent_role,'sentiment':user_cust_sentiment,'tone':user_agent_tone,'language':user_chat_lang,'yni_tone':user_chat_yni_tone,'configurations':configurations}
        updateConfiguration(context)
    })

})

function showhideTabs(tabId, tabBtnId){ 
    $('.nav-link').removeClass('active') 
    $('.tab-pane').removeClass('show active')
    $(tabId).addClass('active show')
    $(tabBtnId).addClass('active')
}

function getAdminSettingsInfo(){
    $.ajax({
        method:"GET",
        url:  '/get_admin_settings' ,
        success:function(data) {  
           result = data
           role = JSON.parse(result['role'])
           sentiment = JSON.parse(result['sentiment'])
           tone = JSON.parse(result['tone'])
           language = JSON.parse(result['language'])
           yni_tone = JSON.parse(result['yni_tone'])
           $('.ui-role-group .ui-role-select').html(``)
           $('.api-role-group .api-role-select').html(``)
           $('.ui-sentiment-group .ui-sentiment-select').html(``)
           $('.api-sentiment-group .api-sentiment-select').html(``)
           $('.ui-tone-group .ui-tone-select').html(``)
           $('.api-tone-group .api-tone-select').html(``)
           $('.ui-language-group .ui-language-select').html(``)
           $('.ui-yni-tone-group .ui-yni-tone-select').html(``)
           $('.api-language-group .api-language-select').html(``)
           $('.api-yni-tone-group .api-yni-tone-select').html(``)

           $.each(role, function(index, item){
            $('.ui-role-group .ui-role-select').append(
            `
            <div class="agent-role mb-2">
                <input type="text" class="form-control ui-role" data-id="${item.roleId}" value="${item.agentRoleUI}">
            </div>
            `
            )
            $('.api-role-group .api-role-select').append(
            `
            <div class="agent-role-api mb-2">
                <input type="text" class="form-control api-role"data-id="${item.roleId}" value="${item.agentRoleAPI}">
            </div>
            `
            )
           })
           $.each(sentiment, function(index, item){
            $('.ui-sentiment-group .ui-sentiment-select').append(
            `
            <div class="mb-2 cust-sentiment">
                <input type="text" class="form-control ui-sentiment}" data-id="${item.sentimentId}" value="${item.customerSentimentUI}">
            </div>
            `
            )
            $('.api-sentiment-group .api-sentiment-select').append(
            `
            <div class="mb-2 cust-sentiment-api">
                <input type="text" class="form-control api-sentiment" data-id="${item.sentimentId}" value="${item.customerSentimentAPI}">
            </div>
            `
            )
           })
           $.each(tone, function(index, item){
            $('.ui-tone-group .ui-tone-select').append(
            `
            <div class="mb-2 agent-tone">
                <input type="text" class="form-control ui-tone" data-id="${item.toneId}" value="${item.replyToneUI}">
            </div>
            `
            )
            $('.api-tone-group .api-tone-select').append(
            `
            <div class="mb-2 agent-tone-api">
                <input type="text" class="form-control api-tone" data-id="${item.toneId}" value="${item.replyToneAPI}">
            </div>
            `
            )
           })
           $.each(language, function(index, item){
            $('.ui-language-group .ui-language-select').append(
            `
            <div class="mb-2 reply-language">
                <input type="text" class="form-control ui-language" data-id="${item.languageId}" value="${item.replylanguageUI}">
            </div>
            `
            )
            $('.api-language-group .api-language-select').append(
            `
            <div class="mb-2 reply-language-api">
                <input type="text" class="form-control api-language" data-id="${item.languageId}" value="${item.replylanguageAPI}">
            </div>
            `
            )
           })
           $.each(yni_tone, function(index, item){
            $('.ui-yni-tone-group .ui-yni-tone-select').append(
            `
            <div class="mb-2 reply-yni-tone">
                <input type="text" class="form-control ui-yni-tone" data-id="${item.yniId}" value="${item.yniToneUI}">
            </div>
            `
            )
            $('.api-yni-tone-group .api-yni-tone-select').append(
            `
            <div class="mb-2 reply-yni-tone-api">
                <input type="text" class="form-control api-yni-tone" data-id="${item.yniId}" value="${item.yniToneAPI}">
            </div>
            `
            )
           })
        },
        error: function() {
            alert("Something went wrong, Please try again.")
        }
    })
}


function updateConfiguration(context){
    console.log(context)
    $.ajax({
        method:"POST",
        url: '/update_config/' ,
        data:  JSON.stringify(context),
        processData: false,
        contentType: false, 
        success:function(data) {  
            console.log(data)
            alert("saved successfully")
        },
        error: function() {
           alert("Something went wrong, Please try again.")
        }
    })
}

function getUserInfo(user_id){
    $.ajax({
        method:"GET",
        url: '/get_users/'+user_id ,
        success:function(data) {  
            $('.configure-form').attr('id',user_id)
            users_configure = JSON.parse(data['users_configure'])[0]
            role = JSON.parse(data['role'])
            sentiment = JSON.parse(data['sentiment'])
            tone = JSON.parse(data['tone'])
            language = JSON.parse(data['language'])
            yni_tone = JSON.parse(data['yni_tone'])
            $('#role').empty()
            $('#sentiment').empty()
            $('#tone').empty()
            $('#language').empty()
            $('#yni_tone').empty()
            $.each(role, function(index, item){
                $('#role').append(`<option value="${item.agentRoleAPI}">${item.agentRoleUI}</option>`);
            })
            $.each(sentiment, function(index, item){
                $('#sentiment').append(`<option value="${item.customerSentimentAPI}">${item.customerSentimentUI}</option>`);
            })
            $.each(tone, function(index, item){
                $('#tone').append(`<option value="${item.replyToneAPI}">${item.replyToneUI}</option>`);
            })
            $.each(language, function(index, item){
                $('#language').append(`<option value="${item.replylanguageAPI}">${item.replylanguageUI}</option>`);
            })
            $.each(yni_tone, function(index, item){
                $('#yni_tone').append(`<option value="${item.yniToneAPI}">${item.yniToneUI}</option>`);
            })
            try{
                selected_role = users_configure['role__agentRoleAPI']
                selected_sentiment = users_configure['sentiment__customerSentimentAPI']
                selected_tone = users_configure['tone__replyToneAPI']
                console.log(users_configure)
                selected_language = users_configure['language__replylanguageAPI']
                selected_yni_tone = users_configure['yni_tone__yniToneAPI']
                $('#role').val(selected_role)
                $('#sentiment').val(selected_sentiment)
                $('#tone').val(selected_tone) 
                $('#language').val(selected_language)
                $('#yni_tone').val(selected_yni_tone)
            }
            catch(e){
                console.log(e)
            }

            $('.user-ui-role-group .ui-role-select').html(``)
            $('.user-api-role-group .api-role-select').html(``)
            $('.user-ui-sentiment-group .ui-sentiment-select').html(``)
            $('.user-api-sentiment-group .api-sentiment-select').html(``)
            $('.user-ui-tone-group .ui-tone-select').html(``)
            $('.user-api-tone-group .api-tone-select').html(``)
            $('.user-ui-language-group .ui-language-select').html(``)
            $('.user-api-language-group .api-language-select').html(``)
            $('.user-ui-yni-tone-group .ui-yni-tone-select').html(``)
            $('.user-api-yni-tone-group .api-yni-tone-select').html(``)
            
            $.each(role, function(index, item){
                $('.user-ui-role-group .ui-role-select').append(
                `
                <div class="user-agent-role mb-2">
                    <input type="text" class="form-control ui-role" data-id="${item.roleId}" value="${item.agentRoleUI}">
                </div>
                `
                )
                $('.user-api-role-group .api-role-select').append(
                `
                <div class="user-agent-role-api mb-2">
                    <input type="text" class="form-control api-role"data-id="${item.roleId}" value="${item.agentRoleAPI}">
                </div>
                `
                )
            })
            $.each(sentiment, function(index, item){
                $('.user-ui-sentiment-group .ui-sentiment-select').append(
                `
                <div class="mb-2 user-cust-sentiment">
                    <input type="text" class="form-control ui-sentiment}" data-id="${item.sentimentId}" value="${item.customerSentimentUI}">
                </div>
                `
                )
                $('.user-api-sentiment-group .api-sentiment-select').append(
                `
                <div class="mb-2 user-cust-sentiment-api">
                    <input type="text" class="form-control api-sentiment" data-id="${item.sentimentId}" value="${item.customerSentimentAPI}">
                </div>
                `
                )
            })
            $.each(tone, function(index, item){
                $('.user-ui-tone-group .ui-tone-select').append(
                `
                <div class="mb-2 user-agent-tone">
                    <input type="text" class="form-control ui-tone" data-id="${item.toneId}" value="${item.replyToneUI}">
                </div>
                `
                )
                $('.user-api-tone-group .api-tone-select').append(
                `
                <div class="mb-2 user-agent-tone-api">
                    <input type="text" class="form-control api-tone" data-id="${item.toneId}" value="${item.replyToneAPI}">
                </div>
                `
                )
            })
            $.each(language, function(index, item){
                $('.user-ui-language-group .ui-language-select').append(
                `
                <div class="mb-2 user-language">
                    <input type="text" class="form-control ui-language" data-id="${item.languageId}" value="${item.replylanguageUI}">
                </div>
                `
                )
                $('.user-api-language-group .api-language-select').append(
                `
                <div class="mb-2 user-language-api">
                    <input type="text" class="form-control api-language" data-id="${item.languageId}" value="${item.replylanguageAPI}">
                </div>
                `
                )
            })
            $.each(yni_tone, function(index, item){
                $('.user-ui-yni-tone-group .ui-yni-tone-select').append(
                `
                <div class="mb-2 user-yni-tone">
                    <input type="text" class="form-control ui-yni-tone" data-id="${item.yniId}" value="${item.yniToneUI}">
                </div>
                `
                )
                $('.user-api-yni-tone-group .api-yni-tone-select').append(
                `
                <div class="mb-2 user-yni-tone-api">
                    <input type="text" class="form-control api-yni-tone" data-id="${item.yniId}" value="${item.yniToneAPI}">
                </div>
                `
                )
            })
        },
        error: function() {
            alert("Something went wrong, Please try again.")
        }
    })
}

function initializeProjectDataTable(role, user_id)
{
    if ($.fn.DataTable.isDataTable('#activity_table')) {
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
        pageLength: 25,
        oLanguage: {
           sZeroRecords: "No data found",
           sProcessing: '<i class="fa fa-spinner fa-spin fa-3x fa-fw"></i><span class="sr-only">Loading...</span>'
        },
        // order: [[0, "desc"]],        
        columns: [
            {
                data: null,
                render: function(data, type, full, meta) {
                    return meta.row + meta.settings._iDisplayStart + 1;
                }                   
            },
            {
                data: 'date',
                searchable: true,
            },
            {
                data: 'hit_count',
                searchable: true,
            },
       
        ],
        ajax: {
            "url":"/apihit_info/?role="+role+"&&user_id="+user_id,
            "data": function (d) {
                return $.extend( {},d, {
                    "search": {'value':$('#activity_table_filter input').val(),
                    'from_date':$('#from_date').val(),
                    'to_date': $('#to_date').val()
                }
                });
         }
        }
    }
    // Merge Table options With constant data
    // var FinalTableOptions = $.extend(basicDataTableProperties, projectDataTableProps);
    TaskTable = $('#activity_table').DataTable(FinalTableOptions);
}

function initializeAllAccountOwnersDataTable()
{
    if ($.fn.DataTable.isDataTable('.account-owners-table')) {
        // Destroy existing DataTable instance
        TaskTable2.destroy();
    }
    var FinalTableOptions = {
        searching: true,
        processing: true,
        serverSide: true,
        stateSave: false,
        responsive: true,
        pagination:true,
        pageLength: 100,
        oLanguage: {
           sZeroRecords: "No data found",
           sProcessing: '<i class="fa fa-spinner fa-spin fa-3x fa-fw"></i><span class="sr-only">Loading...</span>'
        },
        // order: [[0, "desc"]],        
        columns: [
            {
                data: null,
                render: function(data, type, full, meta) {
                    return meta.row + meta.settings._iDisplayStart + 1;
                }                   
            },
            {
                data: 'name',
                searchable: true,
            },
            {
                data: 'email',
                searchable: true,
            },
            {
                data: 'subs_plan',
                searchable: true,
                orderable:false,
            },
            {
                data: 'subs_interval',
                searchable: true,
                orderable:false,
            },
            {
                data: 'billing_date',
                searchable: true,
                orderable:false,
            },
            {
                data: 'status',
                searchable: true,
                orderable:false,
            },
            // {
            //     data: 'install_date',
            //     searchable: true,
            //     orderable:false,
            // },
            {
                data: 'last_date_api_call',
                searchable: true,
                orderable:false,
            },
            {
                data: 'id',
                render: function(data, type, full, meta) {
                    return `<button type="button" class="btn btn-primary view_user_btn" id="${data}">View</button>`
                } 
            }     
       
        ],
        ajax: {
            "url":"/get_users/",
            "data": function (d) {
                return $.extend( {},d, {
                    "search": {'value':$('.account-owners-table-div input').val(),
                }
                });
         }
        }
    }
    TaskTable2 = $('.account-owners-table').DataTable(FinalTableOptions);
}


function initializePlanTable()
{
    if ($.fn.DataTable.isDataTable('.plan-table')) {
        // Destroy existing DataTable instance
        TaskTable1.destroy();
    }
    var FinalTableOptions = {
        searching: true,
        processing: true,
        serverSide: true,
        stateSave: false,
        responsive: true,
        pagination:true,
        oLanguage: {
           sZeroRecords: "No data found",
           sProcessing: '<i class="fa fa-spinner fa-spin fa-3x fa-fw"></i><span class="sr-only">Loading...</span>'
        },
        // order: [[0, "desc"]],        
        columns: [
            {
                data: null,
                render: function(data, type, full, meta) {
                    return meta.row + meta.settings._iDisplayStart + 1;
                }                   
            },
            {
                data: 'title',
                searchable: true,
            },
            {
                data: 'interval',
                searchable: true,
            },
            {
                data: 'price',
                searchable: true,
            },
            {
                data: 'total_users',
                searchable: true,
                orderable:false
            },       
            {
                data: 'rewords_per_day',
                searchable: true,
            },       
        ],
        ajax: {
            "url":"/get_plans/",
            "data": function (d) {
                return $.extend( {},d, {
                    "search": {'value':$('.plan-table-div input').val(),
                }
                });
         }
        }
    }
    // Merge Table options With constant data
    TaskTable1 = $('.plan-table').DataTable(FinalTableOptions);
}