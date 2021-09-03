from typing import Sequence, cast
import unreal
import random
texture_tga = "C:/LearnGitHubProject/UE4/Python-In-UE4/Script/MyTexture.TGA"
sound_wav = "C:/LearnGitHubProject/UE4/Python-In-UE4/Script/MySound.WAV"

#创建加载资源的任务
#filename 需要加载的资源路径
#destination_path 加载后的目录
#option 加载资源的额外参数
def bulidImportTask(filename, destination_path,option=None):
    task = unreal.AssetImportTask()
    task.set_editor_property('automated',True)
    #destination_name 资产名
    task.set_editor_property('destination_name','')
    task.set_editor_property('destination_path',destination_path)
    task.set_editor_property('filename',filename)
    task.set_editor_property('replace_existing',True)
    task.set_editor_property('save',True)
    task.set_editor_property('options',option)
    return task
    
#创建加载静态网格的选项
def buildStaticMeshImportOption():
    options = unreal.FbxImportUI()
    options.set_editor_property('import_mesh',True)
    options.set_editor_property('import_textures',True)
    options.set_editor_property('import_materials',True)
    options.set_editor_property('import_as_skeletal',False)
    
    options.static_mesh_import_data.set_editor_property('import_translation',unreal.Vector(50.0,0,0))
    options.static_mesh_import_data.set_editor_property('import_rotation',unreal.Rotator(0.0,110.0,0.0))
    options.static_mesh_import_data.set_editor_property('import_uniform_scale',1.0)
    options.static_mesh_import_data.set_editor_property('combine_meshes',True)
    options.static_mesh_import_data.set_editor_property('generate_lightmap_u_vs',True)
    options.static_mesh_import_data.set_editor_property('auto_generate_collision',True)
    return options

#创建加载谷骨骼网格的选项
def buildSkeletalMeshImportOption():
    options = unreal.FbxImportUI()
    options.set_editor_property('import_mesh',True)
    options.set_editor_property('import_textures',True)
    options.set_editor_property('import_materials',True)
    options.set_editor_property('import_as_skeletal',True)
    
    options.static_mesh_import_data.set_editor_property('import_translation',unreal.Vector(50.0,0,0))
    options.static_mesh_import_data.set_editor_property('import_rotation',unreal.Rotator(0.0,110.0,0.0))
    options.static_mesh_import_data.set_editor_property('import_uniform_scale',1.0)
    options.static_mesh_import_data.set_editor_property('combine_meshes',True)
    options.static_mesh_import_data.set_editor_property('generate_lightmap_u_vs',True)
    options.static_mesh_import_data.set_editor_property('auto_generate_collision',True)
    return options
    
#创建加载动画的选项
def buildAnimationImprotOptions(skeleton_path):
    options = unreal.FbxImportUI()
    options.set_editor_property('import_animations',True)
    #需要给动画资源设置骨骼 资源类型为skeleton
    options.skeleton = unreal.load_asset(skeleton_path)
    options.anim_sequence_import_data.set_editor_property('import_translation',unreal.Vector(50.0,0,0))
    options.anim_sequence_import_data.set_editor_property('import_rotation',unreal.Rotator(0.0,110.0,0.0))
    options.anim_sequence_import_data.set_editor_property('import_uniform_scale',1.0)
    options.anim_sequence_import_data.set_editor_property('animation_length',unreal.FBXAnimationLengthImportType.FBXALIT_ANIMATED_KEY)
    options.anim_sequence_import_data.set_editor_property('remove_redundant_keys',False)
    return options
    
#开始执行任务
def executeImportTasks(tasks):
    #通过资源管理工具，执行导入资源的任务
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)
    for task in tasks:
        for path in task.get_editor_property('imported_object_paths'):
            print('Imported: %s'%path)
            
#导入图片和音效资源
def importMyAssets():
    texture_task = bulidImportTask(texture_tga,'/Game/Texture')
    sound_task = bulidImportTask(sound_wav,'/Game/Sounds')
    executeImportTasks([texture_task,sound_task])
 
#导入静态网格和骨骼网格
def importMeshAsset():
    static_mesh_fbx = 'C:/LearnGitHubProject/UE4/Python-In-UE4/Script/SM_StaticMesh.FBX';
    skeletal_mesh_fbx =  'C:/LearnGitHubProject/UE4/Python-In-UE4/Script/SM_SkeletalMesh.FBX';
    
    static_mesh_task = bulidImportTask(static_mesh_fbx,'/Game/StaticMeshes',buildStaticMeshImportOption());
    static_skeletal_task = bulidImportTask(skeletal_mesh_fbx,'/Game/SkeletalMeshes',buildSkeletalMeshImportOption());
    executeImportTasks([static_mesh_task,static_skeletal_task])

