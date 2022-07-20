class MultiInstrumentProduct:
    def __init__(self, res, name = "multi-instrument"):
        self.product = res
        self.name = name
        
    def get_plot(self):
        return self.product.get('bokeh_plot', None)
