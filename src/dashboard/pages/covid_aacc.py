from api import community_names, community_data, community_coord, selected_data
from utils.show_functions import *
from utils.process_data import change_key_name

def aacc():
    communities_names = community_names()

    chosen = st.multiselect('Covid at the Autonomous Community in Spain', communities_names)
    
    vac_death_show = st.select_slider("Select if you prefer to show covid data, vaccinated data or both",["deceased", "vaccinated", "both"])

    if chosen:
        data = selected_data(chosen, vac_death_show, ["Lat","Long"])

        st.dataframe(data)
        geospatial_data = community_coord(chosen)
        geospatial_map(change_key_name(geospatial_data, "Community", "Name"), [40.43755797071899, -3.710357240720364])