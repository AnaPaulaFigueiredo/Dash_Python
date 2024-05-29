#O dash é dividido em duas grander partes 
#Layout : O que vemos 
#Basics Callbacks: Funcionalidade do que vemos 


#########
#Layout
#########

from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import dash_bootstrap_components as dbc


app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY]) #Iniciando o app 

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.read_csv(r"..\Dados\sale.csv")
lojas = list(df['Store'].unique())
lojas.append('Todas Lojas')

dept_venda_todos = df.groupby(['Dept'])['Weekly_Sales'].sum().reset_index().sort_values('Weekly_Sales', ascending = False)
dept_venda_todos['Dept'] = dept_venda_todos['Dept'].astype(str)
dept_venda_todos['Acumulado'] = 100*dept_venda_todos['Weekly_Sales'].cumsum()/ dept_venda_todos['Weekly_Sales'].sum()

df['IsHoliday'] = df['IsHoliday'].replace({True : 'Feriado', False : 'Dia normal'})

#Métricas
total_departamentos = df['Dept'].nunique() 
total_vendas = df['Weekly_Sales'].sum()

#Gráficos
fig_hist = px.line(df, x="Date", y="Weekly_Sales", 
                   color_discrete_sequence=['#3D30EC'])

fig_box = px.box(df, 
                     x = "IsHoliday", y = "Weekly_Sales", 
                     color = "IsHoliday", 
                     title = "Vendas em feriados e dias normais",
                     color_discrete_sequence = ['#dfec30','#3D30EC']
                     )    
#Pareto 
fig_pareto = make_subplots(specs=[[{"secondary_y": True}]])
fig_pareto.add_trace(go.Bar(x= dept_venda_todos['Dept'], 
                                y = dept_venda_todos['Weekly_Sales'],
                                name="Total Vendido",
                                marker=dict(color= '#3D30EC') #Dá a cor as barras
                              ), 
                        secondary_y=False )
    
fig_pareto.add_trace(go.Scatter(x= dept_venda_todos['Dept'], 
                                    y = dept_venda_todos['Acumulado'], 
                                    name="% Acumulado", 
                                    line=go.scatter.Line(color= "#dfec30"), #Dá a cor a linha
                                    ), 
                        secondary_y= True),
   
            
fig_pareto.update_layout(title_text="Vendas por departamento e '%' acumulado ",
                             title_x = .5, #Centralizando o título
                             paper_bgcolor = '#242424', #Cor do gráfico
                             plot_bgcolor = '#242424', #Colocando o fundo do gráfico com a mesma cor
                             autosize = True, #Preenche o tamanho do gráfico no conteiner
                             margin = go.layout.Margin(l = 0, r=0, b=0), #definindo margens, no caso sem margens
                             showlegend = True, #Mostrar ou não Legenda 
                             template = "plotly_dark", 
                             legend=dict(
                                         title=None, 
                                         orientation="h", 
                                         y=1, 
                                         yanchor="bottom", 
                                         x=0.5, 
                                         xanchor="center"
    )
                             )
    
fig_pareto.update_xaxes(title_text="Departamentos")
fig_pareto.update_yaxes(title_text="Valor Vendas", secondary_y=False)
fig_pareto.update_yaxes(title_text="Percentual", secondary_y=True)

# #Estilo gráfico 
fig_hist.update_layout( title_x = .5, #Centralizando o título
                            paper_bgcolor = '#242424', #Cor do gráfico
                            plot_bgcolor = '#242424', #Colocando o fundo do gráfico com a mesma cor
                            #foregroundColor = '#242424', #Cor da grade
                            autosize = True, #Preenche o tamanho do gráfico no conteiner
                            margin = go.layout.Margin(l = 0, r=0, b=0), #definindo margens,no caso sem margens
                            template = "plotly_dark" 
                        )
fig_hist.update_yaxes(title_text="Valor Vendas")
fig_hist.update_xaxes(title_text=None)
    



fig_box.update_layout( title_x = .5, #Centralizando o título
                           paper_bgcolor = '#242424', #Cor do gráfico
                           plot_bgcolor = '#242424', #Colocando o fundo do gráfico com a mesma cor
                           autosize = True, #Preenche o tamanho do gráfico no conteiner
                           margin = go.layout.Margin(l = 0, r=0, b=0), #definindo margens, no caso sem margens
                           showlegend = False, #Mostrar ou não Legenda
                           template = "plotly_dark"
                         )
fig_box.update_yaxes(title_text="Valor Vendas")
fig_box.update_xaxes(title_text=None)


# fig_pareto.update_layout(
#     #title_text="Vendas por departamento e Percentual representante",
#     paper_bgcolor = '#242424', #Cor do gráfico
#     plot_bgcolor = '#242424', #Colocando o fundo do gráfico com a mesma cor
#     autosize = False, #Preenche o tamanho do gráfico no conteiner
#     margin = go.layout.Margin(l = 0, r=0, b=0), #definindo margens, no caso sem margens
#     showlegend = False,
# )

