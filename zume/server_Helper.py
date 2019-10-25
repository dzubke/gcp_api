"""
This is the loan_book module and supports all the ReST actions for the
loan_book collection
"""

# standard libraries
from datetime import datetime
import pickle
from typing import DefaultDict, Any
from collections import defaultdict

# 3rd party libararies
from flask import make_response, abort
import numpy as np


def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


# Data to serve with our API,


def read_all():
    """
    This function responds to a request for /api/loan_book
    with the complete lists of loan_book
    :return:        json string of list of loan_book
    """
    # Create the list of loan_book from our data
    return [loan_book[key] for key in sorted(loan_book.keys())]


def read_one(loan_id):
    """
    This function responds to a request for /api/loan_book/{loan_id}
    with one matching loan application from loan_book
    :param loan_id:   ID of the loan application to find
    :return:         loan application matching loan_id
    """
    # Does the loan application exist in loan_book?
    if loan_id in loan_book:
        loan_application = loan_book.get(loan_id)

    # otherwise, nope, not found
    else:
        abort(
            404, "Loan Application with ID: {loan_id} not found".format(loan_id=loan_id)
        )

    return loan_application


def create(loan_application):
    """
    This function creates a new loan_application in the loan_book structure
    based on the passed in loan_application data
    :param loan_application:  loan_application to create in loan_book structure
    :return:        201 on success, 406 on loan_application exists

    """
    loan_id = loan_application.get("loan_id", None)
    # loan_status = loan_application.get("loan_status", None)
    # loan_amnt = loan_application.get("loan_amnt", None)
    # funded_amnt = loan_application.get("funded_amnt", None)
    # predict = loan_application.get("predict", None)
    

    # Does the loan application exist already?
    if loan_id not in loan_book and loan_id is not None:
        # loan_book = {**loan_book, **loan_application}   # i tried to be cleverer about this updated but I got a 'loan_book referenced before assignment' error
        loan_book.update({loan_id: loan_application})
        
        '''
        for key in loan_book.get(loan_id).keys():
            if key != "predict":        # the update method should not be able to change the predict value
                loan_book.get(loan_id).update({key: loan_application.get(key)})



        loan_book[loan_id] = {
            "loan_id": loan_id,
            "loan_status": loan_status,
            "loan_amnt": loan_amnt,
            "funded_amnt": funded_amnt,
            "predict": predict,
            "timestamp": get_timestamp(),
        }
        
        '''
        return make_response(
            "Loan application with ID: {loan_id} successfully created".format(loan_id=loan_id), 201
        )

    # Otherwise, they exist, that's an error
    else:
        abort(
            406,
            "Loan application with ID: {loan_id} already exists".format(loan_id=loan_id),
        )


def update(loan_id, loan_application):
    """
    This function updates an existing loan_application in the loan_book structure
    :param loan_id:   last name of loan_application to update in the loan_book structure
    :param loan_application:  loan_application to update
    :return:        updated loan_application structure
    """
    # Does the loan_application exist in loan_book?
    if loan_id in loan_book:
        for key in loan_application.keys():
            if key != "predict":        # the update method should not be able to change the predict value
                loan_book.get(loan_id).update({key: loan_application.get(key)})


        return loan_book.get(loan_id)

    # otherwise, nope, that's an error
    else:
        abort(
            404, "loan_application with ID: {loan_id} not found".format(loan_id=loan_id)
        )

'''
loan_book.get(loan_id).update({"loan_status": loan_application.get("loan_status")})
        loan_book[loan_id]["loan_amnt"] = loan_application.get("loan_amnt")
        loan_book[loan_id]["funded_amnt"] = loan_application.get("funded_amnt")
        loan_book[loan_id]["timestamp"] = get_timestamp()

'''

def delete(loan_id):
    """
    This function deletes a loan_application from the loan_book structure
    :param loan_id:   ID of loan_application to delete
    :return:        200 on successful delete, 404 if not found
    """
    # Does the loan_application to delete exist?
    if loan_id in loan_book:
        del loan_book[loan_id]
        return make_response(
            "loan application with ID: {loan_id} successfully deleted".format(loan_id=loan_id), 200
        )

    # Otherwise, nope, loan_application to delete not found
    else:
        abort(
            404, "loan_application with ID: {loan_id} not found".format(loan_id=loan_id)
        )

