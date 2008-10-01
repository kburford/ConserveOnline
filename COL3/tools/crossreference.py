# COL3
# Copyright(C), 2008, Enfold Systems, Inc. - ALL RIGHTS RESERVED
# 
# This software is licensed under the Terms and Conditions
# contained within the "license.txt" file that accompanied 
# this software.  Any inquiries concerning the scope or 
# enforceability of the license should be addressed to:
#
#
# Enfold Systems, Inc.
# 4617 Montrose Blvd., Suite C215
# Houston, Texas 77006 USA
# p. +1 713.942.2377 | f. +1 832.201.8856
# www.enfoldsystems.com
# info@enfoldsystems.com

import logging
import imaplib
import time, random
import httplib, mimetypes
from cStringIO import StringIO
from lxml import etree
from elementtree.ElementTree import Element, SubElement, tostring, fromstring

from StringIO import StringIO
from zope import interface
from zExceptions import BadRequest
from Acquisition import aq_inner, aq_parent
from Globals import InitializeClass, DTMLFile
from OFS.SimpleItem import SimpleItem
from OFS.PropertyManager import PropertyManager
from Products.BTreeFolder2.BTreeFolder2 import BTreeFolder2
from AccessControl.SecurityInfo import ClassSecurityInfo
from Products.CMFCore.utils import UniqueObject, getToolByName
from Products.CMFCore import permissions

from Products.COL3.browser.mail import simple_mail_tool
from Products.COL3.content.base import generateOID
from Products.COL3 import config
from Products.COL3 import crossref_config
from Products.COL3.interfaces.tools import ICrossReference

def encode(text, fix_leading=False):
    if fix_leading:
        if text[0].isdigit() or text[0]=='?':
            text = '_' + text[1:]
    return unicode(text, 'utf-8', errors='replace')

