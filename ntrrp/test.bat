@setlocal

@set PYTHONPATH=%PYTHONPATH%;%OSGEO4W_ROOT%\apps\qgis\python
@set PYTHONPATH=%PYTHONPATH%;%OSGEO4W_ROOT%\apps\qgis\python\plugins
@set PYTHONPATH=%PYTHONPATH%;%OSGEO4W_ROOT%\apps\Python37\lib\site-packages

@python -m pytest -rP --cov-report term-missing test

@endlocal
