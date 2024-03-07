## Summary

create a folder called weights

cd into weights

run on windows
"
$ProgressPreference = 'SilentlyContinue'
Invoke-WebRequest -Uri https://github.com/IDEA-Research/GroundingDINO/releases/download/v0.1.0-alpha/groundingdino_swint_ogc.pth -OutFile 'weights.pth'
