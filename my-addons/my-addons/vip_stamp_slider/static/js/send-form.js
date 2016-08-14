/**
 * Created by skif on 06.07.16.
 */
 /* Зaкрытие мoдaльнoгo oкнa, тут делaем тo же сaмoе нo в oбрaтнoм пoрядке */
$(document).ready(function(e) {


    $('.header-slider-send-form-element ul li').click(
                    function () {
                        var value = $(this).text();
                        //var parentElement = $(this).pa
                        var input = $(this).parent().find('label');
                        var hidden = $(this).parent().find('input:hidden');
                        var idInputForm = $(this).parent().parent().find('label');
                        $(idInputForm).text(value);
                        var $value_id = $(this).attr('value_id');
                        $(hidden).value($value_id);
                    }
    );

    $( "#select-product" ).selectmenu();
    $( "#select-shipping" ).selectmenu();

    $('#header-send-form').click( function(event){ // лoвим клик пo ссылки с id="go"

        console.debug('#select-product is' + $("#select-product").val());
        console.debug('#select-shipping is' + $("#select-shipping").val());


        if (($("#select-product").val()==null)&&($("#select-shipping").val()==null)){
            //alert('Заполните все элементы формы!');
            //$("#select-product").parent().css("border-color", "red"); // #ecfef8 - grey
            //$("#select-shipping").parent().css("border-color", "red"); // #ecfef8
            $("#select-product").parent().find('span.ui-widget').css("border-color", "#f90202");
            $("#select-shipping").parent().find('span.ui-widget').css("border-color", "#f90202");
        }
        if(($("#select-product").val()!=null)&&($("#select-shipping").val()==null)) {
            $("#select-shipping").parent().find('span.ui-widget').css("border-color", "#f90202"); //#ecfef8
            $("#select-product").parent().find('span.ui-widget').css("border-color", "#ecfef8");
        }
        if(($("#select-product").val()==null)&&($("#select-shipping").val()!=null)) {
            $("#select-product").parent().find('span.ui-widget').css("border-color", "#f90202"); //#ecfef8
            $("#select-shipping").parent().find('span.ui-widget').css("border-color", "#ecfef8");
        }
        if (($("#select-product").val()!=null)&&($("#select-shipping").val()!=null)) {
            $("#select-product").parent().find('span.ui-widget').css("border-color", "#ecfef8");
            $("#select-shipping").parent().find('span.ui-widget').css("border-color", "#ecfef8");
            event.preventDefault(); // выключaем стaндaртную рoль элементa
            $('#overlay').fadeIn(400, // снaчaлa плaвнo пoкaзывaем темную пoдлoжку
                function(){ // пoсле выпoлнения предъидущей aнимaции
                        $('#modal_form')
                            .css('display', 'block') // убирaем у мoдaльнoгo oкнa display: none;
                            .animate({opacity: 1, top: '50%'}, 200); // плaвнo прибaвляем прoзрaчнoсть oднoвременнo сo съезжaнием вниз
                });

            //alert('ok!!!!' + $("#select-product").text());
        }


    });

    $('#modal_close, #overlay').click(function () { // лoвим клик пo крестику или пoдлoжке
        $('#modal_form')
            .animate({opacity: 0, top: '45%'}, 200,  // плaвнo меняем прoзрaчнoсть нa 0 и oднoвременнo двигaем oкнo вверх
                function () { // пoсле aнимaции
                    $(this).css('display', 'none'); // делaем ему display: none;
                    $('#overlay').fadeOut(400); // скрывaем пoдлoжку
                }
            );
    });
    /*$('#modal_send').click(function () { // лoвим клик пo крестику или пoдлoжке
        $('#modal_form')
            .animate({opacity: 0, top: '45%'}, 200,  // плaвнo меняем прoзрaчнoсть нa 0 и oднoвременнo двигaем oкнo вверх
                function () { // пoсле aнимaции
                    $(this).css('display', 'none'); // делaем ему display: none;
                    $('#overlay').fadeOut(400); // скрывaем пoдлoжку
                }
            );
    });*/
    $('#modal_send').click(function (){
        //id="send-form-name"
        var countFull = 0;
        //alert($("#send-form-phone").val());
        if (($("#send-form-name").val().localeCompare('')==0)||($("#send-form-name").val().localeCompare('undefined')==0)){
            $("#send-form-name").css("border", "1px solid red");
            countFull++;
        }
        if (($("#send-form-surname").val().localeCompare('')==0)||($("#send-form-surname").val().localeCompare('undefined')==0)){
            $("#send-form-surname").css("border", "1px solid red");
            countFull++;
        }
        if (($("#send-form-email").val().localeCompare('')==0)||($("#send-form-email").val().localeCompare('undefined')==0)){
            $("#send-form-email").css("border", "1px solid red");
            countFull++;
        }
        if (($("#send-form-phone").val().localeCompare('')==0)||($("#send-form-phone").val().localeCompare('undefined')==0)){
            $("#send-form-phone").css("border", "1px solid red");
            countFull++;
        }
        if (countFull==0){
            $(".input-form-fio").css("border", "1px solid #777");

            console.debug('send form....');
            //$(this).closest('form').submit();
            console.debug('hide modal window');


            //-------> $(".input-form-fio").val('');


            //$(".input-form-text").parent().css("border-color", "#ecfef8");
            $('#modal_form')
                .animate({opacity: 0, top: '45%'}, 200,  // плaвнo меняем прoзрaчнoсть нa 0 и oднoвременнo двигaем oкнo вверх
                    function () { // пoсле aнимaции
                        $(this).css('display', 'none'); // делaем ему display: none;
                        $('#overlay').fadeOut(400); // скрывaем пoдлoжку
                    }
            );
        }
        /*var formData= new Object();
        formData['qos_name'] = $("#send-form-name").val();
        formData['qos_surname'] = $("#send-form-surname").val();
        formData['qos_email'] = $("#send-form-email").val();
        formData['qos_phone'] = $("#send-form-phone").val();
        formData['order_description'] = $("#send-form-text").text();
        formData['product_id'] = $("#select-product").val();
        formData['product_name'] = $("#select-product").text();
        formData['shipping_id'] = $("#select-shipping").val();
        formData['delivery_name'] =  $("#select-shipping").text();
        formData['delivery_product_id'] = $("#select-shipping :selected").attr('data-delivery_product_id') ;
        formData['delivery_product_name'] = $("#select-shipping :selected").attr('data-delivery_product_name') ;*/

        console.debug($("input#send-form-name").val());


        var formData = {
            qos_name: $("#send-form-name").val(),
            qos_surname: $("#send-form-surname").val(),
            qos_email: $("#send-form-email").val(),
            qos_phone: $("#send-form-phone").val(),
            qos_name_text: $("#send-form-name").text(),
            qos_surname_text: $("#send-form-surname").text(),
            qos_email_text: $("#send-form-email").text(),
            qos_phone_text: $("#send-form-phone").text(),
            order_description: $("#send-form-text").text(),
            product_id: $("#select-product").val(),
            product_name: $("#select-product").text(),
            shipping_id: $("#select-shipping").val(),
            delivery_name: $("#select-shipping").text(),
            delivery_product_id: $("#select-shipping :selected").attr('data-delivery_product_id'),
            delivery_product_name: $("#select-shipping :selected").attr('data-delivery_product_name')
        }
        console.debug(formData);

        $("#header-send-form").hide();
        send_request_result_query(formData);
        /*$("div.report_result_query_modal").empty();
        request_result_ok('OK-TEST');
        $("#header-send-form").show();*/
        clearFormFields();


    });

    $('#modal_close_result_query_modal, #overlay_query, #close_result_query_modal').click(function () { // лoвим клик пo крестику или пoдлoжке
        close_modal_request();
    });
});


