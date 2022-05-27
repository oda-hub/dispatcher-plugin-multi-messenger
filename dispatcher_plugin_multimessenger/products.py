from gwpy.spectrogram import Spectrogram
from oda_api.data_products import NumpyDataProduct

from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.models import Whisker, ColumnDataSource
from bokeh.layouts import gridplot

from astropy.time import Time
from astropy import units as u

class MultiInstrumentProduct:
    def __init__(self, res, name = "multi-instrument"):
        if len(res) != 2:
            raise NotImplemented
        
        if set([type(res[0]._p_list[0]), type(res[1]._p_list[0])]) != set([Spectrogram, NumpyDataProduct]):
            raise NotImplemented
        
        self.prod_list = res
        self.name = name
        
    def get_plot(self):
        dp0 = [x._p_list[0] for x in self.prod_list if type(x._p_list[0]) == NumpyDataProduct][0]
        dp1 = [x._p_list[0] for x in self.prod_list if type(x._p_list[0]) == Spectrogram][0]
        
        data0 = dp0.get_data_unit(1).data
        header0 = dp0.get_data_unit(1).header
        tref0 = Time( (header0['TIMEZERO'] * u.s).to('d') + header0['MJDREF'] * u.d , format='mjd', scale='tt' )
        xval0 = tref0 + data0['TIME'] * u.s
        
        xval1 = Time( dp1.xindex , format='gps' )
        
        xmin = min(xval0[0], xval1[0])
        xmax = max(xval0[-1], xval1[-1])
        
        
        f1 = figure(plot_width = 650,
                    plot_height = 300,
                    x_axis_type = 'linear',
                    y_axis_type = 'log',
                    x_range = ( 0, (xmax - xmin).to('s').value ), 
                    y_range = (dp1.yindex[0].value, dp1.yindex[-1].value),
                    y_axis_label = 'Frequency [Hz]',
                    )
        f1_im = f1.image(image=[dp1.T.value], 
                 x = (xval1[0] - xmin).to('s').value, 
                 y = dp1.yindex[0].value, 
                 dw = (xval1[-1] - xval1[0]).to('s').value,
                 dh = dp1.yindex[-1].value - dp1.yindex[0].value,
                 palette = 'Plasma256',
                 )
        
        f2 = figure(plot_width = 650,
                    plot_height = 300,
                    x_axis_type = 'linear',
                    y_axis_type = 'linear',
                    x_range= f1.x_range, 
                    x_axis_label = 'Time [seconds] from %s' % xmin.strftime("%Y-%m-%d %T UTC"),
                    y_axis_label = 'Rate (cts/s)'
                    )
        cr = f2.circle( (xval0 - xmin).to('s').value,
                data0['RATE'],
                )
        errors_src = ColumnDataSource(data = dict(
                            lower = data0['RATE'] - data0['ERROR'],
                            upper = data0['RATE'] + data0['ERROR'],
                            base = (xval0 - xmin).to('s').value,
                            ))
        errorbars = Whisker( source = errors_src,
                            lower = "lower",
                            upper = "upper",
                            dimension = "height",
                            base = "base",
                            line_color = cr.glyph.fill_color,
                            line_width = 2,
                            ) 
        errorbars.upper_head.line_color = cr.glyph.fill_color
        errorbars.lower_head.line_color = cr.glyph.fill_color

        f2.add_layout( errorbars )        
        
        pl = gridplot([[f1], [f2]])
        
        script, div = components(pl)
        html_dict = {}
        html_dict['script'] = script
        html_dict['div'] = div
        return html_dict
