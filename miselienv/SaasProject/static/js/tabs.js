const div = document.getElementById('detalle-tabs')
const link_tabs = document.getElementById("linktabs")
const contenedor_ul = document.getElementById("idul")

// no sé por qué, pero al crear el listener correctamente tenemos que invertir el orden de los parametros(Event, "menu")
link_tabs.addEventListener('click', gestionarTabs.bind(Event)) // esto es para el menu
// contenedor_ul.addEventListener('click', seleccionar_tab.bind(Event))

function seleccionar_tab(event) {

    if (event.target.tagName === 'LI') {
        let li = document.querySelectorAll('.contenedor-ul > li.activo')
        let bloque = document.querySelectorAll('.detalle-tabs > div.activo')
        let v_tab_id = event.target.attributes.tab_id.value

        li.forEach((cadaLi, i) => { // inactivamos los li, todos los que esten como activos, deberia haber siempre solo 1
            li[i].classList.replace('activo', 'inactivo')
            bloque[i].classList.replace('activo', 'inactivo')
        })

        li = document.querySelectorAll(`.contenedor-ul > li[tab_id="${v_tab_id}"]`) // como debe haber la misma cantidad de bloques y tabs accedemos al par por medio de la posicion
        bloque = document.querySelectorAll(`.detalle-tabs > div[block_id="${v_tab_id}"]`)

        li.forEach((cadaTab, i) => {
            li[i].classList.replace('inactivo', 'activo')
            bloque[i].classList.replace('inactivo', 'activo')
        })
    }
}

function gestionarTabs(event) { // event --> click y dentro del evento se encuentra el elemento que lo origina.
    try {

        let firedElement = event.target
        let abriren = firedElement.attributes.abrir_en.value
        let tab_text = firedElement.attributes.tab_text.value
        if (abriren !== "") { // solo aceptamos click de quienes tenga configurado donde abrirse...
            if (VerifTab(firedElement) === false) {
                let contenedorDestino = AgregarTab(abriren, tab_text)
                //Cargamos de contenido el tab creado
                CargarTabs(contenedorDestino, firedElement)
            } else {
                // AgregarTab("Empleados") no se todavia que pasa. Tal vez nada.

            }

        }
    } catch (e) {

    }

}


function cerrar_tab() {

    let elem_tab = document.getElementById('idul').getElementsByClassName("activo")
    let elem_block = document.getElementById('detalle-tabs').getElementsByClassName("activo")
    if (elem_tab[0].id === 'tab_dashboard') {
        alert("Tab Dashboard no puede ser cerrado")
    } else {
        let tab = document.getElementById(elem_tab[0].id)
        let block = document.getElementById(elem_block[0].id)
        let tab_destino = tab.previousElementSibling
        tab.remove()
        block.remove()
        tab_destino.click()
    }
}

function load_tables(dir_url, cols, id_tabla, url_agregar_registro, block, tab_texto) {
    let randomNum = randomNumber()
    let datatable = $('#' + id_tabla).DataTable({
        "aoColumnDefs": [{"sClass": "dpass", "aTargets": [0]}],
        "serverSide": true,
        "processing": true,
        "ajax": function (data, callback, settings) {
            let column_order = data.columns[data.order[0].column].data.replace(/\./g, "__")
            $.get(dir_url, {
                    limite: data.length,
                    inicio: data.start,
                    filtro: data.search.value,
                    order_by: column_order
                }, function (res) {
                    callback({
                        recordsTotal: res.count,
                        recordsFiltered: "",
                        data: res.objects,

                    });

                    let tbody = document.getElementById(id_tabla).getElementsByTagName('tbody')
                    tbody.item(0).addEventListener('click', gestionarTabs.bind(Event))
                }
            )
        },
        "columns": cols,
        "dom": 'Bfrtip',
        "buttons": [
            {
                text: "Agregar",
                attr: {
                    id: randomNum,
                    abrir_en: "tab-principal",
                    href: '#',
                    url: url_agregar_registro,
                    tab_text: tab_texto,
                    charger_function: 'cf',
                },
                className: "agregar",
                // action: function (e, dt, node, config) {
                //     crear_tab("boton_agregar", id_tabla)
                // }

            }
        ]
    })
    let itemAgregar = document.getElementById(randomNum)
    itemAgregar.innerHTML = "Agregar" // hacemos este artilujo mientras.
    itemAgregar.addEventListener('click', gestionarTabs.bind(Event))


}

