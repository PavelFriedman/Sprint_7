import requests
import urls
class ScooterApi:
    @staticmethod
    def create_courier(body):
        return requests.post(urls.CREATE_COURIER_ENDPOINT, json=body)

    @staticmethod
    def login_courier(body):
        return requests.post(urls.LOGIN_COURIER_ENDPOINT, json=body)

    @staticmethod
    def create_order(body):
        return requests.post(urls.ORDER_ENDPOINT, json=body)

    @staticmethod
    def get_order():
        return requests.get(urls.ORDER_ENDPOINT)

    @staticmethod
    def delete_courier(id):
        return requests.delete(urls.CREATE_COURIER_ENDPOINT+"/"+id)

    @staticmethod
    def cancel_order(body):
        return requests.put(urls.CANCEL_ORDER_ENDPOINT, json=body)