from xero import Xero
from xero.auth import PrivateCredentials
from xero.exceptions import XeroNotFound, XeroBadRequest


class PrivateApp:
    class LenGenerator:
        """
        Helper class to provide len() to generator
        Xero SDK returns always a list. However, we can control the data stream using generators.

        """
        def __init__(self, data):
            self._data = data

        def __len__(self):
            return len(self._data)

        def __iter__(self):
            for r in self._data:
                yield r

        def __next__(self):
            return next(self.__iter__())

        @property
        def keys(self):
            if not len(self._data):
                return []
            return self._data[0].keys()

    def __init__(self, private_key, consumer_key):
        self._credentials = PrivateCredentials(consumer_key, private_key)
        self._xero = Xero(self._credentials)

    def payments(self, id=None, *, page=1, as_list=False, **kwargs):
        return self.get('payments', id=id, page=page, as_list=as_list, **kwargs)

    def invoices(self, id=None, *, page=1, as_list=False, **kwargs):
        return self.get('invoices', id=id, page=page, as_list=as_list, **kwargs)

    def get(self, entity, id=None, *, page=1, as_list=False, **kwargs):
        """
        Retrieve <entities> according to the paramenters
        - if id is provided, only that <entity> will be returned (if exists)
        - if no parameters are provided all <entities> will be returned
        - kwargs will be used as filters on Xero API (Django way supported: Name__startswith='John')

        Special kwargs supported by Xero SDK:
        - since: accepts datetime object
        - raw: string to be used when a filter is not supported by the SDK: raw='AmountDue > 0'
        - order: string to sort the response: order='EmailAddress DESC'

        If as_list is False (default) a generator is returned
        :return: dict/generator/list
        """
        api = self._xero.__getattribute__(entity)
        if id:
            try:
                return api.get(id)[0]
            except XeroNotFound as ex:
                print(f'Error: {ex}')
                return None
        if not kwargs:
            res = api.all()
            if as_list:
                return res
            return self.LenGenerator(res)
        try:
            res = api.filter(**kwargs, page=page)
            if as_list:
                return res
            return self.LenGenerator(res)
        except XeroBadRequest as ex:
            print(f'Error: {ex}')
            return []
