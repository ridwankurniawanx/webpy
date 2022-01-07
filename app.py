from re import template
from pywebio import *
from pywebio.output import *
from pywebio.pin import *
from pywebio import config
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import plotly.express as px
img_link = "https://www.influxdata.com/wp-content/uploads/histogram.png"
md = '*Welcome, here is an instruction.....*'

def gdp_chart(plot_type):
    import plotly.express as px

    df = px.data.gapminder()
    fig = px.line_geo(df.query('year == 2007'), locations='iso_alpha', 
        color='continent', projection='orthographic', template="plotly_dark", )
    fig.update_layout(showlegend=False)
    
    animation = px.scatter(df, x='gdpPercap', y='lifeExp', color='continent', size='pop', size_max=40, 
                hover_name='country', template="plotly_dark", log_x=True, animation_frame='year',
                 animation_group='country', range_x=[100, 50000], range_y=[20,90])
                 
    if plot_type == 'animation':
        #put_html(gdp_chart('animation')) #put the plot on a pywebio app
        return animation.to_html(include_plotlyjs="require", full_html=True)
    elif plot_type == 'geo':
        #put_html(gdp_chart('geo')) #put the plot on a pywebio app
        return fig.to_html(include_plotlyjs="require", full_html=True)

def meshchart():
    z_data = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/api_docs/mt_bruno_elevation.csv')

    fig = go.Figure(data=[go.Surface(z=z_data.values)])

    fig.update_layout(template="plotly_dark", title='Mt Bruno Elevation', autosize=False,
                    width=500, height=500,
                    margin=dict(l=65, r=50, b=65, t=90))

       
    return fig.to_html(include_plotlyjs="require", full_html=True)

def isochart():
    df = px.data.tips()

    fig = px.violin(df, x="sex", y="total_bill", color="smoker")
    fig.update_layout(template="plotly_dark")
    return fig.to_html(include_plotlyjs="require", full_html=True)

def scatterchart():
    N = 100000
    fig = go.Figure(data=go.Scattergl(
        x = np.random.randn(N),
        y = np.random.randn(N),
        mode='markers',
        marker=dict(
            color=np.random.randn(N),
            colorscale='Viridis',
            line_width=1
        )
    ))
    fig.update_layout(template="plotly_dark")
    return fig.to_html(include_plotlyjs="require", full_html=True)

def peta():
    df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_us_cities.csv')
    df.head()

    df['text'] = df['name'] + '<br>Population ' + (df['pop']/1e6).astype(str)+' million'
    limits = [(0,2),(3,10),(11,20),(21,50),(50,3000)]
    colors = ["royalblue","crimson","lightseagreen","orange","lightgrey"]
    cities = []
    scale = 5000

    fig = go.Figure()

    for i in range(len(limits)):
        lim = limits[i]
        df_sub = df[lim[0]:lim[1]]
        fig.add_trace(go.Scattergeo(
            locationmode = 'USA-states',
            lon = df_sub['lon'],
            lat = df_sub['lat'],
            text = df_sub['text'],
            marker = dict(
                size = df_sub['pop']/scale,
                color = colors[i],
                line_color='rgb(40,40,40)',
                line_width=0.5,
                sizemode = 'area'
            ),
            name = '{0} - {1}'.format(lim[0],lim[1])))

    fig.update_layout(template="plotly_dark",
            title_text = '2014 US city populations<br>(Click legend to toggle traces)',
            showlegend = True,
            geo = dict(
                scope = 'usa',
                landcolor = 'rgb(217, 217, 217)',
            )
        )

    return fig.to_html(include_plotlyjs="require", full_html=True)

config(theme='dark')
def main():
    session.set_env(title='My Chart!!', output_max_width='90%')
    put_grid([
        [span(put_markdown('## Section A'), col=3)],
        [put_markdown('### Chart 1'), put_markdown('### Chart 2'), put_markdown('### Chart 3')],
        [put_scope('haha'), put_scope('1-2'), put_scope('1-3')],
        [span(put_markdown('## Section B'), col=2, row=1), put_markdown('## Section C')],
        [put_scope('haha1'), put_scope('haha2'), put_scope('haha3')]
        #[span(put_row([
        #        put_select('x', help_text='X column', options=['a', 'b']),
        #        put_select('y', help_text='Y column', options=['x', 'y']),
        #        ]), col=2, row=1),
        #    None, 
        #],
        #[span(put_image(img_link), col=2, row=1), put_scope('2-3')],
    ], cell_widths='33% 33% 33%')

    with use_scope('1-2'):
        put_html(scatterchart())
    
    with use_scope('haha'):
        put_html(isochart())
    with use_scope('haha1'):
        put_html(gdp_chart('geo'))
    with use_scope('haha2'):
        put_html(peta())
    with use_scope('haha3'):
        put_html(meshchart())
        
    with use_scope('1-3'):
        put_html(gdp_chart('animation'))
        
    #with use_scope('2-3'):
    #    put_markdown(md)
    #    put_input('something', label='input something to show as a toast message')
    #    put_button('submit', onclick=lambda: toast(pin.something))


main()
    
