# ba tavakol be khoda , tavasol be emam (rah)
from tkinter import Tk
from tkinter.filedialog import askopenfilename

Tk().withdraw()
e = askopenfilename()
split = e.split('/')
entityName = split[len(split) - 1].split('.')
entityName = entityName[0].capitalize()
f = open(e, "r")
constructText = ""
constructTextArray = []
while True:
    line = f.readline()
    if '@param' in line:
        line = line.split("$")
        constructTextArray.append("$fields['" + line[len(line) - 1].replace('\n', '') + "']")
    if '__construct' in line or not line:
        break
f.close()
constructText = ','.join(constructTextArray)
fileCode = "<?php\n namespace App\Views;\n use App\Exceptions\WrongInputException;\n use App\Misc\Containers\\" + entityName + " ;\n use App\Services;\n class " + entityName + "sView\n {\n     /**\n      * @param array $ids\n      * @return " + entityName + "[]|null\n      */\n     public function get" + entityName + "s(array $ids): ?array\n     {\n         if (empty($ids)) {\n             return [];\n         }\n         $result = Services::mysqlService()->select('" + entityName.lower() + "s', $ids);\n         if (empty($result)) {\n             return [];\n         }\n         $containers = [];\n         foreach ($result as $id => $fields) {\n             $containers[$fields['id']] = new " + entityName + "(" + constructText + ");\n         }\n         return $containers;\n     }\n     public function get" + entityName + "(int $id): " + entityName + "\n     {\n         if (!Services::ValidationService()->idNumber($id))\n             throw new WrongInputException('`ID` is not valid');\n         return $this->get" + entityName + "s([$id])[$id];\n     }\n     public function getAll()\n     {\n         $list = array_column(Services::mysqlService()->selectAll('" + entityName.lower() + "s'), 'id');\n         return $this->get" + entityName + "s($list);\n     }\n}"
f = open(entityName + "sView.php", "w")
f.write(fileCode)
f.close()
