from flask import Flask,jsonify,request
import xml.etree.ElementTree as ET

app=Flask('__name__')


@app.route("/discos/")
def discos():
    doc=ET.parse("discos.xml")
    raiz=doc.getroot()

    lista=[]

    for cd in raiz:
        diccionario={
            "title":cd.findall("title")[0].text,
            "artist":cd.findall("artist")[0].text,
            "country":cd.findall("country")[0].text,
            "price":cd.findall("price")[0].text

        }
        lista.append(diccionario)

    return jsonify({"Discos":lista})

@app.route("/discosTitulo/",methods=["POST"])
def disco_titulo():

    json=request.get_json()
    doc=ET.parse("discos.xml")
    raiz=doc.getroot()
    lista=[]

    try:
        title=json["title"]
    except:
        return jsonify({"Error":"atributo mal escrito"})


    for cd in raiz:
        if cd.findall("title")[0].text==title.strip():
            diccionario={
                "title":cd.findall("title")[0].text,
                "artist":cd.findall("artist")[0].text,
                "country":cd.findall("country")[0].text,
                "price":cd.findall("price")[0].text
            }
            lista.append(diccionario)
            return jsonify(lista)

    return jsonify({"Error":"no existe un disco con este titulo"})
    

@app.route("/agregarDisco/",methods=["POST"])
def agregarDisco():
    
    doc=ET.parse("discos.xml")
    raiz=doc.getroot()
    json=request.get_json()

    try:
        title=json["title"]
        artist=json["artist"]
        country=json["country"]
        company=json["company"]
        price=json["price"]
        year=json["year"]
    except:
        return jsonify({"Error":"atributo mal escrito"})


    nuevoDisco=ET.SubElement(raiz,"cd")
    ET.SubElement(nuevoDisco,"title").text=title
    ET.SubElement(nuevoDisco,"artist").text=artist
    ET.SubElement(nuevoDisco,"country").text=country
    ET.SubElement(nuevoDisco,"company").text=company
    ET.SubElement(nuevoDisco,"price").text=str(price)
    ET.SubElement(nuevoDisco,"year").text=str(year)

    doc.write("discos.xml",xml_declaration=True,encoding="utf-8")
    return jsonify({"Exito":"Disco agregado con exito"})


@app.route("/empleados/")
def empleados():
    doc=ET.parse("empleados.xml")
    raiz=doc.getroot()

    departamentos={}

    for dep in raiz:
        depto=dep.attrib["departamento"]
        empleadosDep=[]
        for empleado in dep:
            diccionario={
                "id":empleado.attrib["id"],
                "nombre":empleado.findall("nombre")[0].text,
                "puesto":empleado.findall("puesto")[0].text,
                "salario":empleado.findall("salario")[0].text
            }
            empleadosDep.append(dict(diccionario))
        departamentos[depto]=empleadosDep
    
    return jsonify({"empresa 1":departamentos})


@app.route("/buscarEmpleado/",methods=["POST"])
def buscarEmpleado():
    doc=ET.parse("empleados.xml")
    raiz=doc.getroot()
    jsonres=request.get_json()

    try:
        nombre=jsonres["nombre"]
    except:
        return jsonify({"Error":"atributo mal escrito"})

    for dep in raiz:
        for emp in dep:
            if emp.findall("nombre")[0].text==nombre.strip():
                diccionario={
                    "departamento":dep.attrib["departamento"],
                    "id":emp.attrib["id"],
                    "puesto":emp.findall("puesto")[0].text,
                    "salario":emp.findall("salario")[0].text
                }
                return jsonify({emp.findall("nombre")[0].text:diccionario})
    
    return jsonify({"Error":"no existe un empleado con este nombre"})
        


@app.route("/agregarEmpleado/",methods=["POST"])
def agregarEmpleado():
    doc=ET.parse("empleados.xml")
    raiz=doc.getroot()
    jsonres=request.get_json()
    rs=False

    try:
        depto=jsonres["departamento"]
        id=jsonres["id"]
        nombre=jsonres["nombre"]
        puesto=jsonres["puesto"]
        salario=jsonres["salario"]
    except:
        return jsonify({"Error":"atributo mal escrito o no se recibio alguno"})

    
    for dep in raiz:
        for emp in dep:
            if dep.attrib["departamento"]==depto.strip() and rs==False:
                rs=True
                nuevoEmpleado=ET.SubElement(dep,"empleado",id=f"{id}")
                ET.SubElement(nuevoEmpleado,"nombre").text=nombre
                ET.SubElement(nuevoEmpleado,"puesto").text=puesto
                ET.SubElement(nuevoEmpleado,"salario").text=salario
                doc.write("empleados.xml",xml_declaration=True,encoding="utf-8")
                return jsonify({"Exito":"empleado agregado con exito"})

    return jsonify({"Error":"No existe un repartamento con este nombre"})
                




    
    

   

    
    


    



if __name__=='__main__':
    app.run(debug=True,port=3000)