#  #Lista de opções 
lista_opcoes = dcc.Dropdown(lojas, 
                 value = 'Todas Lojas',#valor padrão de escolha
                 id='lista-loja', 
                 searchable = True, #Habilita uma lista de pesquisa
                  style = {'backgroundColor': 'white',  #Cor do fundo da caixa
                         'color': 'black', #Cor da Letra
                         },      
                 )  
    


##Layout
app.layout = dbc.Container(
    [
       
        #Cabeçalho 
        dbc.Row([
            html.Div([
                html.Img(id='logo_walmart', src =app.get_asset_url("logoWalmart.png"), height = 50), #Busca a imagem dentro da pasta assets
                html.H3('Análise descritiva das vendas nas lojas do Walmart ''', id = 'subtitulo'),
                html.Hr(), #Linha
                    ]),
    ]),

    #Começa template
         dbc.Row([ 
             #Adicionando a lista de opçoes
                 dbc.Col([
                         lista_opcoes,
                    #Na mesma coluna da lista em outra linha adicionando os cartões    
                        dbc.Row([
                            dbc.Col([
                                     dbc.Card([
                                        dbc.CardBody([
                                        html.Span("Departamentos"),
                                        html.H3(total_departamentos, 
                                                id= 'total_departamentos_loja', 
                                                style={"color": '#3D30EC'}
                                                ), # O que vai dentro do card
                                        html.Span("Quantidade"),
                                                     ]),
                                            ], 
                                        color= "light", 
                                        outline = True, 
                                        style={'margin-top':'10px',
                                                'color': '#FFFFFF'}
                                            ),
                                     ], width=4), #Tamanho da coluna,

                            dbc.Col([
                                     dbc.Card([
                                        dbc.CardBody([
                                        html.Span("Vendas", className='title'),
                                        html.H3(f'R$ {float(total_vendas): .2f}',
                                                style={"color": '#dfec30'}, 
                                                id= 'total_vendido'
                                                ), # O que vai dentro do card
                                        html.Span("Total", className="card-subtitle"),
                                                     ]),
                                            ], 
                                    color= "light", outline = True, style={'margin-top':'10px',
                                                                       'color': '#FFFFFF'}
                                                ),
                                     ], width=8)
                                         
                        
                        
                        ]),
                    #Adicionando o gráfico de pareto    
                    dbc.Row([dbc.Col([
                                    # dcc.Loading( #Coloca um loading
                                    #     id = 'loading-pareto',
                                    #     children = [
                                            dcc.Graph(id = "fig-pareto",
                                                    figure = fig_pareto,
                                                    style ={'height': '80vh'}
                                                    )
                                        # ],
                                        # overlay_style={"visibility":"visible",
                                        #                 "filter": "blur(2px)"},
                                        # type="circle"
                                                  #)
                                    ])
                            ])
                            
                    ], 
                    width=5)
            ,
        
                dbc.Col([
                    #Colocando os gráficos com loading 
                    # dcc.Loading(id = "loading-hist", 
                    #             children=[
                                dcc.Graph(id = "fig-hist", 
                                          figure = fig_hist,
                                          style = {'height': '50vh'}), # height': '50vh: ocupa 50% da tela na vertical
                                          #],
                                # overlay_style={"visibility":"visible",
                                #                 "filter": "blur(2px)"},
                                # type="circle" ),

                    # dcc.Loading(id = "loading-box", 
                    #             children=[
                                    dcc.Graph(id = "fig-box", 
                                              figure = fig_box, 
                                              style = {'height': '50vh'})
                                #           ],
                                # overlay_style={"visibility":"visible",
                                #                 "filter": "blur(2px)"},
                                #         type="circle" ),
                        ]),

             ]),
     

    ])


   
## Iteratividade - função de retorno

@app.callback( #Quem será modificado (editado) - A ordem importa
              Output("total_departamentos_loja", "children"),
              Output("total_vendido", "children"),
              Output("fig-hist", "figure"), 
              Output("fig-box", "figure"),
              Output("fig-pareto", "figure")
              ,
             [#Cara que modifica
              Input("lista-loja", "value")
              ]
              )