class CrossRefTool(UniqueObject, BTreeFolder2, SimpleItem):
    """ This tool will contain all the methods to interact with the
        CrossRef system
    """
    id = 'crossreference_tool'
    meta_type = 'ConserveOnline CrossRef Tool'
    
    manage_crossref = DTMLFile('www/crossref', globals())
    
    logger = logging.getLogger('*** CrossrefTool ***')
    
    host = crossref_config.crossref_host 
    tnc_crossref_prefix = crossref_config.tnc_crossref_prefix
    crossref_login = crossref_config.crossref_login
    crossref_pwd = crossref_config.crossref_pwd
    selector = '/servlet/deposit?operation=doMDUpload&login_id=%s&login_passwd=%s&area=%s'
    tnc_contact_email = crossref_config.crossref_tnc_contact_email
    crossref_admin_email = crossref_config.crossref_admin_email
    imapserver = 'email.tnc.org'
    maillogin = crossref_config.imap_login
    mailpassword = crossref_config.imap_pwd

    manage_options = (
                      {'label': 'CrossRef Update',
                       'action': 'manage_crossref'
                       },
                      ) +PropertyManager.manage_options + SimpleItem.manage_options
    
    _properties =(
                  {'id':'host', 'type':'string', 'mode':'w'},
                  {'id':'tnc_crossref_prefix', 'type':'string', 'mode':'w'},
                  {'id':'crossref_login', 'type':'string', 'mode':'w'},
                  {'id':'crossref_pwd', 'type':'string', 'mode':'w'},
                  {'id':'tnc_contact_email', 'type':'string', 'mode':'w'},
                  {'id':'crossref_admin_email', 'type':'string', 'mode':'w'},
                  {'id':'imapserver', 'type':'string', 'mode':'w'},
                  {'id':'maillogin', 'type':'string', 'mode':'w'},
                  {'id':'mailpassword', 'type':'string', 'mode':'w'},
                  )

    interface.implements(ICrossReference)

    security = ClassSecurityInfo()
    
    
    security.declareProtected(permissions.ManagePortal, 'processEmailReports') 
    def processLibraryFiles(self, from_queue=True, area='live'):
        """ 
            This will will add the library file metadata to the crossref site:
            a) If from_queue is False:
               library files which don't currently have a DOI will be assigned one and 
               submitted to CrossRef to be created, in theory, it could be called any numbers of
               times as even if doi's are resubmitted to CrossRef, if the doi has 
               already been deposited then any subsequent submissions will just update the 
               metadata (if it has been changed), or leave the submission alone if the metadata 
               hasn't changed
            b) If from_queue is True:
               All library files which have been added and placed in the library file queue
               will be processed and submitted to CrossRef and the queue will be cleared out.
        """
        pcat = getToolByName(self, 'portal_catalog')
        root = Element('doi_batch')
        root.attrib['version'] = '4.3.0'
        root.attrib['xmlns'] = 'http://www.crossref.org/schema/4.3.0'
        root.attrib['xmlns:xsi'] = 'http://www.w3.org/2001/XMLSchema-instance'
        root.attrib['xmlns:schemaLocation'] ='http://www.crossref.org/schema/4.3.0 http://www.crossref.org/schema/deposit/crossref4.3.0.xsd'
        
        #####      The head section    #####
        head = SubElement(root, 'head')
        SubElement(head, 'doi_batch_id').text = self.tnc_crossref_prefix
        SubElement(head, 'timestamp').text = str(int(time.time()))
        depositor = SubElement(head, 'depositor')
        SubElement(depositor, 'name').text = 'The Nature Conservancy'
        SubElement(depositor, 'email_address').text = self.tnc_contact_email
        SubElement(head, 'registrant').text = 'The Nature Conservancy'

        ####    The body which contains all the file metadata     #####
        body = SubElement(root, 'body')
        if from_queue is True:
            keylist = [r for r in self.keys()]
            for key in keylist:
                library_file_node = self.generateReportPaperNode(self[key], body)
                body.append(library_file_node)
                if area =='live':
                    del self[key]
        else:
            libfiles = pcat.searchResults(portal_type='LibraryFile')
            for file in libfiles:
                localfile = file.getObject()
                if localfile.getOid():
                    if localfile.getCreatedoi() != 'No':
                        library_file_node = self.generateReportPaperNode(localfile, body)
                        body.append(library_file_node)
        config.crossref_schema.seek(0)
        xmlschema_doc = etree.parse(config.crossref_schema)
        xmlschema = etree.XMLSchema(xmlschema_doc)
        xmlfile = etree.parse(StringIO(tostring(root)))
        if xmlschema.validate(xmlfile):
            return self.crossref_post_multipart(root, area)
        else:
            errorstr = ''
            for error in xmlschema.error_log:
                errorstr += '<p>'+str(error.line)+' - '+str(error.message)+'</p>'
            return """<html>
                        <head><head>
                        <body>
                           <b>Schema validatiion failed!!!</b>
                           %s
                        </body>
                      </html>
                   """ % errorstr
    
    def generateReportPaperNode(self, file, body):
        """ takes a library file brains object and creates an xml representation """
        reportpaper = Element('report-paper')
        papermetadata = SubElement(reportpaper, 'report-paper_metadata')
        authors = file.getAuthors()
        contributors = SubElement(papermetadata, 'contributors')
        if authors:
            i = 0
            authors = list(authors)
            for author in authors:
                i += 1
                given_name = ''
                surname = ''
                currentauthor = SubElement(contributors, 'person_name')
                currentauthor.attrib['sequence'] = i == 1 and 'first' or 'additional' 
                currentauthor.attrib['contributor_role'] = 'author'
                names = author.split(',')
                # authors list format is [(surname1, givenname),(surname2, givenname)...]
                if len(names) >= 1:
                    surname = names[0].strip()
                if len(names) >= 2:
                    given_name = names[1].strip()
                # surname is required, given_name is optional; neither can start with digit or ?, apparently
                if given_name and not surname:
                    surname = given_name
                    given_name = ''
                if given_name and given_name != 'undefined':
                    SubElement(currentauthor, 'given_name').text = encode(given_name, fix_leading=True)
                SubElement(currentauthor, 'surname').text = encode(surname, fix_leading=True)
                
        #####  The document title #####
        titles = SubElement(papermetadata, 'titles')
        SubElement(titles, 'title').text = encode(file.Title())
        
        #####   The document publication date#####
        pubdata = SubElement(papermetadata, 'publication_date')
        pubdata.attrib['media_type'] = 'print'
        pubdate = file.getDateauthored() and file.getDateauthored() or file.creation_date
        SubElement(pubdata, 'month').text = str(pubdate.month())
        SubElement(pubdata, 'day').text = str(pubdate.day())
        SubElement(pubdata, 'year').text = str(pubdate.year())
        doidata = SubElement(papermetadata, 'doi_data')
        SubElement(doidata, 'doi').text = file.getOid() and file.getOid() or generateOID()
        SubElement(doidata, 'resource').text = file.absolute_url()
        return reportpaper

    security.declareProtected(permissions.ManagePortal, 'listQueuedFiles') 
    def listQueuedFiles(self):
        """ Just dumps a list of file ids queued """
        i = 0
        buff = StringIO()
        buff.seek(0)
        for key in self.keys():
            i += 1
            libfile = self[key]
            buff.write('File #'+str(i)+' '+libfile.Title()+'['+libfile.id+']\n')
        buff.write('===========================\n')
        buff.write('   '+str(i)+' Total Files Found\n')
        buff.write('===========================\n')
        buff.seek(0)
        returnval =  buff.read()
        buff.close()
        return returnval
        

    security.declareProtected(permissions.ManagePortal, 'processEmailReports') 
    def processEmailReports(self):
        """ Method to pull all the email messages recieved from CrossRef and process
            the failure messages if there are any.  There are two alternatives, either an
            email will sent to crossref support or to a tnc admin based on the error message
            received
        """
        context = aq_inner(aq_parent(self))
        errors = ('Connection refused',
                  'Operation timed out'
                  'Logon failure')
        server = imaplib.IMAP4(self.imapserver)
        server.login(self.maillogin, self.mailpassword)
        server.select()
        (status, msg_numbers) = server.search(None, 'SUBJECT', 'CrossRef')
        if status == 'OK':
            mailtool = simple_mail_tool()
            for msg_num in msg_numbers[0].split():
                try:
                    msg = server.fetch(str(msg_num), '(BODY[TEXT])')
                    if msg:
                        msg = msg[1][0][1].replace('3D', '') #when getting text from my exchange account 3D is in there...
                        self.logger.debug('Processing message number '+str(msg_num)+' Message-['+msg+']')
                        msg = fromstring(msg[msg.index('<doi_batch'):]) 
                        submission_id = msg.find('submission_id')
                        batch_id = msg.find('batch_id')
                        record_diagnostics = msg.findall('record_diagnostic')
                        for record in record_diagnostics:
                            if record.attrib['status'] == 'Failure':
                                doi = record.find('doi')
                                status_msg = record.find('msg')
                                submission_id = submission_id is not None and submission_id.text or 'No submission id found'
                                doi = doi is not None and doi.text or 'No DOI Found!'
                                batch_id = batch_id is not None and batch_id.text or 'No Batch Id Found!'
                                status_msg = status_msg is not None and status_msg.text or 'No Message Found!'
                                if self._shouldContactCrossrefAdmin(status_msg):
                                    mailtool.sendEmailToCrossRefAdmin(context,
                                                                      status_msg,
                                                                      self.crossref_admin_email, 
                                                                      submission_id, 
                                                                      batch_id, 
                                                                      doi)
                                else:
                                    mailtool.sendCrossrefEmailToTNC(context,
                                                                    status_msg,  
                                                                    submission_id, 
                                                                    batch_id, 
                                                                    doi,
                                                                    to_email=self.tnc_contact_email)
                except Exception, e:
                    if e.__str__() in errors:
                        self.logger.error("There was an http connection error in the crossref tool... "+e.__str__())
                    else:
                        self.logger.error("There was an error thrown in the crossref tool... ["+e.__class__.__name__+' - '+e.__str__()+']')
            
    
    def _shouldContactCrossrefAdmin(self, errorstr):
        """ tiny helper method """
        for errmsg in config.CROSS_REF_ERRORS_TNC:
            if errmsg.lower() in errorstr:
                return True
        return False
    
    security.declareProtected(permissions.ManagePortal, 'processEmailReports') 
    def requeueLibraryFile(self, id):
        """ method so that admins can add a file back to the queue """
        pcat = getToolByName(self, 'portal_catalog')
        results = pcat.searchResults(id=id)
        if results:
            return self.queueLibraryFile(results[0].getObject())
        return 'No results returned for file with id '+id
    
    security.declarePrivate('queueLibraryFile')    
    def queueLibraryFile(self, libraryfile):
        """ method to queue up a library file """
        if len(libraryfile) > 0:
            if not libraryfile.getOid():
                libraryfile.setOid(generateOID())
            try:
                self[libraryfile.getId()] = libraryfile
            except BadRequest, e:
                return e
            return 'Sucessfully queued file... ['+libraryfile.id+']'
    
    def libraryFileIsQueued(self, libraryfile):
        """ simple method to determine if the file is in the queue"""
        return self.has_key(libraryfile.getId())

    def get_content_type(self, filename):
        return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

    def crossref_encode_multipart(self, key, value):
        BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$'
        CRLF = '\r\n'
        filename = 'TNC_'+self.tnc_crossref_prefix+'_'+str(random.random())+'.xml'
        L = []
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
        L.append('Content-Type: text/xml')
        L.append('')
        L.append(value)
        L.append('--' + BOUNDARY + '--')
        L.append('')
        body = CRLF.join(L)
        content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
        return content_type, body

    def crossref_post_multipart(self, xmlpayload, area):
        """
        Posts files to an http host as multipart/form-data.
        Return the server's response page.
        """
        host=self.host
        selector = self.selector % (self.crossref_login, self.crossref_pwd, area)
        key='fname'

        value = tostring(xmlpayload)
        content_type, body = self.crossref_encode_multipart(key, value)
        h = httplib.HTTP(host)
        h.putrequest('POST', selector)
        h.putheader('content-type', content_type)
        h.putheader('content-length', str(len(body)))
        h.endheaders()
        h.send(body)
        errcode, errmsg, headers = h.getreply()
        return h.file.read()

InitializeClass(CrossRefTool)
        
    