function randomNumber() {
    return Date.now().toString(36) + Math.random().toString(36).substring(2)
}


function AgregarTab(abrir_en, descripcion) {
    let tab = document.getElementById(abrir_en) // para estos ejemplos, abriremos en tab-principal
    let tab_contenido = document.getElementById("tab-contenido")
    let html_cab = ''
    let html_det = ''
    let randomNro = randomNumber()
    let randomId = randomNumber()
    // cabecera
    html_cab += '<li class="nav-item" role="presentation">'
    html_cab += '    <button class="nav-link" id=' + '"' + randomNro + '"' + ' data-bs-toggle="tab" data-bs-target="#' + randomId + '"' + '  type="button" role="tab" aria-controls="profile-tab-pane" aria-selected="false" tab_text="' + descripcion + '">' + descripcion
    html_cab += '    </button>'
    html_cab += '</li>'

    tab.insertAdjacentHTML("beforeend", html_cab)
    // tab_principal.innerHTML =html_cab

    // detalle
    html_det += '<div class="tab-pane fade" id=' + '"' + randomId + '"' + ' role="tabpanel" aria-labelledby=' + '"' + randomNro + '"' + ' tabIndex="0">' + descripcion
    html_det += '</div>'

    tab_contenido.insertAdjacentHTML("beforeend", html_det)
    // tab_principal_contenido.innerHTML = html_det

    Goto = document.getElementById(randomNro)
    containerElement = document.getElementById(randomId)
    Goto.click()
    return containerElement // id del nuevo contenedor creado
}

function VerifTab(element) { // con esta funcion verificamos si ya esta abierto el tab solicitado
    let abrir_en = element.attributes.abrir_en.value

    if (abrir_en === 'tab-principal') {
        let tabPrincipal = document.getElementById('tab-principal')
        let tab_text = element.attributes.tab_text.value
        let tab = tabPrincipal.querySelectorAll(`#tab-principal button[tab_text="${tab_text}"]`)

        if (typeof (tab[0]) === "object") {
            tab[0].click()
        } else {
            return false

        }
    }
}

function CargarTabs(contenedorDestino, firedElement) {
    let dir_url = ""
    switch (firedElement.attributes.charger_function.value) {
        default:

            alert("Debe seleccionar un Cargador de funciones.")
            return

        case 'ctc':

            dir_url = firedElement.attributes.url.value
            CargarTablasConsultas(dir_url, contenedorDestino)
            return

        case 'cf':

            dir_url = firedElement.attributes.url.value
            CargarFormularios(dir_url, contenedorDestino)
            return

    }


    function CargarTablasConsultas(dir_url, contenedorDestino) {
        axios.get(dir_url, {
            params: {tablacreada: "yes"}
        }).then(function (resp) {


            let cols = resp.data["cols"]
            contenedorDestino.innerHTML = resp.data["plantilla"]
            let tabla = contenedorDestino.getElementsByTagName("table")
            load_tables(dir_url, cols, tabla.item(0).id, resp.data['url_agregar_registro'], contenedorDestino, resp.data["tab_texto"])


        }).catch(function (err) {
            console.log(err, "Error en Axios Tabs.js =(")
            alert(err + " - Error en Axios Tabs.js")
        })
    }

    function CargarFormularios(dir_url, contenedorDestino) {
        console.log("entraaaaa pio aqui?=", dir_url)
        axios.get(dir_url, {
            // params: {pk: parent.textContent} para agregar no necesitamos enviar pk
        }).then(function (resp) {

            contenedorDestino.innerHTML = resp.data

        }).catch(function (err) {
            console.log(err, "Error en Axios Tabs.js =(")
            alert(err + " - Error en Axios Tabs.js")
        }).then(function () {

            // itemLi.click() no recuerdo para que es esta linea

        })
    }

}