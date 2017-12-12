import branca, folium, pandas as pd, os
from jinja2 import Environment, FileSystemLoader
fpath = os.path.dirname(os.path.realpath(__file__))

def colors(val):
    if val < 50:
        return 'rgba(77,175,78,0.8)'
    elif 50 < val < 99:
        return 'rgba(248,152,29,0.8)'
    elif val > 100:
        return 'rgba(239,68,56,0.9)'


def create_html(s,location):
    x_dict = {}
    y_dict = {}
    z_dict = {}

    # For x
    x_dict['val'] = round(float(s.X),2)
    x_dict['color'] = colors(float(s.X))

    # For y
    y_dict['val'] = round(float(s.Y),2)
    y_dict['color'] = colors(float(s.Y))

    # For z
    z_dict['val'] = round(float(s.Z),2)
    z_dict['color'] = colors(float(s.Z))

    final = {'X':x_dict,'Y':y_dict,'Z':z_dict}

    X = []
    color = []
    for k in sorted(final.keys(),reverse=True):
        X.append(final[k]['val'])
        color.append(final[k]['color'])


    # create the jinja env
    env = Environment(loader=FileSystemLoader(os.path.join(fpath, 'templates')))
    template = env.get_template('sensor.html')
    output_from_parsed_template = template.render(location = location,data=X,color=color).encode('utf8')
    with open("my_new_file.html", "wb") as fh:
        fh.write(output_from_parsed_template)
    return output_from_parsed_template


def read_series(csv):
    s = pd.Series.from_csv(csv)
    return s

def make_map():
    csvloc = 'csv'
    dirr = os.listdir(csvloc)
    df = pd.read_csv('loc.csv')
    m = folium.Map(location = [14.6760,121.0437], zoom_start=12)

    for k,v in df.iterrows():
        # data = pd.read_csv(os.path.join(csvloc,v.tag+'.csv'))
        s = read_series(os.path.join(csvloc,v.tag+'.csv'))
        html = create_html(s,v['name'])
        iframe = branca.element.IFrame(html=html,width=490,height=400)
        popup = folium.Popup(iframe,max_width=2650)


        # html = """
        #         <h5><strong> {} </strong></h5>
        #        """.format(v['name'])
        if 't' in list(s.triggered):
            folium.Marker(
                location = [v.lat,v.lon],
                popup = popup,
                icon = folium.Icon(color='red')
            ).add_to(m)
        else:
            folium.Marker(
                location = [v.lat,v.lon],
                popup = popup,
                icon = folium.Icon(color='green')
            ).add_to(m)

    m.save('templates/test.html')
    print "Done making map..."

if __name__ == '__main__':
    make_map()