def read_predict(loan_id):
    """
    This function responds to a request for /api/loan_book/{loan_id}/predict
    with the predict element in the loan application from loan_book. 
    The predict element can have three values:
        -1      the loan application hasn't been evaluated
        0       the loan application has been rejected
        1       the loan application has been approved

    :param loan_id:   ID of the loan application to find
    :return predict:         predict value loan application matching loan_id
    """
    # Does the loan application exist in loan_book?
    if loan_id in loan_book:
        prediction = loan_book.get(loan_id).get('predict')

    # otherwise, nope, not found
    else:
        abort(
            404, "Loan Application with ID: {loan_id} not found".format(loan_id=loan_id)
        )

    return prediction


def update_predict(loan_id):
    """
    This function responds to the request PUT /api/loan_book/{loan_id}/predict
    by updating the predict element using the model for credit prediction. 
    The predict element can have three values:
        -1      the loan application hasn't been evaluated
        0       the loan application has been rejected
        1       the loan application has been approved

    :param loan_id:         ID of the loan application to find
    :return predict:         predict value loan application matching loan_id
    """
    # Does the loan application exist in loan_book?
    if loan_id in loan_book:
        
        prediction = model_fit(loan_book.get(loan_id))
        
        loan_book.get(loan_id).update({'predict': prediction})

    # otherwise, nope, not found
    else:
        abort(
            404, "Loan Application with ID: {loan_id} not found".format(loan_id=loan_id)
        )

def update_all_predict(loan_id):
    """
    This function responds to the request PUT /api/loan_book/predict
    by updating the all of the predict element in loan book using the model for credit prediction. 
    The predict element can have three values:
        -1      the loan application hasn't been evaluated
        0       the loan application has been rejected
        1       the loan application has been approved

    :param loan_id:         ID of the loan application to find
    """
    # Does the loan application exist in loan_book?
    if loan_id in loan_book:
        prediction = loan_book.get(loan_id).get('predict')

    # otherwise, nope, not found
    else:
        abort(
            404, "Loan Application with ID: {loan_id} not found".format(loan_id=loan_id)
        )

def model_fit(loan_app: dict):
    """This model will take a loan application loan_app as input and will return the predicted 

    Parameters
    ---------
    loan_app: dict

    Returns
    -------
    prediction

    """

    # unpack the dictionary as a list
    loan_array = dict_to_numpy(loan_app)

    # load the model_fit object from the computer
    model_fn = '/Users/dustin/CS/jobs/interview_problems/Zume/CreditClassification/src/credit_classification/model_fit.pickle'
   
    # as a test, I imported some picked data
    # data_fn = '/Users/dustin/CS/jobs/interview_problems/Zume/CreditClassification/src/credit_classification/data_sample.pickle'

    with open(model_fn, 'rb') as f:
        model_fit = pickle.load(f)

        #with open(data_fn, 'rb') as d:
        #    data_sample = pickle.load(d)

        prediction = model_fit.predict(loan_array)     #

    return int(prediction[0])


def dict_to_numpy(loan_app: dict):
    """this funciton takes a dictionary loan_app as input and converts the data into a numpy array

    Parameters
    ----------
    loan_app: dict of shape -  # samples x 24

    Returns
    -------
    array: np.ndarray of shape - # samples x 24

    """
    # creates an array with the elements of the loan_app dict except the loan_id and predict elements
    array = np.array([val for key, val in loan_app.items() if key != "loan_id" and key != "predict" and key != "timestamp" ])
    array = array.reshape(1, -1) 

    return array
    



def main():
    

    loan_app = {
        "loan_id": 1,
        "loan_amnt": 7000,
        "funded_amnt": 7000,
        "funded_amnt_inv": 6475.0,
        "term": 36,
        "int_rate": 8.88,
        "installment": 222.21,
        "annual_inc": 55000.0,
        "dti": 7.61,
        "delinq_2yrs": 0.0,
        "inq_last_6mths": 1.0,
        "open_acc": 6.0,
        "pub_rec": 0.0,
        "revol_bal": 8869,
        "total_acc": 21.0,
        "total_pymnt": 7644.870263,
        "total_pymnt_inv": 7182.51,
        "total_rec_prncp": 7000.00,
        "total_rec_int": 764.87,
        "total_rec_late_fee": 0.0,
        "recoveries": 0.0,
        "collection_recovery_fee": 0.0,
        "last_pymnt_amnt": 2786.50,
        "pub_rec_bankruptcies": 0.0,
        "predict": -1,
        "timestamp": get_timestamp(),
    }

    print(read_one(0))
    print(read_all())
    create(loan_app)
    print(loan_book)
    #print(model_fit(loan_app))


if __name__ == '__main__': main()