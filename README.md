# Job Web Scrappers 2024

[![Built with Devbox](https://www.jetify.com/img/devbox/shield_galaxy.svg)](https://www.jetify.com/devbox/docs/contributor-quickstart/)

<details>
<summary>Install required packages via devbox</summary>

1. Initialize devbox

```
devbox init
```

2. Run devbox env

```
devbox shell
```

It'll output the following message:

"""
Python in Devbox works best when used with a virtual environment (vent, virtualenv, etc.). Devbox will automatically create a virtual environment using `venv` for python3 projects, so you can install packages with pip as normal.
To activate the environment, run `. $VENV_DIR/bin/activate` or add it to the init_hook of your devbox.json
To change where your virtual environment is created, modify the $VENV_DIR environment variable in your init_hook

This plugin creates the following helper files:
* /Users/fernandomtrade/Documents/TEC-DE-MTY/SCRAPING/Job-web-scrapper-2024/.devbox/virtenv/python/bin/venvShellHook.sh

This plugin sets the following environment variables:
* VENV_DIR=/Users/fernandomtrade/Documents/TEC-DE-MTY/SCRAPING/Job-web-scrapper-2024/.devbox/virtenv/python/.venv

To show this information, run `devbox info python`
"""

3. If needed to change the python kernel, add it via the python version installed in .devbox

4. If in need to start the venv created by devbox, run:

```
source $VENV_DIR/bin/activate

or

. $VENV_DIR/bin/activate
```

5. Create `requirements.txt` file and add 

```
`pip install -r requirements.txt` in the `init_hook` 
```

</details>

<details>
<summary>Using venv as Python Kernel</summary>

If your .ipynb file isn't detecting the current virtual environment (venv) created by Devbox, there are a few things you can check and try to resolve the issue:

- Kernel Configuration:
Make sure that the Jupyter notebook kernel is set to use the Python interpreter from the virtual environment. You might need to add the virtual environment as a Jupyter kernel.You can add a new Jupyter kernel from your virtual environment by running:

```bash
source $VENV_DIR/bin/activate
pip install ipykernel
python -m ipykernel install --user --name=myenv
# Replace myenv with a name that you prefer for the kernel.
```

python -m ipykernel install --user --name=scrapper-env
</details>
