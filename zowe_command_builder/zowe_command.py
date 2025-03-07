#----------------------------------------------------------------------------
# streamlit run main.py
# uni - @broadcom/dbm-db2-for-zowe-cli
# ins - @broadcom/dbm-db2-for-zowe-cli@zowe-v2-lts
#------------------- IMPORTS ------------------------------------------------
import streamlit as st
import json
import zw
#----------------------------------------------------------------------------

#------------------- INITIAL MESSAGE ----------------------------------------
st.title(f'Zowe CLI Command Builder')
#----------------------------------------------------------------------------

#------------------- RUNS ONLY FIRST TIME -----------------------------------
#- Initialize sesion variables
if 'reset' not in st.session_state: # Reset values to start process
    st.session_state.reset=False
if 'create_file' not in st.session_state: # To create the json file
    st.session_state.create_file=False
if 'zowe_dict' not in st.session_state: # Store the working json file
    st.session_state.zowe_dict=False
if 'zowe_command' not in st.session_state: # Zowe command 
    st.session_state.zowe_command=''
if 'zowe_group_command' not in st.session_state: # Zowe command groups
    st.session_state.zowe_group_command='zowe'
if 'zowe_options_command' not in st.session_state: # Zowe command options
    st.session_state.zowe_options_command=''
if 'selectb' not in st.session_state: # Selectbox value when drilling into groups
    st.session_state.selectb=False
if "create_button_disabled" not in st.session_state: # Create button state
    st.session_state.create_button_disabled = True  # Button starts as disabled
if "submit_button_disabled" not in st.session_state: # Submit command button state
    st.session_state.submit_button_disabled = True  # Button starts as disabled
if "queue_button_disabled" not in st.session_state: # Queue command button state
    st.session_state.queue_button_disabled = True  # Button starts as disabled
if "queue" not in st.session_state: # Queue command button state
    st.session_state.queue = []  # Command queue initialized


def create_json():
    with st.spinner("Processing..."):
        sto, ste, rc = zw.execute_command('zowe --ac --rfj > ./zowe_command_builder/zowe.json')

#- Create json zowe --ac --rfj command
if not st.session_state.create_file:
    st.session_state.create_file=True 
    create_json()
#----------------------------------------------------------------------------

#------------------- RUNS ONLY FIRST TIME OR RESET --------------------------
#- Loads json zowe --ac --rfj command
#- Creates Zowe_dict from [data]
if not st.session_state.reset:
    st.session_state.reset=True 
    #- Read zowe.json' file:
    with open('./zowe_command_builder/zowe.json', 'r') as file:
        st.session_state.zowe_dict = json.load(file)
    st.session_state.zowe_dict = st.session_state.zowe_dict['data']

    #- Initialize Zowe command
    st.session_state.zowe_command=''
    st.session_state.zowe_group_command='zowe'
    st.session_state.zowe_options_command=''
    st.session_state.create_button_disabled = True # Disable create button
    st.session_state.queue_button_disabled = True # Disable queue button
#----------------------------------------------------------------------------


#------------------- LIST CHILDREN ------------------------------------------
def list_children(actions):
    for name in st.session_state.zowe_dict["children"]:
        actions.append(name["name"])
    return actions.sort()
#----------------------------------------------------------------------------


#------------------- CREATE WIDGETS -----------------------------------------
def create_widgets(group,value):
    options_dict={}
    text_types=["string", "number", "existingLocalFile", "array", "stringOrEmpty"]

    for item in st.session_state.zowe_dict[f'{group}']:

        if group != 'positionals':
            if item["group"]!=f'{value}':
                continue
        st.divider()

        options_dict[f'{item["name"]}'] = item["type"]
        desc = f'{item["name"]} - {item["description"]}'
        desc = zw.remove_ansi_codes(desc)

        if "required" in item:
            if item["required"]:
                desc = 'Required - '+ desc
        
        if item["type"]=="boolean":
            st.toggle(f'{desc}',key=item["name"])

        #- selectbox for profiles
        if item["name"]=="zosmf-profile":
            st.selectbox('zosmf-profile', 
                           st.session_state.zosmf_list,
                           index=None,
                           key=item["name"])
            continue
        
        if item["name"]=="ssh-profile":
            st.selectbox('ssh-profile', 
                           st.session_state.ssh_list,
                           index=None,
                           key=item["name"])
            continue

        if item["name"]=="zftp-profile":
            st.selectbox('zftp-profile', 
                           st.session_state.zftp_list,
                           index=None,
                           key=item["name"])
            continue

        if item["name"]=="tso-profile":
            st.selectbox('tso-profile', 
                           st.session_state.tso_list,
                           index=None,
                           key=item["name"])
            continue

        if item["type"] in text_types:
            if item["name"]=="password":
                st.text_input(f'{desc}',key=item["name"],type="password")
            else:
                st.text_input(f'{desc}',key=item["name"])


    return options_dict
