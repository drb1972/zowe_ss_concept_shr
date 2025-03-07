import streamlit as st
import zw
import pandas as pd
import json
import requests
from datetime import datetime, timedelta

#------------------- INITIAL MESSAGE ----------------------------------------
st.title(f'Zowe CLI Check Team Config')
#----------------------------------------------------------------------------

if 'first_time_zosmf_prof' not in st.session_state:
    st.session_state.first_time_zosmf_prof=False
if 'sb_check_zosmf_value' not in st.session_state:
    st.session_state.sb_check_zosmf_value = None
if 'sb_check_jwt_value' not in st.session_state:
    st.session_state.sb_check_jwt_value = None
if 'sb_query_jwt_value' not in st.session_state:
    st.session_state.sb_query_jwt_value = None
if 'sb_create_jwt_value' not in st.session_state:
    st.session_state.sb_create_jwt_value = None
if 'sb_logout_jwt_value' not in st.session_state:
    st.session_state.sb_logout_jwt_value = None
if 'sb_show_jwt_value' not in st.session_state:
    st.session_state.sb_show_jwt_value = None
if 'sb_check_ssh_value' not in st.session_state:
    st.session_state.sb_check_ssh_value = None
if 'sb_check_zftp_value' not in st.session_state:
    st.session_state.sb_check_zftp_value = None
if 'sb_check_tso_value' not in st.session_state:
    st.session_state.sb_check_tso_value = None
if 'jwt_credentials' not in st.session_state:
    st.session_state.jwt_credentials = True
if 'jwt_user' not in st.session_state:
    st.session_state.jwt_user = None
if 'jwt_password' not in st.session_state:
    st.session_state.jwt_password = None
if 'table' not in st.session_state:
    st.session_state.table = None
if 'color_cell' not in st.session_state:
    st.session_state.color_cell = False


if not st.session_state.first_time_zosmf_prof:
    st.session_state.first_time_zosmf_prof=True 

    st.session_state.table = {}
    # check ✅
    # x ❌
    # rocket 🚀
    # doesn't apply 😐
 
    if 'prof_parents' not in st.session_state:
        st.session_state.prof_parents = []

    for parent in st.session_state.all_profiles_list:
        if parent == 'tso' or parent == "":
            continue
        if '.' not in parent:
            st.session_state.prof_parents.append(parent)
            st.session_state.table[f'[{parent}][table_check_jwt]'] = 'n/a'
            st.session_state.table[f'[{parent}][table_query_jwt_created]'] = 'n/a'
            st.session_state.table[f'[{parent}][table_query_jwt_expired]'] = 'n/a'
            st.session_state.table[f'[{parent}][table_create_jwt]'] = 'n/a'
            st.session_state.table[f'[{parent}][table_logout_jwt]'] = 'n/a'
            st.session_state.table[f'[{parent}][table_check_zosmf]'] = 'n/a'
            st.session_state.table[f'[{parent}][table_check_ssh]'] = 'n/a'
            st.session_state.table[f'[{parent}][table_check_zftp]'] = 'n/a'
            st.session_state.table[f'[{parent}][table_check_tso]'] = 'n/a'


    for parent in st.session_state.prof_parents:
        # st.write('parent: ', parent, 'rest: ', st.session_state.all_profiles_list)
        if '_apiml' in parent and f'{parent}.zosmf' in st.session_state.all_profiles_list:
            st.session_state.table[f'[{parent}][table_check_jwt]'] = '🚀'
            st.session_state.table[f'[{parent}][table_query_jwt_created]'] = '🚀'
            st.session_state.table[f'[{parent}][table_query_jwt_expired]'] = '🚀'
            st.session_state.table[f'[{parent}][table_create_jwt]'] = '🚀'
            st.session_state.table[f'[{parent}][table_logout_jwt]'] = '🚀'

        if '_apiml' not in parent and f'{parent}.zosmf' in st.session_state.all_profiles_list:
            st.session_state.table[f'[{parent}][table_check_zosmf]'] = '🚀'
        
        if '_apiml' not in parent and f'{parent}.ssh' in st.session_state.all_profiles_list:
            st.session_state.table[f'[{parent}][table_check_ssh]'] = '🚀'

        if '_apiml' not in parent and f'{parent}.zftp' in st.session_state.all_profiles_list:
                st.session_state.table[f'[{parent}][table_check_zftp]'] = '🚀'

        if '_apiml' not in parent and f'{parent}.tso' in st.session_state.all_profiles_list:
                st.session_state.table[f'[{parent}][table_check_tso]'] = '🚀'




