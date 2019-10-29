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
    loan_amnt = messages.IntegerField(2, required=False)
    funded_amnt = messages.IntegerField(3, required=False)
    info = messages.StringField(4, required=False)



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
        # Loan_app(loan_id=request.loan_id, loan_amnt=LOAN_BOOK.get(request.loan_id)['loan_amnt'], funded_amnt=LOAN_BOOK.get(request.loan_id)['funded_amnt'])


    @endpoints.method(
        message_types.VoidMessage,
        LoanList,
        path='airports',
        http_method='GET',
        name='list_airports')
    def list_airports(self, request):
        codes = LOAN_BOOK.keys()
        codes.sort()
        return AirportList(airports=[
          Airport(iata=iata, name=AIRPORTS[iata]) for iata in codes
        ])

'''
    @endpoints.method(
        IATA_RESOURCE,
        message_types.VoidMessage,
        path='airport/{iata}',
        http_method='DELETE',
        name='delete_airport',
        api_key_required=True)
    def delete_airport(self, request):
        if request.iata not in AIRPORTS:
            raise endpoints.NotFoundException()
        del AIRPORTS[request.iata]
        return message_types.VoidMessage()

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