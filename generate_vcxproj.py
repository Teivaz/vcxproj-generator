'''
This software is provided 'as-is', without any express or implied
warranty.  In no event will the authors be held liable for any damages
arising from the use of this software.

Permission is granted to anyone to use this software for any purpose,
including commercial applications, and to alter it and redistribute it
freely, subject to the following restrictions:

1. The origin of this software must not be misrepresented; you must not
   claim that you wrote the original software. If you use this software
   in a product, an acknowledgment in the product documentation would be
   appreciated but is not required.
2. Altered source versions must be plainly marked as such, and must not be
   misrepresented as being the original software.
3. This notice may not be removed or altered from any source distribution.

@authors: Teivaz [github.com/Teivaz]
'''

import os, uuid

PATHS_TO_SEARCH = ['.']
PROJECT = '' # by default will use ccurrent directory name
PLATFORMS = ['Win32']
CONFIGURATIONS = ['Debug', 'Release']

HEADER_EXT = ['.h', '.inl', '.hpp']
SOURCE_EXT = ['.c', '.cc', '.cpp']

def UUID(name):
    return str(uuid.uuid3(uuid.NAMESPACE_OID, name)).upper()

def IsDebug(configuration):
    return 'debug' in configuration.lower()

def FilterFromPath(path):
    (head, tail) = os.path.split(path)
    head = head.replace('/', '\\').replace('..\\', '').replace('.\\', '')
    if head == '.':
        return ''
    return head

class Vcxproj:
    Header = '<?xml version="1.0" encoding="utf-8"?>'
    Project0 = '<Project DefaultTargets="Build" ToolsVersion="12.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">'
    Project1 = '</Project>'
    ProjectConfigurations0 = '  <ItemGroup Label="ProjectConfigurations">'
    ProjectConfigurations1 = '  </ItemGroup>'
    # configuration, platform
    ConfigurationT = '\n'.join([
            '    <ProjectConfiguration Include="{0}|{1}">',
            '      <Configuration>Debug</Configuration>',
            '      <Platform>{1}</Platform>',
            '    </ProjectConfiguration>'])
    # project name, project uuid
    GlobalsT = '\n'.join([
            '  <PropertyGroup Label="Globals">',
            '    <ProjectGuid>{{{1}}}</ProjectGuid>',
            '    <RootNamespace>{0}</RootNamespace>',
            '  </PropertyGroup>'])
    # configuration, platform, debug
    PropertyT = '\n'.join([
            '  <PropertyGroup Condition="\'$(Configuration)|$(Platform)\'==\'{0}|{1}\'" Label="Configuration">',
            '    <ConfigurationType>Application</ConfigurationType>',
            '    <UseDebugLibraries>{2}</UseDebugLibraries>',
            '    <PlatformToolset>v120</PlatformToolset>',
            '    <CharacterSet>MultiByte</CharacterSet>',
            '  </PropertyGroup>'])
    # configuration, platform
    ItemDefenitionDebugT = '\n'.join([
        '  <ItemDefinitionGroup Condition="\'$(Configuration)|$(Platform)\'==\'{0}|{1}\'">',
        '    <ClCompile>',
        '      <WarningLevel>Level3</WarningLevel>',
        '      <Optimization>Disabled</Optimization>',
        '      <SDLCheck>true</SDLCheck>',
        '      <PreprocessorDefinitions>%(PreprocessorDefinitions)</PreprocessorDefinitions>',
        '    </ClCompile>',
        '    <Link>',
        '      <GenerateDebugInformation>true</GenerateDebugInformation>',
        '    </Link>',
        '  </ItemDefinitionGroup>'])
    # configuration, platform
    ItemDefenitionReleaseT = '\n'.join([
        '  <ItemDefinitionGroup Condition="\'$(Configuration)|$(Platform)\'==\'{0}|{1}\'">',
        '    <ClCompile>',
        '      <WarningLevel>Level3</WarningLevel>',
        '      <Optimization>MaxSpeed</Optimization>',
        '      <FunctionLevelLinking>true</FunctionLevelLinking>',
        '      <IntrinsicFunctions>true</IntrinsicFunctions>',
        '      <SDLCheck>true</SDLCheck>',
        '      <PreprocessorDefinitions>%(PreprocessorDefinitions)</PreprocessorDefinitions>',
        '    </ClCompile>',
        '    <Link>',
        '      <GenerateDebugInformation>true</GenerateDebugInformation>',
        '      <EnableCOMDATFolding>true</EnableCOMDATFolding>',
        '      <OptimizeReferences>true</OptimizeReferences>',
        '    </Link>',
        '  </ItemDefinitionGroup>'])
    ItemGroup0 = '  <ItemGroup>'
    ItemGroup1 = '  </ItemGroup>'
    # path
    IncludesT = '    <ClInclude Include="{0}" />'
    # path
    SourcesT = '    <ClCompile Include="{0}" />'

    ImportTargets = '  <Import Project="$(VCTargetsPath)\Microsoft.Cpp.targets" />'
    ImportProps = '  <Import Project="$(VCTargetsPath)\Microsoft.Cpp.props" />'
    ImportDefaultProps = '  <Import Project="$(VCTargetsPath)\Microsoft.Cpp.Default.props" />'

    @staticmethod
    def Configuration(configuration, platform):
        return Vcxproj.ConfigurationT.format(configuration, platform)
    @staticmethod
    def Globals(name):
        uid = UUID(name)
        return Vcxproj.GlobalsT.format(name, uid)
    @staticmethod
    def Property(configuration, platform):
        debug = 'false'
        if IsDebug(configuration) : debug = 'true'
        return Vcxproj.PropertyT.format(configuration, platform, debug)
    @staticmethod
    def ItemDefenition(configuration, platform):
        defenition = Vcxproj.ItemDefenitionReleaseT
        if IsDebug(configuration): defenition = Vcxproj.ItemDefenitionDebugT
        return defenition.format(configuration, platform)
    @staticmethod
    def Includes(name):
        return Vcxproj.IncludesT.format(name)
    @staticmethod
    def Sources(name):
        return Vcxproj.SourcesT.format(name)