#导入动画资源
def importAnimationAssets():
    animation_fbx = 'C:/LearnGitHubProject/UE4/Python-In-UE4/Script/Animation.FBX'
    animation_fbx_task = bulidImportTask(animation_fbx,'/Game/Animations',buildAnimationImprotOptions('/Game/SkeletalMeshes/SM_SkeletalMesh_Skeleton'))
    executeImportTasks([animation_fbx_task])
    
#保存资源
#path 保存的路径
#force_save 是否强制保存 
def saveAsset(path = "", force_save = True):
    return unreal.EditorAssetLibrary.save_asset(asset_to_save = path,only_if_is_dirty =not force_save)
    

#保存文件夹
#path:文件夹路径
#force_save 是否强制保存 
#recursive 是否保存子文件夹
def saveDirectory(path='', force_save = True, recursive = True):
    return unreal.EditorAssetLibrary.save_directory(directory_path=path, only_if_is_dirty=not force_save, recursive=recursive)
    
#加载资源包
#path 资源包路径
#return obj
def getPackageFromPath(path):
    return unreal.load_package(path)
    
#获得所有修改过的包
def getAllDirtyPackages():
    packages = []
    for x in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages():
        packages.append(x)
    for x in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages():
        packages.append(x)
    return packages
    
#保存所有修改过的包
#show_dialog 是否显示保存框
def saveAllDirtyPackages(show_dialog = False):
    if show_dialog:
        return unreal.EditorLoadingAndSavingUtils.save_dirty_packages_with_dialog(True,True)
    else:
        return unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True,True)
    
#保存包
def savePackages(packages=[], show_dialog = False):
    if show_dialog:
        return unreal.EditorLoadingAndSavingUtils.save_packages_with_dialog(packages,False)
    else:
        return unreal.EditorLoadingAndSavingUtils.save_packages(packages,False)

#判断路径是否存在    
def directoryExist(path):
    return unreal.EditorAssetLibrary.does_directory_exist(path)
    
#创建路径
def createDirectory(path):
    return unreal.EditorAssetLibrary.make_directory(path)
      
#拷贝目录
def duplicateDirectory(source_path,destination_path):
    return unreal.EditorAssetLibrary.duplicate_directory(source_path,destination_path)

#删除目录
def deleteDirectory(path):
    return unreal.EditorAssetLibrary.delete_directory(path)
   
#重命名目录   
def renameDirectory(source_path,destination_path):
    return unreal.EditorAssetLibrary.rename_directory(source_path,destination_path)
    
#资源是否存在
def assetExist(path):
    return unreal.EditorAssetLibrary.does_asset_exist(path) 

#拷贝资源
def duplicateAsset(source_path,destination_path):
    return unreal.EditorAssetLibrary.duplicate_asset(source_path,destination_path)
    
#带对话框的拷贝资源
def duplicateAsset(source_path,destination_path,show_dialog = True):
    if show_dialog:
        return unreal.AssetToolsHelpers.get_asset_tools().duplicate_asset_with_dialog(
            source_path.split('/',1)[0],source_path.rsplit('/',1)[1],unreal.load_asset(destination_path))
    else:
        return unreal.duplicate_asset.get_asset_tools().duplicate_asset(
                source_path.split('/',1)[0],source_path.rsplit('/',1)[1],unreal.load_asset(destination_path))
#删除资源
def deleteAsset(path):
    return unreal.EditorAssetLibrary.delete_asset(path)
#重命名资源   
def renameAsset(source_path,destination_path):
    return unreal.EditorAssetLibrary.rename_asset(source_path, destination_path) 

#带对话框的重命名资源
def renameAssetWithDialog(original_asset,destination_asset,show_dialog = True):
    spltted_path = original_asset.rsplit('/',1)
    asset_path = spltted_path[0]
    asset_name = spltted_path[1]
    rename_data0 = unreal.AssetRenameData(unreal.load_asset(original_asset+'Remaed'),asset_path,asset_name)
    spltted_path = destination_asset.rsplit('/',1)
    asset_path = spltted_path[0]
    asset_name = spltted_path[1]
    rename_data1 = unreal.AssetRenameData(unreal.load_asset(destination_asset+'Remaed'),asset_path,asset_name)
    if show_dialog:
        return unreal.AssetToolsHelpers.get_asset_tools().rename_assets_with_dialog([rename_data0,rename_data1])
    else:
        return unreal.AssetToolsHelpers.get_asset_tools().rename_assets([rename_data0,rename_data1])

