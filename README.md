# zowe_ss_concept_shr
  
## Requirements
- Zowe CLI
- Python
- streamlit library (pip install streamlit in Windows)

## Recomendations
- Create a Python venv (not mandatory but recommended)
- If you are interested in the code:
  - Learn Python basics
  - Learn [Streamlit](https://streamlit.io/)
  - Included a library for common functions [zw.py](./zw.py)

## zowe.config.json
- Please, create your profile as the sample provided: copy.zowe.config.json
- This nested profile allows you to store independent JWTs
- Create JWTs with zowe CLI "`zowe auth login apiml --base-p ca32_apiml`" <- Just the name of the parent
- Usage: "`zowe files list ds 'sys1.parmlib'`" with default profile or with `--zosmf-p ca32` for zosmf or `ca32_apiml` for token authentication


 