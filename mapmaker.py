import branca, folium, pandas as pd, os


def make_map():
	csvloc = 'csv'
	dirr = os.listdir(csvloc)
	df = pd.read_csv('loc.csv')
	m = folium.Map(location = [14.6760,121.0437], zoom_start=12)

	for k,v in df.iterrows():
	    data = pd.read_csv(os.path.join(csvloc,v.tag+'.csv'))
	    html = """
	            <h5> {} </h5>
	           """.format(v['name'])
	    if 't' in list(data.triggered):
	        folium.Marker(
	            location = [v.lat,v.lon],
	            popup = html,
	            icon = folium.Icon(color='red')
	        ).add_to(m)
	    else:
	        folium.Marker(
	            location = [v.lat,v.lon],
	            popup = html,
	            icon = folium.Icon(color='green')
	        ).add_to(m)

	m.save('templates/test.html')

if __name__ == '__main__':
	make_map()