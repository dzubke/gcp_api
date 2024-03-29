# Copyright 2018 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This is a sample Airport Information service implemented using
Google Cloud Endpoints Frameworks for Python."""

# [START imports]
# import sys
# sys.path
# sys.path.append('/Users/dustin/CS/jobs/interview_problems/Zume/CreditClassification/src/server/gcp_api/zume_api/zume/lib')

import endpoints
from endpoints import message_types
from endpoints import messages
from endpoints import remote

from data import LOAN_BOOK, FEATURE_KEYS

# [END imports]

# [START messages]
LOAN_RESOURCE = endpoints.ResourceContainer(
    loan_id=messages.IntegerField(1, required=True)
)


class Loan_app(messages.Message):
    loan_id = messages.IntegerField(1, required=True)
    loan_amnt = messages.FloatField(2, required=False)
    funded_amnt = messages.FloatField(3, required=False)
    funded_amnt_inv = messages.FloatField(4, required=False)
    term = messages.FloatField(5, required=False)
    int_rate = messages.FloatField(6, required=False)
    installment = messages.FloatField(7, required=False)
    annual_inc = messages.FloatField(8, required=False)
    dti = messages.FloatField(9, required=False)
    delinq_2yrs = messages.FloatField(10, required=False)
    inq_last_6mths = messages.FloatField(11, required=False)
    open_acc = messages.FloatField(12, required=False)
    pub_rec = messages.FloatField(13, required=False)
    revol_bal = messages.FloatField(14, required=False)
    total_acc = messages.FloatField(15, required=False)
    total_pymnt = messages.FloatField(16, required=False)
    total_pymnt_inv = messages.FloatField(17, required=False)
    total_rec_prncp = messages.FloatField(18, required=False)
    total_rec_int = messages.FloatField(19, required=False)
    total_rec_late_fee = messages.FloatField(20, required=False)
    recoveries = messages.FloatField(21, required=False)
    collection_recovery_fee = messages.FloatField(22, required=False)
    last_pymnt_amnt = messages.FloatField(23, required=False)
    pub_rec_bankruptcies = messages.FloatField(24, required=False)
    predict = messages.IntegerField(25, required=False)



LOAN_APP_RESOURCE = endpoints.ResourceContainer(
    Loan_app,
    loan_id=messages.IntegerField(1, required=True)
)


class LoanList(messages.Message):
    loans = messages.MessageField(Loan_app, 1, repeated=True)
# [END messages]

# mapping dict
# IATA_RESOURCE: LOAN_RESOURCE
# Airport: Loan_app
# IATA_AIRPORT_RESOURCE: LOAN_APP_RESOURCE
# AirportList: LoanList
# IataApi: LoanApi

# iata URL: https://zume-api-v2.appspot.com/_ah/api/iata/v1/airport/ABQ
# loanbook URL: https://zume-api-v2.appspot.com/_ah/api/loanbook/v1/loan_app/0

# [START loanbook_api]
@endpoints.api(name='loanbook', version='v1')
class LoanApi(remote.Service):
    @endpoints.method(
        LOAN_RESOURCE,
        Loan_app,
        path='loan_app/{loan_id}',
        http_method='GET',
        name='get_loan')
    def get_loan(self, request):
        if request.loan_id not in LOAN_BOOK:
            raise endpoints.NotFoundException()
        temp_app = Loan_app()
        for keys in FEATURE_KEYS:
            setattr(temp_app, keys, LOAN_BOOK.get(request.loan_id)[keys])
        return temp_app


    @endpoints.method(
        message_types.VoidMessage,
        LoanList,
        path='loan_apps',
        http_method='GET',
        name='list_loans')
    def list_loans(self, request):
        loan_ids = LOAN_BOOK.keys()
        loan_ids.sort()
        temp_LoanList = []
        for loan_id in loan_ids:
            temp_app = Loan_app()
            for keys in FEATURE_KEYS:
                setattr(temp_app, keys, LOAN_BOOK.get(loan_id)[keys])
            temp_LoanList.append(temp_app)
        return LoanList(loans=temp_LoanList)

    @endpoints.method(
        LOAN_RESOURCE,
        message_types.VoidMessage,
        path='loan_app/{loan_id}',
        http_method='DELETE',
        name='delete_loanapp',
        api_key_required=True)
    def delete_loanapp(self, request):
        if request.loan_id not in LOAN_BOOK:
            raise endpoints.NotFoundException()
        del LOAN_BOOK[request.loan_id]
        return message_types.VoidMessage()
'''
    @endpoints.method(
        Airport,
        Airport,
        path='airport',
        http_method='POST',
        name='create_airport',
        api_key_required=True)
    def create_airport(self, request):
        if request.iata in AIRPORTS:
            raise endpoints.BadRequestException()
        AIRPORTS[request.iata] = request.name
        return Airport(iata=request.iata, name=AIRPORTS[request.iata])

    @endpoints.method(
        IATA_AIRPORT_RESOURCE,
        Airport,
        path='airport/{iata}',
        http_method='POST',
        name='update_airport',
        api_key_required=True)
    def update_airport(self, request):
        if request.iata not in AIRPORTS:
            raise endpoints.BadRequestException()
        AIRPORTS[request.iata] = request.name
        return Airport(iata=request.iata, name=AIRPORTS[request.iata])
# [END iata_api]
'''

# [START api_server]
api = endpoints.api_server([LoanApi])
# [END api_server]


def main():

    print('weve made it this far')

if __name__ == '__main__': main()