#----------------------------------------------------------------------------


#------------------- DISPLAY SELECTBOX WITH GROUP ---------------------------
if st.session_state.zowe_dict["type"] == "group":
    actions = ['-- select --']
    list_children(actions)
    #- Selects next level of children
    st.session_state.selectb = st.selectbox("Select", actions) # selectbox

    if st.session_state.selectb!='-- select --':
        st.session_state.zowe_group_command=f'{st.session_state.zowe_group_command} {st.session_state.selectb}'
        new_dict = next(
            (item for item in st.session_state.zowe_dict["children"] if item.get("name") == st.session_state.selectb),
            None 
        )
        #- Set the list to the found dictionary
        if new_dict:
            st.session_state.zowe_dict = new_dict
        else:
            st.warning(f"Dictionary with 'name': '{st.session_state.selectb}' not found.")
        st.session_state.zowe_command= f'{st.session_state.zowe_group_command}'

        #- Enable the Create command button when group is at the last level
        if st.session_state.zowe_dict["type"] == "command":
            st.session_state.create_button_disabled = False
        st.rerun()
#----------------------------------------------------------------------------


#------- DISPLAY SUBMIT, RESET, QUEUE, DISPLAY QUEUE & RESET QUEUE BUTTONs --
with st.container(border=True):
    colcom1, colcom2, colcom3, colcom4, colcom5, colcom6 = st.columns([1, 1, 1, 1, 1, 4], vertical_alignment="center")
    with colcom1:
        submit_button=st.button("Submit Commnad",
            type="primary",
            disabled=st.session_state.submit_button_disabled,
            )
    
    with colcom2:
        reset=st.button('Reset Command')
        if reset:
            st.session_state.submit_button_disabled = True
            st.session_state.reset=False
            st.rerun()
    
    with colcom3:
        queue=st.button('Queue Command',
            disabled=st.session_state.submit_button_disabled,
            )
        if queue:
            st.session_state.queue.append(st.session_state.zowe_command)
            st.session_state.submit_button_disabled = False
            st.rerun()
            
    with colcom4:
        show_queue=st.button('Display Queue')
        if show_queue:
            @st.dialog(f"Queued Commands" ,width="large")
            def show_queue(queue):
                my_string = '\n'.join(queue)
                st.code(my_string,wrap_lines=True)
            show_queue(st.session_state.queue)            
    

    with colcom5:
        reset_queue=st.button('Reset Queue',
            )
        if reset_queue:
            st.session_state.queue = []

#------------------- DISPLAY ZOWE COMMAND -----------------------------------
    st.code(f"{st.session_state.zowe_command}",wrap_lines=True) # Zowe command field
#----------------------------------------------------------------------------

#------------------- EXECUTE ZOWE COMMAND -----------------------------------
if submit_button:
    #- Refresh defaults config
    with st.spinner("Processing..."):
        sto, ste, rc = zw.execute_command(f'{st.session_state.zowe_command}')
        if rc==0:
            #- Refresh the json input file
            if "zowe plugins install" in st.session_state.zowe_command or "zowe plugins uninstall" in st.session_state.zowe_command:
                create_json()
            #- Refresh the sidebar zowe config defaults info
            if "zowe config set" in st.session_state.zowe_command and "defaults" in st.session_state.zowe_command:
                with st.spinner("Loading..."): st.session_state.default_profile = zw.list_config_defaults()
                st.rerun()
            #-
            if '--rfj' in st.session_state.zowe_command or '--response-format-json' in st.session_state.zowe_command:
                lang='json'
            else:
                lang='text'
            msg = zw.remove_ansi_codes(sto)
        else:
            msg = zw.remove_ansi_codes(sto)
            if '--rfj' in st.session_state.zowe_command or '--response-format-json' in st.session_state.zowe_command:
                lang='json'
            else:
                msg = zw.remove_ansi_codes(ste)
                lang='text'

        with st.expander(f"Command Output",expanded=True):
            st.code(f'{msg}',wrap_lines = False, language=f'{lang}') 
