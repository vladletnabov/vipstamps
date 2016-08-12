# -*- coding: utf-8 -*-
from openerp import http
import werkzeug
from openerp import SUPERUSER_ID
from openerp.http import request
from openerp.tools.translate import _
from openerp.addons.website.models.website import slug
from openerp.addons.web.controllers.main import login_redirect
import datetime
from datetime import timedelta
from models import SessionVisitor, URLList
#Import logger
import logging
#Get the logger
_logger = logging.getLogger(__name__)
import datetime
from datetime import timedelta
import re
import urllib

class vips_vc(http.Controller):
    @http.route('/vips_vc/vips_vc/', auth='public', website=True)
    def index(self, **kw):
         return "Hello, world"

    def check_date_type(self,record_date):
        #_logger.error("check type data of record_date")
        #if type(record_date)!=type(datetime()):
        if (isinstance(record_date, datetime.datetime)==False):
            #_logger.error("convert STR to Datetime: %r", record_date)
            record_date = datetime.datetime.strptime(record_date,"%Y-%m-%d %H:%M:%S")

        #_logger.error("record_date result: %r ", record_date)
        return record_date

    def search_last_check_date(self, sessionID):
        #_logger.info("sessionID : %r", sessionID)
        #_logger.info("SEARCH_COUNT .....")
        table = request.env['vips_vc.session']
        record_date = datetime.datetime.now() - timedelta(days=100)
        if (sessionID>-1):
            #_logger.info("sessionID exist in DB ")
            records = table.sudo().browse([sessionID,])
            record_date = records[0].date_last_check
            #_logger.error("RESULT of QUERY: %r", record_date)
            record_date = self.check_date_type(record_date)


        #_logger.info("RECORD DATE LAST CHECK : %r", record_date)
        record_date = self.check_date_type(record_date)
        return record_date

    # ищем URL в базе и если нет - добавляем
    def search_record_url(self, url, searchEngine, advertEngine):

        #_logger.info("-----> search_record_urlfor URL: %r", url)
        table = request.env['vips_vc.url_list']
        #_logger.info("-----> table : %r", table)
        #_logger.info("-----> SEARCH_COUNT URLs .....")
        record_id = None
        if (table.sudo().search_count([('name', '=', url)])>0):
            #_logger.info("-----| URL exist in DB ")
            record_id = table.sudo().search([('name', '=', url)]).id
            #_logger.error("-----| record ID: %r", record_id)
        else:
            #_logger.info("-----| URL NOT exist in DB ")
            # Если словари поисковой машины и рекламы пусты - запписываем чистый URL,
            # если нет - то только первую его часть
            #_logger.info("-----| Checking Search and Advert engines... record_id now: %r", record_id)
            if ((searchEngine=={})and(advertEngine=={})):
                #_logger.info("-----|> Dictionary Serching and Adverting engines is empty")
                #_logger.info("-----|> Splitting URL...")
                urlRecord = self.splitURL(url)
                #_logger.info("-----|> Checking urlRecord[] size...")
                if(len(urlRecord)>1):
                    #_logger.info("-----!> urlRecord[] size>1")
                    #_logger.info("-----!> {name: %r, url_parametes: %r }", url, urlRecord[1])
                    record=table.sudo().create({'name': url, 'url_parametes': urlRecord[1]})
                    record_id = record.id
                    record.sudo().env.cr.commit()
                    #_logger.info("-----!> record URL ID: %r", record_id)
                    #_logger.error("-----!> record URL data: %r", record.name)

                else:
                    #_logger.info("-----!> urlRecord[] size==1")
                    #_logger.info("-----!> { name: %r }", url)
                    record=table.sudo().create({'name': url})
                    record_id = record.id
                    record.sudo().env.cr.commit()
                    #_logger.info("-----!> record URL ID: %r", record_id)
                    #_logger.error("-----!> record URL data: %r", record.name)
            if ((searchEngine!={})|(advertEngine!={})):
                url = self.splitURL(url)[0]
                record_id=table.sudo().create({'name': url}).id
            #_logger.error(record_id)
        #_logger.info("RECORD ID : %r", record_id)
        return record_id

    def checkValueSessionTimers(self, tableName, parameterName, parametrValue):
        #_logger.info("recieve table %r , parameterName: %r , parameterValue: %r ",
        #             tableName, parameterName, parametrValue)

        #_logger.info(pingTimout.search_count([('timeout','>',0)]))
        if (tableName.search_count([('name','=',parameterName)])>0):
            #_logger.info("record(s) present. get element[0] from table ")
            parametrValue = tableName.sudo().search([('name','=',parameterName)])[0].value

        #_logger.info("return %r : %r ", parameterName, parametrValue)

        return parametrValue




    @http.route(['/vips_vc/register_session'], type='json', auth='public', website=True)
    def register_session(self, prevouseURL, currentURL, sessionID, sessionPing, sessionCookieLive,
                         currentDateTime):
        #cr = request.cr
        sessionID = int(sessionID)
        sessionPing = int(sessionPing)
        sessionCookieLive = int(sessionCookieLive)

        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
        currentDate = datetime.datetime.now()
        remoteAddr = request.httprequest.environ['REMOTE_ADDR']
        #_logger.error("currentURL : %r", currentURL)

        registerSession = request.env['vips_vc.session']

        currentURLid = -1
        prevouseURLid = -1
        searchPhraseID = -1
        prevouseURLsearchEngine = {}

        currentURLadvert = self.checkURLonAdvert(currentURL)
        #_logger.error('-----> len(currentURLadvert): %r', len(currentURLadvert))
        if (len(currentURLadvert)>0):
            currentURL = self.splitURL(currentURL)[0]
        #_logger.error('----->if (self.checkURLonLocal(prevouseURL)!=True):')
        if (self.checkURLonLocal(prevouseURL)!=True):
            #_logger.error('-----|self.checkURLonLocal(prevouseURL)!=True')
            prevouseURLsearchEngine = self.checkURLonSearch(prevouseURL)
            if (prevouseURLsearchEngine!={}):
                #_logger.error('prevouseURLsearchEngine!={}:')
                #_logger.error(prevouseURLsearchEngine)
                searchPhrase = self.splitURLparam(self.splitURL(prevouseURL)[1])[prevouseURLsearchEngine['search_marker']]
                #_logger.error('searchPhrase : %r', searchPhrase)
                searchPhrase = urllib.unquote(str(searchPhrase)).decode('utf8')
                #_logger.error('searchPhrase : %r', searchPhrase)
                #prevouseURLsearchEngineKey = prevouseURLsearchEngine.keys()[0]
                #searchPhrase = searchPhrases[prevouseURLsearchEngineKey]['search_marker']
                #[prevouseURLsearchEngine.keys()[0]].search_marker
                searchPhraseID = self.checkSearchPhrase(searchPhrase, True)
                #_logger.error('searchPhraseID : %r', searchPhraseID)
            else:
                _logger.warning('prevouseURLsearchEngine=={}')
        else:
            _logger.warning('-----| prevouse URL not Local')
        #_logger.error("search_record_url(currentURL: %r,prevouseURLsearchEngine: %r, currentURLadvert:%r) ",
        #              currentURL, prevouseURLsearchEngine, currentURLadvert)

        currentURLid = self.search_record_url(currentURL,prevouseURLsearchEngine, currentURLadvert)

        #_logger.info("CHEKING that currentURLid != prevouseURL ",)
        if (currentURL!=prevouseURL):
            prevouseURLid = self.search_record_url(prevouseURL, prevouseURLsearchEngine, currentURLadvert)
        else:
            prevouseURLid = currentURLid

        #_logger.info("sessionID : %r", sessionID)


        sessionPing = self.checkValueSessionTimers(request.env['vips_vc.session_time_parameter_value'],
                                                 'sessionPing', sessionPing)
        sessionCookieLive = self.checkValueSessionTimers(request.env['vips_vc.session_time_parameter_value'],
                                                 'sessionCookieLive', sessionCookieLive)

        last_date_check = self.search_last_check_date(sessionID)
        last_date_check = last_date_check + timedelta(minutes=sessionCookieLive)

        if ((last_date_check>self.check_date_type(currentDateTime))and (sessionID>-1)):
            # если текущее время меньше веремени последней проверки + таймаут вернуть данные сессии
                writeDateTime =self.check_date_type(currentDateTime)  + timedelta(minutes=sessionCookieLive)
                writeRegisterSession = registerSession.sudo().browse([sessionID])[0]
                writeRegisterSession.sudo().write({'date_last_check': writeDateTime})
        else:
            #создать новую запись сессии и вернуть её клиенту
            #{'client_addr': remoteAddr, 'date_visit': currentDate,'date_last_check': currentDate }
            createParam = {'client_addr': remoteAddr, 'date_visit': currentDate,'date_last_check': currentDate }
            #_logger.info("Create session with params: %r", createParam)

            sessionID = self.createSessionRecord(registerSession,createParam)
            #_logger.info("sessionID: %r", sessionID)
            writeRelationSession = registerSession.sudo().browse([sessionID])[0]
            createParam = {}
            #_logger.info("createParam: cleaned")

            if (prevouseURLsearchEngine!={}):
                #_logger.error("prevouseURLsearchEngine: %r", prevouseURLsearchEngine)
                #_logger.error("search_engine_id: %r", prevouseURLsearchEngine['id'])
                createParam['search_engine_id'] = int(prevouseURLsearchEngine['id'])
                writeRelationSession.sudo().write(createParam)
                if (searchPhraseID!=-1):
                    createParam['search_phrase_id'] =  int(searchPhraseID)
                writeRelationSession.sudo().write(createParam)
            if (currentURLadvert!={}):
                createParam['advert_engine_id']= int(currentURLadvert['advertEngine'])
                createParam['advert_company_id']= int(currentURLadvert['advertCompany'])

            #_logger.info("createParam: %r", createParam)
            writeRelationSession.sudo().write(createParam)


        #_logger.info("sessionID : %r", sessionID)

        self.register_trip(currentURLid, prevouseURLid, sessionID)

        request.session['webcalc_session_id'] = sessionID
        #_logger.error('===== check session : %r', request.session['webcalc_session_id'] )
        return {'remoteAddr': remoteAddr, 'sessionID': sessionID, 'sessionPing': sessionPing,
                'sessionTimout': sessionCookieLive}

    def createSessionRecord(self, table, param):
        result = None
        #_logger.info(".....> table : %r, params : %r", table, param)
        result = table.sudo().create(param)
        name = "Session-ID-" + str(result.id)
        result.sudo().write({'name':name})
        #_logger.info(".....> Commit record ID %r", result.id)
        table.sudo().env.cr.commit()
        #_logger.info(".....> result operation(sessionID): %r", result.id)
        return result.id

    # проверка URL откуда пришёл посетитель на наличие меток поисковой системы
    def checkURLonSearch(self,url):
        #_logger.error("checkURLonSearch get URL: %r", url)
        result = {}
        if (re.search(r'\?', url)):
            arrURL = self.splitURL(url)
            searchHostname = self.getRemoteSiteName(arrURL[0])
            uniqKeyInHostaname = self.getUniqPartInHostnameEngine()

            for uniqKey in uniqKeyInHostaname:
                p= re.compile(uniqKey, re.IGNORECASE)
                if(re.search(p, searchHostname)):
                    result = uniqKeyInHostaname[uniqKey]
                    #_logger.error("Find key: %r , breaking cicle ", uniqKey)
                    break
        #_logger.error("checkURLonSearch result: %r", result)
        return result
    # проверка на наличие меток рекламной машины и компании в целевом URL
    def checkURLonAdvert(self, url):
        #_logger.error("checkURLonAdvert get URL: %r", url)
        result = {}
        tableEngine = request.env['vips_vc.advert_engine']
        tableCompany = request.env['vips_vc.advert_company']
        tableUniqLink = request.env['vips_vc.uniq_link_id_advert']

        if (re.search(r'\?', url)):
            arrURL = self.splitURL(url)
            #hostname = request.get_host() #request['HTTP_HOST']
            urlParams = self.splitURLparam(arrURL[1])
            #_logger.error("urlParams : %r", urlParams)
            #_logger.error(urlParams)
            if ('utm_source' in urlParams):
                #_logger.error("tableEngine.search([('utm_source', '=', %r)]) : %r", urlParams['utm_source'],tableEngine)
                advertEngine = tableEngine.sudo().search([('utm_source', '=', urlParams['utm_source'])])
                if(len(advertEngine)>0):
                    result['advertEngine'] = int(advertEngine[0].id)
                    #_logger.error("tableEngine.search result: %r", result['advertEngine'])

                #_logger.error("tableCompany.search([['name', '=', %r] ,['advert_engine_ids', '=', %r]])",
                #              urlParams['utm_company'], result['advertEngine'])
                advertCompany= tableCompany.sudo().search([['name', '=', urlParams['utm_company']],
                                                    ['advert_engine_ids', '=', result['advertEngine'] ]])
                if(len(advertCompany)>0):
                    result['advertCompany'] = advertCompany[0].id
                #result['advertEngine'] = advertEngine
                #result['advertCompany'] = advertCompany
            else:
                for record in tableEngine.sudo().search([('utm_uniqid', '!=', '')]):
                    if (record.utm_uniqid in urlParams):
                        advertCompany = tableUniqLink.sudo().search([('name', '=', urlParams[record.utm_uniqid])])[0].company_ids
                        advertEngine = tableCompany.sudo().browse([advertCompany,])[0].advert_engine_ids
                        result['advertEngine'] = advertEngine
                        result['advertCompany'] = advertCompany

        #_logger.error("checkURLonAdvert result: %r", result)
        return result

    # проверяем, что предыдущий URL был локальным или нет
    def checkURLonLocal(self, url):
        #_logger.error("checkURLonLocal get URL: %r", url)
        result = False
        hostname = request.httprequest.environ['HTTP_HOST'] #request['HTTP_HOST'] httprequest.environ
        hostname.lower()
        if ((url!='')and(re.search(r'\/\/', url))):
            splitedURL = re.split(r'\/\/',url)[1]
            urlHostname = re.split(r'\/', splitedURL)[0]
            urlHostname.lower()

            if (hostname == urlHostname):
                result = True
                
        #_logger.error("checkURLonLocal result: %r", result)
        return result

    def checkSearchPhrase(self,phrase, create):
        #_logger.error("checkSearchPhrase get phrase: %r , create new record if phrase is absent^ %r", phrase, create)
        result = None

        table =  request.env['vips_vc.search_phrases']
        resultSearch = table.sudo().search([('name', '=', phrase)])
        if (len(resultSearch)>0):
            #_logger.error("Record of phrase: %r is present", phrase)
            result = resultSearch[0].id

        if ((result==None)|(result<0)):
            #_logger.error("Record of phrase: %r is absent", phrase)
            if (create==True):
                #_logger.error("Set parameter for creating new record: %r", create)
                result = table.sudo().create({'name': phrase}).id

        #_logger.error("checkSearchPhrase result: %r", result)
        return result
    # получение имени сайта http://sitename.ru
    def getRemoteSiteName(self, url):
        #_logger.error("getRemoteSiteName get URL: %r", url)
        result = None
        url.lower()
        arrHost = re.split(r'\/', url)
        result = arrHost[0] + '//' + arrHost[2]

        #_logger.error("getRemoteSiteName result: %r", result)
        return result

    def splitURLparam(self, paramStr):
        result = {}

        for record in re.split(r'\&',paramStr):
            strResult = re.split(r'\=', record)
            result[strResult[0]]=strResult[1]

        return result

    def splitURL(self, url):
        #_logger.error("-----? splitURL get URL: %r", url)
        result = []
        result = re.split(r'\?',url)
        #_logger.error("-----? splitURL result: [%r,] and all array: %r", result[0], result)
        return result

    def getUniqPartInHostnameEngine(self):
        #_logger.error("getUniqPartInHostnameEngine")
        result = {}
        table = request.env['vips_vc.search_engine']
        for record in table.sudo().search([]):
            recordMap = {'id': record.id, 'uniq_part_in_host': record.uniq_part_in_host,
                         'search_marker': record.search_marker}
            result[record.uniq_part_in_host] = recordMap
        #_logger.error("getUniqPartInHostnameEngine result: %r", result)
        return result

    def register_trip(self, currentURLid, prevouseURLid, sessionID):
        currentURLid = int(currentURLid)
        prevouseURLid = int(prevouseURLid)
        result = None
        #_logger.info("Registering trip")
        #_logger.info("Recived data: currentURLid  - %r, prevouseURLid - %r, sessionID %r",
        #             currentURLid, prevouseURLid, sessionID)

        table = request.env['vips_vc.site_trip']
        #_logger.info("table: %r", table)

        recordIDs = table.sudo().search([('session_ids','=',sessionID)])

        # проверяем, что есть записи в таблице с таким ID
        #_logger.info("len(recordIDs)>0")
        if (len(recordIDs)>0):
            sorted(recordIDs)
            records = table.sudo().browse([recordIDs[~0].id,])
            #проверяем, что последний элемент currentURLid не равен текущей странице
            prevCurrentURLid = records[~0].url_current_ids
            #_logger.info('----> proveryaem chto posledniy element ne raven tekuschey stranitse: %r i %r',
            #             prevCurrentURLid, currentURLid)

            if(prevCurrentURLid!=currentURLid):
                #проверяем, чтобы предыдущая и текущая не совпадали
                #_logger.info("(currentURLid!=prevouseURLid)")
                #_logger.info("CREATE -----> session_ids: %r url_prevouse_ids: %r url_current_ids: %r",
                #          sessionID, prevouseURLid, currentURLid)
                if (currentURLid!=prevouseURLid):
                    result = self.register_trip_write(table, sessionID, prevouseURLid, currentURLid)
                #param = "trip-id-" + str(result.id)
                #result.write({'name':param})
            #else:
                #_logger.info('----> prevCurrentURLid==currentURLid ne pishem!')
        else:
            # пишем в таблицу, так как для сессии записей ещё нет
            result = self.register_trip_write(table, sessionID, prevouseURLid, currentURLid)

            #param = "trip-id-" + str(result.id)
            #result.write({'name':param})

        if (result== None):
            #_logger.info("Registering trip result: None")
            return None
        else:
            #_logger.info("Registering trip result: %r", result.id)
            return result.id

    def register_trip_write(self, table, sessionID, prevouseURLid, currentURLid):

        record = table.sudo().create(
            {'session_ids': sessionID, 'url_prevouse_ids': prevouseURLid,'url_current_ids': currentURLid}
        )
        name = 'Trip-id-' + str(record.id)
        record.sudo().write({'name': name})
        #_logger.info("!!!!! -----> Commit table trip record ID: %r",record.id )
        record.sudo().env.cr.commit()
        return record

    #def register_trip_write_param(self):

#     @http.route('/vips_vc/vips_vc/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('vips_vc.listing', {
#             'root': '/vips_vc/vips_vc',
#             'objects': http.request.env['vips_vc.vips_vc'].search([]),
#         })

#     @http.route('/vips_vc/vips_vc/objects/<model("vips_vc.vips_vc"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vips_vc.object', {
#             'object': obj
#         })