class Filters:
    Header = '<?xml version="1.0" encoding="utf-8"?>'
    Project0 = '<Project ToolsVersion="4.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">'
    Project1 = '</Project>'
    ItemGroup0 = '  <ItemGroup>'
    ItemGroup1 = '  </ItemGroup>'
    # path, folder
    SourcesT = '\n'.join([
        '    <ClCompile Include="{0}">',
        '      <Filter>{1}</Filter>',
        '    </ClCompile>'])
    # path, folder
    IncludesT = '\n'.join([
        '    <ClInclude Include="{0}">',
        '      <Filter>{1}</Filter>',
        '    </ClInclude>'])
    # folder, uuid
    FoldersT = '\n'.join([
        '    <Filter Include="{0}">',
        '      <UniqueIdentifier>{{{1}}}</UniqueIdentifier>',
        '    </Filter>'])

    @staticmethod
    def Sources(path):
        folder = FilterFromPath(path)
        return Filters.SourcesT.format(path, folder)
    @staticmethod
    def Includes(path):
        folder = FilterFromPath(path)
        return Filters.IncludesT.format(path, folder)
    @staticmethod
    def Folders(folder):
        uid = UUID(folder)
        return Filters.FoldersT.format(folder, uid)

class Generator:
    Folders = set()
    Includes = set()
    Sources = set()
    Platforms = set()
    Configurations = set()
    Name = ''

    def __init__(self, name, platforms, configurations):
        self.Name = name
        for platform in platforms:
            self.Platforms.add(platform)
        for configuration in configurations:
            self.Configurations.add(configuration)

    def AddFolder(self, path):
        filt = FilterFromPath(path)
        if filt == '':
            return
        if filt not in self.Folders:
            self.Folders.add(filt)
            filters = ''
            for f in os.path.split(filt):
                filters = os.path.join(filters, f)
                if filters != '':
                    self.Folders.add(filters)

    def AddSource(self, path):
        self.Sources.add(path)

    def AddHeader(self, path):
        self.Includes.add(path)

    def AddFile(self, path):
        (root, ext) = os.path.splitext(path)
        if ext in HEADER_EXT:
            self.AddHeader(path)
        elif ext in SOURCE_EXT:
            self.AddSource(path)
        else:
            return
        self.AddFolder(path)

    def Walk(self, path):
        if os.path.isfile(path):
            self.AddFile(path)
        else:
            for subPath in os.listdir(path):
                self.Walk(os.path.join(path, subPath))

    def CreateProject(self):
        project = []
        project.append(Vcxproj.Header)
        project.append(Vcxproj.Project0)

        project.append(Vcxproj.ProjectConfigurations0)
        for c in self.Configurations:
            for p in self.Platforms:
                project.append(Vcxproj.Configuration(c, p))
        project.append(Vcxproj.ProjectConfigurations1)

        project.append(Vcxproj.Globals(self.Name))

        project.append(Vcxproj.ImportDefaultProps)

        for c in self.Configurations:
            for p in self.Platforms:
                project.append(Vcxproj.Property(c, p))

        project.append(Vcxproj.ImportProps)

        for c in self.Configurations:
            for p in self.Platforms:
                project.append(Vcxproj.ItemDefenition(c, p))

        project.append(Vcxproj.ItemGroup0)
        for f in self.Includes:
            project.append(Vcxproj.Includes(f))
        project.append(Vcxproj.ItemGroup1)

        project.append(Vcxproj.ItemGroup0)
        for f in self.Sources:
            project.append(Vcxproj.Sources(f))
        project.append(Vcxproj.ItemGroup1)
        project.append(Vcxproj.ImportTargets)

        project.append(Vcxproj.Project1)
        return '\n'.join(project)

    def CreateFilters(self):
        project = []
        project.append(Filters.Header)
        project.append(Filters.Project0)

        project.append(Filters.ItemGroup0)
        for f in self.Folders:
            project.append(Filters.Folders(f))
        project.append(Filters.ItemGroup1)

        project.append(Filters.ItemGroup0)
        for f in self.Includes:
            project.append(Filters.Includes(f))
        project.append(Filters.ItemGroup1)

        project.append(Filters.ItemGroup0)
        for f in self.Sources:
            project.append(Filters.Sources(f))
        project.append(Filters.ItemGroup1)

        project.append(Filters.Project1)
        return '\n'.join(project)

    def Generate(self):
        f = open(self.Name + '.vcxproj', 'w')
        f.write(self.CreateProject())
        f.close()

        f = open(self.Name + '.vcxproj.filters', 'w')
        f.write(self.CreateFilters())
        f.close()

def main(paths, name, platforms, configurations):
    if name == '':
        name = os.path.split(os.getcwd())[-1]
    generator = Generator(name, platforms, configurations)
    for path in paths:
        generator.Walk(path)
    generator.Generate()

main(PATHS_TO_SEARCH, PROJECT, PLATFORMS, CONFIGURATIONS)
