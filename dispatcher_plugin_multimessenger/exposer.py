from cdci_data_analysis.analysis.instrument import Instrument
from cdci_data_analysis.analysis.queries import SourceQuery, InstrumentQuery
from .queries import MMProductQuery, MMProposalQuery
from .dataserver_dispatcher import MMDataDispatcher
from . import conf_file


def instr_factory():
    return Instrument('multimessenger',
                      src_query = SourceQuery('src_query'),
                      instrumet_query = InstrumentQuery('multi_instrument_query'),
                      data_serve_conf_file=conf_file,
                      product_queries_list=[MMProductQuery('mm_prod_query'), MMProposalQuery('mm_proposal_query')],
                      query_dictionary={'combine': 'mm_prod_query', 'propose': 'mm_proposal_query'},
                      asynch=True, 
                      data_server_query_class=MMDataDispatcher,
                      )

instr_factory_list = [instr_factory]
