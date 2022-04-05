const div = document.getElementById('detalle-tabs')
const link_tabs = document.getElementById("linktabs")
const contenedor_ul = document.getElementById("idul")

// no se porque pero en crear el listener correctamente tenemos que invertir el orden de los parametros(Event, "menu")
link_tabs.addEventListener('click', crear_tab.bind(Event, "menu")) // esto es para el menu
contenedor_ul.addEventListener('click', seleccionar_tab.bind(Event))

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

function crear_tab(origenes, evento) {
    let element = ""
    let tab_text = ""
    let dir_url = ""

    if (origenes === "menu" && evento.target.tagName === 'A') {
        element = evento.target
        tab_text = element.textContent
    } else if (origenes === "datatables") {
        if (evento.target.tagName === 'I' || evento.target.tagName === 'SPAN') {
            element = evento.target.parentNode
            if (element.tagName !== 'BUTTON') {
                console.log("Esta es una exception, debemos tratarla")
                return
            }
        } else if (evento.target.tagName === 'BUTTON') {
            element = evento.target
        } else {
            return
        }
        if (element.classList.contains('agregar')) {
            tab_text = element.attributes.tab_text.value
            console.log("apretaste Agregar")
        } else if (element.classList.contains('editar')) {
            tab_text = element.attributes.tab_text.value
            console.log("apretaste Editar")
        } else if (element.classList.contains("eliminar")) {
            tab_text = element.attributes.tab_text.value
            console.log("apretaste Eliminar")
        }
    } else {
        return
    }
    dir_url = element.attributes.url.value


    if ((element.tagName === 'A' && origenes === 'menu') || (element.tagName === 'BUTTON' && origenes === 'datatables')) {

        let cant = document.querySelectorAll(`div[menu_id="${element.id}"]`)
        if (cant.length === 0) {

            let itemLi = document.createElement('li')
            let itemDiv = document.createElement('div')
            let randomNro = randomNumber()

            itemLi.textContent = tab_text
            itemLi.classList.add('inactivo')
            itemLi.setAttribute('id', randomNumber())
            itemLi.setAttribute('menu_id', element.id)
            itemLi.setAttribute('tab_id', randomNro)

            contenedor_ul.appendChild(itemLi)

            itemDiv.classList.add('bloque')
            itemDiv.classList.add('inactivo')
            itemDiv.setAttribute('id', randomNumber())
            itemDiv.setAttribute('menu_id', element.id)
            itemDiv.setAttribute('block_id', randomNro)

            div.appendChild(itemDiv)


            let menu_id = document.querySelectorAll(`div[menu_id="${element.id}"]`)
            let block = document.getElementById(menu_id.item(0).attributes.id.value)

            itemLi.click()

            if (origenes === "menu") {
                axios.get(dir_url, {
                    params: {tablacreada: "yes"}
                }).then(function (resp) {


                    let cols = resp.data["cols"]
                    block.innerHTML = resp.data["plantilla"]
                    let tabla = block.getElementsByTagName("table")
                    load_tables(dir_url, cols, tabla.item(0).id, resp.data['url_agregar_registro'], block)


                }).catch(function (err) {
                    console.log(err, "Error en Axios Tabs.js =(")
                    alert(err + " - Error en Axios Tabs.js")
                })

            } else if (origenes === "datatables") {
                let tr = element.parentNode.parentNode
                let parent = tr.querySelector(".dpass")
                axios.get(dir_url, {
                    params: {pk: parent.textContent}
                }).then(function (resp) {

                    block.innerHTML = resp.data

                }).catch(function (err) {
                    console.log(err, "Error en Axios Tabs.js =(")
                    alert(err + " - Error en Axios Tabs.js")
                }).then(function () {

                    itemLi.click()

                })
            }

        } else {
            let menu_id = document.querySelectorAll(`li[menu_id="${event.target.id}"]`)
            let li = document.getElementById(menu_id[0].attributes.id.value)
            li.click()
        }
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

function load_tables(dir_url, cols, id_tabla, url_agregar_registro, block) {

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
                    tbody.item(0).addEventListener('click', crear_tab.bind(Event, "datatables"))
                }
            )
        },
        "columns": cols,
        "dom": 'Bfrtip',
        "buttons": [
            {
                text: "Agregar",
                attr: {href: '#', url: url_agregar_registro, tab_text: "Cargar Facturas"},
                className: "agregar"
                // action: function (e, dt, node, config) {
                //     crear_tab("boton_agregar", id_tabla)
                // }

            }
        ]
    })

    let item = block.getElementsByClassName('dt-buttons').item(0).getElementsByClassName('agregar').item(0)
    item.addEventListener('click', crear_tab.bind(Event, 'datatables'))


    //funciona correctamente, vamos a ver de usar otro metodo
    // eventosbotones()
    // function eventosbotones() {
    //
    //     datatable.on('click', 'button.editar', function () {
    //         console.log(datatable.row($(this).parents("tr")).data(), "aca editamos")
    //         console.log(this.attributes.url, "aca borramosc")
    //         console.log(Event, "estoooooooooooooooooooooooo es evento")
    //         console.log("", "estoooooooooooooooooooooooo es eventosssssssssss")
    //     })
    //
    //     datatable.on('click', 'button.eliminar', function () {
    //
    //         console.log(datatable.row($(this).parents("tr")).data(), "aca borramos")
    //         console.log(datatable.row($(this)), "aca borramosa")
    //         console.log(this, "aca borramosb")
    //         console.log(this.url, "aca borramosc")
    //
    //
    //     })


}

function randomNumber() {
    return Date.now().toString(36) + Math.random().toString(36).substring(2)
}