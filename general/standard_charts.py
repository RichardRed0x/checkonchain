#Establish typical charts

from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default = "browser"

#Establish a standard set of chart features in __init__
# Font type
# Font sizes
# background colors
# Gridlines


#fig=check_standard_charts(
#       title_data,     =['Chart Title','x-axis', 'Y-Axis-1', 'Y-Axis-2']
#       range_data,     =[[x1,x2],[y1_1,y1_2],[y2_1,y2_2]]
#       type_data,      =['linear','log','log']
#       autorange_data) =[True,True,False] - overrides range

#.subplot_lines_singleaxis(
#.subplot_lines_doubleaxis(
#        loop_data,     =[[a,b,c],[d,e]] where a-c are primary plots, d-e secondary plots
#        x_data,        =[a,b,c,d,e]
#        y_data,        =[a,b,c,d,e]
#        name_data,     =[a,b,c,d,e]
#        color_data,    =[a,b,c,d,e]
#        dash_data,     =[a,b,c,d,e] ('solid','dash','dot')
#        width_data,    =[a,b,c,d,e]
#        opacity_data,  =[a,b,c,d,e]
#        legend_data    =[a,b,c,d,e] (boolean, show legend or not)
#        )


class check_standard_charts():

    def __init__(self):
        self._background = 'rgb(20,20,20)'
        self._font = 'Raleway'
        self._titlesize = 26
        self._legendsize = 16
        self._axesfontsize = 20
        self._tickfontsize = 16
        self._gridcolor = 'rgb(50,50,50)'
        self._gridwidth = 0.1
        self._zerolinecolor = 'rgb(50,50,50)'

    def add_traces_lines():
        return fig

    def basic_chart(self,x_data,y_data,name_data,loop_data,title_data,type_data):
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        for i in loop_data[0]:
            fig.add_trace(go.Scatter(
                x=x_data[i], 
                y=y_data[i],
                mode='lines',
                name=name_data[i]),
                secondary_y=False)

        for i in loop_data[1]:
            fig.add_trace(go.Scatter(
                x=x_data[i], 
                y=y_data[i],
                mode='lines',
                name=name_data[i]),
                secondary_y=True)
        # Add figure title
        fig.update_layout(title_text=title_data[0])
        fig.update_xaxes(title_text=title_data[1],type=type_data[0])
        fig.update_yaxes(title_text=title_data[2],type=type_data[1],secondary_y=False)
        fig.update_yaxes(title_text=title_data[3],type=type_data[2],secondary_y=True)
        fig.update_layout(template="plotly_dark")
        return fig


    def subplot_lines_singleaxis(
        self,
        title_data, range_data ,autorange_data ,type_data,
        loop_data,x_data,y_data,name_data,color_data,
        dash_data,width_data,opacity_data,legend_data,
        ):

        fig = make_subplots(specs=[[{"secondary_y": False}]])
        """#######  Add Traces   #######"""
        for i in loop_data[0]:
            fig.add_trace(go.Scatter(
                mode='lines',
                x=x_data[i], 
                y=y_data[i],
                name=name_data[i],
                opacity=opacity_data[i],
                showlegend=legend_data[i],
                line=dict(
                    width=width_data[i],
                    color=color_data[i],
                    dash=dash_data[i]
                    )),
                secondary_y=False)        
        
                
        """#######  Title Block   #######"""
        fig.update_layout(
            paper_bgcolor=self._background,
            plot_bgcolor=self._background,
            autosize=True,            
            title=go.layout.Title(
                text=title_data[0],
                x=0.5, 
                xref='paper',
                font=dict(
                    family=self._font,
                    size = self._titlesize
                )),
            legend=dict(
                yanchor='middle',
                y=0.5,
                font=dict(
                    family=self._font,
                    size=self._legendsize
                )))
        
        """#######  X-Axis   #######"""
        fig.update_xaxes(
            title_text=title_data[1],
            type=type_data[0],
            range=range_data[0],
            title_font=dict(
                family=self._font,
                size=self._axesfontsize
                ),
            tickfont=dict(
                family=self._font,
                size=self._tickfontsize
                ),
            gridcolor=self._gridcolor,
            gridwidth=self._gridwidth,
            zerolinecolor=self._zerolinecolor
            )
        fig.update_xaxes(autorange=autorange_data[0]) #override range
        

        """#######  Y-Axis-1   #######"""
        fig.update_yaxes(
            title_text=title_data[2],
            type=type_data[1],
            range=range_data[1],
            title_font=dict(
                family=self._font,
                size=self._axesfontsize
                ),
            tickfont=dict(
                family=self._font,
                size=self._tickfontsize
                ),
            gridcolor=self._gridcolor,
            gridwidth=self._gridwidth,
            zerolinecolor=self._zerolinecolor,
            secondary_y=False
            )
        fig.update_yaxes(autorange=autorange_data[1],secondary_y=False) #override range
        
        fig.update_layout(template="plotly_dark")
        return fig

    def subplot_lines_doubleaxis(self,
        title_data, range_data ,autorange_data ,type_data,
        loop_data,x_data,y_data,name_data,color_data,
        dash_data,width_data,opacity_data,legend_data):

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.update_layout(template="plotly_dark")
        
        """#######  Add PRIMARY Traces   #######"""
        for i in loop_data[0]:
            fig.add_trace(go.Scatter(
                x=x_data[i], 
                y=y_data[i],
                name=name_data[i],
                opacity=opacity_data[i],
                showlegend=legend_data[i],
                line=dict(
                    width=width_data[i],
                    color=color_data[i],
                    dash=dash_data[i]
                    )),
                secondary_y=False)

        """#######  Add SECONDARY Traces   #######"""
        for i in loop_data[1]:
            fig.add_trace(go.Scatter(
                x=x_data[i], 
                y=y_data[i],
                name=name_data[i],
                opacity=opacity_data[i],
                showlegend=legend_data[i],
                line=dict(
                    width=width_data[i],
                    color=color_data[i],
                    dash=dash_data[i]
                    )),
                secondary_y=True)
                
        """#######  Title Block   #######"""
        fig.update_layout(
            paper_bgcolor=self._background,
            plot_bgcolor=self._background,
            autosize=True,            
            title=go.layout.Title(
                text=title_data[0],
                x=0.5, 
                xref='paper',
                font=dict(
                    family=self._font,
                    size = self._titlesize
                )),
            legend=dict(
                yanchor='middle',
                y=0.5,
                font=dict(
                    family=self._font,
                    size=self._legendsize
                )))

        """#######  X-Axis   #######"""
        fig.update_xaxes(
            title_text=title_data[1],
            type=type_data[0],
            range=range_data[0],
            title_font=dict(
                family=self._font,
                size=self._axesfontsize
                ),
            tickfont=dict(
                family=self._font,
                size=self._tickfontsize
                ),
            gridcolor=self._gridcolor,
            gridwidth=self._gridwidth,
            zerolinecolor=self._zerolinecolor
            )
        fig.update_xaxes(autorange=autorange_data[0]) #override range

        """#######  Y-Axis-1   #######"""
        fig.update_yaxes(
            title_text=title_data[2],
            type=type_data[1],
            range=range_data[1],
            title_font=dict(
                family=self._font,
                size=self._axesfontsize
                ),
            tickfont=dict(
                family=self._font,
                size=self._tickfontsize
                ),
            gridcolor=self._gridcolor,
            gridwidth=self._gridwidth,
            zerolinecolor=self._zerolinecolor,
            secondary_y=False
            )
        fig.update_yaxes(autorange=autorange_data[1],secondary_y=False) #override range
        
        """#######  Y-Axis-2   #######"""
        fig.update_yaxes(
            title_text=title_data[3],
            type=type_data[2],
            range=range_data[2],
            title_font=dict(
                family=self._font,
                size=self._axesfontsize
                ),
            tickfont=dict(
                family=self._font,
                size=self._tickfontsize
                ),
            gridcolor=self._gridcolor,
            gridwidth=self._gridwidth,
            zerolinecolor=self._zerolinecolor,
            secondary_y=True
            )
        fig.update_yaxes(autorange=autorange_data[2],secondary_y=True) #override range
        
        return fig




















