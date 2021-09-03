// Fill out your copyright notice in the Description page of Project Settings.


#include "MyPythonFunctions.h"
#include "Subsystems/AssetEditorSubsystem.h"
#include "AssetRegistryModule.h"
#include "Modules/ModuleManager.h"
#include "ContentBrowserModule.h"
#include "AssetRegistry/AssetRegistryModule.h"
#include "IContentBrowserSingleton.h"
#include "UObject/UnrealType.h"
#include "LevelEditorViewport.h"
#include "../Plugins/Experimental/PythonScriptPlugin/Source/PythonScriptPlugin/Private/PythonScriptPlugin.h"

void UMyPythonFunctions::CalledFromPython(FString InputString)
{
	UE_LOG(LogTemp,Warning,TEXT("%s"),*InputString);
}

void UMyPythonFunctions::SetFolderColor(FString FolderPath, FLinearColor Color) {
	GConfig->SetString(TEXT("PathColor"), *FolderPath, *Color.ToString(),GEditorPerProjectIni);
}

void UMyPythonFunctions::CloseEditorForAssets(TArray<UObject*> Assets)
{
	for (UObject* Asset : Assets)
	{
		GEditor->GetEditorSubsystem<UAssetEditorSubsystem>()->CloseAllEditorsForAsset(Asset);
	}
}

TArray<UObject*> UMyPythonFunctions::GetAssetsOpenedInEditor()
{
	return GEditor->GetEditorSubsystem<UAssetEditorSubsystem>()->GetAllEditedAssets();
}

TArray<FString> UMyPythonFunctions::GetSelectedAssets()
{
	FContentBrowserModule& ContentBrowserModule = FModuleManager::LoadModuleChecked<FContentBrowserModule>("ContentBrowser");
	TArray<FAssetData> SelectedAssets;

	ContentBrowserModule.Get().GetSelectedAssets(SelectedAssets);
	TArray<FString> Results;
	for (FAssetData& AssetData:SelectedAssets)
	{
		Results.Add(AssetData.PackageName.ToString());
	}
	return Results;

}

void UMyPythonFunctions::SetSelectedAssets(TArray<FString> Paths)
{
	FContentBrowserModule& ContentBrowserModule = FModuleManager::LoadModuleChecked<FContentBrowserModule>("ContentBrowser");
	FAssetRegistryModule& AssetRegistryModule = FModuleManager::LoadModuleChecked<FAssetRegistryModule>("AssetRegistry");
	TArray<FName> PathsName;
	for (FString Path : Paths)
	{
		PathsName.Add(*Path);
	}
	FARFilter AssetFilter;
	AssetFilter.PackageNames = PathsName;
	TArray<FAssetData> SelectedAssets;
	AssetRegistryModule.Get().GetAssets(AssetFilter,SelectedAssets);
	ContentBrowserModule.Get().SyncBrowserToAssets(SelectedAssets);

}

TArray<FString> UMyPythonFunctions::GetSelectedFolders()
{
	FContentBrowserModule& ContentBrowserModule = FModuleManager::LoadModuleChecked<FContentBrowserModule>("ContentBrowser");
	TArray<FString> SelectedFolders;
	ContentBrowserModule.Get().GetSelectedFolders(SelectedFolders);
	return SelectedFolders;
}

TArray<FString> UMyPythonFunctions::GetSelectedPaths()
{

	FContentBrowserModule& ContentBrowserModule = FModuleManager::LoadModuleChecked<FContentBrowserModule>("ContentBrowser");
	TArray<FString> SelectedFolders;
	ContentBrowserModule.Get().GetSelectedPathViewFolders(SelectedFolders);
	return SelectedFolders;
}

void UMyPythonFunctions::SetSelectedFolders(TArray<FString> Paths)
{
	FContentBrowserModule& ContentBrowserModule = FModuleManager::LoadModuleChecked<FContentBrowserModule>("ContentBrowser");
	ContentBrowserModule.Get().SyncBrowserToFolders(Paths);
}

TArray<FString> UMyPythonFunctions::GetAllPorperties(UClass* Class)
{
	TArray<FString> Ret;
	//迭代器获得类的属性
	for (TFieldIterator<UProperty> It(Class);It; ++It)
	{
		UProperty *Property = *It;
		if (Property->HasAnyPropertyFlags(EPropertyFlags::CPF_Edit)) {
			Ret.Add(Property->GetName());
		}
	}
	return Ret;
}

void UMyPythonFunctions::ExecuteConsoleCmd(FString Cmd)
{
	if (GEditor) {
		UWorld* World = GEditor->GetEditorWorldContext().World();
		if (World) {
			GEditor->Exec(World,*Cmd,*GLog);
		}
	}
}

int UMyPythonFunctions::GetActiveViewportIndex()
{
	int Index =1;
	if (GEditor != nullptr && GCurrentLevelEditingViewportClient != nullptr) {
		GEditor->GetLevelViewportClients().Find(GCurrentLevelEditingViewportClient,Index);
	}
	return Index;
}

void UMyPythonFunctions::SetViewportLocationAndRotation(int Index, FVector Location, FRotator Rotaion)
{
	if (GEditor != nullptr&& Index< GEditor->GetLevelViewportClients().Num()) {
		FLevelEditorViewportClient* LevelEditorViewportClient = GEditor->GetLevelViewportClients()[Index];
		if (LevelEditorViewportClient) {
			LevelEditorViewportClient->SetViewLocation(Location);
			LevelEditorViewportClient->SetViewRotation(Rotaion);
		}
	}
}

void UMyPythonFunctions::ExecutePythonScript(FString PythonScript)
{
	FPythonScriptPlugin::Get()->ExecPythonCommand(*PythonScript);
}