#--------- Reset all selectboxes except the one that was changed ------------
def reset_other_selectboxes(changed_selectbox):
    list = ['sb_check_zosmf_value',
            'sb_check_jwt_value',
            'sb_query_jwt_value',
            'sb_create_jwt_value', 
            'sb_logout_jwt_value', 
            'sb_show_jwt_value', 
            'sb_check_ssh_value', 
            'sb_check_zftp_value', 
            'sb_check_tso_value']
    for item in list:
        if item != changed_selectbox:
            st.session_state[item] = None
#----------------------------------------------------------------------------


#------------------------- Create a 6-column layout -------------------------
col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns([1, 1, 1, 1, 1, 1,1 ,1 ,1], vertical_alignment="top")

temp_zsomf_list = []
temp_jwt_list   = []
temp_ssh_list   = []
temp_zftp_list  = []
temp_tso_list   = []

for item in st.session_state.zosmf_list:
    if 'apiml' not in item:
        temp_zsomf_list.append(item)
    else:
        temp_jwt_list.append(item)
for item in st.session_state.ssh_list:
    temp_ssh_list.append(item)
for item in st.session_state.zftp_list:
    temp_zftp_list.append(item)
for item in st.session_state.tso_list:
    temp_tso_list.append(item)
temp_zsomf_list.append('all')
temp_jwt_list.append('all')
temp_ssh_list.append('all')
temp_zftp_list.append('all')
temp_tso_list.append('all')




with col1:
    st.selectbox('Check zOSMF profile', 
                       temp_zsomf_list,
                       key='sb_check_zosmf_value',
                       on_change=reset_other_selectboxes,
                       args=('sb_check_zosmf_value',)
                       )
with col2:
    st.selectbox('Check API ML JWT', 
                       temp_jwt_list,
                       key='sb_check_jwt_value',
                       on_change=reset_other_selectboxes,
                       args=('sb_check_jwt_value',)
                       )

with col3:
    st.selectbox('Query API ML JWT', 
                       temp_jwt_list,
                       key='sb_query_jwt_value',
                       on_change=reset_other_selectboxes,
                       args=('sb_query_jwt_value',)
                       )

with col4:
    st.selectbox('Generate API ML JWT', 
                       (x for x in st.session_state.zosmf_list if 'apiml' in x),
                       key='sb_create_jwt_value',
                       on_change=reset_other_selectboxes,
                       args=('sb_create_jwt_value',)
                       )

with col5:
    st.selectbox('Logout API ML JWT', 
                       temp_jwt_list,
                       key='sb_logout_jwt_value',
                       on_change=reset_other_selectboxes,
                       args=('sb_logout_jwt_value',)
                       )

with col6:
    st.selectbox('Show JWT', 
                       (x for x in st.session_state.zosmf_list if 'apiml' in x),
                       key='sb_show_jwt_value',
                       on_change=reset_other_selectboxes,
                       args=('sb_show_jwt_value',)
                       )
    
with col7:
    st.selectbox('Check ssh profile', 
                       temp_ssh_list,
                       key='sb_check_ssh_value',
                       on_change=reset_other_selectboxes,
                       args=('sb_check_ssh_value',)
                       )

