write_file_csv(){
   python -c "$(cat <<EOPY
from  openpyxl import Workbook
import openpyxl
import os
import sys
data = sys.stdin.read()
if not os.path.exists("myExcel.xlsx"):
    wb = Workbook()
    sheet = wb.active
    sheet.title="caesar"
    wb.save("myExcel.xlsx")
book=openpyxl.load_workbook("myExcel.xlsx")
worksheet=book.worksheets[0]
rows=worksheet.max_row
if data.find("+++") > -1:
    worksheet.cell(rows+1, 1, data)
else:
    worksheet.cell(rows+1, 2, "'%s" %data)
book.save("myExcel.xlsx")
EOPY
)"
}

main(){
  index=$(grep -nr "@@\|+++" $1 |awk -F: '{print $1}')
  endlino=$(cat $1 |awk 'END{print NR}')
  m=($index $endlino)
  for((i=0;i<${#m[@]};i++)) 
  do
     if [ $(( $i+1)) -lt ${#m[@]} ] 
     then
         if [ $((${m[i]}+1)) -eq ${m[i+1]} ];then
             sed -n ${m[i]}'p' $1|write_file_csv $i 
         else
             sed -n "${m[i]},$((${m[i+1]}-1))p" $1 |write_file_csv $i
         fi
     fi
  done
}

main $1
