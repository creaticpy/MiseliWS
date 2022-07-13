const const_id_menu_principal = document.getElementById("id_menu_principal")
const_id_menu_principal.addEventListener('click', gestionarTabs.bind(Event))

function randomNumber() {
    return Date.now().toString(36) + Math.random().toString(36).substring(2)
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
                    style: "margin-top: 10px; ",
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
    let dir_url = firedElement.attributes.url.value

    switch (firedElement.attributes.charger_function.value) {
        case 'ctc':

            CargarTablasConsultas(dir_url, contenedorDestino)
            return

        case 'cf':

            CargarFormularios(dir_url, contenedorDestino)
            return

        case 'fm':

            FormularioModificacion(dir_url, firedElement, contenedorDestino)
            return

        default:

            alert("Debe seleccionar un Cargador de funciones.")
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
            console.log(err, "Error en Axios Tabs 1.js =(")
            alert(err + " - Error en Axios Tabs 1.js")
        })
    }

    function CargarFormularios(dir_url, contenedorDestino) {
        axios.get(dir_url, {
            // params: {pk: parent.textContent} para agregar no necesitamos enviar pk
        }).then(function (resp) {

            contenedorDestino.innerHTML = resp.data

        }).catch(function (err) {
            console.log(err, "Error en Axios Tabs 2.js =(")
            alert(err + " - Error en Axios Tabs 2.js")
        }).then(function () {

            // itemLi.click() no recuerdo para que es esta linea

        })
    }

    function FormularioModificacion(dir_url, firedElement, contenedorDestino) {
        let tr = firedElement.parentNode.parentNode.parentNode
        let parent = tr.querySelector(".dpass")
        axios.get(dir_url, {
            params: {pk: parent.textContent}
        }).then(function (resp) {

            contenedorDestino.innerHTML = resp.data

        }).catch(function (err) {
            console.log(err, "Error en Axios Tabs 3.js =(")
            alert(err + " - Error en Axios Tabs 3.js")
        }).then(function () {

            // itemLi.click() no recuerdo para que es esta linea

        })
    }

}

function cerrar_tab() {

    let elem_tab = document.getElementById('tab-principal').getElementsByClassName("active")
    let elem_block = document.getElementById('tab-contenido').querySelectorAll(` div[aria-labelledby="${elem_tab.item(0).id}"]`)

    if (elem_tab[0].id === 'Dashboard') {
        alert("Tab Dashboard no puede ser cerrado")
    } else {
        let tab = document.getElementById(elem_tab[0].id).parentNode
        let block = document.getElementById(elem_block[0].id)
        let tab_destino = tab.previousElementSibling

        tab.remove()
        block.remove()
        tab_destino.getElementsByTagName("button").item(0).click()

    }
}
