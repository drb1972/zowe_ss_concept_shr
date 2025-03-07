import streamlit as st
import time
import zw

#--------------------- zosmf_list - .zosmf profiles in my config ------------- 
if 'zosmf_list' not in st.session_state:
    all_profiles_list = []
    zosmf_list=[]                                 
    ssh_list=[]
    zftp_list=[]
    tso_list = []
    with st.spinner("Loading..."): sto, ste, rc = zw.list_config_profiles()
    if rc == 0:
        sto=sto.split('\n')
        all_profiles_list.extend(x for x in sto)
        zosmf_list.extend(x for x in sto if '.zosmf' in x)
        zosmf_list.sort()
        ssh_list.extend(x for x in sto if '.ssh' in x)
        ssh_list.sort()
        zftp_list.extend(x for x in sto if '.zftp' in x)
        zftp_list.sort()
        tso_list.extend(x for x in sto if '.tso' in x)
        tso_list.sort()
    else:
        st.write('sto: ',sto)
        st.write('ste: ',ste)
        st.write('rc:  ',rc)

    st.session_state.all_profiles_list=all_profiles_list    
    st.session_state.zosmf_list=zosmf_list
    st.session_state.ssh_list=ssh_list
    st.session_state.zftp_list=zftp_list
    st.session_state.tso_list=tso_list

if 'my_profiles' not in st.session_state:
    with st.spinner("Loading..."): sto, ste, rc = zw.list_config_profiles()
    if rc == 0:
        st.session_state.my_profiles = sto.split()
    else:
        st.write('sto: ',sto)
        st.write('ste: ',ste)
        st.write('rc:  ',rc)
#----------------------------------------------------------------------------- 


st.title(f'Welcome')

with st.container(border=True,key='container1'):
    welcome_message1 = """Welcome to the Zowe Self Service Concept Portal. """ 
    welcome_message2 = """Please, select the utility you want to use from the left sidebar. """
    welcome_message3 = """To stop the app, click the 'Stop App' button in the sidebar. """

def stream_data1():
    for word in welcome_message1.split(" "):
        yield word + " "
        time.sleep(0.02)
def stream_data2():
    for word in welcome_message2.split(" "):
        yield word + " "
        time.sleep(0.02)
def stream_data3():
    for word in welcome_message3.split(" "):
        yield word + " "
        time.sleep(0.02)


st.write_stream(stream_data1)
st.write_stream(stream_data2)
st.write_stream(stream_data3)


with st.container(border=True,key='global_variables'):
    st.write('General Info')

    st.code('ZOWE_SHOW_SECURE_ARGS = true')

    with st.expander("My Profiles"):
        st.code('''
                - Auth login/logout: --base-p lpar_apiml
                - Connect via zosmf: --zosmf-p lpar.zosmf
                - Connect via JWT:   --zosmf-p lpar_apiml.zosmf
                - Connect via SSH:   --ssh-p lpar.shh
                - Connect via zftp:  --zftp-p lpar.zftp
                - Connect via tso:   --tso-p lpar.tso

                This shape:

                {
                "$schema": "./zowe.schema.json",
                "profiles": {
                    "my_lpar": {
                        "properties": {
                            "host": "my_lpar.lvn.broadcom.net"
                        },
                        "secure": [
                            "user",
                            "password"
                        ],
                        "profiles": {
                            "zosmf": {
                                "type": "zosmf",
                                "properties": {
                                    "port": 1443
                                }
                            },
                            "ssh": {
                                "type": "ssh",
                                "properties": {
                                    "port": 22
                                }
                            },
                            "zftp": {
                                "type": "zftp",
                                "properties": {
                                    "port": 21
                                }
                            },
                            "tso": {
                                "type": "tso",
                                "properties": {
                                    "account": "IZUACCT",
                                    "codePage": "1047",
                                    "logonProcedure": "IZUFPROC"
                                }
                            }
                        }
                    },
                    "my_lpar_apiml": {
                        "properties": {
                            "host": "my_lpar.lvn.broadcom.net",
                            "port": 7554
                        },
                        "profiles": {
                            "zosmf": {
                                "type": "zosmf",
                                "properties": {
                                    "basePath": "/ibmzosmf/api/v1",
                                    "tokenType": "apimlAuthenticationToken",
                                    "baseProfile": "hey_Joe"
                                }
                            }
                        },
                        "secure": []
                    },
                "defaults": {
                    "zosmf": "my_lpar.zosmf",
                    "ssh": "my_lpar.ssh",
                    "zftp": "my_lpar.zftp",
                    "tso": "my_lpar.tso"
                },
                "autoStore": true
}
                ''')

    st.write('Global variables')

    with st.expander("st.session_state.all_profiles_list - All Profiles"):
        st.code(st.session_state.all_profiles_list)

    with st.expander("st.session_state.zosmf_list - Profiles with string 'zosmf'"):
        st.code(st.session_state.zosmf_list)

    with st.expander("st.session_state.ssh_list - Profiles with string 'ssh'"):
        st.code(st.session_state.ssh_list)

    with st.expander("st.session_state.zftp_list - Profiles with string 'zftp'"):
        st.code(st.session_state.zftp_list)

    with st.expander("st.session_state.tso_list - Profiles with string 'tso'"):
        st.code(st.session_state.tso_list)
    