with col8:
    st.selectbox('Check zftp profile', 
                       temp_zftp_list,
                       key='sb_check_zftp_value',
                       on_change=reset_other_selectboxes,
                       args=('sb_check_zftp_value',)
                       )

with col9:
    st.selectbox('Check tso profile', 
                       temp_tso_list,
                       key='sb_check_tso_value',
                       on_change=reset_other_selectboxes,
                       args=('sb_check_tso_value',)
                       )
#----------------------------------------------------------------------------

profile = '' 
rc = ''
sto = ''
ste = ''
msg = ''

# To generate tokens with my Team Config:
#   - zowe auth login apiml --base-p b043_apiml
# To use them:
#   - zowe files list ds 'sys1.parmlib' --zosmf-p b043_apiml.zosmf

#------------------- DIPLAY SUCCESS OR ERROR MESSAGE ------------------------
def success_error(event, msg=''):
    if event == 'ok':
        st.toast('Process completed!', icon='🎉')
        st.success(f'{msg}')
    else:
        st.toast('Error!', icon='❌')
        st.error(f'{msg}')
    # st.info('This is a purely informational message', icon="ℹ️")
    # st.warning('This is a warning', icon="⚠️")
#----------------------------------------------------------------------------

#------------------- CHECKS JWT CREATION AND EXPIRATION DATES ---------------
def token_expiration(sto, row):
    sto_dict    = json.loads(sto)
    token_value = sto_dict["data"]["commandValues"]["token-value"]
    apiml_uri   = sto_dict["data"]["commandValues"]["host"]
    apiml_uri   = 'https://' + apiml_uri
    apiml_port  = sto_dict["data"]["commandValues"]["port"]
    base_path   = 'gateway/api/v1/auth/query'
    url         = f'{apiml_uri}:{apiml_port}/{base_path}'
    headers     = { 'Authorization': f'Bearer {token_value}'}
    response    = requests.get(url, headers=headers, verify=True)
    token_info  = json.loads(response.text)

    if "messages" in token_info and token_info["messages"] and "messageReason" in token_info["messages"][0]:
        error_msg = token_info["messages"][0]["messageReason"]
        return error_msg
    else:
        creation = token_info["creation"]
        expiration = token_info["expiration"]

        # Convert to seconds
        creation_sec = creation / 1000 
        expiration_sec = expiration / 1000 
        # Convert to datetime
        dtcr = datetime.utcfromtimestamp(creation_sec)
        dtcr = dtcr + timedelta(hours=1)
        dtex = datetime.utcfromtimestamp(expiration_sec)
        dtex = dtex + timedelta(hours=1)
        # Format as readable date
        formatted_creation = dtcr.strftime('%m-%d %H:%M UTC')
        formatted_expiration = dtex.strftime('%m-%d %H:%M UTC')

        st.session_state.table[f'[{row}][table_query_jwt_created]'] = f'{formatted_creation}' 
        st.session_state.table[f'[{row}][table_query_jwt_expired]'] = f'{formatted_expiration}' 
        return 'ok'
#----------------------------------------------------------------------------

#------------------- CHECKS IF A JWT EXISTS IN THE token-value FIELD  -------
def check_token_exists(profile, row, table_cell=''):
    with st.spinner("Processing..."): 
        flags=f'--rto 10 --zosmf-p {profile} --rfj --show-inputs-only'
        sto, ste, rc = zw.check_zosmf_connection(flags)
        sto_dict   = json.loads(sto)
        if rc !=0 or "token-value" not in sto_dict["data"]["commandValues"]:
            msg = f'JWT not found for {profile}'
            if rc !=0:
                msg = sto_dict["stderr"]
            success_error('ko',f'{msg}')
            if table_cell != '':
                st.session_state.table[f'[{row}][{table_cell}]'] = '❌'
            return False, sto
        else:
            return True, sto
#----------------------------------------------------------------------------

