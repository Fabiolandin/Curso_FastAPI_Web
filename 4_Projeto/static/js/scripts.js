/*!
* Start Bootstrap - Modern Business v5.0.6 (https://startbootstrap.com/template-overviews/modern-business)
* Copyright 2013-2022 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-modern-business/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project



$(document).on('show.bs.modal', '#modal-delete', function (event) {
    var element = $(event.relatedTarget);
    $("#modal-delete-button").attr("data-url", element.data("url"));
});

$(document).on('click', '#modal-delete-button', function() {
    $.ajax({
        url: $(this).data('url'), // <-- corrigido
        method: 'DELETE',
        success: function(result) {
            // Se o backend retornar JSON
            if (result.redirect) {
                window.location.href = result.redirect;
            } else {
                // fallback: recarregar a página
                location.reload();
            }
        },
        error: function(err) {
            console.error("Erro ao deletar:", err);
        }
    });
});
