def worldwide():
    countries = countries_names()

    chosen = st.multiselect('Countries', countries)

    st.text('Enter the range of days between the dates (if boths are set at 0, the range will be 7 days)')
    column = st.beta_columns(2)
    with column[0]:
        periodo_days = st.slider('Days', min_value=0, max_value=30)  
    with column[1]:
        periodo_months = st.slider('Months', min_value=0, max_value=12)  

    if chosen:

        periodo = periodo_days + periodo_months*30
        if periodo == 0 or periodo > len(data_global[0])-4:
            periodo = 7
        
        #Buscar alguna forma de que no tenga que poner las collections aqui
        cases = countries_data("covid", chosen)
        deaths =countries_data("deaths", chosen)
        recovered = countries_data("recovered", chosen)

        for countries in chosen:
            st.markdown(f"\n<h3 style='text-align:center; background-color:orange;'><b>{countries}</b></h3>", unsafe_allow_html=True)
            data_countries_columns = st.beta_columns(3)
            with data_countries_columns[0]:
                st.markdown("<h2 style='text-align:center; background-color:blue;'><b>Cases</b></h2>", unsafe_allow_html=True)
                num_cases = list(cases[cases['Country/Region'] == countries].values[0])
                st.markdown(f"<p style='text-align:center'><b>{num_cases[1]}</b></p>", unsafe_allow_html=True)
            
            with data_countries_columns[1]:
                st.markdown("<h2 style='text-align:center; background-color:red;'><b>Deaths</b></h2>", unsafe_allow_html=True)
                num_deaths = list(deaths[deaths['Country/Region'] == countries].values[0])
                st.markdown(f"<p style='text-align:center'><b>{num_deaths[1]}</b></p>", unsafe_allow_html=True)

            with data_countries_columns[2]:
                st.markdown("<h2 style='text-align:center; background-color:green;'><b>Recovered</b></h2>", unsafe_allow_html=True)
                num_recovered = list(recovered[recovered['Country/Region'] == countries].values[0])
                st.markdown(f"<p style='text-align:center'><b>{num_recovered[1]}</b></p>", unsafe_allow_html=True)

        plt = covid_cases_graph(data_global, periodo)
        st.pyplot(plt)
        for country in data_global:
            country.pop("_id")

        geospatial = geospatial_data(data_global)
        geospatial_map(geospatial)

    cols = st.beta_columns((2,1,2))
    with cols[1]:
        if st.button('Download PDF'):
            pdf = FPDF()
            pdf.add_page(orientation="L", format="A3")
            plt.savefig("Cases_dates.jpg")
            pdf.image("./Cases_dates.jpg", w=400, h=260)
            pdf.add_page()

            covid_cases_data = pd.DataFrame(data_global).drop(columns=["Lat", "Long"])
            num_case_date = []

            columns = [column for column in covid_cases_data.columns[1::periodo]]
            columns.insert(0,covid_cases_data.columns[0])
            for country in covid_cases_data.values: 
                cases = [int(case) for case in country[1::periodo]]
                cases.insert(0,country[0])
                num_case_date.append(cases)
            
            pdf.set_font('Arial', 'BIU', 16)
            pdf.write(16,"Data in JSON format\n")

            pdf.set_font('Arial', '', 9)
            for country in range(len(num_case_date)):
                if country == 0:
                    pdf.write(5, "\n{")
                pdf.write(5, "\n    {\n")
                for position in range(len(columns)):
                    if position == len(columns)-1:
                        pdf.write(5, f'        "{columns[position]}" : "{num_case_date[country][position]}"\n')
                    else:
                        pdf.write(5, f'        "{columns[position]}" : "{num_case_date[country][position]}",\n')
                if country == len(num_case_date)-1:
                    pdf.write(5, "    }\n")
                    pdf.write(5, "}\n")
                else:
                    pdf.write(5, "    },")
            
            pdf.output("Covid_Cases_Dashboard.pdf",dest="F")