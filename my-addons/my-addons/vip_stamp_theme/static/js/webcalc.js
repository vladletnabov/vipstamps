/**
 * Created by skif on 08.07.16.
 */
var prevouseURL = document.referrer;
var currentURL = window.location.href;
var sessionID = -1;
var sessionIDname = 'webCalc_sessionID';
var sessionPingName = 'webCalc_sessionPingTimeout'; // имя куки для проверки активности страницы пользователя
var sessionPingTimeout = 10; // значение по умолчанию проверки активности стараницы у пользователя в секундах
var sessionCookieLiveName = 'webCalc_sessionCookieLive';
var sessionCookieLive = 10;

console.debug('checkCookieParam(sessionID, sessionIDname);');
sessionID = checkCookieParam(sessionID, sessionIDname);
console.debug('checkCookieParam(sessionPingTimeout, sessionPingName)');
sessionPingTimeout = checkCookieParam(sessionPingTimeout, sessionPingName);
console.debug('checkCookieParam(sessionCookieLive, sessionCookieLiveName)');
sessionCookieLive = checkCookieParam(sessionCookieLive, sessionCookieLiveName);
//console.debug('');

var currentDateTime = new Date();
//expiry.setTime(expiry.getTime()+(sessionCookieLive*60*1000));

console.debug('trying to register session: ' + prevouseURL + ', ' + currentURL + ', ' + sessionID + ', ' +
        sessionPingTimeout + ', ' + sessionCookieLive);
registerSession(prevouseURL, currentURL, sessionID, sessionPingTimeout, sessionCookieLive, currentDateTime,
    sessionPingName);

function checkCookieParam(checkParam, cookieParam) {
    console.debug('receivingparams: : checkParam = ' + checkParam + ', cookieParam = ' + cookieParam);
    var result  = getCookie(cookieParam);
    console.debug('CHECKING RECEIVED PARAM: ' + result);
    if ((result==null) || (result=='undefined')){
        result=checkParam;
    }
    console.debug('result: ' + result);
    return result;
}


"use strict";

function registerSession(prevouseURL, currentURL, sessionID, sessionPingTimeout, sessionCookieLive,
         currentDateTime, sessionPingName){
    // регистрация сессии на сервере
    var result = false;
    var requestUrl = '/vips_vc/register_session';
    openerp.jsonRpc(requestUrl, 'call', {'prevouseURL': prevouseURL, 'currentURL': currentURL,
        'sessionID': sessionID, 'sessionPing': sessionPingTimeout, 'sessionCookieLive': sessionCookieLive,
        'currentDateTime' : currentDateTime})
            .then(function (data) {
                console.debug('registerSession result: ' + data);
                console.debug(data);

                console.debug('setCoockie: '  + sessionIDname + ', ' + data['sessionID'] + ', ' +
                        currentDateTime + ', ' + data['sessionTimout']);
                setCookie(sessionIDname, data['sessionID'], currentDateTime,
        data['sessionTimout']);

                console.debug('setCoockie: '  + sessionPingName + ', ' +  data['sessionPing'] +
        ', ' +  currentDateTime + ', ' + data['sessionTimout']);
                setCookie(sessionPingName, data['sessionPing'], currentDateTime,
        data['sessionTimout']);
                sessionCookieLive = data['sessionTimout'];
//result = data;
            });
    console.debug(result);
    return result;
}

function setCookie(name, value, currentTime, timeout) {
    //name - имя параметра;
    //value - значение параметра сохраняемого в куках
    //time - время жизни в минутах
    console.debug('-----> setCookie(' + name+', ' + value + ', ' + currentTime + ', ' + timeout + ')');
    console.debug('currentTime: ' + currentTime);
    var expiry = new Date(currentTime);
    console.debug('expiry: ' + expiry);
    expiry.setTime(expiry.getTime()+(timeout*60*1000)); // Ten minutes
    console.debug('-----> expiry with delta: ' + expiry);
    // Date()'s toGMTSting() method will format the date correctly for a cookie
    var param = name+ "=" + value;
    console.debug ('writing cookie...');
    document.cookie = param + "; expires=" + expiry.toGMTString();
    console.debug ('-----> checking cookie ' + name + ' ... ' + getCookie(name));

}

var delCookie = function(name) {
    document.cookie = name + '=;expires=Thu, 01 Jan 1970 00:00:01 GMT;';
    alert('deleted!');
};

function getCookie(name) {
    var cookie = " " + document.cookie;
    var search = " " + name + "=";
    var setStr = null;
    var offset = 0;
    var end = 0;
    if (cookie.length > 0) {
        offset = cookie.indexOf(search);
        if (offset != -1) {
            offset += search.length;
            end = cookie.indexOf(";", offset)
            if (end == -1) {
                end = cookie.length;
            }
            setStr = unescape(cookie.substring(offset, end));
        }
    }
    return(setStr);
}