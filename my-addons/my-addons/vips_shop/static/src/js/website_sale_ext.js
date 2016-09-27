/**
 * Created by skif on 20.07.16.
 */

var hwSlideSpeed = 700;
var hwTimeOut = 5000;
var hwNeedLinks = true;
$(document).ready(function() {

    $('.slide').css(
            {"position" : "absolute",
                "top":'0', "left": '0'}).hide().eq(0).show();



    var slideNum = 0;
    var slideTime;
    slideCount = $("#page-slider .slide").size();
    var animSlide = function(arrow){
        clearTimeout(slideTime);
        $('.slide').eq(slideNum).fadeOut(hwSlideSpeed);
        if(arrow == "next"){
            if(slideNum == (slideCount-1)){slideNum=0;}
            else{slideNum++}
        }
        else if(arrow == "prew")
        {
            if(slideNum == 0){slideNum=slideCount-1;}
            else{slideNum-=1}
        }
        else{
            slideNum = arrow;
        }
        $('.slide').eq(slideNum).fadeIn(hwSlideSpeed, rotator);
        $(".control-slide.active").removeClass("active");
        $('.control-slide').eq(slideNum).addClass('active');
    }
    if(hwNeedLinks){
        var $linkArrow = $('<a id="prewbutton" href="#"></a><a id="nextbutton" href="#"></a>')
                .prependTo('#slider');
        $('#nextbutton').click(function(){
            animSlide("next");

        })
        $('#prewbutton').click(function(){
            animSlide("prew");
        })
    }
    var $adderSpan = '';
    $('.slide').each(function(index) {
        $adderSpan += '<span class = "control-slide">' + index + '</span>';
    });
    //$('<div class ="sli-links">' + $adderSpan +'</div>').appendTo('#page-slider-wrap');
    $(".control-slide:first").addClass("active");

    $('.control-slide').click(function(){
        var goToNum = parseFloat($(this).text());
        animSlide(goToNum);
    });
    var pause = false;
    var rotator = function(){
        if(!pause){slideTime = setTimeout(function(){animSlide('next')}, hwTimeOut);}
    }
    $('#page-slider-wrap').hover(
            function(){clearTimeout(slideTime); pause = true;},
            function(){pause = false; rotator();
            });
    rotator();





    $('.oe_website_sale').each(function(){

        var oe_website_sale =this;

        $('.oe_website_sale .a-submit, #comment .a-submit').off('click').on('click', function () {
            $(this).closest('form').submit();
            //$(this).closest('form').submit();
            console.debug('.oe_website_sale .a-submit, #comment .a-submit - CLICKED! ' +
                "oe_website_sale: " + oe_website_sale.nodeName);
            //alert('.oe_website_sale .a-submit, #comment .a-submit - CLICKED!\n' +
            //    "oe_website_sale: " + oe_website_sale.nodeName);
        });

        var $shippingDifferent = $("select[name='shipping_id']", oe_website_sale);
        $shippingDifferent.change(function (event) {
            var value = +$shippingDifferent.val();
            var data = $shippingDifferent.find("option:selected").data();
            var $snipping = $(".js_shipping", oe_website_sale);
            var $snipping_metro = $(".js_metro_station_shipping", oe_website_sale);
            var $inputs = $snipping.find("input");
            var $selects = $snipping.find("select");
            var $select_metro = $snipping_metro.find("select");
            //alert(oe_website_sale.nodeName);
            //alert(Object.keys(data));
            $snipping.hide();
            $snipping_metro.hide();

            //$snipping.toggle(!!value);

            $inputs.attr("readonly", value <= 0 ? null : "readonly" ).prop("readonly", value <= 0 ? null : "readonly" );
            $selects.attr("disabled", value <= 0 ? null : "disabled" ).prop("disabled", value <= 0 ? null : "disabled" );


            switch(value) {
                case -1:
                    $snipping.show();
                    $snipping_metro.hide();
                    $select_metro.attr("disabled", "disabled").prop("disabled",  "disabled" );
                    break;

                case -2:
                    $snipping.hide();
                    $snipping_metro.show();
                    $select_metro.attr("disabled", "").prop("disabled",  "" );
                    break;

                case 0:
                    $snipping.hide();
                    $snipping_metro.hide();
                    $select_metro.attr("disabled", "disabled").prop("disabled",  "disabled" );
                    break;

                default:
                    $snipping.show();
                    $snipping_metro.hide();
                    $select_metro.attr("disabled", "disabled").prop("disabled",  "disabled" );
            }

            $inputs.each(function () {
                $(this).val( data[$(this).attr("name")] || "" );
            });
            var metro = $snipping.find("select[name='shipping_metro_id']");

            $(metro).find('option').each(function(){
                console.debug(this.value + ' ' + data['shipping_metro_id']);
                if(this.value==data['shipping_metro_name']){
                    this.selected = true;
                }
                   else {
                    this.selected = false;
                }
            });
            console.debug('delivery_price: '+ data['shipping_price']);
            $('#delivery_price').text(parseFloat(data['shipping_price']).toFixed(2));
            $('#price_shipping_wo_order').text(parseFloat(data['shipping_price']).toFixed(2));
            setFullPriceCheckout(genFullPriceCheckout());
            setHiddenShippingProductId();
        });


        //Старая функция обновления стоимости товара при добавлении/уменьшении количества товара
        $(oe_website_sale).find(".oe_cart input.js_quantity").on("change", function () {
            var $input = $(this);
            if ($input.data('update_change')) {
                return;
            }
            var value = parseInt($input.val(), 10);
            var $dom = $(this).closest('tr');
            var default_price = parseFloat($dom.find('.text-danger > span.oe_currency_value').text());
            var $dom_optional = $dom.nextUntil(':not(.optional_product.info)');
            var line_id = parseInt($input.data('line-id'),10);
            var product_id = parseInt($input.data('product-id'),10);
            var product_ids = [product_id];
            $dom_optional.each(function(){
                product_ids.push($(this).find('span[data-product-id]').data('product-id'));
            });
            if (isNaN(value)) value = 0;
            $input.data('update_change', true);
            openerp.jsonRpc("/shop/get_unit_price", 'call', {
                'product_ids': product_ids,
                'add_qty': value,
                'use_order_pricelist': true,
                'line_id': line_id})
            .then(function (res) {
                //basic case
                $dom.find('span.oe_currency_value').last().text(res[product_id].toFixed(2));
                $dom.find('.text-danger').toggle(res[product_id]<default_price && (default_price-res[product_id] > default_price/100));
                //optional case
                $dom_optional.each(function(){
                    var id = $(this).find('span[data-product-id]').data('product-id');
                    var price = parseFloat($(this).find(".text-danger > span.oe_currency_value").text());
                    $(this).find("span.oe_currency_value").last().text(res[id].toFixed(2));
                    $(this).find('.text-danger').toggle(res[id]<price && (price-res[id]>price/100));
                });
                openerp.jsonRpc("/shop/cart/update_json", 'call', {
                'line_id': line_id,
                'product_id': parseInt($input.data('product-id'),10),
                'set_qty': value})
                .then(function (data) {
                    $input.data('update_change', false);
                    if (value !== parseInt($input.val(), 10)) {
                        $input.trigger('change');
                        return;
                    }
                    if (!data.quantity) {
                        location.reload(true);
                        return;
                    }
                    var $q = $(".my_cart_quantity");
                    $q.parent().parent().removeClass("hidden", !data.quantity);
                    $q.html(data.cart_quantity).hide().fadeIn(600);

                    $input.val(data.quantity);
                    $('.js_quantity[data-line-id='+line_id+']').val(data.quantity).html(data.quantity);
                    $("#cart_total").replaceWith(data['website_sale.total']);
                });
            });
        });

    });

    setShippingPrice();
    setFullPriceCheckout(genFullPriceCheckout());
    setHiddenShippingProductId();


});

