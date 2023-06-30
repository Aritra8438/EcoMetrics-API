from plotly.subplots import make_subplots
import plotly.express as px
import plotly.graph_objects as go

def create_pie(json_response, num):
        res = []
        for obj in json_response:
            if(obj['country']!='World' and obj['country']!='Less developed regions'):
                res.append((obj['population'], obj['country']))
        result = res[:num]
        values=[]
        labels=[]
        for item in result:
            values.append(item[0])
            labels.append(item[1]) 
        
        fig = make_subplots(rows=1, cols=2, specs=[[{"type": "pie"}, {"type": "pie"}]], 
                            subplot_titles=[ "Top {} countries".format(num), "Bottom {} countries".format(num)])
                                            
 
        fig.add_trace(go.Pie(values=values, labels=labels, name="Least Populated {} countries".format(num)),row=1, col=1)           
        res.sort(reverse=True)    
        result = res[:num]
        values=[]
        labels=[]
        for item in result:
            values.append(item[0])
            labels.append(item[1])
        fig.add_trace(go.Pie(values=values, labels=labels, name ="Most Populated {} countries".format(num)), row=1, col=2)      
        return fig.to_html(full_html=False) 
    

def create_bar(json_response):
        year = []
        country = []
        population = []
        
        dict = {}
        for obj in json_response:
            country.append(obj['country'])
            year.append(obj['year'])
            population.append(obj['population'])
        dict['country']=country    
        dict['year']=year    
        dict['population']=population
        # fig = px.bar(dict, x='country', y='population', color="year", barmode="group")
        fig = px.bar(dict, x='country', y='population', color="country",
                     animation_frame="year", animation_group="country", range_y=[0,2000000000],
                     barmode="group")
        
        
        return fig.to_html(full_html=False) 


def create_fig(country_year,country_pop):
    fig = go.Figure()
    layout = go.Layout(
    title='Population vs Year Index',
    xaxis=dict(title='Year'),
    yaxis=dict(title='Population')
    )
    for country in country_year :
        fig.add_trace(go.Scatter(x=country_year[country], y=country_pop[country],mode="lines", 
                                 name=country))
    fig.update_layout(layout)    
    return fig.to_html(full_html=False)
    
     