DEFAULT_GOAL:  pythonanalysis

.PHONY: pythonanalysis
pythonanalysis:
	pip install --upgrade -r requirements.txt
	python3  code/python/a0000_main.py