#打印当前所有的类
for x in sorted(dir(unreal)):
    print(x)
    
#调用自定义的C++函数
def callCFunction():
    #打印当前类中的所有函数
    for x in sorted(dir(unreal.MyPythonFunctions)):
        print(x)
    unreal.MyPythonFunctions.called_from_python('called_from_python');

def getGradientColor(x):
    return (x/512.0,1-x/512.0,0,1)
    
#自动创建文件夹并设置文件夹的颜色
def generateColoredDirectories():
    for x in range(100,400):
        dir_path = '/Game/PythonGenerated/'+str(x);
        linear_color = getGradientColor(x);
        #要先设置目录的颜色在创建文件夹，不要需要重启编辑器才会生效
        unreal.MyPythonFunctions.set_folder_color(dir_path,linear_color)
        unreal.EditorAssetLibrary.make_directory(dir_path);
        
#打开资源编辑器
def openAssets(path):
    asset = unreal.load_asset(path);
    unreal.AssetToolsHelpers.get_asset_tools().open_editor_for_assets([asset])

#获得所有打开的资源    
def getAllOpenedAssets():
    return unreal.MyPythonFunctions.get_assets_opened_in_editor();
    
#关闭资源
def closeAsset():
    assets = getAllOpenedAssets()
    unreal.MyPythonFunctions.close_editor_for_assets(assets)
    
#将资源在内容文件夹中显示
#paths 资源列表[]
def showAssetsInContentBrowser(paths):
    unreal.EditorAssetLibrary.sync_browser_to_objects(paths)

#获得选中的资源 
def getSelectedAssets():
   return unreal.MyPythonFunctions.get_selected_assets()

#将配置的路径选中    
def setSelectedAssets(paths):
    return unreal.MyPythonFunctions.set_selected_assets(paths)  
    
#获得选中的文件夹   
def getSelectedFolders():
    return unreal.MyPythonFunctions.get_selected_folders()

#获得选中的路径    
def getSelectedPaths():
    return unreal.MyPythonFunctions.get_selected_paths();
 
#将配置的文件夹路径选中 
def setSelectedFolders(paths):
    unreal.MyPythonFunctions.set_selected_folders(paths);
        

#创建Actor
def deferredSpawnActor(AssetPath):
    #加载资源为蓝图类
    actor_class = unreal.EditorAssetLibrary.load_blueprint_class(AssetPath)
    actor_location = unreal.Vector(random.uniform(0,2000),random.uniform(0,2000),0)
    actor_rotation = unreal.Rotator(random.uniform(0,180),random.uniform(0,180),random.uniform(0,180))
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(actor_class,actor_location,actor_rotation)
    actor.tags.append("My python Actor")
    return actor
    
def executeSlowTask():
    quantity_steps_in_slow_task = 100
    #生成100个actor 每生成一个进度加1
    with unreal.ScopedSlowTask(quantity_steps_in_slow_task,"My Slow Task Text...") as show_task:
        show_task.make_dialog(True)
        for x in range(quantity_steps_in_slow_task):
            if show_task.should_cancel():
               break
            show_task.enter_progress_frame(1.0,"My Slow Task Text..."+str(x)+'/'+str(quantity_steps_in_slow_task))
            deferredSpawnActor('/Game/Bp_actor')
#显示类的所有属性
def ShowAllPorpeties(AssetPath):
    actor_class = unreal.EditorAssetLibrary.load_blueprint_class(AssetPath)
    print(unreal.MyPythonFunctions.get_all_porperties(actor_class))

#执行命令行
def executeConsoleCmd():
    console_cmd = ['r.ScreenPercentage 0.1','r.Color.Max 6','stat fps','stat unit']
    for cmd in console_cmd:
        unreal.MyPythonFunctions.execute_console_cmd(cmd)

#获得场景中所有的actors
def getAllActors(use_selection = False,actor_class = None,actor_tag = None):
    if use_selection:
        selected_actors = unreal.EditorLevelLibrary.get_selected_level_actors()
        class_actors = selected_actors
        if actor_class:
            class_actors = [actor for actor in selected_actors if cast(x,actor_class)]
        tag_actors = class_actors
        if actor_tag:
            tag_actors = [actor for actor in selected_actors if actor.actor_has_tag(actor_tag)]
        return tag_actors
    else:
        uWorld = unreal.EditorLevelLibrary.get_editor_world()
        if actor_class:
            worldactors = unreal.GameplayStatics.get_all_actors_of_class(uWorld,actor_class)
            if actor_tag:
                tag_actors = [actor for actor in worldactors if actor.actor_has_tag(actor_tag)]
            return tag_actors
        elif actor_tag:
             worldactors = unreal.GameplayStatics.get_all_actors_with_tag(uWorld,actor_tag)
             return worldactors
        else:
            worldactors = unreal.GameplayStatics.get_all_actors_of_class(uWorld,unreal.Actor)
            return worldactors


