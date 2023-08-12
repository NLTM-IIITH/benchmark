window.addEventListener('DOMContentLoaded', event => {
    // Simple-DataTables
    // https://github.com/fiduswriter/Simple-DataTables/wiki

    // const datatablesSimple = document.getElementById('datatablesSimple');
    // if (datatablesSimple) {
    //     new simpleDatatables.DataTable(datatablesSimple, {paging: false, searchable: false});
    // }

    const a = document.getElementsByClassName('datatablesSimple');
    for (const datatablesSimple of a) {
        if (datatablesSimple) {
            new simpleDatatables.DataTable(datatablesSimple, {paging: false, searchable: false});
        }
    }
});
