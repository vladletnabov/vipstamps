/**
 * Created by skif on 03.07.16.
 */
var officeAddr = {};
officeAddr['Москва, м.Беговая']='Хорошёвское шоссе 13а, корп.2';
officeAddr['Москва, м. Деловой центр']='Хорошёвское шоссе 13а, корп.2';
officeAddr['Москва, м. Полежаевская']='Хорошёвское шоссе 13а, корп.2';
officeAddr['МО, Красногорск']='Хорошёвское шоссе 13а, корп.2';
officeAddr['Выберите удобный филиал']='...';

function setAddressOffice() {
    var office = $('#office-address-selecter').val();
    $('#office-address').text(officeAddr[office]);


}
$(document).ready(function(e) {



    $('.dropdown-poi-office ul li').click(
            function () {
                //alert(2);
                var value = $(this).text();
                //var parentElement = $(this).pa
                //var input = $(this).parent().find('input');
                //var idInputForm = $(this).parent().parent().find('input');
                $('#office-address').text(officeAddr[value]);
                $('#dropdown-poi-office').text(value);
            }
    );
});