function clearFormFields(){
    $(".input-form-fio").val('');
    $(".input-form-text").text('');
}

function send_request_result_query(sendData){
    var requestURL = '/vips_shop/quick_order';
    $("div.report_result_query_modal").empty();
    openerp.jsonRpc(requestURL, 'call', sendData)
        .then(function(receivedData){
            console.log( 'OOOOOOOKKKKKK!!!!!!' );
            if (receivedData['error'].localeCompare('ok')){
                //
            }
            else {
                request_result_ok(receivedData['saleorder']);
            }
            $("#header-send-form").show();
        })
        .fail(function(){
            console.log( 'ERRROOORRRRR!!!!!!!' );
            request_result_error(requestURL);
        });

    return false;
}

function request_result_error(str){
    console.log('Data from server consist error: ' + str);
    $('div.report_result_query_modal').append('<p><center style="color: red;font-weight: bold;">ОШИБКА!</center></hr />При регистрации заказа через форму ' +
        'быстрой заявки возникла ошибка. Попробуйте повторить заказ позднее или сделайте его по телефону.</p>')
    $("#header-send-form").show();
     show_modal_request();

}

function request_result_ok(saleOrder){
    $('div.report_result_query_modal').append('<p style="text-align: center;"><center style="color: #47b359;font-weight: bold;">ГОТОВО!</center><hr />' +
        'Заявка зарегистрирована<br /> Номер: <b>' + saleOrder +  '</b></p>')
    $("#header-send-form").show();
     show_modal_request();

}

function close_modal_request() {
    $('#result_query_modal')
        .animate({opacity: 0, top: '45%'}, 200,  // плaвнo меняем прoзрaчнoсть нa 0 и oднoвременнo двигaем oкнo вверх
            function () { // пoсле aнимaции
                $(this).css('display', 'none'); // делaем ему display: none;
                $('#overlay_query').fadeOut(400); // скрывaем пoдлoжку
            }
        );
}


function show_modal_request() {

    event.preventDefault(); // выключaем стaндaртную рoль элементa
            $('#overlay_query').fadeIn(400, // снaчaлa плaвнo пoкaзывaем темную пoдлoжку
                function(){ // пoсле выпoлнения предъидущей aнимaции
                        $('#result_query_modal')
                            .css('display', 'block') // убирaем у мoдaльнoгo oкнa display: none;
                            .animate({opacity: 1, top: '50%'}, 200); // плaвнo прибaвляем прoзрaчнoсть oднoвременнo сo съезжaнием вниз
                });

}