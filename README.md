# Test playability of an asset
Connect to services and playout a crid
 - This tool requires corporate network access and assumes QA tests have been checked out 
### Example:

```
playable [crid|title]
playable The Firm
playable 3e1589785251a510VgnVCM1000000b43150a____  

```

## Dependencies

- Python3
- Pyenv
- zsh complete
- Popcorn Mongo db 

## Installing to the pyenv 'tools3'

**Installation**

```
pyenv activate tools3
pip install .
pyenv deactivate

# or use the script:
reinstall
```

**Uninstalling**

```
pyenv activate tools3
pip uninstall playable
pyenv deactivate
```

**Development**

```
pyenv local tools3
pip install -e .
py.test -vs
```

**zsh Completion**

```
# Add script to .oh-my-zsh/custom/plugins with:
cd scripts
./setup_completions

# Update .zshrc with:
plugins=(
  playable
)
```

**Testing**

```
cd tests
py.test -v
# OR:
py.test --cov-report html --cov tool.playable
open htmlcov/index.html
```