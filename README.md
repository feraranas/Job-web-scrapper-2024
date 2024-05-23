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