#------------------- UPDATE TABLE VALUES WHEN THERE IS A JWT ERROR ----------
def jwt_error(row):
    st.session_state.table[f'[{row}][table_check_jwt]'] = '❌'
    st.session_state.table[f'[{row}][table_query_jwt_created]'] = '❌'
    st.session_state.table[f'[{row}][table_query_jwt_expired]'] = '❌'
    st.session_state.table[f'[{row}][table_create_jwt]'] = '🚀'
    cell_color = 'lightcoral'
    return cell_color
#----------------------------------------------------------------------------

#------------------- SELECTBOXES ACTIONS ------------------------------------
def check_zosmf_value(profile, row, table_cell):
    with st.spinner("Processing..."):  
        flags=f'--rto 10 --zosmf-p {profile}'
        sto, ste, rc = zw.check_zosmf_connection(flags)
    if rc == 0:
        success_error('ok', f'z/OSMF profile {profile} working')
        st.session_state.table[f'[{row}][{table_cell}]'] = '✅' 
        cell_color = 'lightgreen'
    else:
        success_error('ko', f'z/OSMF profile {profile} error')
        st.session_state.table[f'[{row}][{table_cell}]'] = '❌' 
        cell_color = 'lightcoral'
    return cell_color

if st.session_state.sb_check_zosmf_value:
    profile = f'{st.session_state.sb_check_zosmf_value}' 
    row = profile.split('.')[0]
    table_cell = 'table_check_zosmf'
    column = 'zOSMF access'
    st.session_state.color_cell = True
    if st.session_state.sb_check_zosmf_value != 'all':
        cell_color = check_zosmf_value(profile, row, table_cell)
    else:
        temp_zsomf_list.remove('all')
        for profile in temp_zsomf_list:
            row = profile.split('.')[0]
            cell_color = check_zosmf_value(profile, row, table_cell)


def check_jwt_value(profile, row, table_cell):
    tf, sto = check_token_exists(profile, row, table_cell)
    if tf == True:
        flags=f'--rto 10 --zosmf-p {profile}'
        sto, ste, rc = zw.check_zosmf_connection(flags)
        if rc == 0:
            success_error('ok', f'JWT z/OSMF profile {profile} working')
            st.session_state.table[f'[{row}][{table_cell}]'] = '✅'
            st.session_state.table[f'[{row}][table_create_jwt]'] = '🚀'
            st.session_state.table[f'[{row}][table_logout_jwt]'] = '🚀' 
            st.session_state.table[f'[{row}][table_query_jwt_created]'] = '🚀'
            st.session_state.table[f'[{row}][table_query_jwt_expired]'] = '🚀'
            cell_color = 'lightgreen'
        else:
            success_error('ko',f'{ste}')
            cell_color = jwt_error(row)
            st.session_state.table[f'[{row}][{table_cell}]'] = '❌'
    else:
        cell_color = jwt_error(row)
        st.session_state.table[f'[{row}][{table_cell}]'] = '❌'
    return(cell_color)

if st.session_state.sb_check_jwt_value:
    profile = f'{st.session_state.sb_check_jwt_value}'
    row = profile.split('.')[0]
    table_cell = 'table_check_jwt'
    column = 'JWT access'
    st.session_state.color_cell = True
    if st.session_state.sb_check_jwt_value != 'all':
        cell_color = check_jwt_value(profile, row, table_cell)
    else:
        temp_jwt_list.remove('all')
        for profile in temp_jwt_list:
            row = profile.split('.')[0]
            cell_color = check_jwt_value(profile, row, table_cell)
        

def query_jwt_value(profile, row):
    tf, sto = check_token_exists(profile, row)
    if tf == False:
        cell_color = jwt_error(row)
    else:
        msg = token_expiration(sto, row)
        if msg != 'ok': 
            success_error('ko',f'{msg} for {profile}')
            cell_color = jwt_error(row)
        else:
            success_error('ok', 'JWT Dates Checked')
            cell_color = 'lightgreen'
    return(cell_color)

