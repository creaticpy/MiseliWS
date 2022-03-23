function msg(msg) {
    console.log(msg);
}

_minsearch = 3;

winfunc = {
    add_load_events: function () {
        let links = document.querySelectorAll('a[data-call="view"]');
        links.forEach((link) => {
            link.addEventListener('click', (event) => {
                let url = link.getAttribute('data-url');
                let lbl = link.getElementsByClassName("app-menu__label")[0].innerText;
                this.loadrecord(url, lbl, false);
            });
        });
    },

    load_record: function (url, title = 'DashBoard', pk = false, allowclose = true) {
        axios.get(url, {responseType: 'text', params: {pk: pk}})
            .then(function (response) {
                var data = response.data;
                if (winTabs) {
                    var id = Math.ceil(Math.random() * 1000);
                    winTabs.addTab({
                        id: "tab-" + id,
                        title: title,
                        content: data,
                        active: true,
                        allowClose: allowclose
                    });

                }
            })
            .catch(function (error) {
                console.log(error);
                console.log(url);
            });
    },

    load_record_list: function (uuid, url, recordurl, lbl, cols) {

        $('#' + uuid).DataTable({
            processing: true,
            serverSide: true,
            filter: true,
            ajax: {
                url: url,
                type: "POST",
                datatype: "json"
            },
            columns: cols,
            language: {
                url: "/static/js/dt_lang_opts.json"
            },
            scrollY: '50vh',
            scrollCollapse: true,
            paging: false,
            responsive: true,
            columnDefs: [
                {targets: 0, visible: false},

            ],
            dom: '<"toolbar' + uuid + '">frtip',
            initComplete: (settings, json) => {
                axios.post('/core/toolbar/', {uuid: uuid, recordurl: recordurl, lbl: lbl})
                    .then((response) => {
                        $("div.toolbar" + uuid).html(response.data);
                    });

                let table = new $.fn.dataTable.Api('#' + uuid);
                table.$('tr').on('click', function () {
                    let data = table.row(this).data();

                    if (data.hasOwnProperty("id")) {
                        var ids = data.id;
                    } else if (data.hasOwnProperty("codigo")) {
                        var ids = data.codigo;
                    }
                    winfunc.loadrecord(recordurl, lbl + ': ' + ids, ids);
                });
            }
        });
    },
/*$('.typeahead').bind('typeahead:select', function(ev, suggestion) {
  console.log('Selection: ' + suggestion);
});*/
    foreign_autocomplete(target, modelname, url, targetfk, search_col, modulename) {
        console.log(url)
        var elem = $('#'+target);
        elem.autocomplete({
            source: function(request, response){
                const params = new URLSearchParams();
                params.append('modelname', modelname);
                params.append('search_term', request.term);
                /*axios.post(url, params).then(function(resp){
                    msg(resp.data);
                });*/
                $.ajax({
                    url: url,
                    type: 'post',
                    dataType: 'json',
                    data: {modelname: modelname, search_term: request.term, search_col: search_col, modulename: modulename},
                    success: function(data){
                        const res = [];
                        data.forEach((rows)=> {
                            res.push({
                                label: rows.fields[search_col],
                                value: rows.pk
                            });
                        });
                        response(res);
                    },

                });
           },
            select: function(event, ui){
                elem.val(ui.item.label);
                $('#'+targetfk).val(ui.item.value);
                return false;
            },
            focus: function(event, ui){
                elem.val(ui.item.label);
                $('#'+targetfk).val(ui.item.value);
                return false;
            },
        });
        /*let elem = document.getElementById(target);
       */

        /*fetch('' + val).then(
            function (response) {
                return response.json();
            }).then(function (data) {
            for (i = 0; i < data.length; i++) {
                list += '<li>' + data[i] + '</li>';
            }
            res.innerHTML = '<ul>' + list + '</ul>';
            return true;
        }).catch(function (err) {
            console.warn('Something went wrong.', err);
            return false;
        });*/
    }

}
_record = {
    loadForm: function (uuid) {
        //data-erp="foreign" data-model="Empresas"
        let frgs = document.querySelectorAll('[data-erp="foreign"]');
        frgs.forEach(function (data) {
            setTimeout(function () {
                winfunc.foreign_autocomplete(data.id,
                    data.attributes['data-model'].value,
                    data.attributes['data-search-url'].value,
                    data.attributes['data-target'].value,
                    data.attributes['data-search-col'].value,
                    data.attributes['data-module'].value,
                    );
            }, 10);
        })
    },
    /*serializeForm: function (uuid){
         const  form = $('#' + uuid).serializeArray();
          form.forEach((data, key)=>{
              //for start with 1 not zero
              msg(data);
              if (data.value in ['on', 'off']) {
                  form[key-1].value = (data.value === 'on') ? 1 : 0;
              }
          })
         return form;
    },*/
    form_json: function (arr) {
        newo = {};
        $.each(arr, function (i, item) {
            newo[item.name] = item.value;
        });
        return newo;
    },
    serializeform: function (form) {
        var serialized = [];
        for (var i = 0; i < form.elements.length; i++) {
            var field = form.elements[i];
            if (!field.name || field.type === 'file' || field.type === 'reset' || field.type === 'submit' || field.type === 'button') continue;
            if (field.type === 'select-multiple') {
                for (var n = 0; n < field.options.length; n++) {
                    if (!field.options[n].selected) continue;
                    serialized.push({
                        name: field.name,
                        value: field.options[n].value
                    });
                }
            } else if (field.type !== 'checkbox' && field.type !== 'radio') {
                serialized.push({
                    name: field.name,
                    value: field.value
                });
            } else if (field.type === 'checkbox' || field.type === 'radio') {
                serialized.push({
                    name: field.name,
                    value: field.checked
                });
            }
        }
        return serialized;
    },
    saveForm: function (uuid, url) {
        console.log('procesando formulario' + uuid);
        ffdata = _record.form_json(_record.serializeform(document.querySelector('#'+uuid)));
        formd = new FormData();
        //Object.keys(params).forEach(key => formd.append(params[key].name, params[key].value));
        for (let idx in ffdata) {
            formd.append(idx, ffdata[idx]);
        }
        axios.post(url, formd).then(function(rsp){
           if (rsp.data.status) {
               Swal.fire({icon: 'success'});
           } else {
               Swal.fire({icon: 'error', text: rsp.data.msg});
           }

        });
        // $.ajax({
        //     type: "POST",
        //     url: url,
        //     data: ffdata,
        //     success: function (data) {
        //         if (data.status) {
        //             Swal.fire({icon: 'success'});
        //         } else {
        //             Swal.fire({icon: 'error', text: data.msg});
        //         }
        //     }
        // });
    },
    delete: function (uuid, url) {
        $.ajax({
            type: "POST",
            url: url,
            data: $('#' + uuid).serialize(),
            success: function (data) {
                if (data.status) {
                    Swal.fire({icon: 'success'});
                } else {
                    Swal.fire({icon: 'error', text: data.msg});
                }
            }
        });
    }
}