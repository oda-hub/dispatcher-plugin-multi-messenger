from cdci_data_analysis.analysis.instrument import Instrument
from cdci_data_analysis.analysis.queries import SourceQuery, InstrumentQuery
from .queries import MMProductQuery



def instr_factory():
    return Instrument('multimessenger',
                      SourceQuery('src_query'),
                      InstrumentQuery('multi_instrument_query'),
                      product_queries_list=[MMProductQuery('mm_prod_query')],
                      query_dictionary={'multimessenger': 'mm_prod_query'},
                      asynch=False, 
                      )

instr_factory_list = [instr_factory]