def update_output(value):
    if value == "Todas Lojas":
         df_selecao = df.copy()
         dept_venda_todos = df_selecao.groupby(['Dept'])['Weekly_Sales'].sum().reset_index().sort_values('Weekly_Sales', ascending = False)
         dept_venda_todos['Dept'] = dept_venda_todos['Dept'].astype(str)
         dept_venda_todos['Acumulado'] = 100*dept_venda_todos['Weekly_Sales'].cumsum()/ dept_venda_todos['Weekly_Sales'].sum()
    else:
        df_selecao = df[df['Store'] == value]
        dept_venda_todos = df_selecao.groupby(['Dept'])['Weekly_Sales'].sum().reset_index().sort_values('Weekly_Sales', ascending = False)
        dept_venda_todos['Dept'] = dept_venda_todos['Dept'].astype(str)
        dept_venda_todos['Acumulado'] = 100*dept_venda_todos['Weekly_Sales'].cumsum()/ dept_venda_todos['Weekly_Sales'].sum()
       
    #Métricas
    total_departamentos = df_selecao['Dept'].nunique() 
    total_vendas = df_selecao['Weekly_Sales'].sum()

    ##Desenhando os gráficos 

    #Histograma
    fig_hist = px.line(df_selecao, x="Date", y="Weekly_Sales", 
                       template= "simple_white",
                       title = "Histórico de vendas",
                       color_discrete_sequence=['#3D30EC'])
    #Estilo gráfico 
    fig_hist.update_layout( title_x = .5, #Centralizando o título
                            paper_bgcolor = '#242424', #Cor do gráfico
                            plot_bgcolor = '#242424', #Colocando o fundo do gráfico com a mesma cor
                            #foregroundColor = '#242424', #Cor da grade
                            autosize = True, #Preenche o tamanho do gráfico no conteiner
                            margin = go.layout.Margin(l = 0, r=0, b=0), #definindo margens,no caso sem margens
                            template = "plotly_dark" 
                        
                           )
    fig_hist.update_yaxes(title_text="Valor Vendas")
    fig_hist.update_xaxes(title_text=None)
    

    #Boxplot
    fig_box = px.box(df_selecao, 
                     x = "IsHoliday", y = "Weekly_Sales", 
                     color = "IsHoliday", 
                     title = "Vendas em feriados e dias normais",
                     color_discrete_sequence = ['#dfec30','#3D30EC']
                     )
    fig_box.update_layout( title_x = .5, #Centralizando o título
                           paper_bgcolor = '#242424', #Cor do gráfico
                           plot_bgcolor = '#242424', #Colocando o fundo do gráfico com a mesma cor
                           autosize = True, #Preenche o tamanho do gráfico no conteiner
                           margin = go.layout.Margin(l = 0, r=0, b=0), #definindo margens, no caso sem margens
                           showlegend = False, #Mostrar ou não Legenda
                           template = "plotly_dark"
                         )
    fig_box.update_yaxes(title_text="Valor Vendas")
    fig_box.update_xaxes(title_text=None)

    
    #Pareto 
    fig_pareto = make_subplots(specs=[[{"secondary_y": True}]])
    fig_pareto.add_trace(go.Bar(x= dept_venda_todos['Dept'], 
                                y = dept_venda_todos['Weekly_Sales'],
                                name="Total Vendido",
                                marker=dict(color= '#3D30EC') #Dá a cor as barras
                              ), 
                        secondary_y=False )
    
    fig_pareto.add_trace(go.Scatter(x= dept_venda_todos['Dept'], 
                                    y = dept_venda_todos['Acumulado'], 
                                    name="% Acumulado", 
                                    line=go.scatter.Line(color= "#dfec30"), #Dá a cor a linha
                                    ), 
                        secondary_y= True),
   
    # fig_pareto.update_traces(marker_color=['rgb(158,202,225)', '#3D30EC'], marker_line_color='rgb(8,48,107)',
    #               marker_line_width=1.5, opacity=0.6)
            
    fig_pareto.update_layout(title_text="Vendas por departamento e '%' acumulado ",
                             title_x = .5, #Centralizando o título
                             paper_bgcolor = '#242424', #Cor do gráfico
                             plot_bgcolor = '#242424', #Colocando o fundo do gráfico com a mesma cor
                             autosize = True, #Preenche o tamanho do gráfico no conteiner
                             margin = go.layout.Margin(l = 0, r=0, b=0), #definindo margens, no caso sem margens
                             showlegend = True, #Mostrar ou não Legenda 
                             template = "plotly_dark", 
                             legend=dict(
                                         title=None, 
                                         orientation="h", 
                                         y=1, 
                                         yanchor="bottom", 
                                         x=0.5, 
                                         xanchor="center"
    )
                             )
    
    fig_pareto.update_xaxes(title_text="Departamentos")
    fig_pareto.update_yaxes(title_text="Valor Vendas", secondary_y=False)
    fig_pareto.update_yaxes(title_text="Percentual", secondary_y=True)
    
    return (total_departamentos, 
            f'R$ {float(total_vendas): .2f}', 
            fig_hist, 
            fig_box,
            fig_pareto
            )

if __name__ == '__main__':
    app.run(debug=True)