from marshmallow import Schema, fields, INCLUDE

class PropositionInput(Schema):
    anal_par_json = fields.Str()
    # list of paam dicts as json encoded string 

class MMInput(PropositionInput):
    pass

# returned as 'proposition' product
class PropositionOutput(Schema):
    class Meta:
        unknown = INCLUDE
        # other combinations possible in the future
    
    message = fields.Str()            
    time = fields.List(fields.Dict()) # list of param dicts
    energy = fields.List(fields.Dict())
    space = fields.List(fields.Dict())
    