if st.session_state.sb_query_jwt_value:
    profile = f'{st.session_state.sb_query_jwt_value}'
    row = profile.split('.')[0]
    column = 'JWT expiration date'
    st.session_state.color_cell = True
    if st.session_state.sb_query_jwt_value != 'all':
        cell_color = query_jwt_value(profile, row)
    else:
        temp_jwt_list.remove('all')
        for profile in temp_jwt_list:
            row = profile.split('.')[0]
            cell_color = query_jwt_value(profile, row)
 

if st.session_state.sb_create_jwt_value:
    if st.session_state.jwt_credentials:
        @st.dialog("Enter credentials")
        def credentials():
            st.write(f"Enter your credentials")
            st.session_state.jwt_user = st.text_input("User")
            st.session_state.jwt_password = st.text_input("Password",type="password")
            if st.button("Submit"):
                st.session_state.jwt_credentials = False
                st.rerun()
        credentials()
    else:
        st.session_state.jwt_credentials = True
        profile = f'{st.session_state.sb_create_jwt_value}'
        row = profile.split('.')[0]
        base_p = profile.replace(".zosmf", "")
        table_cell = 'table_create_jwt'
        column = 'Create JWT'
        st.session_state.color_cell = True

        with st.spinner("Processing..."):
            sto, ste, rc = zw.create_jwt_token(st.session_state.jwt_user,st.session_state.jwt_password, f'--base-p {base_p}')
        if rc == 0:
            sto_dict   = json.loads(sto)
            success_msg = sto_dict["stdout"]
            # Query token
            tf, sto = check_token_exists(profile, row)
            if tf == False:
                st.session_state.table[f'[{row}][table_query_jwt_created]'] = '❌'
                st.session_state.table[f'[{row}][table_query_jwt_expired]'] = '❌'
                cell_color = 'lightcoral'
            else:
                msg = token_expiration(sto, row)
                if msg != 'ok': 
                    success_error('ko',f'{msg} for {profile}')
                    st.session_state.table[f'[{row}][table_query_jwt_created]'] = '❌'
                    st.session_state.table[f'[{row}][table_query_jwt_expired]'] = '❌'
                    cell_color = 'lightcoral'
                else:
                    success_error('ok', 'JWT Dates Updated')
                    success_error('ok', success_msg)
                    st.session_state.table[f'[{row}][table_create_jwt]'] = '✅' 
                    st.session_state.table[f'[{row}][table_check_jwt]'] = '🚀'
                    st.session_state.table[f'[{row}][table_logout_jwt]'] = '🚀' 
                    cell_color = 'lightgreen'
        else:
            sto_dict   = json.loads(sto)
            error_msg = sto_dict["message"]
            success_error('ko', error_msg)
            st.session_state.table[f'[{row}][{table_cell}]'] = '❌'
            cell_color = 'lightcoral'


def logout_jwt_value(profile, row, table_cell, base_p):
    tf, sto = check_token_exists(profile, table_cell)
    if tf == True:
        flags=f'--base-p {base_p}'
        sto, ste, rc = zw.logout_jwt_token(flags)
        if rc == 0:
            success_error('ok', f'{row} JWT Deleted')
            jwt_error(row)
            st.session_state.table[f'[{row}][{table_cell}]'] = '✅' 
            cell_color = 'lightgreen'
        else:
            success_error('ko',f'{ste}')
            cell_color = jwt_error(row)
            st.session_state.table[f'[{row}][{table_cell}]'] = '❌'
    else:
        cell_color = jwt_error(row)
        st.session_state.table[f'[{row}][{table_cell}]'] = '❌'
    return(cell_color)