#----------------------------------------------------------------------------


#------------------- FORM START TO SELECT OPTIONS ---------------------------
with st.form("Create_Command"):

    #- Create button
    create_button=st.form_submit_button("Create Command",
        disabled=st.session_state.create_button_disabled,
        )


    if st.session_state.zowe_dict["type"] == "command":
        text_types=["string", "number", "existingLocalFile", "array", "stringOrEmpty", ""]
        st.session_state.zowe_options_command=''
        
        def set_options(group,value):
            #- Create widgets
            options_dict = create_widgets(f'{group}',f'{value}')

            #- Retrieve values from option fields and build the Zowe command
            for name, type in options_dict.items(): # name: field name; st.session_state.get(name): value 
                if group=="positionals":
                    st.session_state.zowe_options_command=f'{st.session_state.zowe_options_command} {st.session_state.get(name)}'
                elif type=="boolean" and st.session_state.get(name) == True :
                    st.session_state.zowe_options_command=f'{st.session_state.zowe_options_command} --{name}'
                elif (type in text_types) and st.session_state.get(name) != '':
                    if name=="user" and st.session_state.get(name)==None:
                        continue
                    if name=="password" and st.session_state.get(name)==None:
                        continue
                    if name=="zosmf-profile" and st.session_state.get(name)==None:
                        continue
                    if name=="ssh-profile" and st.session_state.get(name)==None:
                        continue
                    if name=="zftp-profile" and st.session_state.get(name)==None:
                        continue
                    if name=="tso-profile" and st.session_state.get(name)==None:
                        continue
                    st.session_state.zowe_options_command=f'{st.session_state.zowe_options_command} --{name} {st.session_state.get(name)}'
                elif type not in text_types and type!="boolean": 
                    st.write(f'Name {name} Type {type} Not available')


        #- Positionals (required) section
        if 'positionals' in st.session_state.zowe_dict:
            if st.session_state.zowe_dict["positionals"] != []:
                positional_dict = set_options('positionals','')

        #- For each set of options create an expander section
        if 'options' in st.session_state.zowe_dict:
            if st.session_state.zowe_dict["options"] != []:
                groups = []
                options_dict={}
                for item in st.session_state.zowe_dict["options"]:
                    if "group" in item:
                        if item["group"] not in groups:
                            groups.append(item["group"])

                for options in groups:
                    with st.expander(f"{options}"):
                        options_dict = set_options('options',f'{options}')

        #- Examples in last expander section
        if 'examples' in st.session_state.zowe_dict:
            if st.session_state.zowe_dict["examples"] != []:
                with st.expander("Examples"):
                    for item in st.session_state.zowe_dict["examples"]:
                        st.write(f'{item["description"]}')
                        st.code(f'{st.session_state.zowe_group_command} {item["options"]}', wrap_lines=True)

  
    if create_button:
        st.session_state.zowe_command= f'{st.session_state.zowe_group_command} {st.session_state.zowe_options_command}' # Create Zowe command
        st.session_state.submit_button_disabled = False # Enable submit command button
        st.session_state.queue_button_disabled = False # Enable queue command button
        st.rerun()
    else: 
        st.session_state.submit_button_disabled = True
#----------------------------------------------------------------------------


#------------------- DISPLAY DESCRIPTION ------------------------------------
st.divider()
if st.session_state.zowe_dict["description"] != '':
    st.write(f'{st.session_state.zowe_dict["description"]}') 
st.divider()
#----------------------------------------------------------------------------
