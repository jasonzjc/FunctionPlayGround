Attribute VB_Name = "Module1"
Sub Button2_Click()

'Define Constants
'Sheet names
Const cstrResultShtNm As String = "Result"   'This is the Sheet name to put result. Change as needed.
Const cstrDataShtNm As String = "Data"  'This is the Sheet name with data. Change as needed.

'Days and time interval
Const cintTmIntv As Integer = 15    'This is the default time interval between two neighborling data (unit: min)
Const cintOneDayDataAmt As Integer = 24 * 60 / cintTmIntv   'Data amount of one day
Const cintDayNm = 2 ' default number of days

Const cdoubleThreshold As Double = 4     'This is the default value of threshold.

'Data Sheet Structure
Const cintHeadNo As Integer = 1 'Number of rows used for table head
Const cintLeftColNo As Integer = 3 'Number of columns to be copied to Result Sheet

'Result Sheet Structure
Const cstrMaxPdNo As String = "Peak Length (no. of periods)"
Const cstrBegTm As String = "Peak Starting Time "
Const cstrEndTm As String = "Peak Ending Time"

'Define Variables
Dim doubleTd As Double: doubleTd = cdoubleThreshold
Dim intOneDayDataAmt As Integer: intOneDayDataAmt = cintOneDayDataAmt
Dim intDayNm As Integer: intDayNm = cintDayNm

Dim strDataShtNm As String: strDataShtNm = cstrDataShtNm
Dim strResultsShtNm As String: strResultsShtNm = cstrResultShtNm


Dim intCounter1 As Integer: intCounter1 = 0
Dim intMaxCnt As Integer: intMaxCnt = 0
Dim intMaxEndTime As Integer: intMaxEndTime = 0

Dim i As Integer: i = 0
Dim j As Integer: j = 0
Dim doubleCurrentData As Double: doubleCurrentData = 0

'Read Number of Days
If IsEmpty(ActiveSheet.Range("B2").Value) = True Then
    MsgBox "Please Fill in Number of Days"
    Exit Sub
Else
    intDayNm = ActiveSheet.Range("B2").Value
End If

'Read Data Time Interval
If IsEmpty(ActiveSheet.Range("B3").Value) = True Then
    MsgBox "Please Fill in Data Time Interval (min)"
    Exit Sub
Else
    intOneDayDataAmt = ActiveSheet.Range("B3").Value
End If

'Read Threshold
If IsEmpty(ActiveSheet.Range("B4").Value) = True Then
    MsgBox "Please Fill in Threshold"
    Exit Sub
Else
    doubleTd = ActiveSheet.Range("B4").Value
End If

'check if Data Sheet exists
'If Not SheetExists(strDataShtNm) Then
'    MsgBox "Datasheet " & strDataShtNm & " doesn't exist"
'End If

'create Result Sheet if doesn't exist
Dim wb As Workbook: Set wb = ActiveWorkbook
Dim shts As Sheets: Set shts = wb.Sheets
Dim obj As Object

If Not SheetExists(strResultsShtNm) Then
    Set obj = shts.Add(After:=ActiveSheet, Count:=1, Type:=XlSheetType.xlWorksheet)
    obj.Name = strResultsShtNm
End If

'Copy Table Head from Data Sheet to Result Sheet
For i = 1 To cintHeadNo
    j = 1
    Do While IsEmpty(Worksheets(strDataShtNm).Cells(i, j).Value) = False
        If j <= cintLeftColNo Then
            Worksheets(strResultsShtNm).Cells(i, j).Value = Worksheets(strDataShtNm).Cells(i, j).Value
        End If
        j = j + 1
    Loop
    intOneDayDataAmt = j
    Worksheets(strResultsShtNm).Cells(i, cintLeftColNo + 1).Value = cstrMaxPdNo
    Worksheets(strResultsShtNm).Cells(i, cintLeftColNo + 2).Value = cstrBegTm
    Worksheets(strResultsShtNm).Cells(i, cintLeftColNo + 3).Value = cstrEndTm
Next i

'Process rows below the Table Head
For i = cintHeadNo + 1 To intDayNm + 1

'copy left columns (non-data columns)
    For j = 1 To cintLeftColNo
        Worksheets(strResultsShtNm).Cells(i, j).Value = Worksheets(strDataShtNm).Cells(i, j).Value
    Next j
    
'Data process
    For j = cintLeftColNo + 1 To cintLeftColNo + intOneDayDataAmt
        doubleCurrentData = Worksheets(strDataShtNm).Cells(i, j).Value  'read one data from cell
        
        'start to count if over threshold
        If doubleCurrentData >= doubleTd Then
            intCounter1 = intCounter1 + 1
            
        'stop count if below threshold and record length and time
        Else
            If intCounter1 > intMaxCnt Then
                intMaxCnt = intCounter1 'update data length
                intMaxEndTime = j - 1 'update time (column no.) of the last data in this continous peak period
            End If
            intCounter1 = 0
        End If
    Next j
    
    'update maximum peak period record if this row (day) ends
    If intCounter1 > intMaxCnt Then
            intMaxCnt = intCounter1 'update data length
            intMaxEndTime = j   'update time (column no.) of the last data in this continous peak period
    End If
    intCounter1 = 0
    
    'write result into Result Sheet
    Worksheets(strResultsShtNm).Cells(i, cintLeftColNo + 1).Value = intMaxCnt
    Worksheets(strResultsShtNm).Cells(i, cintLeftColNo + 2).Value = Worksheets(strDataShtNm).Cells(1, intMaxEndTime - intMaxCnt + 1).Value
    Worksheets(strResultsShtNm).Cells(i, cintLeftColNo + 3).Value = Worksheets(strDataShtNm).Cells(1, intMaxEndTime).Value
    intMaxCnt = 0
Next i




End Sub

Public Function SheetExists(strSheetName As String, Optional wbWorkbook As Workbook) As Boolean
    If wbWorkbook Is Nothing Then Set wbWorkbook = ActiveWorkbook 'or ThisWorkbook - whichever appropriate
    Dim obj As Object
    On Error GoTo HandleError
    Set obj = wbWorkbook.Sheets(strSheetName)
    SheetExists = True
    Exit Function
HandleError:
    SheetExists = False
End Function
