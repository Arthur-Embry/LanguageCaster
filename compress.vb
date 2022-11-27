set objArgs = Wscript.Arguments
set objFso = CreateObject("Scripting.FileSystemObject")
content = ""

'Iterate through all the arguments passed
for i = 0 to objArgs.count  
    on error resume next
    'Try and treat the argument like a folder
    Set folder = objFso.GetFolder(objArgs(i))
    'If we get an error, we know it is a file
    if err.number <> 0 then
        'This is not a folder, treat as file
        content = content & ReadFile(objArgs(i))
    else
        'No error? This is a folder, process accordingly
        for each file in folder.Files
            content = content & ReadFile(file.path)
        next
    end if
    on error goto 0
next

'Get system Temp folder path
set tempFolderPath = objFso.GetSpecialFolder(2)
'Generate a random filename to use for a temporary file
strTempFileName = objFso.GetTempName
'Create temporary file in Temp folder
set objTempFile = tempFolderPath.CreateTextFile(strTempFileName)
'Write content from JavaScript files to temporary file
objTempFile.WriteLine(content)
objTempFile.Close

'Open temporary file in Notepad
set objShell = CreateObject("WScript.Shell")
objShell.Run("Notepad.exe " & tempFolderPath & "\" & strTempFileName)


function ReadFile(strFilePath)
    'If file path ends with ".js", we know it is JavaScript file
    if Right(strFilePath, 3) = ".js" then       
        set objFile = objFso.OpenTextFile(strFilePath, 1, false)
        'Read entire contents of a JavaScript file and returns it as a string
        ReadFile = objFile.ReadAll & vbNewLine
        objFile.Close
    else
        'Return empty string
        ReadFile = ""
    end if  
end function