/*function setSessionIDtoSaleOrder(saleorderID){
    #
}*/

    function genFullPriceCheckout(){
        console.debug('genFullPriceCheckout...');
        var order_price = parseFloat($('#order_price_wo_shipping').text());
        console.debug('order_price: ' + order_price);
        var shipping_price = parseFloat($('#price_shipping_wo_order').text());
        console.debug('shipping_price: ' + shipping_price);
        var full_price = order_price + shipping_price;

        result = parseFloat(full_price).toFixed(2);
        console.debug('genFullPriceCheckout result: ' + full_price);
        return result;
    }

    function setFullPriceCheckout(price){
        console.debug('setFullPriceCheckout...');
        var full_price = $('#price_order_with_shipping');
        full_price.text(price);
        console.debug('setted value #price_order_with_shipping...');
    }

    function setShippingPrice(){
        var delivery_price = parseFloat($('#delivery_price').text()).toFixed(2);
        $('#price_shipping_wo_order').text(delivery_price);
    }


    function setHiddenShippingProductId() {
        if ($("select").is("#select_shipping_id")){
            var select_shipping_id  = $('#select_shipping_id option:selected').data()['shipping_product_id'];
            var hidden_shipping_product_id = $('#hidden_shipping_product_id');
            console.debug("--!!> " + select_shipping_id);
            hidden_shipping_product_id.val(select_shipping_id);

        }

    }
