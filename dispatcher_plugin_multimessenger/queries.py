from tokenize import Name
from cdci_data_analysis.analysis.queries import ProductQuery, QueryOutput
from cdci_data_analysis.analysis.parameters import Name
import json
import os
from collections import OrderedDict

from oda_api.api import DispatcherAPI
from bokeh.io import output_notebook
from bokeh.plotting import figure, show
from bokeh.models import Whisker, ColumnDataSource
from bokeh.layouts import gridplot

from astropy.time import Time
from astropy import units as u

from .products import MultiInstrumentProduct

class MMProductQuery(ProductQuery):
    def __init__(self, name):
        ids_csv = Name(name='ids_csv')
        super().__init__(name, parameters_list = [ids_csv])
    
    # TODO: can be defined in MMDataDispatcher, what's better?
    def test_communication(self, *args, **kwargs):
        query_out = QueryOutput()
        query_out.set_done()
        return query_out
    
    def test_has_products(self, *args, **kwargs):
        # TODO: actual testing for dirs here?
        query_out = QueryOutput()
        query_out.set_products(['input_prod_list'], [[]])
        query_out.set_done()
        return query_out    
    
    def get_data_server_query(self, instrument, config=None, **kwargs):
        param_dict = {'ids_csv': instrument.get_par_by_name('ids_csv')}
        return MMDataDispatcher(param_dict) 
    
    def build_product_list(self, instrument, res, out_dir, api=False):
        prod_list = [MultiInstrumentProduct(res)]
        return prod_list
    
    def process_product_method(self, instrument, prod_list, api=False):
        query_out = QueryOutput()
        image_prod  = prod_list.prod_list[0]

        if api is True:
            raise NotImplemented
        else:
            plot_dict = {'image': image_prod.get_plot()}
            #image_prod.write() 

            query_out.prod_dictionary['name'] = image_prod.name
            query_out.prod_dictionary['file_name'] = 'foobar' 
            query_out.prod_dictionary['image'] = plot_dict
            query_out.prod_dictionary['download_file_name'] = 'multi_image.tar.gz'
            query_out.prod_dictionary['prod_process_message'] = ''

        return query_out
    
class MMDataDispatcher:
    def __init__(self, param_dict) -> None:
        self.ids = param_dict['ids_csv'].value.split(',')
    
    def run_query(self, 
                  call_back_url=None,
                  run_asynch = False,
                  logger=None):
        
        # FIXME: hardcoded dispatcher self-address
        disp = DispatcherAPI(url='http://127.0.0.1:8000', instrument='mock')
        
        self.get_products_api_params()
        
        res = [disp.get_product(**par_dict) for par_dict in self.products_api_params]
                
        query_out = QueryOutput()
        query_out.set_done(job_status='done')
        return res, query_out
    
    @staticmethod
    def get_params_from_dir(path):
        try:
            with open(os.path.join(path, 'analysis_parameters.json')) as fd:
                query_dict = json.load(fd)
        except FileNotFoundError:
            with open(os.path.join(path+'_aliased', 'analysis_parameters.json')) as fd:
                query_dict = json.load(fd)
                
        # TODO: adapted from oda_api, some code duplication
        query_dict = OrderedDict(sorted(query_dict.items()))

        _skip_list_ = ['job_id', 'query_status',
                       'session_id', 'use_resolver[local]', 'use_scws']

        _alias_dict = {}
        _alias_dict['product_type'] = 'product'
        _alias_dict['query_type'] = 'product_type'

        _api_dict = {}
        for k in query_dict.keys():
            if k not in _skip_list_:

                if k in _alias_dict.keys():
                    n = _alias_dict[k]

                else:
                    n = k

                if query_dict[k] is not None:
                    _api_dict[n] = query_dict[k]
        
        return _api_dict
    
    def get_products_api_params(self):
        self.products_api_params = []
        for dirid in self.ids:
            self.products_api_params.append(self.get_params_from_dir(dirid))
            
    
    