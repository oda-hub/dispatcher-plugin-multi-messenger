from marshmallow import Schema, fields, INCLUDE, validate

class ParameterDict(fields.Dict):
    pass
  
class PropositionInput(Schema):
    anal_par_json = fields.List(ParameterDict()) 
    
    # parameter value passed as json-encoded string    
    # example GET query url:
    # http://localhost:8000/run_analysis?instrument=multimessenger&product_type=propose&query_status=new&query_type=Real&anal_par_json=[{"DEC":-23.381484166666667,"RA":197.45035416666664,"T1":"2017-08-17T12:40:59.400","T2":"2017-08-17T12:41:14.400","T_format":"isot","instrument":"spi_acs","job_id":"","product_type":"spi_acs_lc","query_status":"new","query_type":"Real","selected_catalog":null,"session_id":"BYYFE1O3I18PYAU7","src_name":"gw170817","time_bin":2,"time_bin_format":"sec","token":null},{"DEC":-23.381484166666667,"RA":197.45035416666664,"T1":"2017-08-17T12:40:59.400","T2":"2017-08-17T12:41:14.400","T_format":"isot","detector":"H1","instrument":"gw","job_id":"6ac3260935cdadd6","product_type":"gw_spectrogram","qmax":64,"qmin":4,"query_status":"ready","query_type":"Real","session_id":"VVGJNPW7AO1JFYZ3","src_name":"gw170817","token":null,"whiten":"true"}]

class MMInput(PropositionInput):
    pass

class ProductIndex(fields.Integer):
    pass

class Proposition(Schema):
    label = fields.String(required=False)
    method = fields.String(validate=validate.OneOf(["time", "energy", "space"])) 
    combination = fields.List(ProductIndex())

# returned as 'propositions_product' product    
class PropositionsProduct(Schema):
    message = fields.String()
    proposistions = fields.Nested(Proposition(), many=True)
