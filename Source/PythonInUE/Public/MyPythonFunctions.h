// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "MyPythonFunctions.generated.h"

/**
 * 
 */
UCLASS()
class PYTHONINUE_API UMyPythonFunctions : public UBlueprintFunctionLibrary
{
	GENERATED_BODY()
public:
	UFUNCTION(BlueprintCallable)
	static void CalledFromPython(FString InputString);
	//设置文件夹的颜色
	UFUNCTION(BlueprintCallable,Category = "Unreal Python")
	static void SetFolderColor(FString FolderPath,FLinearColor Color);
	//关闭资源管理器
	UFUNCTION(BlueprintCallable, Category = "Unreal Python")
	static void CloseEditorForAssets(TArray<UObject*> Assets);
	//获得所有打开的资源
	UFUNCTION(BlueprintCallable, Category = "Unreal Python")
	static TArray<UObject*> GetAssetsOpenedInEditor();
	//获得选中的资源
	UFUNCTION(BlueprintCallable, Category = "Unreal Python")
	static TArray<FString> GetSelectedAssets();
	//设置选中的路径
	UFUNCTION(BlueprintCallable, Category = "Unreal Python")
	static void SetSelectedAssets(TArray<FString> Paths);
	//获得选中的文件夹
	UFUNCTION(BlueprintCallable, Category = "Unreal Python")
	static TArray<FString>GetSelectedFolders();
	//获得选中的文件路径
	UFUNCTION(BlueprintCallable, Category = "Unreal Python")
	static TArray<FString>GetSelectedPaths();
	//设置选中的文件夹
	UFUNCTION(BlueprintCallable, Category = "Unreal Python")
	static void SetSelectedFolders(TArray<FString> Paths);
	//获得某个类的所有属性
	UFUNCTION(BlueprintCallable, Category = "Unreal Python")
	static TArray<FString> GetAllPorperties(UClass* Class);
	//执行控制台命令行
	UFUNCTION(BlueprintCallable, Category = "Unreal Python")
	static void ExecuteConsoleCmd(FString Cmd);
	//获得当前激活的视口
	UFUNCTION(BlueprintCallable, Category = "Unreal Python")
	static int GetActiveViewportIndex();
	//设置视口为位置和旋转
	UFUNCTION(BlueprintCallable, Category = "Unreal Python")
	static void SetViewportLocationAndRotation(int Index,FVector Location,FRotator Rotaion);
	//蓝图执行python脚本(目前支持编辑器环境)
	UFUNCTION(BlueprintCallable, Category = "Unreal Python")
	static void ExecutePythonScript(FString PythonScript);
};