if st.session_state.sb_logout_jwt_value:
    profile = f'{st.session_state.sb_logout_jwt_value}'
    row = profile.split('.')[0]
    base_p =profile.replace(".zosmf", "")
    table_cell = 'table_logout_jwt'
    column = 'Logout JWT'
    st.session_state.color_cell = True
    if st.session_state.sb_logout_jwt_value != 'all':
        cell_color = logout_jwt_value(profile, row, table_cell, base_p)
    else:
        temp_jwt_list.remove('all')
        for profile in temp_jwt_list:
            row = profile.split('.')[0]
            cell_color = logout_jwt_value(profile, row, table_cell, base_p)


if st.session_state.sb_show_jwt_value:
    profile = f'{st.session_state.sb_show_jwt_value}'
    row = profile.split('.')[0]
    base_p =profile.replace(".zosmf", "")

    tf, sto = check_token_exists(profile, row)
    if tf == True:
        sto_dict    = json.loads(sto)
        token_value = sto_dict["data"]["commandValues"]["token-value"]
        @st.dialog(f"JWT for {base_p}")
        def show_jwt(token_value):
            st.write(f"{token_value}")
        show_jwt(token_value)
    else:
        jwt_error(row)


def check_ssh_value(profile, row, table_cell):
    with st.spinner("Processing..."):  
        flags=f'--ssh-p {profile}'
        userid, ste, rc = zw.find_userid(flags)
    if rc == 0:
        success_error('ok', f'ssh profile {profile} working')
        st.session_state.table[f'[{row}][{table_cell}]'] = f'{userid}' 
        cell_color = 'lightgreen'
    else:
        success_error('ko', f'ssh profile {profile} error {ste}')
        st.session_state.table[f'[{row}][{table_cell}]'] = '❌' 
        cell_color = 'lightcoral'
    return cell_color

if st.session_state.sb_check_ssh_value:
    profile = f'{st.session_state.sb_check_ssh_value}' 
    row = profile.split('.')[0]
    table_cell = 'table_check_ssh'
    column = 'ssh access'
    st.session_state.color_cell = True
    if st.session_state.sb_check_ssh_value != 'all':
        cell_color = check_ssh_value(profile, row, table_cell)
    else:
        temp_ssh_list.remove('all')
        for profile in temp_ssh_list:
            row = profile.split('.')[0]
            cell_color = check_ssh_value(profile, row, table_cell)


def check_zftp_value(profile, row, table_cell):
    with st.spinner("Processing..."):  
        flags=f'--zftp-p {profile}'
        sto, ste, rc = zw.check_zftp_connection(flags)
    if rc == 0:
        success_error('ok', f'zFTP profile {profile} working')
        st.session_state.table[f'[{row}][{table_cell}]'] = '✅' 
        cell_color = 'lightgreen'
    else:
        success_error('ko', f'z/FTP profile {profile} error: {ste}')
        st.session_state.table[f'[{row}][{table_cell}]'] = '❌' 
        cell_color = 'lightcoral'
    return cell_color

if st.session_state.sb_check_zftp_value:
    profile = f'{st.session_state.sb_check_zftp_value}' 
    row = profile.split('.')[0]
    table_cell = 'table_check_zftp'
    column = 'zftp access'
    st.session_state.color_cell = True
    if st.session_state.sb_check_zftp_value != 'all':
        cell_color = check_zftp_value(profile, row, table_cell)
    else:
        temp_zftp_list.remove('all')
        for profile in temp_zftp_list:
            row = profile.split('.')[0]
            cell_color = check_zftp_value(profile, row, table_cell)


def check_tso_value(profile, row, table_cell):
    with st.spinner("Processing..."):  
        flags=f'"time" --tso-p {profile}'
        userid, ste, rc = zw.issue_tso_command(flags)
    if rc == 0:
        success_error('ok', f'tso profile {profile} working')
        st.session_state.table[f'[{row}][{table_cell}]'] = '✅' 
        cell_color = 'lightgreen'
    else:
        success_error('ko', f'tso profile {profile} error {ste}')
        st.session_state.table[f'[{row}][{table_cell}]'] = '❌' 
        cell_color = 'lightcoral'
    return cell_color

