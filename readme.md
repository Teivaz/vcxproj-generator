# Visual Studio 2013/2015 C++ project file generator.
### Create `.vcxproj` from sources directly
Script will recursively search for the C++ files starting from current directory. All files found will be placed included in the project file. Also will generate `.filters` file to preserv folder structure within project.

## Usage
1. Download script [here](https://rawgit.com/Teivaz/vcxproj-generator/master/generate_vcxproj.py)
2. Put it to the root folder of your sources
3. Run it    

## Settings
In case you need to customize you have following settings:
```python
PATHS_TO_SEARCH = ['.']
PROJECT_NAME = '' # by default will use ccurrent directory name
PLATFORMS = ['Win32']
CONFIGURATIONS = ['Debug', 'Release']

HEADER_EXT = ['.h', '.inl', '.hpp']
SOURCE_EXT = ['.c', '.cc', '.cpp']
VS_VERSION = '2013' # 2013 or 2015
```
