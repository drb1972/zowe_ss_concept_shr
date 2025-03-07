# streamlit run main.py
import streamlit as st
import zw

st.set_page_config(page_title="ZSSConcept", layout="wide")

# if 'first_time_main' not in st.session_state:
#     st.session_state.first_time_main = None
if 'refresh_profile' not in st.session_state:
    st.session_state.refresh_profile = True
if 'default_profile' not in st.session_state:
    st.session_state.default_profile = ''
if 'page_dict' not in st.session_state:
    st.session_state.page_dict = {}
if 'enter_defaults' not in st.session_state:
    st.session_state.enter_defaults = False

welcome = st.Page(
    "welcome/welcome.py", 
    title="Welcome"
)
zosmf_prof = st.Page(
    "zosmf/zosmf_prof.py", 
    title="Check zOSMF profiles"
)
zowe = st.Page(
    "zowe_command_builder/zowe_command.py",
    title="Zowe Command Builder"
)

welcome = [welcome]
zosmf   = [zosmf_prof]
zowe    = [zowe]

st.logo("images/Gafas-Turkas-6.png",size="large")

st.session_state.page_dict = {}
st.session_state.page_dict["Welcome"] = welcome
st.session_state.page_dict["zOSMF"]   = zosmf
st.session_state.page_dict["Zowe"]    = zowe

pg = st.navigation(st.session_state.page_dict)

#------------------- SIDEBAR ------------------------------------------------
with st.sidebar:
    with st.container(border=True):
        if st.session_state.refresh_profile==True:
            st.session_state.refresh_profile=False
            with st.spinner("Loading..."): st.session_state.default_profile = zw.list_config_defaults()
        st.write('Default Profiles')
        st.code(f'{st.session_state.default_profile}',wrap_lines = True, language='json') 
        
        col_def_prof1, col_def_prof2 = st.columns([1,1],vertical_alignment="top")
        
        with col_def_prof1:
            refresh_button=st.button("Refresh",
                    key='refresh',
                    )
            if refresh_button:
                st.session_state.refresh_profile=True
                # with st.spinner("Loading..."): st.session_state.default_profile = zw.list_config_defaults()
                st.rerun()

        with col_def_prof2:
            set_defaults_button=st.button("Set Defaults",
                    key='setdefaults',
                    )
            if set_defaults_button:
                @st.dialog("Select Default Values")
                def set_defaults():
                    # Split the input string into key-value pairs
                    pairs = st.session_state.default_profile.split()
                    # Extract keys that end with ':' and remove the ':'
                    keys = [pair.split(":")[0] for pair in pairs if pair.endswith(":")]
                    
                    # Create a selectbox for each extracted key (item before ':')
                    for item in keys:
                        st.selectbox(f'{item}',
                                     (x for x in st.session_state.my_profiles if item in x),
                                     key=item,
                                     index=None)
                    
                    if st.button("Submit"):
                        for item in keys:
                            value = st.session_state.get(item)
                            if value !=None:
                                command = f'zowe config set "defaults.{item}" "{value}" --global-config'
                                with st.spinner("Setting defaults..."): zw.execute_command(command)
                        with st.spinner("Refreshing defaults..."): st.session_state.default_profile = zw.list_config_defaults()

                        st.rerun()
                set_defaults()


    stop_button=st.button("Stop App",
            key='stop',
            )
    if stop_button:
        st.stop()  # Stops the execution of the app

pg.run()