if st.session_state.sb_check_tso_value:
    profile = f'{st.session_state.sb_check_tso_value}' 
    row = profile.split('.')[0]
    table_cell = 'table_check_tso'
    column = 'tso access'
    st.session_state.color_cell = True
    if st.session_state.sb_check_tso_value != 'all':
        cell_color = check_tso_value(profile, row, table_cell)
    else:
        temp_tso_list.remove('all')
        for profile in temp_tso_list:
            row = profile.split('.')[0]
            cell_color = check_tso_value(profile, row, table_cell)


#----------------------------------------------------------------------------
        

#------------------- CREATE TABLE -------------------------------------------
profile_name_list = []
table_check_zosmf_list = []
table_check_jwt_list = []
table_query_jwt_created_list = []
table_query_jwt_expired_list = []
table_create_jwt_list = []
table_logout_jwt_list = []
table_check_ssh = []
table_check_zftp = []
table_check_tso = []
for item in st.session_state.prof_parents:
    table_profile_name = item
    table_profile_name = table_profile_name.replace(".zosmf", "")
    profile_name_list.append(table_profile_name)
    table_check_zosmf_list.append(st.session_state.table[f'[{item}][table_check_zosmf]'])
    table_check_jwt_list.append(st.session_state.table[f'[{item}][table_check_jwt]'])
    table_query_jwt_created_list.append(st.session_state.table[f'[{item}][table_query_jwt_created]'])
    table_query_jwt_expired_list.append(st.session_state.table[f'[{item}][table_query_jwt_expired]'])
    table_create_jwt_list.append(st.session_state.table[f'[{item}][table_create_jwt]'])
    table_logout_jwt_list.append(st.session_state.table[f'[{item}][table_logout_jwt]'])
    table_check_ssh.append(st.session_state.table[f'[{item}][table_check_ssh]'])
    table_check_zftp.append(st.session_state.table[f'[{item}][table_check_zftp]'])
    table_check_tso.append(st.session_state.table[f'[{item}][table_check_tso]'])

table = {
    # "Profile Name": profile_name_list,
    "zOSMF access": table_check_zosmf_list,
    "JWT access": table_check_jwt_list,
    "JWT creation date": table_query_jwt_created_list,
    "JWT expiration date": table_query_jwt_expired_list,
    "Create JWT": table_create_jwt_list,
    "Logout JWT": table_logout_jwt_list,
    "ssh access": table_check_ssh,
    "zftp access": table_check_zftp,
    "tso access": table_check_tso
}
df = pd.DataFrame(table, index=profile_name_list)

if st.session_state.color_cell:
    st.session_state.color_cell = False
    # Function to highlight a specific cell
    def highlight_cell(df, row_name, column_name, color="lightgreen"):
        def apply_style(data):
            styles = pd.DataFrame('', index=data.index, columns=data.columns)  # Default no style
            if row_name in data.index and column_name in data.columns:
                styles.loc[row_name, column_name] = f'background-color: {color};'
            return styles

        return df.style.apply(apply_style, axis=None)

    # df = highlight_cell(df, 'b043.zosmf', 'zOSMF access', 'lightgreen')
    df = highlight_cell(df, row, column, cell_color)

# Display the DataFrame
st.write("DataFrame:")
st.dataframe(df)
#----------------------------------------------------------------------------

#--------------------- STATUS MESSAGE ------------------------------------
with st.expander("Debug"):
    with st.container(border=True,key='status_container'):
        st.write('rc : ', rc)
        st.write('sto: ', sto)
        st.write('ste: ', ste)


# # Function to execute on button click
# def execute_function(row):
#     st.write(f"Function executed for: {row['Name']}, Age: {row['Age']}, City: {row['City']}")

# # Generate a button for each row in the DataFrame
# for i, row in df.iterrows():
#     if st.button(f"Execute function for {row['Name']}"):
#         execute_function(row)
