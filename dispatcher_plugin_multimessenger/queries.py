from cdci_data_analysis.analysis.queries import ProductQuery, QueryOutput
from cdci_data_analysis.analysis.parameters import Name

from .products import MultiInstrumentProduct

class MMProductQuery(ProductQuery):
    def __init__(self, name):
        anal_par_json = Name(name='anal_par_json')
        super().__init__(name, parameters_list = [anal_par_json])
   
 
    def get_data_server_query(self, instrument, config=None, **kwargs):
        param_dict = {'anal_par_json': instrument.get_par_by_name('anal_par_json').value}
        return instrument.data_server_query_class(instrument=instrument,
                                                  config=config,
                                                  param_dict=param_dict,
                                                  task='/api/v1.0/get/prodcombine')

    
    def build_product_list(self, instrument, res, out_dir, api=False):
        prod_list = []
        if out_dir is None:
            out_dir = './'
        if 'output' in res.json().keys(): # in synchronous mode
            _o_dict = res.json() 
        else:
            _o_dict = res.json()['data']
        prod_list = [MultiInstrumentProduct(_o_dict['output'])]
        return prod_list
    
    def process_product_method(self, instrument, prod_list, api=False):
        query_out = QueryOutput()
        image_prod  = prod_list.prod_list[0]

        if api is True:
            raise NotImplementedError
        else:
            plot_dict = {'image': image_prod.get_plot()}
            #image_prod.write() 

            query_out.prod_dictionary['name'] = image_prod.name
            query_out.prod_dictionary['file_name'] = 'foobar' 
            query_out.prod_dictionary['image'] = plot_dict
            query_out.prod_dictionary['download_file_name'] = 'multi_image.tar.gz'
            query_out.prod_dictionary['prod_process_message'] = ''

        return query_out
    
class MMProposalQuery(ProductQuery):
    def __init__(self, name):
        anal_par_json = Name(name='anal_par_json')
        super().__init__(name, parameters_list = [anal_par_json])
   
 
    def get_data_server_query(self, instrument, config=None, **kwargs):
        param_dict = {'anal_par_json': instrument.get_par_by_name('anal_par_json').value}
        return instrument.data_server_query_class(instrument=instrument,
                                                  config=config,
                                                  param_dict=param_dict,
                                                  task='/api/v1.0/get/propose')

    
    def build_product_list(self, instrument, res, out_dir, api=False):
        prod_list = []
        if out_dir is None:
            out_dir = './'
        if 'output' in res.json().keys(): # in synchronous mode
            _o_dict = res.json() 
        else:
            _o_dict = res.json()['data']
        prod_list = [_o_dict['output']]
        return prod_list
    
    def process_product_method(self, instrument, prod_list, api=False):
        query_out = QueryOutput()
        prod  = prod_list.prod_list[0]

        if api is True:
            raise NotImplementedError
        else:
            combinations = prod['combinations']
            
            #only one possibility currently
            if len(combinations) == 1:
                proposition = { 
                    'message': 'OK',
                    'time': combinations[0],
                    'energy': [],
                    'space': [] 
                }
            elif len(combinations) == 0:
                proposition = {
                    'message': 'not possible',
                    'time': [],
                    'energy': [],
                    'space': [],     
                }
            elif len(combinations) > 1:
                proposition = {
                    'message': 'not unique',
                    'time': [],
                    'energy': [],
                    'space': [],     
                }
            
            
            query_out.prod_dictionary['proposition'] = proposition

        return query_out