#loop_data = [[0,1],[2]]
#x_data = [[0,1,2,3,4,5],[0,1,2,3,4,5],[0,1,2,3,4,5]]
#y_data = [[0,1,2,3,4,5],[4,5,0,5,9,5],[-4,-5,0,-5,-9,-5]]
#name_data = ['Bitcoin Market Cap','tap2','secondary']
#color_data = ['rgb(237, 109, 71)','rgb(237, 109, 71)','rgb(237, 109, 71)' ]
#dash_data = ['solid','dash','solid']
#width_data = [2,2,2]
#opacity_data = [1,0.5,1]
#legend_data = [True,True,True]
#title_data = [
#    '<b>Market Capitalisation vs Supply Mined</b>',
#    '<b>Coin Supply Issued</b>',
#    '<b>Coin Market Cap</b>',
#    'secondary Y'
#]
#type_data = ['linear','linear','linear']
#range_data = [[-10,10],[-5,12],[-10,20]]
#autorange_data = [False,False,False]
#
#
#
#fig=check_standard_charts(
#    title_data,
#    range_data,
#    type_data,
#    autorange_data
#    ).subplot_lines_singleaxis(
#        loop_data,
#        x_data,
#        y_data,
#        name_data,
#        color_data,
#        dash_data,
#        width_data,
#        opacity_data,
#        legend_data
#        ).show()
#
#fig=check_standard_charts(
#    title_data,
#    range_data,
#    type_data,
#    autorange_data
#    ).subplot_lines_doubleaxis(
#        loop_data,
#        x_data,
#        y_data,
#        name_data,
#        color_data,
#        dash_data,
#        width_data,
#        opacity_data,
#        legend_data
#        )










