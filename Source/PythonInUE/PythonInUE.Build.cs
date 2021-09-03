// Copyright Epic Games, Inc. All Rights Reserved.

using UnrealBuildTool;

public class PythonInUE : ModuleRules
{
	public PythonInUE(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;
	
		PublicDependencyModuleNames.AddRange(new string[] { "Core", "CoreUObject", "Engine", "InputCore","ContentBrowser","AssetRegistry" });
		// "PythonScriptPlugin" 增加对python的蓝图调用支持
		PrivateDependencyModuleNames.AddRange(new string[] { "UnrealEd", "PythonScriptPlugin"});

		// Uncomment if you are using Slate UI
		// PrivateDependencyModuleNames.AddRange(new string[] { "Slate", "SlateCore" });
		
		// Uncomment if you are using online features
		// PrivateDependencyModuleNames.Add("OnlineSubsystem");

		// To include OnlineSubsystemSteam, add it to the plugins section in your uproject file with the Enabled attribute set to true
	}
}
