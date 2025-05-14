document.addEventListener("DOMContentLoaded", function () {
    new DataTable('#table', {
      language: {
        "decimal": ",",
        "thousands": ".",
        "processing": "Processando...",
        "search": "Buscar:",
        "lengthMenu": "Mostrar _MENU_ registros",
        "info": "Mostrando de _START_ até _END_ de _TOTAL_ registros",
        "infoEmpty": "Mostrando 0 até 0 de 0 registros",
        "infoFiltered": "(filtrado de _MAX_ registros no total)",
        "infoPostFix": "",
        "loadingRecords": "Carregando...",
        "zeroRecords": "Nenhum registro encontrado",
        "emptyTable": "Nenhum dado disponível na tabela",
        "aria": {
            "sortAscending": ": ativar para ordenar a coluna em ordem crescente",
            "sortDescending": ": ativar para ordenar a coluna em ordem decrescente"
        }
      }
    });
  });