#获得场景中选中的actor
def getSelectedActors():
    return unreal.EditorLevelLibrary.get_selected_level_actors()

#设置场景中的actor为选中状态
def select_actors(actorsToSelected =[]):
    unreal.EditorLevelLibrary.set_selected_level_actors(actors_to_select=actorsToSelected)

#随机选中场景中的actor
def randomSelectedActor():
    all_actors = getAllActors()
    actorToSelected =[]
    for i in range(len(all_actors)):
        if random.randrange(1,10) > 4:
            actorToSelected.append(all_actors[i])
    select_actors(actorToSelected)

#视口聚焦某个actor
def fouceViewportToActor(activeViewOnly = False, actor = None):
    cmd = 'CAMERA ALIGN'
    if activeViewOnly:
        cmd +=' ACTIVEVIEWPORTONLY'
    if actor:
        cmd +=' NAME=' + actor.get_name()
    print(cmd)
    unreal.MyPythonFunctions.execute_console_cmd(cmd)

def testViewport():
    selectedActor =  getSelectedActors()
    fouceViewportToActor(activeViewOnly = True, actor = selectedActor[0])

#获得当前视口的viewindex
def get_active_viewport_index():
    return unreal.MyPythonFunctions.get_active_viewport_index()

#设置视口的位置和旋转
def setViewLocationAndRotation(index = 1,location = unreal.Vector(),rotaion = unreal.Rotator()):
    unreal.MyPythonFunctions.set_viewport_location_and_rotation(index,location,rotaion)

#设置视口对齐到指定的actor
def snapViewprotToActor(index = 1,actor = None):
    setViewLocationAndRotation(index,actor.get_actor_location(),actor.get_actor_rotation())

#动态创建资源
def create_generic_asset(asset_path='',unique_name = True,asset_class =None,asset_factory = None):
    if unique_name:
        asset_path,asset_name = unreal.AssetToolsHelpers.get_asset_tools().create_unique_asset_name(base_package_name=asset_path, suffix='')
    print(asset_path,asset_name,asset_factory)
    if not unreal.EditorAssetLibrary.does_asset_exist(asset_path = asset_path):
        path = asset_path.rsplit('/',1)[0]
        name = asset_path.rsplit('/',1)[1]
        return unreal.AssetToolsHelpers.get_asset_tools().create_asset(
            asset_name = name,
            package_path = path,
            asset_class = asset_class,
            factory = asset_factory
        )
    return unreal.load_asset(asset_path)

def TestCreate():
    base_path ='/Game/'
    AssetInfo = [
        base_path+'partilce_system',
        unreal.ParticleSystem,
        unreal.ParticleSystemFactoryNew
    ]
    create_generic_asset(asset_path=AssetInfo[0],unique_name = True,asset_class =AssetInfo[1],asset_factory = AssetInfo[2])

#给指定的sequence增加指定的动画
def add_skeletal_animiation_track_on_possessable(animation_path ='',possessable = None):
    animation_asset = unreal.AnimSequence.cast(unreal.load_asset(animation_path))
    params = unreal.MovieSceneSkeletalAnimationParams()
    params.set_editor_property('Animation',animation_asset)
    animation_tarck = possessable.add_track(track_type=unreal.MovieSceneSkeletalAnimationTrack)
    animation_secene = animation_tarck.add_section()
    animation_secene.set_editor_property('Params',params)
    #设置插入的帧位置
    animation_secene.set_range_seconds(0,animation_asset.sequence_length)

def get_or_add_possessable_insequence_asset(sequence_path='',actor=None):
    sequence_asset = unreal.LevelSequence.cast(unreal.load_asset(sequence_path))
    #将actor绑定到sequence
    possessable = sequence_asset.add_possessable(actor)
    return possessable

def TestAddAnimation():
    sequence_path = '/Game/Seq_Test'
    animation_path = '/Game/Death_1'
    world = unreal.EditorLevelLibrary.get_editor_world()
    actor_in_world = unreal.GameplayStatics.get_all_actors_of_class(world,unreal.SkeletalMeshActor)[0]
    possessable = get_or_add_possessable_insequence_asset(sequence_path,actor_in_world)
    add_skeletal_animiation_track_on_possessable(animation_path,possessable)