import sys
import requests
import json
import base64


key = 'Basic ' + base64.b64encode(bytes(sys.argv[1], 'utf-8')).decode('utf-8')

def getCustomerPage(page):
    return requests.get('https://api.reepay.com/v1/customer?page=' + str(page) + '&size=20', headers={'authorization':key})

def loopCustomerPage(content):
    for customerObj in content:
        # print(customerObj)
        deleteCustomers(customerObj)

def deleteCustomers(customerObj):
    response = requests.delete('https://api.reepay.com/v1/customer/' + customerObj['handle'], headers={'authorization':key})
    if response.status_code == 200:
        print('Deleted!', customerObj['handle'])
    else:
        print('Failed', response.status_code, 'https://api.reepay.com/v1/customer/' + customerObj['handle'], json.loads(response.text))

def customerDeletionStart():
    response = getCustomerPage(1)
    if response.status_code == 200:
        customers = json.loads(response.text)
        loopCustomerPage(customers['content'])
        pages = customers['total_pages']
        for page in range(2, int(pages) + 1):
            response = getCustomerPage(page)
            if response.status_code == 200:
                loopCustomerPage(json.loads(response.text)['content'])
            else:
                print('Failed get', response.status_code)

def getSubscriptionPage(page):
    return requests.get('https://api.reepay.com/v1/subscription?page=' + str(page) + '&size=20', headers={'authorization':key})

def loopSubscriptionPage(content):
    for subObj in content:
        if subObj['state'] != 'expired':
            # print(subObj)
            deleteSubscription(subObj)

def deleteSubscription(subObj):
    body = {"compensation_method": "prorated_refund"}
    response = requests.post('https://api.reepay.com/v1/subscription/' + subObj['handle'] + '/expire', headers={'authorization':key}, data=body)
    if response.status_code == 200:
        print('Deleted sub handle', subObj['handle'])
    else:
        print('Failed', response.status_code, 'https://api.reepay.com/v1/subscription/' + subObj['handle'] + '/expire', json.loads(response.text))

def subscriptionDeletionStart():
    response = getSubscriptionPage(1)
    if response.status_code == 200:
        subs = json.loads(response.text)
        loopSubscriptionPage(subs['content'])
        pages = subs['total_pages']
        for page in range(2, int(pages) + 1):
            response = getSubscriptionPage(page)
            if response.status_code == 200:
                loopSubscriptionPage(json.loads(response.text)['content'])
            else:
                print('Failed get', response.status_code)

def getInvoicePage(page):
    return requests.get('https://api.reepay.com/v1/invoice?page=' + str(page) + '&size=20', headers={'authorization':key})

def loopInvoicePage(content):
    for invoiceObj in content:
        if invoiceObj['state'] != 'cancelled':
            # print(invoiceObj)
            cancelInvoice(invoiceObj)

def cancelInvoice(invoiceObj):
    response = requests.post('https://api.reepay.com/v1/invoice/' + str(invoiceObj['handle']) + '/cancel', headers={'authorization':key})
    if response.status_code == 200:
        print('Cancel invoice handle', invoiceObj['handle'])
    else:
        print('Failed', response.status_code, 'https://api.reepay.com/v1/invoice/' + invoiceObj['handle'] + '/cancel', json.loads(response.text))

def invoiceDeletionStart():
    response = getInvoicePage(1)
    if response.status_code == 200:
        invoice = json.loads(response.text)
        loopInvoicePage(invoice['content'])
        pages = invoice['total_pages']
        for page in range(2, int(pages) + 1):
            response = getInvoicePage(page)
            if response.status_code == 200:
                loopInvoicePage(json.loads(response.text)['content'])
            else:
                print('Failed get', response.status_code)

invoiceDeletionStart()
subscriptionDeletionStart()
customerDeletionStart()